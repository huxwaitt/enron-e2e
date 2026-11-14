"""Front office: masters (GCP, ERMS books/desks/traders, locations) and deal capture.

Counterparties, desks and locations come from what the corpus shows
(gold/reference/*.parquet, lexicon_hits). Traders are pseudonymous IDs, so no real
person is attached to a fabricated trade. Activity follows the 2001 collapse timeline.
"""
from __future__ import annotations

import datetime as dt
import math
import re

import numpy as np
import pandas as pd

from .. import paths
from .market import GAS_HUBS, POWER_POINTS, Market

TRADING_END = dt.date(2001, 11, 29)  # EnronOnline stopped trading at the end of November 2001

LEGAL_ENTITIES = [
    # code, name, SAP company code, is the code observed in the corpus?
    ("ENA", "Enron North America Corp.", "0413", True),
    ("EPMI", "Enron Power Marketing, Inc.", "0393", False),
    ("ECC", "Enron Canada Corp.", "0570", False),
]
DESKS = [
    # desk, commodity, region, legal entity, locations
    ("GAS-EAST", "natural_gas", "east", "ENA", ["transco-z6-ny", "tetco-m3", "dominion-south", "henry-hub"]),
    ("GAS-CENTRAL", "natural_gas", "central", "ENA", ["chicago-citygate", "michcon", "henry-hub"]),
    ("GAS-TEXAS", "natural_gas", "texas", "ENA", ["katy", "houston-ship-channel", "waha", "carthage", "agua-dulce"]),
    ("GAS-WEST", "natural_gas", "west", "ENA", ["socal-border", "pge-citygate", "malin", "sumas", "permian", "san-juan", "rockies"]),
    ("GAS-CANADA", "natural_gas", "canada", "ECC", ["aeco", "sumas", "chicago-citygate"]),
    ("GAS-FIN", "natural_gas", "gulf", "ENA", ["henry-hub"]),
    # West power desk names are as they appear in the corpus (LT/ST = long/short term)
    ("PWR-LTNW", "power", "west", "EPMI", ["mid-c", "cob"]),
    ("PWR-STNW", "power", "west", "EPMI", ["mid-c", "cob"]),
    ("PWR-LTSW", "power", "west", "EPMI", ["palo-verde", "four-corners", "mead"]),
    ("PWR-STSW", "power", "west", "EPMI", ["palo-verde", "four-corners", "mead"]),
    ("PWR-LTCA", "power", "west", "EPMI", ["np15", "sp15", "zp26"]),
    ("PWR-STCA", "power", "west", "EPMI", ["np15", "sp15", "zp26"]),
    ("PWR-EAST", "power", "east", "EPMI", ["pjm-west", "cinergy", "entergy", "tva", "comed", "into-southern", "nepool", "nyiso"]),
    ("PWR-ERCOT", "power", "texas", "EPMI", ["ercot"]),
]
PIPE_FOR_HUB = {
    "transco-z6-ny": "transco", "tetco-m3": "texas-eastern", "dominion-south": "columbia-gas", "henry-hub": "columbia-gulf",
    "chicago-citygate": "ngpl", "michcon": "anr", "katy": "hpl", "houston-ship-channel": "hpl", "waha": "el-paso",
    "carthage": "texas-gas", "agua-dulce": "tennessee", "socal-border": "transwestern", "pge-citygate": "pge-gt-nw",
    "malin": "pge-gt-nw", "sumas": "northwest-pipeline", "permian": "el-paso", "san-juan": "el-paso",
    "rockies": "cig", "aeco": "nova",
}
ISO_FOR_POINT = {"np15": "CAISO", "sp15": "CAISO", "zp26": "CAISO", "pjm-west": "PJM", "nepool": "ISO-NE",
                 "nyiso": "NYISO", "ercot": "ERCOT"}


def activity(d: dt.date) -> float:
    if d > TRADING_END:
        return 0.0
    if d >= dt.date(2001, 11, 8):
        return 0.35   # restatement; counterparties pulling back
    if d >= dt.date(2001, 10, 16):
        return 0.65   # Q3 earnings / equity reduction
    if d >= dt.date(2001, 8, 14):
        return 0.9
    return 1.0 if d.year == 2001 else 0.85


