"""Download and verify registered sources into data/landing."""
from __future__ import annotations

import hashlib
import shutil
import urllib.request
from pathlib import Path

import yaml

from . import paths


def load_registry() -> list[dict]:
    return yaml.safe_load(paths.SOURCES_FILE.read_text())["sources"]


def md5_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while b := f.read(chunk):
            h.update(b)
    return h.hexdigest()


def fetch(include_optional: bool = False, only: str | None = None) -> list[dict]:
    results = []
    for src in load_registry():
        if only and src["source_id"] != only:
            continue
        dest_dir = paths.LANDING / src["source_id"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in src["files"]:
            if not f.get("required", True) and not include_optional:
                continue
            dest = dest_dir / f["name"]
            if dest.exists() and dest.stat().st_size == f["bytes"] and md5_of(dest) == f["md5"]:
                results.append({"file": str(dest), "status": "present"})
                continue
            tmp = dest.with_suffix(dest.suffix + ".part")
            req = urllib.request.Request(f["url"], headers={"User-Agent": "enron-e2e/0.1"})
            with urllib.request.urlopen(req) as r, tmp.open("wb") as out:
                shutil.copyfileobj(r, out, 1 << 20)
            got = md5_of(tmp)
            if got != f["md5"]:
                tmp.unlink()
                raise RuntimeError(f"Checksum mismatch for {f['name']}: {got} != {f['md5']}")
            tmp.replace(dest)
            results.append({"file": str(dest), "status": "downloaded"})
    return results
