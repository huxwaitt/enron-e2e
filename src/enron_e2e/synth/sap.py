"""SAP R/3 FI postings (BKPF/BSEG) derived from the synthetic sub-ledgers.

Account numbers are synthetic, but their captions follow Enron's 2000 Form 10-K
balance-sheet lines (e.g. "Assets from price risk management activities"). Company
code 0413 (ENA) is observed in the corpus; the others are flagged in T001.
"""
from __future__ import annotations

import calendar
import datetime as dt
from collections import defaultdict

import numpy as np
import pandas as pd

GL = [
    # account, text, type, 10-K caption
    ("100100", "Cash - Concentration Account", "BS", "Cash and cash equivalents"),
    ("110100", "Trade Receivables - Wholesale", "BS", "Trade receivables"),
    ("120500", "Unbilled Receivables", "BS", "Trade receivables"),
    ("140100", "Price Risk Mgmt Assets - Current", "BS", "Assets from price risk management activities"),
    ("150100", "Margin Deposits Posted", "BS", "Other current assets"),
    ("210100", "Trade Payables - Wholesale", "BS", "Accounts payable"),
    ("220500", "Accrued Cost of Sales", "BS", "Accounts payable"),
    ("240100", "Price Risk Mgmt Liabilities - Current", "BS", "Liabilities from price risk management activities"),
    ("250100", "Customer Deposits Received", "BS", "Other current liabilities"),
    ("260100", "Intercompany - Enron Corp Cash Pool", "BS", "Intercompany (eliminated in consolidation)"),
    ("400100", "Revenue - Natural Gas", "PL", "Revenues: natural gas and other products"),
    ("400200", "Revenue - Electricity", "PL", "Revenues: electricity"),
    ("400300", "Revenue - Financial Settlements", "PL", "Revenues: other"),
    ("410100", "Unrealized Gain/Loss - Price Risk Mgmt", "PL", "Revenues: other"),
    ("500100", "Cost of Gas Purchased", "PL", "Cost of gas, electricity and other products"),
    ("500200", "Cost of Power Purchased", "PL", "Cost of gas, electricity and other products"),
    ("500300", "Financial Settlements Paid", "PL", "Cost of gas, electricity and other products"),
]
REV = {"GAS": "400100", "POWER": "400200", "FIN": "400300"}
COST = {"GAS": "500100", "POWER": "500200", "FIN": "500300"}


class Poster:
    RANGES = {"DR": 1800000000, "KR": 5100000000, "DZ": 1400000000, "KZ": 1500000000, "SA": 100000000, "AB": 200000000}

    def __init__(self, le_map: dict[str, str], rc_by_le: dict[str, str]):
        self.le_map, self.rc = le_map, rc_by_le
        self.seq = defaultdict(int)
        self.h, self.l = [], []

    def doc(self, le, blart, budat, bldat, lines, xblnr="", bktxt="", usnam="UNIFY_IF", tcode="FB01", stblg=None,
            cpudt=None):
        bukrs = self.le_map[le]
        key = (bukrs, budat.year, blart)
        self.seq[key] += 1
        belnr = f"{self.RANGES[blart] + self.seq[key]:010d}"
        self.h.append({"MANDT": "100", "BUKRS": bukrs, "BELNR": belnr, "GJAHR": budat.year, "BLART": blart,
                       "BLDAT": bldat, "BUDAT": budat, "MONAT": budat.month, "CPUDT": cpudt or budat,
                       "USNAM": usnam, "TCODE": tcode, "XBLNR": xblnr, "BKTXT": bktxt, "WAERS": "USD",
                       "STBLG": stblg})
        for n, (bschl, hkont, amt, partner, zuonr, sgtxt) in enumerate(lines, 1):
            koart = "D" if bschl in ("01", "15") else "K" if bschl in ("25", "31") else "S"
            self.l.append({"MANDT": "100", "BUKRS": bukrs, "BELNR": belnr, "GJAHR": budat.year, "BUZEI": n,
                           "BSCHL": bschl, "KOART": koart, "SHKZG": "S" if bschl in ("01", "25", "40") else "H",
                           "DMBTR": round(abs(amt), 2), "WRBTR": round(abs(amt), 2), "HKONT": hkont,
                           "KUNNR": f"{partner:010d}" if koart == "D" else None,
                           "LIFNR": f"{partner:010d}" if koart == "K" else None,
                           "KOSTL": self.rc.get(le), "ZUONR": zuonr, "SGTXT": sgtxt, "AUGBL": None, "AUGDT": None})
        return belnr