def _cp_type(name: str) -> str:
    n = name.upper()
    if re.search(r"CITY OF|MUNICIPAL|DISTRICT|AUTHORITY|COOPERATIVE|\bPUD\b|\bCOOP\b", n):
        return "MUNI_COOP"
    if re.search(r"CAPITAL|BANK|SECURITIES|MORGAN|GOLDMAN|MERRILL|CITIBANK|CREDIT|FINANCIAL", n):
        return "FINANCIAL"
    if re.search(r"ELECTRIC|EDISON|POWER & LIGHT|UTILIT|\bP ?& ?L\b|GAS & ELECTRIC|PUBLIC SERVICE", n):
        return "UTILITY"
    if re.search(r"OIL|PETROLEUM|EXPLORATION|PRODUCTION|RESOURCES|\bE ?& ?P\b", n):
        return "PRODUCER"
    if re.search(r"MARKETING|TRADING|ENERGY SERVICES|MERCHANT|ENERGY SUPPLY", n):
        return "MARKETER"
    return "INDUSTRIAL"


def build_masters(rng: np.random.Generator, scale: float) -> dict[str, pd.DataFrame]:
    ref = paths.GOLD / "reference"
    cp = pd.read_parquet(ref / "counterparties.parquet")
    cp = cp[~cp.is_enron_affiliate]
    cp = cp[cp.name_norm.str.len().between(4, 60)]
    junk = r"^(CONTACT|TOTAL|BUY|SELL|PRICE|VOLUME|DEAL|PHONE|FAX|ATTN|NAME|DATE|SUB|NOTE|CP |CPTY|N/A|\W)"
    cp = cp[~cp.name_norm.str.contains(junk, regex=True) & ~cp.name_norm.str.contains(r"\d{3,}|[:@]", regex=True)]
    cp = cp[cp.name_norm.str.contains(r"[A-Z]{2,}\s+[A-Z]{2,}|^[A-Z]{4,}$", regex=True)]
    cp = cp.head(max(60, int(450 * scale))).reset_index(drop=True)
    ids = 10000 + np.cumsum(rng.integers(1, 40, len(cp)))
    types = cp.name_norm.map(_cp_type)
    short = cp.name_norm.map(lambda s: re.sub(r"[^A-Z0-9]", "", "".join(w[:5] for w in s.split()[:2]))[:10])
    gcp = pd.DataFrame({
        "CP_ID": ids, "SHORT_NAME": short, "LEGAL_NAME": cp.aliases.map(lambda a: max(a, key=len)),
        "CP_TYPE": types, "STATUS": "A",
        "CREATED_DT": [dt.date(1995, 1, 1) + dt.timedelta(days=int(x)) for x in rng.integers(0, 1800, len(cp))],
    })
    # duplicate short names exist in real masters; make them unique the way GCP admins did (suffix digit)
    gcp["SHORT_NAME"] = gcp.groupby("SHORT_NAME").cumcount().astype(str).radd(gcp.SHORT_NAME).str.replace(r"0$", "", regex=True)
    crosswalk = pd.DataFrame({"CP_ID": ids, "cp_iri": cp.cp_iri, "corpus_files": cp.n_files})
    weights = (cp.n_files / cp.n_files.sum()).to_numpy()
    trades_gas = ~types.isin(["MUNI_COOP"]) | (rng.random(len(cp)) < 0.3)
    trades_pwr = types.isin(["UTILITY", "MARKETER", "MUNI_COOP", "FINANCIAL"]) | (rng.random(len(cp)) < 0.25)
    gcp["TRADES_GAS"] = trades_gas.to_numpy()
    gcp["TRADES_POWER"] = trades_pwr.to_numpy()
    gcp["_W"] = weights

    ratings = rng.choice(["AA", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "NR"], len(gcp),
                         p=[0.04, 0.08, 0.14, 0.14, 0.16, 0.16, 0.12, 0.06, 0.04, 0.06])
    lim_base = {"AA": 150, "A+": 120, "A": 100, "A-": 80, "BBB+": 60, "BBB": 45, "BBB-": 30, "BB+": 15, "BB": 8, "NR": 5}
    credit = []
    agmts = []
    aid = 50000
    for r, rating in zip(gcp.itertuples(), ratings):
        for le in ("ENA", "EPMI"):
            credit.append({"CP_ID": r.CP_ID, "LE_CD": le, "RATING_SP": rating,
                           "LIMIT_USD": float(lim_base[rating] * 1e6 * rng.uniform(0.6, 1.4)),
                           "TENOR_LIMIT_MOS": int(rng.choice([12, 24, 36, 60, 120])), "APPROVED_BY": "RAC",
                           "EFF_DT": dt.date(1999, 12, 1) + dt.timedelta(days=int(rng.integers(0, 60)))})
        forms = []
        if r.TRADES_GAS:
            forms += [("ENA", "GISB_1996" if rng.random() < 0.6 else "ENFOLIO")]
        if r.TRADES_POWER:
            forms += [("EPMI", "EEI_2000" if rng.random() < 0.55 else "ENFOLIO")]
        if r.CP_TYPE in ("FINANCIAL", "MARKETER", "UTILITY") or rng.random() < 0.3:
            forms += [("ENA", "ISDA_1992")]
        forms += [("ENA", "EOL_GTC")]
        for le, form in forms:
            aid += int(rng.integers(1, 9))
            exec_dt = dt.date(1996, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1800)))
            if form == "EEI_2000":
                exec_dt = dt.date(2000, 5, 1) + dt.timedelta(days=int(rng.integers(0, 420)))
            agmts.append({"AGMT_ID": aid, "CP_ID": r.CP_ID, "LE_CD": le, "AGMT_TYPE": form, "EXEC_DT": exec_dt,
                          "NETTING_FLG": form in ("ISDA_1992", "EEI_2000", "ENFOLIO") or rng.random() < 0.3,
                          "CSA_THRESHOLD_USD": float(rng.choice([0, 5e6, 10e6, 25e6])) if form == "ISDA_1992" else None})

    desks, books, traders = [], [], []
    rc = 105600
    t_id = 1000
    for desk, comm, region, le, locs in DESKS:
        desks.append({"DESK_CD": desk, "COMMODITY": comm, "REGION": region, "LE_CD": le})
        kinds = ["PHY", "FIN"] + (["BASIS", "OPT"] if comm == "natural_gas" else ["OPT"])
        for k in kinds:
            rc += int(rng.integers(1, 30))
            books.append({"BOOK_CD": f"{le}-{desk}-{k}", "DESK_CD": desk, "LE_CD": le, "COMMODITY": comm,
                          "BOOK_TYPE": k, "REGION": region, "RC_CD": str(rc)})
        for _ in range(int(rng.integers(3, 8))):
            t_id += int(rng.integers(1, 12))
            traders.append({"TRADER_ID": f"TRD{t_id}", "DESK_CD": desk, "ACTIVE_FROM": dt.date(1999, 1, 4)})

    hits = pd.read_parquet(ref / "lexicon_hits.parquet").set_index("slug")["cells"].to_dict()
    locs = []
    for hub, (region, _, _) in GAS_HUBS.items():
        locs.append({"LOCATION_CD": hub.upper(), "SLUG": hub, "COMMODITY": "natural_gas", "LOC_TYPE": "HUB",
                     "REGION": region, "PIPELINE_CD": PIPE_FOR_HUB.get(hub, "").upper() or None, "ISO_CD": None,
                     "CORPUS_CELLS": int(hits.get(hub, 0))})
    for pt, (region, _, _) in POWER_POINTS.items():
        locs.append({"LOCATION_CD": pt.upper(), "SLUG": pt, "COMMODITY": "power", "LOC_TYPE": "POINT",
                     "REGION": region, "PIPELINE_CD": None, "ISO_CD": ISO_FOR_POINT.get(pt),
                     "CORPUS_CELLS": int(hits.get(pt, 0))})
    le = pd.DataFrame(LEGAL_ENTITIES, columns=["LE_CD", "LE_NAME", "SAP_BUKRS", "BUKRS_OBSERVED_IN_CORPUS"])
    return {"le": le, "gcp": gcp, "crosswalk": crosswalk, "credit": pd.DataFrame(credit), "agmt": pd.DataFrame(agmts),
            "desk": pd.DataFrame(desks), "book": pd.DataFrame(books), "trader": pd.DataFrame(traders),
            "location": pd.DataFrame(locs)}


