"""Filesystem layout of the data estate.

data/landing/<source_id>/   immutable downloads, checksum-verified
lake/bronze/                raw-fidelity extracts (one table per source object)
lake/silver/                conformed, typed, deduplicated, keyed to the ontology
lake/gold/                  business-ready marts (process-area views, KPIs, graph)
lake/synthetic/             reconstructed source systems (Sitara, EnPower, ERMS, Unify, GCP, SAP)
lake/_meta/                 run manifests, lineage events, data-quality results
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("ENRON_E2E_ROOT", Path(__file__).resolve().parents[2]))
DATA = ROOT / "data"
LANDING = DATA / "landing"
LAKE = Path(os.environ.get("ENRON_E2E_LAKE", ROOT / "lake"))
BRONZE = LAKE / "bronze"
SILVER = LAKE / "silver"
GOLD = LAKE / "gold"
SYNTHETIC = LAKE / "synthetic"
META = LAKE / "_meta"
SOURCES_FILE = ROOT / "sources.yaml"
CONTRACTS = ROOT / "contracts"
ONTOLOGY = ROOT / "ontology"


def ensure(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
