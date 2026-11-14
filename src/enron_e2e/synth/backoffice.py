"""Mid and back office: logistics, Unify settlement, payments, collateral, ERMS DPR, SAP GL."""
from __future__ import annotations

import calendar
import datetime as dt

import numpy as np
import pandas as pd

from .market import Market

EXTRACT_DT = dt.date(2002, 1, 31)   # snapshot date of the source systems
BANKRUPTCY = dt.date(2001, 12, 2)
DOWNGRADE = dt.date(2001, 11, 28)
HOLIDAYS = {dt.date(2000, 5, 29), dt.date(2000, 7, 4), dt.date(2000, 9, 4), dt.date(2000, 11, 23), dt.date(2000, 12, 25),
            dt.date(2001, 1, 1), dt.date(2001, 5, 28), dt.date(2001, 7, 4), dt.date(2001, 9, 3), dt.date(2001, 11, 22),
            dt.date(2001, 12, 25)}


def _adj_bday(d: dt.date) -> dt.date:
    while d.weekday() >= 5 or d in HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def _hours(start: dt.date, end: dt.date, hours: str) -> int:
    n, d = 0, start
    while d <= end:
        if hours == "6X16":
            n += 16 if d.weekday() < 6 and d not in HOLIDAYS else 0
        elif hours == "7X8":
            n += 8
        else:
            n += 24
        d += dt.timedelta(days=1)
    return n


