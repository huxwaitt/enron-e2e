"""Gold: mine reference entities and value profiles from labeled workbook columns.

A header cell (e.g. "Counterparty", "Deal #", "Trader") defines a field family.
Columnar layout: values are the cells below the header in the same column.
Form layout ("Counterparty:"): the value is the next non-empty cell to the right.

Outputs (gold/reference/):
  field_values.parquet       every mined (family, value, file, sheet, cell) observation
  counterparties.parquet     normalized counterparty master candidates with aliases + evidence
  traders.parquet, books.parquet, desks.parquet
  deal_number_profile.parquet  length/prefix/range of deal identifiers by system family
  numeric_profile.parquet    quantiles of price/volume columns by commodity hint and year
  lexicon_hits.parquet       observed counts for each ontology/reference/lexicon.yaml entry
"""
from __future__ import annotations

import re

import duckdb
import pandas as pd
import yaml

from .. import paths

OUT = paths.GOLD / "reference"
FAMILIES = {
    "counterparty": r"counter ?party|cpty|cp|customer|company|shipper|buyer|seller|cp name|counterparty name",
    "trader": r"trader|trader name",
    "book": r"book|portfolio|book name|book code",
    "desk": r"desk",
    "deal_id": r"deal ?(#|no\.?|num(ber)?)?|deal ?id|ena deal ?#?",
    "sitara_id": r"sitara ?(#|deal ?#?|no\.?)?",
    "eol_id": r"eol ?(#|deal ?#?|no\.?|id)?",
    "tagg_id": r"tagg ?(#|no\.?)?",
    "price": r"price|fixed price|deal price",
    "volume": r"volume|vol|quantity|qty",
    "location": r"location|point|delivery point|receipt point|pipeline",
    "index": r"index|price index",
    "product": r"product",
    "trade_date": r"trade date|deal date",
}
SUFFIX_RE = re.compile(
    r"[\s,\.]+(inc|incorporated|corp|corporation|co|company|llc|l\.l\.c|lp|l\.p|ltd|limited|plc|na|n\.a)\.?$", re.I)


def norm_name(s: str) -> str:
    s = re.sub(r"\s+", " ", s.strip().strip('"').strip())
    prev = None
    while prev != s:
        prev = s
        s = SUFFIX_RE.sub("", s).strip(" ,.")
    return s.upper()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:80]


