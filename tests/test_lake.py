"""Integration checks over a built lake. Skipped when the lake has not been built."""
from __future__ import annotations

import duckdb
import pytest

from enron_e2e import paths

pytestmark = pytest.mark.skipif(not (paths.LAKE / "enron.duckdb").exists(), reason="lake not built (run `enron-e2e all`)")


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect(str(paths.LAKE / "enron.duckdb"), read_only=True)
    c.execute("set enable_progress_bar = false")
    return c


def test_every_sap_document_balances(con):
    bad = con.execute("""select count(*) from (select bukrs, belnr, gjahr from bronze.sap_bseg group by all
                         having abs(sum(case shkzg when 'S' then dmbtr else -dmbtr end)) > 0.01)""").fetchone()[0]
    assert bad == 0


@pytest.mark.parametrize("u", ["unify_gas", "unify_power", "unify_financial"])
def test_invoices_foot_to_lines(con, u):
    bad = con.execute(f"""select count(*) from bronze.{u}_invoice_hdr h
        join (select invoice_num, sum(amount) s from bronze.{u}_invoice_line group by 1) l using (invoice_num)
        where abs(h.net_amount - l.s) > 0.05""").fetchone()[0]
    assert bad == 0


def test_sap_cash_is_pooled_to_zero(con):
    bal = con.execute("""select sum(case shkzg when 'S' then dmbtr else -dmbtr end) from bronze.sap_bseg
                         where hkont = '100100'""").fetchone()[0]
    assert abs(bal) < 1.0


def test_no_duplicate_cells(con):
    dup = con.execute("""select count(*) from (select file_id, sheet_idx, ref from bronze.hermans_cells
                         group by all having count(*) > 1)""").fetchone()[0]
    assert dup == 0


def test_ocel_referential_integrity(con):
    orphans = con.execute("""select count(*) from gold.process_log_event_object eo
        left join gold.process_log_events e on e.ocel_id = eo.ocel_event_id where e.ocel_id is null""").fetchone()[0]
    assert orphans == 0
    kinds = dict(con.execute("select split_part(provenance, ':', 1), count(*) from gold.process_log_events group by 1").fetchall())
    assert kinds.get("observed", 0) > 10_000 and kinds.get("synthetic", 0) > 100_000


def test_trading_stops_after_enrononline_shutdown(con):
    late = con.execute("select count(*) from bronze.sitara_deal where trade_dt > date '2001-11-29'").fetchone()[0]
    assert late == 0


def test_dq_rules_pass():
    import pandas as pd
    df = pd.read_parquet(paths.META / "dq_results.parquet")
    failed = df[~df.passed]
    assert failed.empty, failed[["table", "rule", "violations", "error"]].to_string()
