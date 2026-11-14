"""Gold: label each workbook with process area(s) and document role.

Auditable weighted-lexicon model (ontology/reference/classifier_rules.yaml). Output:
gold/workbook_labels.parquet with the top label, runner-up, margin and the evidence
terms that produced each score, so a reviewer can see why a file was labeled.
"""
from __future__ import annotations

import re
from collections import defaultdict

import duckdb
import pandas as pd
import yaml

from .. import paths

RULES = paths.ONTOLOGY / "reference" / "classifier_rules.yaml"


def load_rules():
    r = yaml.safe_load(RULES.read_text())
    comp = lambda d: {k: [re.compile(p, re.I) for p in v] for k, v in d.items()}
    return r, comp(r["process_areas"]), comp(r["document_roles"])


def features(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    b = paths.BRONZE / "hermans"
    con.execute(f"create or replace view wb as select * from read_parquet('{(b / 'workbooks.parquet').as_posix()}')")
    con.execute(f"create or replace view sh as select * from read_parquet('{(b / 'sheets.parquet').as_posix()}')")
    con.execute(f"create or replace view cells as select * from read_parquet('{(b / 'cells' / '*.parquet').as_posix()}')")
    hdr = con.execute("""
        select file_id, string_agg(value_text, ' | ') as header_text from (
            select file_id, value_text, row_number() over (partition by file_id order by sheet_idx, row, col) rn
            from cells where value_text is not null and row <= 12 and length(value_text) between 2 and 80
        ) where rn <= 120 group by file_id
    """).df()
    shn = con.execute("select file_id, string_agg(sheet_name, ' | ') sheet_names from sh group by file_id").df()
    links = paths.SILVER / "workbook_email_links.parquet"
    if links.exists():
        subj = con.execute(f"""
            select l.file_id, string_agg(distinct m.subject, ' | ') email_subjects
            from read_parquet('{links.as_posix()}') l
            join read_parquet('{(paths.SILVER / 'messages.parquet').as_posix()}') m using (message_id)
            where l.score >= 0.45 group by l.file_id
        """).df()
    else:
        subj = pd.DataFrame(columns=["file_id", "email_subjects"])
    wb = con.execute("select file_id, original_filename, custodian from wb").df()
    return wb.merge(shn, how="left").merge(hdr, how="left").merge(subj, how="left")


def _score(text_by_field: dict, compiled: dict, weights: dict):
    scores, hits = defaultdict(float), defaultdict(set)
    for field, text in text_by_field.items():
        if not text:
            continue
        w = weights[field]
        for label, pats in compiled.items():
            for p in pats:
                n = len(p.findall(text))
                if n:
                    scores[label] += w * min(n, 3)
                    hits[label].add(p.pattern)
    return scores, hits


def classify(con: duckdb.DuckDBPyConnection | None = None) -> pd.DataFrame:
    con = con or duckdb.connect()
    rules, pa_rules, role_rules = load_rules()
    fw = rules["field_weights"]
    df = features(con)
    rows = []
    for r in df.itertuples(index=False):
        fname = re.sub(r"[_\-\.]+", " ", r.original_filename or "")
        texts = {"filename": fname, "sheet_name": r.sheet_names, "header_text": r.header_text,
                 "email_subject": r.email_subjects}
        s, h = _score(texts, pa_rules, fw)
        ranked = sorted(s.items(), key=lambda kv: -kv[1])
        top, top_s = ranked[0] if ranked else ("other", 0.0)
        second, second_s = ranked[1] if len(ranked) > 1 else (None, 0.0)
        if top_s < rules["min_score"]:
            top = "unclassified"
        rs, _ = _score(texts, role_rules, fw)
        role = max(rs.items(), key=lambda kv: kv[1])[0] if rs else "other"
        rows.append({
            "file_id": r.file_id, "process_area": top, "score": round(top_s, 2),
            "runner_up": second, "runner_up_score": round(second_s, 2),
            "margin": round((top_s - second_s) / top_s, 3) if top_s else 0.0,
            "secondary_areas": [k for k, v in ranked[1:4] if v >= 0.5 * top_s],
            "document_role": role, "evidence_terms": sorted(h.get(top, [])),
            "rules_version": rules["version"],
        })
    out = pd.DataFrame(rows)
    paths.GOLD.mkdir(parents=True, exist_ok=True)
    out.to_parquet(paths.GOLD / "workbook_labels.parquet", index=False)
    return out
