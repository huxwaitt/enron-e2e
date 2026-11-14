"""Gold: which standards governed each workbook when it was created.

A standard applies to a workbook if they share a process area (primary or secondary
label) and the standard was effective on the workbook's creation date. Standards with
unverified effective dates are kept and flagged (`effective_known = false`), not dropped.
Superseded standards (EITF 98-10 after EITF 02-3, etc.) apply only before the successor
took effect.

gold/workbook_standards.parquet   file_id x standard_id with in-force evidence
gold/standards.parquet            the catalog flattened for SQL use
"""
from __future__ import annotations

import pandas as pd
import yaml

from .. import paths


def _date(v) -> pd.Timestamp | None:
    if v in (None, ""):
        return None
    s = str(v)
    s = s + "-01" * (2 - s.count("-")) if len(s) < 10 else s
    try:
        return pd.Timestamp(s)
    except ValueError:
        return None


def build() -> dict:
    d = yaml.safe_load((paths.ROOT / "standards" / "era_standards.yaml").read_text())
    recs = d if isinstance(d, list) else d["standards"]
    std = pd.DataFrame([{
        "standard_id": r["id"], "title": r["title"], "issuer": r.get("issuer"), "designation": r.get("designation"),
        "category": r.get("category"), "post_enron": bool(r.get("post_enron")),
        "effective": _date(r.get("effective")), "superseded_by": r.get("superseded_by"),
        "process_areas": r.get("process_areas", []), "today_codification": (r.get("today") or {}).get("codification"),
        "enron_relevance": r.get("enron_relevance"),
    } for r in recs])
    eff = std.set_index("standard_id").effective.to_dict()
    sup = []
    for r in std.itertuples():
        succ = r.superseded_by
        if isinstance(succ, list):
            succ = succ[0] if succ else None
        sup.append(eff.get(succ) if isinstance(succ, str) else None)
    std["superseded_on"] = sup
    std.to_parquet(paths.GOLD / "standards.parquet", index=False)

    wb = pd.read_parquet(paths.BRONZE / "hermans" / "workbooks.parquet", columns=["file_id", "created", "duplicate_of"])
    wb = wb[wb.duplicate_of.isna()]
    wb["created_ts"] = pd.to_datetime(wb.created, errors="coerce", utc=True).dt.tz_localize(None)
    wb = wb[wb.created_ts.between("1995-01-01", "2002-12-31")]
    lab = pd.read_parquet(paths.GOLD / "workbook_labels.parquet", columns=["file_id", "process_area", "secondary_areas"])
    lab["areas"] = [[p] + list(s if s is not None else []) for p, s in zip(lab.process_area, lab.secondary_areas)]
    w = wb.merge(lab[["file_id", "areas"]], on="file_id").explode("areas").rename(columns={"areas": "process_area"})
    s = std.explode("process_areas").rename(columns={"process_areas": "process_area"})
    j = w.merge(s, on="process_area")
    in_force = (j.effective.isna() | (j.effective <= j.created_ts)) & (j.superseded_on.isna() | (j.created_ts < j.superseded_on))
    j = j[in_force]
    out = (j.groupby(["file_id", "standard_id"])
             .agg(created=("created_ts", "first"), via_process_areas=("process_area", lambda x: sorted(set(x))),
                  effective=("effective", "first"), post_enron=("post_enron", "first"))
             .reset_index())
    out["effective_known"] = out.effective.notna()
    out.to_parquet(paths.GOLD / "workbook_standards.parquet", index=False)
    return {"standards": len(std), "pairs": len(out), "workbooks": out.file_id.nunique(),
            "post_enron_pairs": int(out.post_enron.sum())}
