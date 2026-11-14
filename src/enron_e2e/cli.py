"""enron-e2e command line.

  enron-e2e all                 fetch -> bronze -> silver -> gold -> synthetic -> process log -> graph -> catalog -> dq
  enron-e2e <step> [<step>...]  run individual steps in order
"""
from __future__ import annotations

import argparse
import json
import time

import duckdb

from . import paths

STEPS = ["fetch", "emails", "workbooks", "silver", "classify", "standards", "reference", "synth", "extract", "ocel", "graph",
         "contracts", "catalog", "dq"]


def catalog() -> dict:
    """lake/enron.duckdb: one schema per layer/source with views over the Parquet files."""
    db = paths.LAKE / "enron.duckdb"
    if db.exists():
        db.unlink()
    con = duckdb.connect(str(db))
    n = 0
    layout = {
        "bronze": paths.BRONZE, "silver": paths.SILVER, "gold": paths.GOLD,
    }
    for schema, root in layout.items():
        con.execute(f"create schema if not exists {schema}")
        for p in sorted(root.rglob("*.parquet")):
            rel = p.relative_to(root)
            if rel.parts[0] == "cells" or (len(rel.parts) > 1 and rel.parts[-2] in ("cells", "messages")):
                continue
            name = "_".join(rel.with_suffix("").parts).lower()
            con.execute(f"create or replace view {schema}.{name} as select * from read_parquet('{p.as_posix()}')")
            n += 1
        for d in sorted(root.rglob("*")):
            if d.is_dir() and d.name in ("cells", "messages"):
                name = "_".join(d.relative_to(root).parts).lower()
                con.execute(f"create or replace view {schema}.{name} as select * from read_parquet('{(d / '*.parquet').as_posix()}')")
                n += 1
    con.close()
    return {"catalog": str(db), "views": n}


def run(step: str, args) -> object:
    if step == "fetch":
        from .fetch import fetch
        return fetch(include_optional=args.with_eml)
    if step == "emails":
        from .ingest import emails
        return emails.ingest()
    if step == "workbooks":
        from .ingest import workbooks
        return workbooks.ingest(workers=args.workers, cells_per_part=2_000_000)
    if step == "silver":
        from .silver import emails
        return emails.build()
    if step == "classify":
        from .gold import classify
        return classify.classify().process_area.value_counts().to_dict()
    if step == "standards":
        from .gold import standards
        return standards.build()
    if step == "reference":
        from .gold import reference
        return reference.mine()
    if step == "synth":
        from .synth import build
        return build.build(seed=args.seed, scale=args.scale)
    if step == "extract":
        from .synth import build
        return {"tables": len(build.extract_to_bronze())}
    if step == "ocel":
        from .gold import ocel
        return ocel.build()
    if step == "graph":
        from .gold import graph
        return graph.build()
    if step == "contracts":
        from . import governance
        return {"written": len(governance.write_contracts())}
    if step == "catalog":
        return catalog()
    if step == "dq":
        from . import governance
        df = governance.run_quality()
        return {"rules": len(df), "failed": df[~df.passed][["table", "rule", "violations", "error"]].to_dict("records")}
    raise SystemExit(f"unknown step {step}")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="enron-e2e", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="+", help=f"'all' or any of: {', '.join(STEPS)}")
    ap.add_argument("--seed", type=int, default=2001)
    ap.add_argument("--scale", type=float, default=1.0, help="synthetic volume multiplier")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--with-eml", action="store_true", help="also download the 8.8 GB Hermans email archive")
    args = ap.parse_args(argv)
    steps = STEPS if args.steps == ["all"] else args.steps
    for s in steps:
        t = time.time()
        out = run(s, args)
        print(json.dumps({"step": s, "secs": round(time.time() - t, 1), "result": out}, default=str))


if __name__ == "__main__":
    main()
