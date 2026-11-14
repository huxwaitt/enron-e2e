"""Data contracts (ODCS v3 style), quality checks, lineage and run manifests.

contracts/<layer>/<table>.yaml is the contract: owner, purpose, schema, PII
classification and quality rules. `enron-e2e contracts` regenerates the schema
section from the physical table while preserving hand-written annotations, and
`enron-e2e dq` executes every rule and writes lake/_meta/dq_results.parquet.
Each pipeline step records an OpenLineage-style event in lake/_meta/lineage.jsonl.
"""
from __future__ import annotations

import datetime as dt
import json
import uuid
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from . import paths

PRODUCER = "https://github.com/huxwaitt/enron-e2e"

# Table registry: physical location, owner, purpose, PII, and quality rules (SQL returning 0 rows == pass)
TABLES: dict[str, dict] = {
    "bronze.hermans_workbooks": {
        "path": "bronze/hermans/workbooks.parquet", "owner": "data-platform", "domain": "corpus",
        "purpose": "One row per spreadsheet file in the Hermans corpus with OOXML document properties.",
        "limitations": "last_modified_by='Felienne' and 2014 modified dates are artifacts of the 2014 xls->xlsx conversion; use `created`.",
        "pii": {"author": "personal_name"},
        "keys": ["file_name"],
        "quality": [
            ("file_name_unique", "select file_name from t group by 1 having count(*) > 1"),
            ("content_hash_unique_among_originals", "select file_id from t where duplicate_of is null group by 1 having count(*) > 1"),
            ("parse_errors_below_2pct", "select 1 from t having avg((parse_status <> 'ok')::int) > 0.02"),
            ("custodian_present", "select * from t where custodian is null"),
        ],
    },
    "bronze.hermans_sheets": {
        "path": "bronze/hermans/sheets.parquet", "owner": "data-platform", "domain": "corpus",
        "purpose": "One row per worksheet, with visibility, dimensions and structural feature counts.",
        "keys": ["file_id", "sheet_idx"],
        "quality": [("pk_unique", "select file_id, sheet_idx from t group by 1,2 having count(*) > 1"),
                    ("state_domain", "select * from t where state not in ('visible','hidden','veryHidden')")],
    },
    "bronze.hermans_cells": {
        "path": "bronze/hermans/cells/*.parquet", "owner": "data-platform", "domain": "corpus",
        "purpose": "Every non-empty cell: cached value, formula text, number format.",
        "limitations": "Shared formulas are stored once on the anchor cell (formula_kind='shared'); dependents carry shared_index only.",
        "keys": ["file_id", "sheet_idx", "ref"],
        "quality": [("has_value_or_formula", "select * from t where value_text is null and value_num is null and formula is null limit 1"),
                    ("row_positive", "select * from t where row < 1 limit 1")],
    },
    "bronze.cmu_messages": {
        "path": "bronze/cmu_email/messages/*.parquet", "owner": "data-platform", "domain": "corpus",
        "purpose": "Every file in the CMU maildir, parsed headers and body.",
        "pii": {"body": "free_text_may_contain_pii", "from_addr": "email_address", "to_addrs": "email_address"},
        "keys": ["path"],
        "quality": [("path_unique", "select path from t group by 1 having count(*) > 1"),
                    ("date_parsed_99pct", "select 1 from t having avg((date_utc is null)::int) > 0.01")],
    },
    "silver.messages": {
        "path": "silver/messages.parquet", "owner": "finance-data-engineering", "domain": "communications",
        "purpose": "Unique messages (copies across mailboxes collapsed) with custodian list.",
        "pii": {"body": "free_text_may_contain_pii"},
        "keys": ["message_id"],
        "quality": [("message_id_unique", "select message_id from t group by 1 having count(*) > 1")],
    },
    "silver.persons": {
        "path": "silver/persons.parquet", "owner": "finance-data-engineering", "domain": "reference",
        "purpose": "People with @enron.com addresses, keyed by enroni:person IRIs.",
        "pii": {"email": "email_address", "display_name": "personal_name"},
        "keys": ["person_iri"],
        "quality": [("iri_unique", "select person_iri from t group by 1 having count(*) > 1")],
    },
    "silver.workbook_email_links": {
        "path": "silver/workbook_email_links.parquet", "owner": "finance-data-engineering", "domain": "communications",
        "purpose": "Scored links between attachment names in email bodies and workbook files.",
        "keys": ["message_id", "filename", "file_id"],
        "quality": [("score_range", "select * from t where score <= 0 or score > 1.0001")],
    },
    "gold.workbook_labels": {
        "path": "gold/workbook_labels.parquet", "owner": "finance-analytics", "domain": "process",
        "purpose": "Process-area and document-role label per workbook with evidence terms.",
        "keys": ["file_id"],
        "quality": [("one_label_per_file", "select file_id from t group by 1 having count(*) > 1"),
                    ("unclassified_below_25pct", "select 1 from t having avg((process_area = 'unclassified')::int) > 0.25")],
    },
    "gold.workbook_standards": {
        "path": "gold/workbook_standards.parquet", "owner": "finance-analytics", "domain": "standards",
        "purpose": "Standards in force for each workbook's process areas at the workbook's creation date.",
        "limitations": "Driven by heuristic process-area labels; standards with unverified effective dates are included and flagged.",
        "keys": ["file_id", "standard_id"],
        "quality": [("pk_unique", "select file_id, standard_id from t group by 1,2 having count(*) > 1"),
                    ("no_future_standards", "select * from t where effective_known and effective > created")],
    },
}