def post(inv: pd.DataFrame, pay: pd.DataFrame, coll: pd.DataFrame, dm: pd.DataFrame, dpr: pd.DataFrame,
         masters: dict) -> dict[str, pd.DataFrame]:
    le = masters["le"]
    le_map = dict(zip(le.LE_CD, le.SAP_BUKRS))
    rc = masters["book"].groupby("LE_CD").RC_CD.first().to_dict()
    P = Poster(le_map, rc)
    inv_doc = {}
    for r in inv.itertuples(index=False):
        lines = []
        if r.GROSS_RECEIVABLE:
            lines += [("50", REV[r.SETTLE_CLASS], r.GROSS_RECEIVABLE, None, r.INVOICE_NUM, f"{r.PROD_MONTH:%b %Y} sales")]
        if r.GROSS_PAYABLE:
            lines += [("40", COST[r.SETTLE_CLASS], r.GROSS_PAYABLE, None, r.INVOICE_NUM, f"{r.PROD_MONTH:%b %Y} purchases")]
        net = r.NET_AMOUNT
        if net >= 0:
            lines.insert(0, ("01", "110100", net, int(r.CP_ID), r.INVOICE_NUM, "Unify settlement"))
            blart = "DR"
        else:
            lines.insert(0, ("31", "210100", -net, int(r.CP_ID), r.INVOICE_NUM, "Unify settlement"))
            blart = "KR"
        inv_doc[r.INVOICE_NUM] = (le_map[r.LE_CD], P.doc(r.LE_CD, blart, r.INVOICE_DT, r.INVOICE_DT, lines,
                                                         xblnr=r.INVOICE_NUM, bktxt=f"UNIFY {r.SETTLE_CLASS} {r.DOC_TYPE}"))
    # payments clear the open item (AUGBL/AUGDT on the invoice's customer/vendor line)
    clear = {}
    for r in pay.itertuples(index=False):
        if r.DIRECTION == "RECEIPT":
            b = P.doc(r.LE_CD, "DZ", r.PAY_DT, r.PAY_DT, [("40", "100100", r.AMOUNT, None, r.BANK_REF, "Incoming wire"),
                                                         ("15", "110100", r.AMOUNT, int(r.CP_ID), r.INVOICE_NUM, "Payment")],
                      xblnr=r.INVOICE_NUM, usnam="TREAS_IF", tcode="F-28")
        else:
            b = P.doc(r.LE_CD, "KZ", r.PAY_DT, r.PAY_DT, [("25", "210100", r.AMOUNT, int(r.CP_ID), r.INVOICE_NUM, "Payment"),
                                                         ("50", "100100", r.AMOUNT, None, r.BANK_REF, "Outgoing wire")],
                      xblnr=r.INVOICE_NUM, usnam="TREAS_IF", tcode="F-53")
        clear[r.INVOICE_NUM] = (b, r.PAY_DT)
    # month-end unbilled accrual for the flow month, auto-reversed on day 1 of the next month
    for (le_cd, m, cls), g in dm.groupby(["LE_CD", "FLOW_MONTH", "SETTLE_CLASS"]):
        rec, cost = g.AMOUNT[g.AMOUNT > 0].sum(), -g.AMOUNT[g.AMOUNT < 0].sum()
        me = dt.date(m.year, m.month, calendar.monthrange(m.year, m.month)[1])
        lines = []
        if rec:
            lines += [("40", "120500", rec, None, f"ACR{m:%Y%m}", "Unbilled revenue"), ("50", REV[cls], rec, None, f"ACR{m:%Y%m}", "Unbilled revenue")]
        if cost:
            lines += [("40", COST[cls], cost, None, f"ACR{m:%Y%m}", "Accrued purchases"), ("50", "220500", cost, None, f"ACR{m:%Y%m}", "Accrued purchases")]
        if not lines:
            continue
        b = P.doc(le_cd, "SA", me, me, lines, bktxt=f"{cls} flow accrual {m:%m/%y}", usnam="GLACCT01",
                  cpudt=me + dt.timedelta(days=3))
        rev_lines = [("50" if k == "40" else "40", a, x, p, z, "REVERSAL " + s) for k, a, x, p, z, s in lines]
        P.doc(le_cd, "SA", me + dt.timedelta(days=1), me + dt.timedelta(days=1), rev_lines, stblg=b,
              bktxt=f"Rev {cls} accrual {m:%m/%y}", usnam="GLACCT01")
    # EITF 98-10 mark-to-market: reverse prior month-end MTM, book current
    books_le = masters["book"].set_index("BOOK_CD").LE_CD.to_dict()
    d = dpr.assign(LE_CD=dpr.BOOK_CD.map(books_le), M=pd.to_datetime(dpr.EFF_DT).dt.to_period("M"))
    me_mtm = d.sort_values("EFF_DT").groupby(["LE_CD", "M"]).apply(
        lambda g: g[g.EFF_DT == g.EFF_DT.max()].MTM_USD.sum(), include_groups=False).reset_index(name="MTM")
    for le_cd, g in me_mtm.groupby("LE_CD"):
        prev_lines, prev_doc = None, None
        for r in g.itertuples(index=False):
            day = r.M.end_time.date()
            if prev_lines:  # reverse last month's booking line-for-line (same accounts, flipped keys)
                rev = [("50" if k == "40" else "40", a, x, p, z, "Reverse prior MTM") for k, a, x, p, z, _ in prev_lines]
                P.doc(le_cd, "SA", day, day, rev, bktxt="ERMS MTM reversal", usnam="ERMS_IF", stblg=prev_doc)
            val = r.MTM
            if abs(val) < 0.01:
                prev_lines = None
                continue
            ref = f"MTM{day:%Y%m}"
            if val > 0:
                prev_lines = [("40", "140100", val, None, ref, "Book MTM"), ("50", "410100", val, None, ref, "Book MTM")]
            else:
                prev_lines = [("40", "410100", -val, None, ref, "Book MTM"), ("50", "240100", -val, None, ref, "Book MTM")]
            prev_doc = P.doc(le_cd, "SA", day, day, prev_lines, bktxt="ERMS MTM (EITF 98-10)", usnam="ERMS_IF")
    for r in coll.itertuples(index=False):
        if r.COLLATERAL_TYPE != "CASH":
            continue
        if r.DIRECTION == "POSTED":
            lines = [("40", "150100", r.AMOUNT, None, f"COLL{r.CALL_ID}", "Margin posted"), ("50", "100100", r.AMOUNT, None, f"COLL{r.CALL_ID}", "Margin posted")]
        else:
            lines = [("40", "100100", r.AMOUNT, None, f"COLL{r.CALL_ID}", "Margin received"), ("50", "250100", r.AMOUNT, None, f"COLL{r.CALL_ID}", "Margin received")]
        P.doc(r.LE_CD, "SA", r.CALL_DT, r.CALL_DT, lines, bktxt="Collateral", usnam="CREDIT01")

    # Enron Corp ran centralized cash management: zero-balance sweep of each
    # company's concentration account to/from Corp at month end.
    hdr = pd.DataFrame(P.h)[["BUKRS", "BELNR", "GJAHR", "BUDAT"]]
    cash = pd.DataFrame(P.l).merge(hdr, on=["BUKRS", "BELNR", "GJAHR"])
    cash = cash[cash.HKONT == "100100"]
    cash["AMT"] = np.where(cash.SHKZG == "S", cash.DMBTR, -cash.DMBTR)
    cash["M"] = pd.to_datetime(cash.BUDAT).dt.to_period("M")
    bukrs_le = {v: k for k, v in le_map.items()}
    for (bukrs, m), amt in cash.groupby(["BUKRS", "M"]).AMT.sum().items():
        if abs(amt) < 0.01:
            continue
        day = m.end_time.date()
        if amt > 0:
            lines = [("40", "260100", amt, None, f"POOL{day:%Y%m}", "Sweep to Enron Corp"), ("50", "100100", amt, None, f"POOL{day:%Y%m}", "Sweep to Enron Corp")]
        else:
            lines = [("40", "100100", -amt, None, f"POOL{day:%Y%m}", "Funding from Enron Corp"), ("50", "260100", -amt, None, f"POOL{day:%Y%m}", "Funding from Enron Corp")]
        P.doc(bukrs_le[bukrs], "SA", day, day, lines, bktxt="Corp cash pool ZBA", usnam="TREAS_IF")

    bkpf, bseg = pd.DataFrame(P.h), pd.DataFrame(P.l)
    # clearing: stamp AUGBL/AUGDT on the receivable/payable line of paid invoices
    inv_line = bseg[bseg.KOART.isin(["D", "K"]) & (bseg.BUZEI == 1)]
    aug = inv_line.ZUONR.map(lambda z: clear.get(z, (None, None)))
    bseg.loc[inv_line.index, "AUGBL"] = [a[0] for a in aug]
    bseg.loc[inv_line.index, "AUGDT"] = [a[1] for a in aug]
    t001 = le.rename(columns={"SAP_BUKRS": "BUKRS", "LE_NAME": "BUTXT"})[["BUKRS", "BUTXT", "BUKRS_OBSERVED_IN_CORPUS"]].assign(WAERS="USD", LAND1="US", KTOPL="ENRN")
    ska1 = pd.DataFrame(GL, columns=["SAKNR", "TXT50", "BS_PL", "FS_CAPTION_10K"]).assign(KTOPL="ENRN")
    gcp = masters["gcp"]
    kna1 = pd.DataFrame({"KUNNR": gcp.CP_ID.map(lambda x: f"{x:010d}"), "NAME1": gcp.LEGAL_NAME.str[:35], "SORTL": gcp.SHORT_NAME, "LAND1": "US"})
    lfa1 = kna1.rename(columns={"KUNNR": "LIFNR"})
    return {"BKPF": bkpf, "BSEG": bseg, "T001": t001, "SKA1": ska1, "KNA1": kna1, "LFA1": lfa1}
