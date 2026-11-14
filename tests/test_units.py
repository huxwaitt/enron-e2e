"""Fast tests that need no downloaded data."""
from __future__ import annotations

import datetime as dt

import numpy as np
import openpyxl
import pandas as pd
import pytest
import yaml

from enron_e2e import paths
from enron_e2e.gold import classify
from enron_e2e.gold.reference import norm_name
from enron_e2e.ingest import emails, workbooks
from enron_e2e.synth import sap
from enron_e2e.synth.market import Market


def test_ooxml_parser_reads_formulas_values_and_structure(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "DPR"
    ws["A1"] = "Counterparty"
    ws["B1"] = "Volume"
    ws["A2"] = "Reliant Energy Services, Inc."
    ws["B2"] = 10000
    ws["B3"] = "=B2*2"
    ws.merge_cells("D1:E1")
    hidden = wb.create_sheet("old")
    hidden.sheet_state = "hidden"
    hidden["A1"] = 1.5
    p = tmp_path / "john_doe__1__test.xlsx"
    wb.save(p)
    r = workbooks.process_file(str(p))
    assert r["workbook"]["custodian"] == "john_doe" and r["workbook"]["original_filename"] == "test.xlsx"
    sheets = {s["sheet_name"]: s for s in r["sheets"]}
    assert sheets["old"]["state"] == "hidden" and sheets["DPR"]["n_merged"] == 1
    cells = {(c[1], c[4]): c for c in r["cells"]}
    assert cells[(0, "A2")][6] == "Reliant Energy Services, Inc."
    assert cells[(0, "B3")][8] == "B2*2"          # formula text preserved
    assert cells[(1, "A1")][7] == 1.5


def test_email_parse_and_attachment_markers():
    raw = (b"Message-ID: <1.2.JavaMail.evans@thyme>\nDate: Mon, 14 May 2001 16:39:00 -0700 (PDT)\n"
           b"From: kate.symes@enron.com\nTo: a@enron.com, b@enron.com\nSubject: RE: DPR\n\n"
           b"See attached.\n\n - DPR_0514.xls\n<<West Positions 5-14.xls>>\n")
    row = emails.parse_message("maildir/symes-k/inbox/1.", raw)
    assert row["custodian"] == "symes-k" and row["to_addrs"] == ["a@enron.com", "b@enron.com"]
    assert row["date_utc"].isoformat().startswith("2001-05-14T23:39")
    names = {r["filename"] for r in emails.attachment_refs(row)}
    assert {"DPR_0514.xls", "West Positions 5-14.xls"} <= names


@pytest.mark.parametrize("raw,expected", [
    ("Duke Energy Trading and Marketing, L.L.C.", "DUKE ENERGY TRADING AND MARKETING"),
    ("Reliant Energy Services, Inc.", "RELIANT ENERGY SERVICES"),
    ("  El Paso Merchant Energy, L.P. ", "EL PASO MERCHANT ENERGY"),
])
def test_norm_name(raw, expected):
    assert norm_name(raw) == expected


def test_classifier_scores_explainably():
    _, pa_rules, _ = classify.load_rules()
    scores, hits = classify._score({"filename": "West Power Position DPR", "sheet_name": None,
                                    "header_text": "Book | MTM | P&L", "email_subject": None},
                                   pa_rules, {"filename": 3.0, "sheet_name": 2.0, "header_text": 1.0, "email_subject": 1.5})
    assert max(scores, key=scores.get) == "risk_and_valuation"
    assert hits["risk_and_valuation"]


def test_market_is_anchored_to_eia_and_skips_holidays():
    m = Market(np.random.default_rng(0))
    s = pd.Series(m.hh_spot, index=m.days).resample("ME").mean()
    assert abs(s["2000-12"].iloc[0] - 8.90) / 8.90 < 0.25
    assert pd.Timestamp("2001-01-01") not in m.days and pd.Timestamp("2001-07-04") not in m.days
    assert m.gas_spot("socal-border")[m.idx[dt.date(2000, 12, 12)]] > 15  # Western basis blowout


def test_sap_documents_balance():
    P = sap.Poster({"ENA": "0413"}, {"ENA": "105601"})
    P.doc("ENA", "DR", dt.date(2001, 5, 10), dt.date(2001, 5, 10),
          [("01", "110100", 100.0, 10020, "G3100001", "x"), ("50", "400100", 120.0, None, "G3100001", "x"),
           ("40", "500100", 20.0, None, "G3100001", "x")])
    df = pd.DataFrame(P.l)
    assert (df.SHKZG.map({"S": 1, "H": -1}) * df.DMBTR).sum() == pytest.approx(0)
    assert df.loc[df.KOART == "D", "KUNNR"].iloc[0] == "0000010020"


def test_ontology_and_reference_files_parse():
    schema = yaml.safe_load((paths.ONTOLOGY / "enron_finance.yaml").read_text())
    assert "Workbook" in schema["classes"] and "ProcessArea" in schema["enums"]
    areas = set(schema["enums"]["ProcessArea"]["permissible_values"])
    std = yaml.safe_load((paths.ROOT / "standards" / "era_standards.yaml").read_text())
    recs = std if isinstance(std, list) else std["standards"]
    assert len({r["id"] for r in recs}) == len(recs)
    for r in recs:
        assert set(r.get("process_areas", [])) <= areas, r["id"]
    for f in ("systems", "organizations", "lexicon", "classifier_rules", "market_history"):
        assert yaml.safe_load((paths.ONTOLOGY / "reference" / f"{f}.yaml").read_text())
