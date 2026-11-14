"""Market data for the synthetic estate: spot paths, forward curves, published indices.

Gas is anchored to EIA Henry Hub monthly averages (ontology/reference/market_history.yaml);
hub basis and power prices are shaped to the 2000-01 Western crisis and to the price
quantiles mined from the corpus (gold/reference/numeric_profile.parquet).
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import yaml

from .. import paths

START = dt.date(2000, 1, 3)
END = dt.date(2001, 12, 31)
HORIZON_MONTHS = 36
GAS_SEASON = np.array([1.12, 1.10, 1.02, 0.95, 0.93, 0.94, 0.97, 0.98, 0.96, 0.98, 1.04, 1.10])
PWR_SEASON = np.array([1.00, 0.95, 0.90, 0.88, 0.95, 1.10, 1.35, 1.40, 1.05, 0.92, 0.95, 1.02])

# hub -> (region, static basis to Henry Hub, crisis weight)
GAS_HUBS = {
    "henry-hub": ("gulf", 0.00, 0.0), "katy": ("texas", -0.05, 0.0), "houston-ship-channel": ("texas", -0.03, 0.0),
    "waha": ("texas", -0.18, 0.2), "carthage": ("texas", -0.07, 0.0), "agua-dulce": ("texas", -0.06, 0.0),
    "chicago-citygate": ("central", 0.08, 0.0), "michcon": ("central", 0.12, 0.0), "transco-z6-ny": ("east", 0.55, 0.0),
    "tetco-m3": ("east", 0.45, 0.0), "dominion-south": ("east", 0.25, 0.0), "socal-border": ("west", 0.20, 1.0),
    "pge-citygate": ("west", 0.30, 0.8), "malin": ("west", 0.05, 0.6), "sumas": ("west", -0.05, 0.6),
    "permian": ("west", -0.25, 0.25), "san-juan": ("west", -0.35, 0.3), "rockies": ("west", -0.55, 0.1),
    "aeco": ("canada", -0.45, 0.1),
}
# power point -> (region, heat rate, crisis weight)
POWER_POINTS = {
    "mid-c": ("west", 10.0, 1.0), "cob": ("west", 10.5, 1.0), "np15": ("west", 11.0, 1.0), "sp15": ("west", 11.0, 1.0),
    "zp26": ("west", 11.0, 0.9), "palo-verde": ("west", 10.5, 0.8), "four-corners": ("west", 10.0, 0.6),
    "mead": ("west", 10.5, 0.7), "pjm-west": ("east", 9.5, 0.0), "cinergy": ("east", 9.0, 0.0),
    "entergy": ("east", 9.0, 0.0), "tva": ("east", 9.0, 0.0), "comed": ("east", 9.0, 0.0),
    "into-southern": ("east", 9.0, 0.0), "nepool": ("east", 10.0, 0.0), "nyiso": ("east", 10.5, 0.0),
    "ercot": ("texas", 9.5, 0.0),
}


def bump(days: np.ndarray, center: str, width: float) -> np.ndarray:
    c = np.datetime64(center)
    return np.exp(-(((days - c).astype("timedelta64[D]").astype(float)) / width) ** 2)


class Market:
    def __init__(self, rng: np.random.Generator):
        hist = yaml.safe_load((paths.ONTOLOGY / "reference" / "market_history.yaml").read_text())
        self.hh_monthly = {k: float(v) for k, v in hist["henry_hub_spot_monthly"]["values"].items()}
        self.days = pd.bdate_range(START, END)
        self.d64 = self.days.values.astype("datetime64[D]")
        n = len(self.days)
        # Henry Hub daily spot: monthly anchor interpolated mid-month to mid-month, OU noise
        mids = sorted(self.hh_monthly)
        mid_dates = np.array([np.datetime64(f"{m}-15") for m in mids])
        mid_vals = np.array([self.hh_monthly[m] for m in mids])
        base = np.interp(self.d64.astype(float), mid_dates.astype("datetime64[D]").astype(float), mid_vals)
        x = np.zeros(n)
        eps = rng.normal(0, 0.035, n)
        for i in range(1, n):
            x[i] = 0.88 * x[i - 1] + eps[i]
        self.hh_spot = base * np.exp(x)
        # western crisis shape for basis and power
        self.west_gas_crisis = 14.0 * bump(self.d64, "2000-12-12", 28) + 4.0 * bump(self.d64, "2001-02-10", 35)
        self.west_pwr_crisis = (3.2 * bump(self.d64, "2000-12-15", 40) + 1.4 * bump(self.d64, "2000-08-10", 30)
                                + 1.8 * bump(self.d64, "2001-01-25", 35) + 1.2 * bump(self.d64, "2001-05-10", 35))
        self.east_summer = 0.6 * bump(self.d64, "2000-07-20", 25) + 0.5 * bump(self.d64, "2001-07-25", 25)
        self.gas_noise = {h: rng.normal(0, 0.02, n) for h in GAS_HUBS}
        self.pwr_noise = {p: np.exp(rng.normal(0, 0.10, n)) for p in POWER_POINTS}
        self.idx = {d.date(): i for i, d in enumerate(self.days)}

    # ---------------- spot ----------------
    def gas_spot(self, hub: str) -> np.ndarray:
        _, basis, crisis = GAS_HUBS[hub]
        return np.maximum(0.8, self.hh_spot + basis + crisis * self.west_gas_crisis + self.gas_noise[hub])

    def power_spot(self, point: str) -> np.ndarray:
        region, hr, crisis = POWER_POINTS[point]
        hh = self.gas_spot("henry-hub")
        gas = hh + 0.25 * (self.gas_spot("socal-border") - hh) if region == "west" else hh
        mult = 1 + crisis * self.west_pwr_crisis + (self.east_summer if region == "east" else 0)
        return np.maximum(8.0, (hr * gas * 0.85 + 6.0) * mult * self.pwr_noise[point])

    # ---------------- forward curves ----------------
    def forward_matrix(self, spot: np.ndarray, season: np.ndarray, long_run: float, tau: float = 5.0) -> np.ndarray:
        """F[i, h] = forward on valuation day i for contract month (month(i) + h)."""
        mon = self.days.month.values - 1
        F = np.empty((len(spot), HORIZON_MONTHS))
        for h in range(HORIZON_MONTHS):
            tgt = (mon + h) % 12
            w = np.exp(-h / tau)
            F[:, h] = w * spot * season[tgt] / season[mon] + (1 - w) * long_run * season[tgt]
        return F

    def curves(self) -> dict[str, np.ndarray]:
        out = {}
        for hub in GAS_HUBS:
            out[f"NG-{hub.upper()}"] = self.forward_matrix(self.gas_spot(hub), GAS_SEASON, 3.4 + GAS_HUBS[hub][1])
        for pt in POWER_POINTS:
            lr = 42.0 if POWER_POINTS[pt][0] == "west" else 36.0
            out[f"PWR-{pt.upper()}-ONPK"] = self.forward_matrix(self.power_spot(pt), PWR_SEASON, lr, tau=3.0)
        return out

    def month_index(self, i: int, month: dt.date) -> int:
        d = self.days[i]
        return (month.year - d.year) * 12 + (month.month - d.month)

    # ---------------- published indices ----------------
    def gas_daily(self) -> pd.DataFrame:
        rows = []
        for hub in GAS_HUBS:
            s = self.gas_spot(hub)
            rows.append(pd.DataFrame({"INDEX_CD": f"GD-{hub.upper()}", "PUBLISHER": "Platts Gas Daily",
                                      "LOCATION_CD": hub, "PRICE_DT": self.days.date, "PRICE": np.round(s, 4)}))
        return pd.concat(rows, ignore_index=True)

    def iferc_monthly(self, curves: dict[str, np.ndarray]) -> pd.DataFrame:
        """First-of-month index = average forward for the prompt month over bidweek (last 5 business days)."""
        rows = []
        months = pd.period_range("2000-02", "2002-01", freq="M")
        for hub in GAS_HUBS:
            F = curves[f"NG-{hub.upper()}"]
            for m in months:
                prev_end = (m - 1).end_time.date()
                bid = [i for i, d in enumerate(self.days) if d.date() <= prev_end][-5:]
                if not bid:
                    continue
                rows.append({"INDEX_CD": f"IF-{hub.upper()}", "PUBLISHER": "Inside FERC Gas Market Report",
                             "LOCATION_CD": hub, "FLOW_MONTH": m.start_time.date(),
                             "PRICE": round(float(np.mean([F[i, 1] for i in bid])), 4)})
        return pd.DataFrame(rows)

    def power_daily(self) -> pd.DataFrame:
        rows = []
        for pt in POWER_POINTS:
            s = self.power_spot(pt)
            rows.append(pd.DataFrame({"INDEX_CD": f"DJ-{pt.upper()}-ONPK", "PUBLISHER": "Dow Jones Power Index",
                                      "LOCATION_CD": pt, "PRICE_DT": self.days.date, "PRICE": np.round(s, 2)}))
        return pd.concat(rows, ignore_index=True)