def mine(con: duckdb.DuckDBPyConnection | None = None) -> dict:
    con = con or duckdb.connect()
    con.execute("set enable_progress_bar = false")
    OUT.mkdir(parents=True, exist_ok=True)
    b = paths.BRONZE / "hermans"
    con.execute(f"create or replace view c as select * from read_parquet('{(b / 'cells' / '*.parquet').as_posix()}')")
    con.execute(f"create or replace view wb as select * from read_parquet('{(b / 'workbooks.parquet').as_posix()}')")
    case = " ".join(f"when regexp_full_match(h, '{p}') then '{f}'" for f, p in FAMILIES.items())
    con.execute(rf"""
        create or replace table headers as
        select file_id, sheet_idx, row, col, value_text as header_raw, family,
               ends_with(trim(value_text), ':') as form_layout
        from (
            select *, case {case} else null end as family
            from (select *, regexp_replace(lower(trim(value_text)), '\s*:\s*$', '') as h
                  from c where value_text is not null and length(value_text) <= 30 and row <= 40)
        ) where family is not null
    """)
    con.execute("""
        create or replace table field_values as
        -- columnar: up to 500 rows below a non-form header, stopping at nothing (blank rows are common)
        select h.family, h.file_id, h.sheet_idx, c.row, c.col, c.ref, coalesce(c.value_text, c.value_num::varchar) as value,
               c.value_num, c.is_date_fmt, 'columnar' as layout
        from headers h join c on c.file_id = h.file_id and c.sheet_idx = h.sheet_idx and c.col = h.col
             and c.row > h.row and c.row <= h.row + 500
        where not h.form_layout
        union all
        select h.family, h.file_id, h.sheet_idx, c.row, c.col, c.ref, coalesce(c.value_text, c.value_num::varchar),
               c.value_num, c.is_date_fmt, 'form'
        from headers h join c on c.file_id = h.file_id and c.sheet_idx = h.sheet_idx and c.row = h.row
             and c.col between h.col + 1 and h.col + 3
        where h.form_layout
    """)
    con.execute(f"copy field_values to '{(OUT / 'field_values.parquet').as_posix()}' (format parquet, compression zstd)")

    # ---- counterparties
    fv = con.execute("""
        select value, count(*) n_cells, count(distinct file_id) n_files, list(distinct file_id)[1:5] sample_files
        from field_values
        where family = 'counterparty' and value_num is null and length(value) between 3 and 70
          and not regexp_matches(lower(value), '^(total|subtotal|grand total|counterparty|company|customer|contact|phone|fax|name|address|date|n/?a|tbd|various|none|other)\\b')
        group by value
    """).df()
    fv["name_norm"] = fv["value"].map(norm_name)
    fv = fv[fv.name_norm.str.contains(r"[A-Z]{3}", regex=True)]
    cp = (fv.groupby("name_norm")
            .agg(n_files=("n_files", "sum"), n_cells=("n_cells", "sum"),
                 aliases=("value", lambda s: sorted(set(s))[:20]),
                 sample_files=("sample_files", lambda s: sorted({f for l in s for f in l})[:5]))
            .reset_index())
    cp["is_enron_affiliate"] = cp.name_norm.str.contains(r"\bENRON\b|\bECT\b|\bENA\b|\bEPMI\b|\bEES\b", regex=True)
    cp = cp[cp.n_files >= 2].sort_values("n_files", ascending=False)
    cp["cp_iri"] = "enroni:cp/" + cp.name_norm.map(slug)
    cp.to_parquet(OUT / "counterparties.parquet", index=False)

    # ---- traders / books / desks
    for fam in ("trader", "book", "desk"):
        d = con.execute(f"""
            select trim(value) value, count(*) n_cells, count(distinct file_id) n_files
            from field_values where family = '{fam}' and value_num is null and length(trim(value)) between 2 and 40
              and not regexp_matches(lower(value), '^(total|subtotal|{fam})')
            group by 1 having count(distinct file_id) >= 2 order by n_files desc
        """).df()
        d.to_parquet(OUT / f"{fam}s.parquet", index=False)

    # ---- deal-number profile per identifier family
    con.execute(f"""
        copy (
            select family, length(v) as id_length, regexp_extract(v, '^[A-Za-z]*', 0) as prefix,
                   count(*) n, count(distinct file_id) n_files,
                   min(try_cast(regexp_extract(v, '\\d+', 0) as bigint)) min_num,
                   approx_quantile(try_cast(regexp_extract(v, '\\d+', 0) as bigint), 0.5) median_num,
                   max(try_cast(regexp_extract(v, '\\d+', 0) as bigint)) max_num
            from (select family, file_id, regexp_replace(trim(value), '\\.0$', '') v from field_values
                  where family in ('deal_id', 'sitara_id', 'eol_id', 'tagg_id'))
            where regexp_matches(v, '^[A-Za-z]{{0,4}}-?\\d{{4,12}}$')
            group by 1, 2, 3 having count(*) >= 20 order by family, n desc
        ) to '{(OUT / 'deal_number_profile.parquet').as_posix()}' (format parquet)
    """)

    # ---- numeric profiles for price / volume, split by commodity hint in file or sheet text
    con.execute(f"""
        copy (
            with fl as (
                select f.file_id,
                       case when regexp_matches(lower(w.original_filename), 'power|mw|peak|epmi|caiso|pjm|ercot|mid-?c|np ?15|sp ?15|palo') then 'power'
                            when regexp_matches(lower(w.original_filename), 'gas|mmbtu|dth|nom|pipe|hub|sitara|nng|tw\\b|transco|el ?paso') then 'natural_gas'
                            else 'unknown' end as commodity_hint,
                       try_cast(substr(w.created, 1, 4) as int) as yr
                from (select distinct file_id from field_values) f join wb w using (file_id)
            )
            select v.family, fl.commodity_hint, fl.yr, count(*) n, count(distinct v.file_id) n_files,
                   approx_quantile(v.value_num, 0.05) p05, approx_quantile(v.value_num, 0.25) p25,
                   approx_quantile(v.value_num, 0.5) p50, approx_quantile(v.value_num, 0.75) p75,
                   approx_quantile(v.value_num, 0.95) p95
            from field_values v join fl using (file_id)
            where v.family in ('price', 'volume') and v.value_num is not null and not v.is_date_fmt
              and v.value_num > 0
            group by 1, 2, 3 having count(*) >= 50 order by 1, 2, 3
        ) to '{(OUT / 'numeric_profile.parquet').as_posix()}' (format parquet)
    """)

    # ---- lexicon hits over distinct text values
    lex = yaml.safe_load((paths.ONTOLOGY / "reference" / "lexicon.yaml").read_text())
    con.execute("""
        create or replace table vals as
        select value_text v, count(*) n_cells, count(distinct file_id) n_files
        from c where value_text is not null and length(value_text) between 2 and 120 group by 1
    """)
    rows = []
    for group, entries in lex.items():
        for e in entries:
            pat = "(?i)(" + "|".join(e["aliases"]) + ")"
            n_vals, n_cells, n_files_upper = con.execute(
                "select count(*), coalesce(sum(n_cells),0), coalesce(sum(n_files),0) from vals where regexp_matches(v, ?)", [pat]).fetchone()
            rows.append({"group": group, "slug": e["slug"], "label": e["label"], "observed": n_cells > 0,
                         "distinct_values": n_vals, "cells": n_cells, "file_mentions_upper_bound": n_files_upper})
    pd.DataFrame(rows).to_parquet(OUT / "lexicon_hits.parquet", index=False)

    return {
        "headers": con.execute("select count(*) from headers").fetchone()[0],
        "field_values": con.execute("select count(*) from field_values").fetchone()[0],
        "counterparties": len(cp), "external_counterparties": int((~cp.is_enron_affiliate).sum()),
    }