def _contract(name: str, spec: dict, con: duckdb.DuckDBPyConnection) -> dict | None:
    p = paths.LAKE / spec["path"]
    if not list(p.parent.glob(p.name)):
        return None
    cols = con.execute(f"describe select * from read_parquet('{p.as_posix()}')").fetchall()
    layer, table = name.split(".", 1)
    props = []
    for c in cols:
        props.append({
            "name": c[0], "physicalType": c[1],
            "logicalType": _logical(c[1]),
            "primaryKey": c[0] in spec.get("keys", []),
            **({"classification": "restricted", "tags": [f"pii:{spec['pii'][c[0]]}"]} if c[0] in spec.get("pii", {}) else {}),
        })
    return {
        "apiVersion": "v3.0.2", "kind": "DataContract",
        "id": f"urn:enron-e2e:{name}", "name": name, "version": "1.0.0", "status": "active",
        "domain": spec["domain"], "dataProduct": layer,
        "description": {"purpose": spec["purpose"], **({"limitations": spec["limitations"]} if "limitations" in spec else {})},
        "team": [{"role": "owner", "username": spec["owner"]}],
        "schema": [{"name": table, "physicalName": spec["path"], "physicalType": "parquet", "properties": props,
                    "quality": [{"name": n, "type": "sql", "query": q, "mustBe": 0, "dimension": "conformity"}
                                for n, q in spec.get("quality", [])]}],
        "tags": [layer, spec["domain"]],
    }


def _logical(phys: str) -> str:
    p = phys.upper()
    if p.startswith(("INT", "BIGINT", "SMALLINT", "TINYINT", "HUGEINT")):
        return "integer"
    if p.startswith(("DOUBLE", "FLOAT", "DECIMAL", "REAL")):
        return "number"
    if p.startswith("BOOL"):
        return "boolean"
    if p.startswith(("TIMESTAMP", "DATE")):
        return "date"
    if p.endswith("[]") or p.startswith(("LIST", "STRUCT", "MAP")):
        return "array" if p.endswith("[]") or p.startswith("LIST") else "object"
    return "string"


def write_contracts() -> list[str]:
    con = duckdb.connect()
    written = []
    for name, spec in TABLES.items():
        c = _contract(name, spec, con)
        if c is None:
            continue
        layer, table = name.split(".", 1)
        out = paths.CONTRACTS / layer / f"{table}.yaml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump(c, sort_keys=False, width=110))
        written.append(str(out))
    return written


def run_quality() -> pd.DataFrame:
    con = duckdb.connect()
    rows, now = [], dt.datetime.now(dt.timezone.utc)
    for name, spec in TABLES.items():
        p = paths.LAKE / spec["path"]
        if not list(p.parent.glob(p.name)):
            continue
        con.execute(f"create or replace view t as select * from read_parquet('{p.as_posix()}')")
        n = con.execute("select count(*) from t").fetchone()[0]
        for rule, q in spec.get("quality", []):
            try:
                bad = con.execute(f"select count(*) from ({q})").fetchone()[0]
                rows.append({"table": name, "rule": rule, "rows_in_table": n, "violations": bad,
                             "passed": bad == 0, "checked_at": now, "error": None})
            except Exception as e:
                rows.append({"table": name, "rule": rule, "rows_in_table": n, "violations": None,
                             "passed": False, "checked_at": now, "error": str(e)[:300]})
    df = pd.DataFrame(rows)
    paths.META.mkdir(parents=True, exist_ok=True)
    df.to_parquet(paths.META / "dq_results.parquet", index=False)
    return df


def lineage(job: str, inputs: list[str], outputs: list[str], state: str = "COMPLETE", facets: dict | None = None):
    """Append an OpenLineage RunEvent (spec 2-0-2 shape) for a pipeline step."""
    paths.META.mkdir(parents=True, exist_ok=True)
    ev = {
        "eventType": state, "eventTime": dt.datetime.now(dt.timezone.utc).isoformat(),
        "producer": PRODUCER, "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/definitions/RunEvent",
        "run": {"runId": str(uuid.uuid4()), "facets": facets or {}},
        "job": {"namespace": "enron-e2e", "name": job},
        "inputs": [{"namespace": "enron-e2e", "name": i} for i in inputs],
        "outputs": [{"namespace": "enron-e2e", "name": o} for o in outputs],
    }
    with (paths.META / "lineage.jsonl").open("a") as f:
        f.write(json.dumps(ev) + "\n")
