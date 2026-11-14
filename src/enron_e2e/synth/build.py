"""Build the synthetic source systems and extract them to bronze.

data/sources/<system>.duckdb   operational databases (what FERC would have imaged)
lake/bronze/<system>/<TABLE>.parquet   extracted snapshot with _source_system/_extracted_at
lake/silver/synthetic_cp_crosswalk.parquet   GCP CP_ID -> enroni:cp IRI (MDM crosswalk)
"""
from __future__ import annotations

import datetime as dt
import json
import time

import duckdb
import numpy as np
import pandas as pd

from .. import paths
from ..governance import lineage
from . import backoffice as bo
from . import sap, trading
from .market import Market

SOURCES = paths.DATA / "sources"


def _eol_products(deals: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    e = deals[deals.EOL_TXN_ID.notna()].copy()
    loc_name = lambda s: s.replace("-", " ").title().replace("Pge", "PG&E").replace("Np15", "NP-15").replace("Sp15", "SP-15")
    def desc(r):
        mon = pd.Timestamp(r.START_DT).strftime("%b%y")
        if r.COMMODITY == "natural_gas":
            kind = "Phy Fwd Firm" if r.INSTRUMENT == "PHYS_FWD" else {"SWAP": "Fin Swap", "BASIS_SWAP": "Fin Basis Swap", "OPTION": "Fin Option"}[r.INSTRUMENT]
            term = {"NEXT_DAY": "Next Day", "BALMO": "BOM"}.get(r.TERM, mon if r.TERM == "MONTHLY" else f"{mon}-{pd.Timestamp(r.END_DT):%b%y}")
            return f"US Gas {kind} {loc_name(r.LOCATION_CD.lower())} {term} USD/MM"
        shape = {"6X16": "Peak", "7X8": "Off-Peak", "7X24": "ATC"}.get(r.HOURS or "6X16", "Peak")
        term = {"NEXT_DAY": "Next Day", "BALMO": "BOM"}.get(r.TERM, mon)
        kind = "Phy Fwd Firm" if r.INSTRUMENT == "PHYS_FWD" else "Fin Swap"
        return f"US Pwr {kind} {loc_name(r.LOCATION_CD.lower())} {shape} {term} USD/MWh"
    e["PRODUCT_DESC"] = [desc(r) for r in e.itertuples(index=False)]
    prods = e[["PRODUCT_DESC", "COMMODITY", "LOCATION_CD"]].drop_duplicates("PRODUCT_DESC").reset_index(drop=True)
    prods.insert(0, "PRODUCT_ID", np.arange(20001, 20001 + len(prods)))
    pid = dict(zip(prods.PRODUCT_DESC, prods.PRODUCT_ID))
    tx = pd.DataFrame({
        "TXN_ID": e.EOL_TXN_ID.astype("int64"), "PRODUCT_ID": e.PRODUCT_DESC.map(pid), "TXN_TS": e.TRADE_TS,
        "CP_ID": e.CP_ID, "CP_SIDE": np.where(e.BUY_SELL == "B", "SELL", "BUY"),  # counterparty hit Enron's bid/offer
        "VOLUME": e.VOLUME, "PRICE": e.FIXED_PRICE.fillna(e.PREMIUM), "ENRON_LE_CD": e.LE_CD,
        "DEAL_NUM": e.DEAL_NUM, "BOOKED_SYSTEM": e.SYSTEM, "TRADER_ID": e.TRADER_ID,
    })
    return prods, tx


def _confirmations(rng, deals: pd.DataFrame, agmt: pd.DataFrame) -> pd.DataFrame:
    rows, cid = [], 600000
    form_by = {}
    for r in agmt.itertuples(index=False):
        form_by.setdefault((r.CP_ID, r.LE_CD), []).append((r.AGMT_TYPE, r.AGMT_ID))
    for r in deals.itertuples(index=False):
        cid += 1
        agmts = form_by.get((r.CP_ID, r.LE_CD)) or form_by.get((r.CP_ID, "ENA")) or [("NONE", None)]
        if r.EOL_FLG:
            a = next((x for x in agmts if x[0] == "EOL_GTC"), agmts[0])
            rows.append((cid, r.DEAL_NUM, r.SYSTEM, a[1], a[0], r.TRADE_DT, r.TRADE_DT, "EOL_GTC", None))
            continue
        want = "ISDA_1992" if r.SYSTEM == "TAGG" else ("EEI_2000" if r.SYSTEM == "ENPOWER" else "GISB_1996")
        a = next((x for x in agmts if x[0] == want), next((x for x in agmts if x[0] != "EOL_GTC"), agmts[0]))
        sent = bo._adj_bday(r.TRADE_DT + dt.timedelta(days=1))
        u = rng.random()
        status = "MATCHED" if u < 0.95 else ("DISPUTED" if u < 0.98 else "OUTSTANDING")
        ret = None if status == "OUTSTANDING" else bo._adj_bday(sent + dt.timedelta(days=int(rng.integers(0, 9))))
        reason = rng.choice(["PRICE", "VOLUME", "DELIVERY POINT", "TERM"]) if status == "DISPUTED" else None
        rows.append((cid, r.DEAL_NUM, r.SYSTEM, a[1], a[0], sent, ret, status, reason))
    return pd.DataFrame(rows, columns=["CONFIRM_ID", "DEAL_NUM", "SOURCE_SYSTEM", "AGMT_ID", "AGMT_TYPE", "SENT_DT",
                                       "RETURNED_DT", "STATUS", "DISPUTE_REASON"])


def _write_db(name: str, tables: dict[str, pd.DataFrame]) -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    p = SOURCES / f"{name}.duckdb"
    if p.exists():
        p.unlink()
    con = duckdb.connect(str(p))
    for t, df in tables.items():
        con.register("df", df)
        con.execute(f'create table "{t}" as select * from df')
        con.unregister("df")
    con.close()


def extract_to_bronze() -> dict:
    """Full-snapshot extract of every source DB, as an ingestion tool would land it."""
    out = {}
    extracted_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    for db in sorted(SOURCES.glob("*.duckdb")):
        con = duckdb.connect(str(db), read_only=True)
        dest = paths.BRONZE / db.stem
        dest.mkdir(parents=True, exist_ok=True)
        for (t,) in con.execute("select table_name from information_schema.tables").fetchall():
            con.execute(f"""copy (select *, '{db.stem}' as _source_system, timestamptz '{extracted_at.isoformat()}' as _extracted_at,
                                       '{bo.EXTRACT_DT}'::date as _source_snapshot_dt from "{t}")
                            to '{(dest / f'{t}.parquet').as_posix()}' (format parquet, compression zstd)""")
            out[f"{db.stem}.{t}"] = con.execute(f'select count(*) from "{t}"').fetchone()[0]
        con.close()
    lineage("extract_synthetic_sources", [f"duckdb://{d.stem}" for d in SOURCES.glob("*.duckdb")],
            [f"bronze/{k}" for k in out])
    return out


def build(seed: int = 2001, scale: float = 1.0) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(seed)
    mk = Market(rng)
    curves = mk.curves()
    ms = trading.build_masters(rng, scale)
    deals = trading.build_deals(rng, mk, curves, ms, scale)
    gd, iferc, dj = mk.gas_daily(), mk.iferc_monthly(curves), mk.power_daily()
    dm = bo.deal_months(deals)
    dm = bo.settle_prices(dm, gd, iferc, dj)
    phys, noms, sched = bo.logistics(rng, dm)
    inv, inv_lines, settled = bo.settlement(rng, dm, phys, ms["agmt"], deals)
    pay = bo.payments(rng, inv)
    coll = bo.collateral(rng, ms["gcp"], ms["credit"])
    dpr = bo.dpr(mk, curves, dm)
    gl = sap.post(inv, pay, coll, settled, dpr, ms)
    prods, eol_tx = _eol_products(deals)
    confirms = _confirmations(rng, deals, ms["agmt"])

    curve_rows = []
    for code, F in curves.items():
        months = [(d.year, d.month) for d in mk.days]
        for h in range(F.shape[1]):
            cm = [dt.date(y + (m - 1 + h) // 12, (m - 1 + h) % 12 + 1, 1) for y, m in months]
            curve_rows.append(pd.DataFrame({"CURVE_CD": code, "EFF_DT": mk.days.date, "CONTRACT_MONTH": cm,
                                            "PRICE": np.round(F[:, h], 4)}))
    curve_price = pd.concat(curve_rows, ignore_index=True)
    curve_master = pd.DataFrame({"CURVE_CD": list(curves)}).assign(
        COMMODITY=lambda d: np.where(d.CURVE_CD.str.startswith("NG"), "natural_gas", "power"),
        CURVE_TYPE="PRICE", UOM=lambda d: np.where(d.CURVE_CD.str.startswith("NG"), "USD/MMBTU", "USD/MWH"),
        LOCATION_CD=lambda d: d.CURVE_CD.str.replace(r"^(NG|PWR)-|-ONPK$", "", regex=True))
    index_price = pd.concat([gd.assign(FREQ="DAILY", FLOW_MONTH=None), dj.assign(FREQ="DAILY", FLOW_MONTH=None),
                             iferc.assign(FREQ="MONTHLY", PRICE_DT=iferc.FLOW_MONTH)], ignore_index=True)

    common = ["DEAL_NUM", "TRADE_DT", "TRADE_TS", "LE_CD", "BOOK_CD", "DESK_CD", "TRADER_ID", "CP_ID", "BUY_SELL",
              "INSTRUMENT", "TERM", "START_DT", "END_DT", "VOLUME", "VOL_UOM", "PRICE_TYPE", "FIXED_PRICE", "INDEX_CD",
              "ADDER", "LOCATION_CD", "EOL_FLG", "EOL_TXN_ID", "STATUS"]
    sys_deals = {s: deals[deals.SYSTEM == s] for s in ("SITARA", "ENPOWER", "TAGG")}
    gcp_cols = ["CP_ID", "SHORT_NAME", "LEGAL_NAME", "CP_TYPE", "STATUS", "CREATED_DT", "TRADES_GAS", "TRADES_POWER"]
    unify = {}
    for cls, name in (("GAS", "unify_gas"), ("POWER", "unify_power"), ("FIN", "unify_financial")):
        ih = inv[inv.SETTLE_CLASS == cls]
        unify[name] = {"INVOICE_HDR": ih, "INVOICE_LINE": inv_lines[inv_lines.INVOICE_NUM.isin(ih.INVOICE_NUM)],
                       "PAYMENT": pay[pay.INVOICE_NUM.isin(ih.INVOICE_NUM)]}
    systems = {
        "gcp": {"CP": ms["gcp"][gcp_cols], "CREDIT_LIMIT": ms["credit"], "MASTER_AGMT": ms["agmt"], "COLLATERAL_CALL": coll},
        "erms": {"LEGAL_ENTITY": ms["le"], "DESK": ms["desk"], "BOOK": ms["book"], "TRADER": ms["trader"],
                 "LOCATION": ms["location"].drop(columns=["SLUG"]), "CURVE": curve_master, "CURVE_PRICE": curve_price,
                 "INDEX_PRICE": index_price, "DPR": dpr},
        "sitara": {"DEAL": sys_deals["SITARA"][common + ["PIPELINE_CD"]], "NOMINATION": noms},
        "enpower": {"PWR_DEAL": sys_deals["ENPOWER"][common + ["HOURS", "ISO_CD"]], "SCHEDULE": sched},
        "tagg": {"FIN_DEAL": sys_deals["TAGG"][common + ["HOURS", "OPTION_TYPE", "STRIKE", "PREMIUM"]]},
        "eol": {"PRODUCT": prods, "TRANSACTION": eol_tx},
        "global_contracts": {"CONFIRMATION": confirms},
        **unify,
        "sap": gl,
    }
    counts = {}
    for name, tables in systems.items():
        _write_db(name, tables)
        counts[name] = {t: len(df) for t, df in tables.items()}
    paths.SILVER.mkdir(parents=True, exist_ok=True)
    ms["crosswalk"].to_parquet(paths.SILVER / "synthetic_cp_crosswalk.parquet", index=False)
    (SOURCES / "_manifest.json").write_text(json.dumps({"seed": seed, "scale": scale, "built_at": dt.datetime.now().isoformat(),
                                                         "extract_snapshot": str(bo.EXTRACT_DT), "tables": counts}, indent=2))
    lineage("build_synthetic_sources", ["gold/reference/counterparties", "gold/reference/lexicon_hits",
                                        "ontology/reference/market_history.yaml"], [f"duckdb://{s}" for s in systems],
            facets={"seed": seed, "scale": scale})
    counts["_secs"] = round(time.time() - t0, 1)
    return counts