def _next_bday(d: dt.date) -> dt.date:
    d += dt.timedelta(days=1)
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def _month_add(d: dt.date, n: int) -> dt.date:
    m = d.month - 1 + n
    return dt.date(d.year + m // 12, m % 12 + 1, 1)


def _month_end(d: dt.date) -> dt.date:
    return _month_add(d, 1) - dt.timedelta(days=1)


def black76(F, K, T, vol, call=True):
    if T <= 0:
        return max(0.0, (F - K) if call else (K - F))
    s = vol * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    d2 = d1 - s
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return F * N(d1) - K * N(d2) if call else K * N(-d2) - F * N(-d1)


def build_deals(rng: np.random.Generator, mk: Market, curves: dict, masters: dict, scale: float) -> pd.DataFrame:
    gcp = masters["gcp"]
    gas_cp = gcp[gcp.TRADES_GAS]
    pwr_cp = gcp[gcp.TRADES_POWER]
    desk_df = masters["desk"]
    traders = masters["trader"].groupby("DESK_CD")["TRADER_ID"].apply(list).to_dict()
    hits = masters["location"].set_index("SLUG")["CORPUS_CELLS"].to_dict()
    gas_spot = {h: mk.gas_spot(h) for h in GAS_HUBS}
    pwr_spot = {p: mk.power_spot(p) for p in POWER_POINTS}
    seq = {"SITARA": 148213, "ENPOWER": 402117, "TAGG": 0, "EOL": 1043120}
    tagg_prefixes = ["QA", "QB", "QL", "QM", "QN", "QO", "QT", "QV", "QW", "QX", "QY", "VC", "VG", "VH"]
    cp_pools = {}
    for comm, pool in (("natural_gas", gas_cp), ("power", pwr_cp)):
        cp_pools[comm] = (pool.CP_ID.to_numpy(), pool._W.to_numpy() / pool._W.sum())
    desk_pools = {
        "gas_phys": desk_df[(desk_df.COMMODITY == "natural_gas") & (desk_df.DESK_CD != "GAS-FIN")].DESK_CD.tolist(),
        "gas_fin": ["GAS-FIN", "GAS-FIN", "GAS-EAST", "GAS-WEST", "GAS-TEXAS"],
        "pwr_phys": desk_df[desk_df.COMMODITY == "power"].DESK_CD.tolist(),
        "pwr_fin": desk_df[desk_df.COMMODITY == "power"].DESK_CD.tolist(),
    }
    desk_le = desk_df.set_index("DESK_CD").LE_CD.to_dict()
    loc_w = {}
    for dk, locs in DESKS_BY.items():
        w = np.array([max(hits.get(l, 0), 1000) for l in locs], float)
        loc_w[dk] = (locs, w / w.sum())
    rows = []
    base = 140 * scale
    mix = [("gas_phys", 0.45), ("gas_fin", 0.20), ("pwr_phys", 0.30), ("pwr_fin", 0.05)]
    for i, ts in enumerate(mk.days):
        d = ts.date()
        a = activity(d)
        if a == 0:
            continue
        n = rng.poisson(base * a)
        kinds = rng.choice([k for k, _ in mix], n, p=[p for _, p in mix])
        eol_share = 0.55 if d.year == 2000 else 0.65
        for kind in kinds:
            comm = "natural_gas" if kind.startswith("gas") else "power"
            desk_cd = desk_pools[kind][int(rng.integers(len(desk_pools[kind])))]
            locs, lw = loc_w[desk_cd]
            loc = locs[int(rng.choice(len(locs), p=lw))]
            ids, pw = cp_pools[comm]
            cp_id = int(ids[rng.choice(len(ids), p=pw)])
            is_eol = rng.random() < (eol_share if kind != "gas_fin" else 0.35)
            bs = "B" if rng.random() < 0.5 else "S"
            trade_ts = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(seconds=int(rng.integers(0, 10 * 3600)))
            rec = {"TRADE_DT": d, "TRADE_TS": trade_ts, "LE_CD": desk_le[desk_cd], "DESK_CD": desk_cd,
                   "TRADER_ID": rng.choice(traders[desk_cd]), "CP_ID": cp_id, "BUY_SELL": bs,
                   "LOCATION_CD": loc.upper(), "EOL_FLG": bool(is_eol), "KIND": kind, "COMMODITY": comm}
            if kind == "gas_phys":
                term = rng.choice(["NEXT_DAY", "BALMO", "MONTHLY", "STRIP"], p=[0.35, 0.10, 0.35, 0.20])
                start, end = _term(rng, d, term)
                vol = float(max(2500, round(rng.lognormal(math.log(10000), 0.8) / 2500) * 2500))
                mi = mk.month_index(i, start)
                mkt = gas_spot[loc][i] if term in ("NEXT_DAY", "BALMO") else curves[f"NG-{loc.upper()}"][i, max(mi, 0)]
                if rng.random() < 0.65:
                    rec.update(PRICE_TYPE="FIXED", FIXED_PRICE=round(mkt * (1 + rng.normal(0, 0.004)), 4), INDEX_CD=None, ADDER=None)
                else:
                    idx = f"GD-{loc.upper()}" if term in ("NEXT_DAY", "BALMO") else f"IF-{loc.upper()}"
                    rec.update(PRICE_TYPE="INDEX", FIXED_PRICE=None, INDEX_CD=idx, ADDER=round(rng.normal(0, 0.02) / 0.0025) * 0.0025)
                rec.update(SYSTEM="SITARA", INSTRUMENT="PHYS_FWD", TERM=term, START_DT=start, END_DT=end,
                           VOLUME=vol, VOL_UOM="MMBTU/D", PIPELINE_CD=(PIPE_FOR_HUB.get(loc) or "").upper(), HOURS=None)
            elif kind == "pwr_phys":
                product = rng.choice(["ND_6X16", "BOM_6X16", "MO_6X16", "MO_7X8", "MO_7X24"], p=[0.35, 0.1, 0.35, 0.1, 0.1])
                term = {"ND_6X16": "NEXT_DAY", "BOM_6X16": "BALMO"}.get(product, "MONTHLY")
                if product.startswith("MO") and rng.random() < 0.3:
                    term = "STRIP"
                start, end = _term(rng, d, term)
                mw = float(rng.choice([25, 25, 50, 50, 50, 75, 100, 150]))
                mi = mk.month_index(i, start)
                mkt = pwr_spot[loc][i] if term in ("NEXT_DAY", "BALMO") else curves[f"PWR-{loc.upper()}-ONPK"][i, max(mi, 0)]
                if product.endswith("7X8"):
                    mkt *= 0.55
                elif product.endswith("7X24"):
                    mkt *= 0.80
                rec.update(SYSTEM="ENPOWER", INSTRUMENT="PHYS_FWD", TERM=term, START_DT=start, END_DT=end, VOLUME=mw,
                           VOL_UOM="MW", HOURS=product.split("_")[1], PRICE_TYPE="FIXED",
                           FIXED_PRICE=round(mkt * (1 + rng.normal(0, 0.02)), 2), INDEX_CD=None, ADDER=None,
                           PIPELINE_CD=None, ISO_CD=ISO_FOR_POINT.get(loc))
            else:  # financial (TAGG): swaps, basis swaps, options
                is_gas = kind == "gas_fin"
                inst = rng.choice(["SWAP", "BASIS_SWAP", "OPTION"], p=[0.6, 0.25, 0.15] if is_gas else [0.8, 0.0, 0.2])
                term = rng.choice(["MONTHLY", "STRIP"], p=[0.4, 0.6])
                start, end = _term(rng, d, term)
                mi = max(mk.month_index(i, start), 0)
                ckey = f"NG-{loc.upper()}" if is_gas else f"PWR-{loc.upper()}-ONPK"
                fwd = curves[ckey][i, min(mi, 35)]
                vol = float(round(rng.lognormal(math.log(10000 if is_gas else 50), 0.6) / (2500 if is_gas else 25)) * (2500 if is_gas else 25)) or (2500.0 if is_gas else 25.0)
                rec.update(SYSTEM="TAGG", TERM=term, START_DT=start, END_DT=end, VOLUME=vol,
                           VOL_UOM="MMBTU/D" if is_gas else "MW", HOURS=None if is_gas else "6X16",
                           PIPELINE_CD=None, PRICE_TYPE="FIXED", ADDER=None)
                if inst == "SWAP":
                    rec.update(INSTRUMENT="SWAP", FIXED_PRICE=round(fwd * (1 + rng.normal(0, 0.003)), 4),
                               INDEX_CD=("NYMEX-HH" if loc == "henry-hub" else f"IF-{loc.upper()}") if is_gas else f"DJ-{loc.upper()}-ONPK")
                elif inst == "BASIS_SWAP":
                    hh = curves["NG-HENRY-HUB"][i, min(mi, 35)]
                    rec.update(INSTRUMENT="BASIS_SWAP", FIXED_PRICE=round(fwd - hh + rng.normal(0, 0.01), 4), INDEX_CD=f"IF-{loc.upper()}")
                else:
                    call = rng.random() < 0.55
                    strike = round(fwd * rng.uniform(0.85, 1.2) / (0.05 if is_gas else 5)) * (0.05 if is_gas else 5) or fwd
                    T = max((start - d).days, 1) / 365.0
                    prem = black76(fwd, strike, T, 0.65 if is_gas else 0.9, call)
                    rec.update(INSTRUMENT="OPTION", OPTION_TYPE="CALL" if call else "PUT", STRIKE=float(strike),
                               PREMIUM=round(prem, 4), FIXED_PRICE=None,
                               INDEX_CD=("NYMEX-HH" if is_gas else f"DJ-{loc.upper()}-ONPK"))
            # deal numbers by system
            if rec["SYSTEM"] == "TAGG":
                seq["TAGG"] += 1
                rec["DEAL_NUM"] = f"{tagg_prefixes[(seq['TAGG'] // 10000) % len(tagg_prefixes)]}{seq['TAGG'] % 10000:04d}"
            else:
                seq[rec["SYSTEM"]] += int(rng.integers(1, 4))
                rec["DEAL_NUM"] = str(seq[rec["SYSTEM"]])
            if is_eol:
                seq["EOL"] += int(rng.integers(1, 6))
                rec["EOL_TXN_ID"] = seq["EOL"]
            else:
                rec["EOL_TXN_ID"] = None
            rec["STATUS"] = "KILLED" if rng.random() < 0.015 else "ACTIVE"
            rows.append(rec)
    df = pd.DataFrame(rows)
    df["BOOK_CD"] = df.LE_CD + "-" + df.DESK_CD + "-" + np.select(
        [df.INSTRUMENT == "PHYS_FWD", df.INSTRUMENT == "BASIS_SWAP", df.INSTRUMENT == "OPTION"], ["PHY", "BASIS", "OPT"], "FIN")
    return df


DESKS_BY = {d[0]: d[4] for d in DESKS}


def _term(rng, d: dt.date, term: str) -> tuple[dt.date, dt.date]:
    if term == "NEXT_DAY":
        s = _next_bday(d)
        e = s + dt.timedelta(days=2) if s.weekday() == 4 else s  # Friday trades cover the weekend package
        return s, e
    if term == "BALMO":
        s = _next_bday(d)
        return s, _month_end(s)
    if term == "MONTHLY":
        s = _month_add(d, 1)
        return s, _month_end(s)
    n = int(rng.choice([3, 5, 6, 12, 12, 24]))
    s = _month_add(d, int(rng.choice([1, 1, 2, 3])))
    if n == 5:  # winter strip Nov-Mar
        s = dt.date(d.year if d.month < 10 else d.year + 1, 11, 1)
    return s, _month_end(_month_add(s, n - 1))