# ------------------------------------------------------------------ deal months
def deal_months(deals: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in deals[deals.STATUS == "ACTIVE"].itertuples(index=False):
        m = dt.date(r.START_DT.year, r.START_DT.month, 1)
        while m <= r.END_DT:
            me = dt.date(m.year, m.month, calendar.monthrange(m.year, m.month)[1])
            ws, we = max(m, r.START_DT), min(me, r.END_DT)
            if r.VOL_UOM == "MW":
                qty = r.VOLUME * _hours(ws, we, r.HOURS or "6X16")
                uom = "MWH"
            else:
                qty = r.VOLUME * ((we - ws).days + 1)
                uom = "MMBTU"
            rows.append((r.DEAL_NUM, r.SYSTEM, r.INSTRUMENT, r.KIND, r.CP_ID, r.LE_CD, r.BOOK_CD, r.LOCATION_CD,
                         r.BUY_SELL, m, ws, we, float(qty), uom, r.PRICE_TYPE, r.FIXED_PRICE, r.INDEX_CD, r.ADDER,
                         getattr(r, "STRIKE", None), getattr(r, "OPTION_TYPE", None), r.HOURS, r.TRADE_DT,
                         getattr(r, "PIPELINE_CD", None)))
            m = dt.date(m.year + (m.month // 12), m.month % 12 + 1, 1)
    cols = ["DEAL_NUM", "SYSTEM", "INSTRUMENT", "KIND", "CP_ID", "LE_CD", "BOOK_CD", "LOCATION_CD", "BUY_SELL",
            "FLOW_MONTH", "WIN_START", "WIN_END", "QTY", "UOM", "PRICE_TYPE", "FIXED_PRICE", "INDEX_CD", "ADDER",
            "STRIKE", "OPTION_TYPE", "HOURS", "TRADE_DT", "PIPELINE_CD"]
    return pd.DataFrame(rows, columns=cols)


def settle_prices(dm: pd.DataFrame, gd: pd.DataFrame, iferc: pd.DataFrame, dj: pd.DataFrame) -> pd.DataFrame:
    """Attach the floating/index price each deal-month settles against."""
    if_map = {(r.INDEX_CD, r.FLOW_MONTH): r.PRICE for r in iferc.itertuples()}
    gd_s = gd.assign(PRICE_DT=pd.to_datetime(gd.PRICE_DT)).set_index(["INDEX_CD", "PRICE_DT"]).PRICE.sort_index()
    dj_m = dj.assign(M=pd.to_datetime(dj.PRICE_DT).dt.to_period("M").dt.start_time.dt.date).groupby(["INDEX_CD", "M"]).PRICE.mean().to_dict()
    gd_m = gd.assign(M=pd.to_datetime(gd.PRICE_DT).dt.to_period("M").dt.start_time.dt.date).groupby(["INDEX_CD", "M"]).PRICE.mean().to_dict()

    def idx_price(code, r):
        if code is None or (isinstance(code, float) and np.isnan(code)):
            return np.nan
        if code == "NYMEX-HH":
            return if_map.get(("IF-HENRY-HUB", r.FLOW_MONTH), np.nan)
        if code.startswith("IF-"):
            return if_map.get((code, r.FLOW_MONTH), np.nan)
        if code.startswith("GD-"):
            try:
                s = gd_s.loc[code].loc[pd.Timestamp(r.WIN_START):pd.Timestamp(r.WIN_END)]
                return float(s.mean()) if len(s) else gd_m.get((code, r.FLOW_MONTH), np.nan)
            except KeyError:
                return np.nan
        if code.startswith("DJ-"):
            return dj_m.get((code, r.FLOW_MONTH), np.nan)
        return np.nan

    flt = [idx_price(r.INDEX_CD, r) for r in dm.itertuples(index=False)]
    dm = dm.assign(FLOAT_PRICE=flt)
    hh = [if_map.get(("IF-HENRY-HUB", m), np.nan) for m in dm.FLOW_MONTH]
    dm.loc[dm.INSTRUMENT == "BASIS_SWAP", "FLOAT_PRICE"] = dm.FLOAT_PRICE - pd.Series(hh, index=dm.index)
    return dm


# ------------------------------------------------------------------ logistics
def logistics(rng, dm: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    phys = dm[dm.INSTRUMENT == "PHYS_FWD"].copy()
    noise = rng.normal(0, 0.025, len(phys))
    phys["ACTUAL_QTY"] = np.where(phys.UOM == "MMBTU", np.round(phys.QTY * (1 + noise)), phys.QTY)
    curtail = (phys.UOM == "MWH") & (rng.random(len(phys)) < 0.01)
    phys.loc[curtail, "ACTUAL_QTY"] = np.round(phys.loc[curtail, "QTY"] * rng.uniform(0.6, 0.95, curtail.sum()))
    nxt = [dt.date(m.year + m.month // 12, m.month % 12 + 1, 1) for m in phys.FLOW_MONTH]
    phys["ACTUALIZED_DT"] = [_adj_bday(n + dt.timedelta(days=int(k))) for n, k in zip(nxt, rng.integers(3, 9, len(phys)))]
    gas = phys[phys.UOM == "MMBTU"]
    noms = pd.DataFrame({
        "NOM_ID": np.arange(700001, 700001 + len(gas)), "DEAL_NUM": gas.DEAL_NUM, "PIPELINE_CD": gas.PIPELINE_CD,
        "LOCATION_CD": gas.LOCATION_CD, "FLOW_MONTH": gas.FLOW_MONTH, "FLOW_START": gas.WIN_START,
        "FLOW_END": gas.WIN_END, "NOM_DAILY_VOL": np.round(gas.QTY / ((pd.to_datetime(gas.WIN_END) - pd.to_datetime(gas.WIN_START)).dt.days + 1)),
        "SCHED_VOL": gas.QTY, "ACTUAL_VOL": gas.ACTUAL_QTY, "IMBALANCE_VOL": gas.ACTUAL_QTY - gas.QTY,
        "ACTUALIZED_DT": gas.ACTUALIZED_DT, "STATUS": "ACTUALIZED",
    })
    # flows after the Chapter 11 filing month were terminated under the masters' early-termination provisions
    future = noms.FLOW_MONTH >= dt.date(2002, 1, 1)
    noms.loc[future, ["ACTUAL_VOL", "IMBALANCE_VOL", "ACTUALIZED_DT"]] = None
    noms.loc[future, "STATUS"] = "TERMINATED"
    pw = phys[phys.UOM == "MWH"]
    sched = pd.DataFrame({
        "SCHED_ID": np.arange(900001, 900001 + len(pw)), "DEAL_NUM": pw.DEAL_NUM, "LOCATION_CD": pw.LOCATION_CD,
        "FLOW_MONTH": pw.FLOW_MONTH, "HOURS_PROFILE": pw.HOURS, "SCHED_MWH": pw.QTY, "ACTUAL_MWH": pw.ACTUAL_QTY,
        "CURTAILED_FLG": curtail[pw.index].to_numpy(), "ACTUALIZED_DT": pw.ACTUALIZED_DT,
        "STATUS": np.where(pw.FLOW_MONTH >= dt.date(2002, 1, 1), "TERMINATED", "ACTUALIZED"),
    })
    sched.loc[sched.STATUS == "TERMINATED", ["ACTUAL_MWH", "ACTUALIZED_DT"]] = None
    return phys, noms, sched


# ------------------------------------------------------------------ settlement (Unify)
def settlement(rng, dm: pd.DataFrame, phys: pd.DataFrame, gcp_agmt: pd.DataFrame, deals: pd.DataFrame):
    dm = dm.copy()
    dm["ACTUAL_QTY"] = dm.QTY
    dm.loc[phys.index, "ACTUAL_QTY"] = phys.ACTUAL_QTY
    sign_buy = np.where(dm.BUY_SELL == "B", 1.0, -1.0)
    price = np.where(dm.PRICE_TYPE == "INDEX", dm.FLOAT_PRICE + dm.ADDER.fillna(0), dm.FIXED_PRICE)
    amt = np.where(
        dm.INSTRUMENT == "PHYS_FWD", -sign_buy * dm.ACTUAL_QTY * price,               # buy -> Enron pays
        np.where(dm.INSTRUMENT.isin(["SWAP", "BASIS_SWAP"]), sign_buy * dm.QTY * (dm.FLOAT_PRICE - dm.FIXED_PRICE),
                 np.where(dm.OPTION_TYPE == "CALL", sign_buy * dm.QTY * np.maximum(dm.FLOAT_PRICE - dm.STRIKE, 0),
                          sign_buy * dm.QTY * np.maximum(dm.STRIKE - dm.FLOAT_PRICE, 0))))
    dm["SETTLE_PRICE"] = np.where(dm.INSTRUMENT == "PHYS_FWD", price, dm.FLOAT_PRICE)
    dm["AMOUNT"] = np.round(amt, 2)
    dm = dm[dm.AMOUNT.notna() & (dm.FLOW_MONTH <= dt.date(2001, 12, 1))]
    dm["SETTLE_CLASS"] = np.where(dm.SYSTEM == "TAGG", "FIN", np.where(dm.UOM == "MWH", "POWER", "GAS"))
    dm["LINE_TYPE"] = "CURRENT"
    # prior-period adjustments: revised actuals for ~4% of gas lines land on next month's invoice
    gas = dm[(dm.SETTLE_CLASS == "GAS")].sample(frac=0.04, random_state=int(rng.integers(1 << 30)))
    ppa = gas.copy()
    delta = rng.uniform(-0.03, 0.03, len(ppa))
    ppa["ACTUAL_QTY"] = np.round(ppa.ACTUAL_QTY * delta)
    ppa["AMOUNT"] = np.round(ppa.AMOUNT * delta, 2)
    ppa["LINE_TYPE"] = "PPA"
    ppa["ORIG_FLOW_MONTH"] = ppa.FLOW_MONTH
    ppa["FLOW_MONTH"] = [dt.date(m.year + m.month // 12, m.month % 12 + 1, 1) for m in ppa.FLOW_MONTH]
    dm["ORIG_FLOW_MONTH"] = dm.FLOW_MONTH
    lines = pd.concat([dm, ppa[ppa.FLOW_MONTH <= dt.date(2001, 12, 1)]], ignore_index=True)

    netting = set(map(tuple, gcp_agmt[gcp_agmt.NETTING_FLG][["CP_ID", "LE_CD"]].drop_duplicates().to_numpy()))
    inv_rows, line_rows = [], []
    seq = {"GAS": 3100000, "POWER": 5200000, "FIN": 7400000}
    for (cp, le, cls, m), g in lines.groupby(["CP_ID", "LE_CD", "SETTLE_CLASS", "FLOW_MONTH"], sort=True):
        nm = dt.date(m.year + m.month // 12, m.month % 12 + 1, 1)
        inv_dt = _adj_bday(nm + dt.timedelta(days={"GAS": 9, "POWER": 7, "FIN": 4}[cls]))
        due_dt = _adj_bday(nm + dt.timedelta(days={"GAS": 24, "POWER": 19, "FIN": 14}[cls]))
        rec, pay = g.AMOUNT[g.AMOUNT > 0].sum(), g.AMOUNT[g.AMOUNT < 0].sum()
        parts = [("NET", g)] if (cp, le) in netting else [("AR", g[g.AMOUNT > 0]), ("AP", g[g.AMOUNT <= 0])]
        for direction, part in parts:
            if part.empty:
                continue
            seq[cls] += int(rng.integers(1, 5))
            inv = f"{cls[0]}{seq[cls]}"
            net = round(float(part.AMOUNT.sum()), 2)
            inv_rows.append({"INVOICE_NUM": inv, "SETTLE_CLASS": cls, "CP_ID": cp, "LE_CD": le, "PROD_MONTH": m,
                             "INVOICE_DT": inv_dt, "DUE_DT": due_dt, "DOC_TYPE": direction,
                             "GROSS_RECEIVABLE": round(float(part.AMOUNT[part.AMOUNT > 0].sum()), 2),
                             "GROSS_PAYABLE": round(float(-part.AMOUNT[part.AMOUNT < 0].sum()), 2),
                             "NET_AMOUNT": net, "N_LINES": len(part)})
            for r in part.itertuples(index=False):
                line_rows.append((inv, r.DEAL_NUM, r.ORIG_FLOW_MONTH, r.LINE_TYPE, r.ACTUAL_QTY, r.UOM,
                                  None if pd.isna(r.SETTLE_PRICE) else round(float(r.SETTLE_PRICE), 4), r.AMOUNT))
    inv = pd.DataFrame(inv_rows)
    il = pd.DataFrame(line_rows, columns=["INVOICE_NUM", "DEAL_NUM", "FLOW_MONTH", "LINE_TYPE", "QTY", "UOM", "PRICE", "AMOUNT"])
    return inv, il, dm


def payments(rng, inv: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pid = 880000
    for r in inv.itertuples(index=False):
        if abs(r.NET_AMOUNT) < 0.01:
            continue
        receipt = r.NET_AMOUNT > 0
        if receipt:
            if r.DUE_DT >= dt.date(2001, 11, 1) and rng.random() < 0.45:
                continue  # counterparty withholds / sets off after the downgrade
            delay = 0 if rng.random() < 0.85 else int(rng.choice([1, 2, 3, 5, 8, 15, 32]))
            pay_dt = _adj_bday(r.DUE_DT + dt.timedelta(days=delay))
            amt = r.NET_AMOUNT * (rng.uniform(0.9, 0.995) if rng.random() < 0.03 else 1.0)
        else:
            if r.DUE_DT >= DOWNGRADE and rng.random() < 0.92:
                continue  # Enron stops paying; post-petition payables stayed
            pay_dt = r.DUE_DT
            amt = r.NET_AMOUNT
        if pay_dt > EXTRACT_DT:
            continue
        pid += int(rng.integers(1, 4))
        rows.append({"PAYMENT_ID": pid, "INVOICE_NUM": r.INVOICE_NUM, "CP_ID": r.CP_ID, "LE_CD": r.LE_CD,
                     "PAY_DT": pay_dt, "AMOUNT": round(abs(amt), 2), "DIRECTION": "RECEIPT" if receipt else "DISBURSEMENT",
                     "METHOD": "WIRE" if abs(amt) > 1e6 or rng.random() < 0.6 else "ACH",
                     "BANK_REF": f"FED{pay_dt:%y%m%d}{int(rng.integers(10000, 99999))}"})
    return pd.DataFrame(rows)


def collateral(rng, gcp: pd.DataFrame, credit: pd.DataFrame) -> pd.DataFrame:
    rows, cid = [], 40000
    weak = credit[credit.RATING_SP.isin(["BBB-", "BB+", "BB", "NR"])].CP_ID.unique()
    months = pd.period_range("2000-01", "2001-12", freq="M")
    for m in months:
        for _ in range(int(rng.integers(2, 7))):
            cid += 1
            d = m.start_time.date() + dt.timedelta(days=int(rng.integers(0, 27)))
            rows.append({"CALL_ID": cid, "CP_ID": int(rng.choice(weak)), "LE_CD": "ENA", "CALL_DT": _adj_bday(d),
                         "DIRECTION": "RECEIVED", "COLLATERAL_TYPE": rng.choice(["CASH", "LC"], p=[0.4, 0.6]),
                         "AMOUNT": round(float(rng.lognormal(np.log(3e6), 0.8)), -3), "REASON": "EXPOSURE_OVER_THRESHOLD"})
    # Enron's own credit collapses: counterparties call collateral from Enron
    big = gcp.sort_values("_W", ascending=False).CP_ID.head(120).to_numpy()
    for d in pd.bdate_range("2001-10-22", "2001-11-30"):
        for _ in range(int(rng.integers(1, 6))):
            cid += 1
            rows.append({"CALL_ID": cid, "CP_ID": int(rng.choice(big)), "LE_CD": rng.choice(["ENA", "EPMI"]),
                         "CALL_DT": d.date(), "DIRECTION": "POSTED", "COLLATERAL_TYPE": rng.choice(["CASH", "LC"], p=[0.55, 0.45]),
                         "AMOUNT": round(float(rng.lognormal(np.log(12e6), 0.9)), -3),
                         "REASON": "RATING_TRIGGER" if d.date() >= dt.date(2001, 11, 28) else "ADEQUATE_ASSURANCE"})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ ERMS daily position report
def dpr(mk: Market, curves: dict, dm: pd.DataFrame) -> pd.DataFrame:
    risk = dm[dm.PRICE_TYPE.eq("FIXED") & dm.INSTRUMENT.isin(["PHYS_FWD", "SWAP", "BASIS_SWAP"])].copy()
    risk["CURVE"] = np.where(risk.UOM == "MWH", "PWR-" + risk.LOCATION_CD + "-ONPK", "NG-" + risk.LOCATION_CD)
    risk = risk[risk.CURVE.isin(curves)]
    factor = np.where(risk.HOURS == "7X8", 0.55, np.where(risk.HOURS == "7X24", 0.80, 1.0))
    keys = sorted(curves)
    C = np.stack([curves[k] for k in keys])                      # [curve, day, horizon]
    ci = risk.CURVE.map({k: i for i, k in enumerate(keys)}).to_numpy()
    hh_i = keys.index("NG-HENRY-HUB")
    is_basis = (risk.INSTRUMENT == "BASIS_SWAP").to_numpy()
    sgn = np.where(risk.BUY_SELL == "B", 1.0, -1.0)
    qty, px = risk.QTY.to_numpy(), risk.FIXED_PRICE.to_numpy()
    fy = np.array([m.year for m in risk.FLOW_MONTH]); fm = np.array([m.month for m in risk.FLOW_MONTH])
    tdi = pd.to_datetime(risk.TRADE_DT).to_numpy().astype("datetime64[D]")
    books = risk.BOOK_CD.to_numpy()
    book_codes, book_idx = np.unique(books, return_inverse=True)
    out = []
    prev = np.zeros(len(book_codes))
    for i, day in enumerate(mk.days):
        h = (fy - day.year) * 12 + (fm - day.month)
        live = (tdi <= np.datetime64(day.date())) & (h >= 0) & (h < C.shape[2])
        hh = np.clip(h, 0, C.shape[2] - 1)
        F = C[ci, i, hh] * factor
        F = np.where(is_basis, C[ci, i, hh] - C[hh_i, i, hh], F)
        val = np.where(live, sgn * qty * (F - px), 0.0)
        new = np.where(live & (tdi == np.datetime64(day.date())), val, 0.0)
        mtm = np.bincount(book_idx, weights=val, minlength=len(book_codes))
        nd = np.bincount(book_idx, weights=new, minlength=len(book_codes))
        delta = np.bincount(book_idx, weights=np.where(live, sgn * qty, 0.0), minlength=len(book_codes))
        for b in range(len(book_codes)):
            if mtm[b] == 0 and prev[b] == 0:
                continue
            out.append((book_codes[b], day.date(), mtm[b], mtm[b] - prev[b], nd[b], mtm[b] - prev[b] - nd[b], delta[b]))
        prev = mtm
    df = pd.DataFrame(out, columns=["BOOK_CD", "EFF_DT", "MTM_USD", "DAILY_PL_USD", "NEW_DEAL_PL_USD",
                                    "CURVE_SHIFT_PL_USD", "NET_DELTA"])
    df["VAR_95_USD"] = (df.groupby("BOOK_CD").DAILY_PL_USD.transform(lambda s: s.rolling(60, min_periods=10).std()) * 1.65).round(2)
    for c in ("MTM_USD", "DAILY_PL_USD", "NEW_DEAL_PL_USD", "CURVE_SHIFT_PL_USD"):
        df[c] = df[c].round(2)
    return df
