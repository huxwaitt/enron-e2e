"""Bronze ingest of the Hermans Enron spreadsheet corpus.

Parses OOXML directly (zip + streaming XML) rather than through openpyxl so one pass
yields formulas *and* cached values, number formats, sheet visibility, merged
ranges, defined names, external-link targets, comments and document properties.
Legacy .xls files go through xlrd (values only; BIFF formulas are not recoverable).

Outputs under lake/bronze/hermans/:
  workbooks.parquet        one row per file
  sheets.parquet           one row per worksheet
  defined_names.parquet    workbook-level named ranges
  external_links.parquet   links to other workbooks/files
  comments.parquet         cell comments (reviewer notes)
  cells/part-*.parquet     one row per non-empty cell
"""
from __future__ import annotations

import hashlib
import posixpath
import re
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from defusedxml import ElementTree as DET

from .. import paths

SRC = paths.LANDING / "hermans_figshare" / "extracted"
OUT = paths.BRONZE / "hermans"
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties",
}
M = "{%s}" % NS["m"]
FNAME_RE = re.compile(r"^(?P<custodian>.+?)__(?P<hid>\d+)__(?P<orig>.+)$")
BUILTIN_DATE_FMTS = set(range(14, 23)) | set(range(45, 48))
DATE_TOKENS = re.compile(r"(?<![\\\"])[dmyhs]", re.I)

CELL_SCHEMA = pa.schema([
    ("file_id", pa.string()), ("sheet_idx", pa.int16()), ("row", pa.int32()), ("col", pa.int16()),
    ("ref", pa.string()), ("cell_type", pa.string()), ("value_text", pa.string()), ("value_num", pa.float64()),
    ("formula", pa.string()), ("formula_kind", pa.string()), ("shared_index", pa.int32()),
    ("num_fmt", pa.string()), ("is_date_fmt", pa.bool_()), ("style_idx", pa.int32()),
])


def col_to_idx(letters: str) -> int:
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


REF_RE = re.compile(r"^([A-Z]{1,3})(\d+)$")


def _read(z: zipfile.ZipFile, name: str) -> bytes | None:
    try:
        return z.read(name)
    except KeyError:
        return None


def _rels(z: zipfile.ZipFile, part: str) -> dict[str, dict]:
    d, b = posixpath.split(part)
    raw = _read(z, posixpath.join(d, "_rels", b + ".rels"))
    if not raw:
        return {}
    out = {}
    for r in DET.fromstring(raw):
        tgt = r.get("Target", "")
        mode = r.get("TargetMode")
        full = tgt if mode == "External" else posixpath.normpath(posixpath.join(d, tgt)).lstrip("/")
        out[r.get("Id")] = {"target": full, "type": r.get("Type", "").rsplit("/", 1)[-1], "external": mode == "External"}
    return out


def _text(el) -> str:
    return "".join(t.text or "" for t in el.iter(M + "t"))


def _styles(z: zipfile.ZipFile) -> list[tuple[str, bool]]:
    raw = _read(z, "xl/styles.xml")
    if not raw:
        return []
    root = DET.fromstring(raw)
    custom = {}
    nf = root.find("m:numFmts", NS)
    if nf is not None:
        for f in nf:
            custom[int(f.get("numFmtId"))] = f.get("formatCode", "")
    out = []
    xfs = root.find("m:cellXfs", NS)
    if xfs is not None:
        for xf in xfs:
            fid = int(xf.get("numFmtId", 0))
            code = custom.get(fid, f"builtin:{fid}")
            is_date = fid in BUILTIN_DATE_FMTS or (fid in custom and bool(DATE_TOKENS.search(re.sub(r"\[[^\]]*\]|\"[^\"]*\"", "", code))))
            out.append((code, is_date))
    return out


def parse_xlsx(path: Path, file_id: str) -> dict:
    res = {"sheets": [], "names": [], "links": [], "comments": [], "cells": [], "props": {}}
    with zipfile.ZipFile(path) as z:
        members = set(z.namelist())
        res["props"]["has_vba"] = "xl/vbaProject.bin" in members
        res["props"]["n_parts"] = len(members)
        core = _read(z, "docProps/core.xml")
        if core:
            root = DET.fromstring(core)
            for tag, key in (("dc:creator", "author"), ("cp:lastModifiedBy", "last_modified_by"),
                             ("dcterms:created", "created"), ("dcterms:modified", "modified"),
                             ("dc:title", "title"), ("dc:subject", "subject"), ("cp:keywords", "keywords"),
                             ("dc:description", "description"), ("cp:category", "category")):
                el = root.find(tag, NS)
                res["props"][key] = el.text if el is not None else None
        app = _read(z, "docProps/app.xml")
        if app:
            root = DET.fromstring(app)
            for tag, key in (("ep:Company", "company"), ("ep:Manager", "manager"), ("ep:Application", "application"),
                             ("ep:AppVersion", "app_version")):
                el = root.find(tag, NS)
                res["props"][key] = el.text if el is not None else None

        sst = []
        raw = _read(z, "xl/sharedStrings.xml")
        if raw:
            for si in DET.fromstring(raw).iter(M + "si"):
                sst.append(_text(si))
        styles = _styles(z)
        wb_rels = _rels(z, "xl/workbook.xml")
        wb = DET.fromstring(z.read("xl/workbook.xml"))
        for dn in wb.iter(M + "definedName"):
            res["names"].append({"file_id": file_id, "name": dn.get("name"), "refers_to": dn.text,
                                 "local_sheet_id": dn.get("localSheetId"), "hidden": dn.get("hidden") == "1"})
        for rid, rel in wb_rels.items():
            if rel["type"] == "externalLink" and not rel["external"]:
                lrels = _rels(z, rel["target"])
                for lr in lrels.values():
                    res["links"].append({"file_id": file_id, "link_part": rel["target"], "target": lr["target"],
                                         "link_type": lr["type"]})
        sheets = wb.find("m:sheets", NS)
        for idx, sh in enumerate(sheets if sheets is not None else []):
            rid = sh.get("{%s}id" % NS["r"])
            rel = wb_rels.get(rid, {})
            part = rel.get("target")
            srow = {"file_id": file_id, "sheet_idx": idx, "sheet_name": sh.get("name"),
                    "state": sh.get("state", "visible"), "sheet_type": rel.get("type"), "part": part,
                    "dimension": None, "n_cells": 0, "n_formulas": 0, "n_numeric": 0, "n_text": 0,
                    "n_merged": 0, "max_row": 0, "max_col": 0, "has_autofilter": False,
                    "n_data_validations": 0, "n_conditional_formats": 0, "tab_color": None, "n_hyperlinks": 0}
            if rel.get("type") == "worksheet" and part in members:
                _parse_sheet(z, part, idx, file_id, sst, styles, srow, res)
            res["sheets"].append(srow)
    return res


def _parse_sheet(z, part, idx, file_id, sst, styles, srow, res):
    cells = res["cells"]
    with z.open(part) as fh:
        for ev, el in DET.iterparse(fh, events=("end",)):
            tag = el.tag
            if tag == M + "c":
                ref = el.get("r")
                t = el.get("t", "n")
                s = int(el.get("s", 0))
                f = el.find(M + "f")
                v = el.find(M + "v")
                formula = kind = None
                si = None
                if f is not None:
                    formula = f.text
                    kind = f.get("t", "normal")
                    if f.get("si") is not None:
                        si = int(f.get("si"))
                vtext = vnum = None
                ctype = t
                if t == "s" and v is not None:
                    try:
                        vtext = sst[int(v.text)]
                    except (IndexError, ValueError, TypeError):
                        vtext = None
                    ctype = "s"
                elif t == "inlineStr":
                    is_ = el.find(M + "is")
                    vtext = _text(is_) if is_ is not None else None
                    ctype = "s"
                elif t in ("str", "e"):
                    vtext = v.text if v is not None else None
                elif t == "b":
                    vnum = float(v.text) if v is not None and v.text else None
                elif v is not None and v.text is not None:
                    try:
                        vnum = float(v.text)
                    except ValueError:
                        vtext = v.text
                if vtext is None and vnum is None and formula is None:
                    el.clear()
                    continue
                m = REF_RE.match(ref or "")
                row, col = (int(m.group(2)), col_to_idx(m.group(1))) if m else (None, None)
                fmt, is_date = styles[s] if s < len(styles) else ("builtin:0", False)
                cells.append((file_id, idx, row, col, ref, ctype, vtext, vnum, formula, kind, si, fmt,
                              bool(is_date and ctype == "n"), s))
                srow["n_cells"] += 1
                srow["n_formulas"] += formula is not None or kind == "shared"
                srow["n_numeric"] += vnum is not None
                srow["n_text"] += vtext is not None
                if row:
                    srow["max_row"] = max(srow["max_row"], row)
                    srow["max_col"] = max(srow["max_col"], col)
                el.clear()
            elif tag == M + "row":
                el.clear()
            elif tag == M + "dimension":
                srow["dimension"] = el.get("ref")
            elif tag == M + "mergeCell":
                srow["n_merged"] += 1
            elif tag == M + "autoFilter":
                srow["has_autofilter"] = True
            elif tag == M + "dataValidation":
                srow["n_data_validations"] += 1
            elif tag == M + "conditionalFormatting":
                srow["n_conditional_formats"] += 1
            elif tag == M + "hyperlink":
                srow["n_hyperlinks"] += 1
            elif tag == M + "tabColor":
                srow["tab_color"] = el.get("rgb") or el.get("theme")
    for rel in _rels(z, part).values():
        if rel["type"] == "comments" and rel["target"] in set(z.namelist()):
            root = DET.fromstring(z.read(rel["target"]))
            authors = [a.text for a in root.iter(M + "author")]
            for c in root.iter(M + "comment"):
                aid = int(c.get("authorId", 0))
                res["comments"].append({"file_id": file_id, "sheet_idx": idx, "ref": c.get("ref"),
                                        "author": authors[aid] if aid < len(authors) else None,
                                        "text": _text(c)})


def parse_xls(path: Path, file_id: str) -> dict:
    import xlrd
    res = {"sheets": [], "names": [], "links": [], "comments": [], "cells": [], "props": {}}
    book = xlrd.open_workbook(str(path), on_demand=True, formatting_info=False)
    res["props"]["author"] = getattr(book, "user_name", None)
    for idx in range(book.nsheets):
        sh = book.sheet_by_index(idx)
        srow = {"file_id": file_id, "sheet_idx": idx, "sheet_name": sh.name,
                "state": {0: "visible", 1: "hidden", 2: "veryHidden"}.get(sh.visibility, "visible"),
                "sheet_type": "worksheet", "part": None, "dimension": None, "n_cells": 0, "n_formulas": 0,
                "n_numeric": 0, "n_text": 0, "n_merged": len(sh.merged_cells), "max_row": sh.nrows,
                "max_col": sh.ncols, "has_autofilter": False, "n_data_validations": 0,
                "n_conditional_formats": 0, "tab_color": None, "n_hyperlinks": 0}
        for r in range(sh.nrows):
            for c in range(sh.ncols):
                cell = sh.cell(r, c)
                if cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                    continue
                num = text = None
                ctype = {1: "s", 2: "n", 3: "n", 4: "b", 5: "e"}.get(cell.ctype, "n")
                if cell.ctype == xlrd.XL_CELL_TEXT:
                    text = cell.value
                elif cell.ctype == xlrd.XL_CELL_ERROR:
                    text = xlrd.error_text_from_code.get(cell.value)
                else:
                    num = float(cell.value)
                ref = f"{_letters(c + 1)}{r + 1}"
                res["cells"].append((file_id, idx, r + 1, c + 1, ref, ctype, text, num, None, None, None,
                                     None, cell.ctype == xlrd.XL_CELL_DATE, None))
                srow["n_cells"] += 1
                srow["n_numeric"] += num is not None
                srow["n_text"] += text is not None
        res["sheets"].append(srow)
        book.unload_sheet(idx)
    return res


def _letters(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def process_file(path_str: str) -> dict:
    path = Path(path_str)
    m = FNAME_RE.match(path.name)
    file_id = _md5(path)
    row = {"file_id": file_id, "file_name": path.name, "bytes": path.stat().st_size,
           "custodian": m.group("custodian") if m else None,
           "hermans_id": int(m.group("hid")) if m else None,
           "original_filename": m.group("orig") if m else path.name,
           "extension": path.suffix.lower().lstrip("."), "parse_status": "ok", "parse_error": None}
    try:
        res = parse_xls(path, file_id) if row["extension"] == "xls" else parse_xlsx(path, file_id)
    except Exception as e:  # corrupt / password-protected / truncated files are real corpus content
        row.update(parse_status="error", parse_error=f"{type(e).__name__}: {e}"[:500])
        res = {"sheets": [], "names": [], "links": [], "comments": [], "cells": [], "props": {}}
    row.update({k: res["props"].get(k) for k in ("author", "last_modified_by", "created", "modified", "title",
                                                 "subject", "keywords", "description", "category", "company",
                                                 "manager", "application", "app_version", "has_vba", "n_parts")})
    row["n_sheets"] = len(res["sheets"])
    row["n_cells"] = sum(s["n_cells"] for s in res["sheets"])
    row["n_formulas"] = sum(s["n_formulas"] for s in res["sheets"])
    return {"workbook": row, **{k: res[k] for k in ("sheets", "names", "links", "comments", "cells")}}


def ingest(limit: int | None = None, workers: int = 10, cells_per_part: int = 5_000_000) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cells").mkdir(exist_ok=True)
    for old in (OUT / "cells").glob("part-*.parquet"):
        old.unlink()
    files = sorted(str(p) for p in SRC.iterdir() if p.is_file())
    if limit:
        files = files[:limit]
    wbs, sheets, names, links, comments = [], [], [], [], []
    buf, part, total_cells = [], 0, 0

    def flush():
        nonlocal buf, part
        if buf:
            cols = list(zip(*buf))
            tbl = pa.table({f.name: pa.array(c, type=f.type) for f, c in zip(CELL_SCHEMA, cols)})
            pq.write_table(tbl, OUT / "cells" / f"part-{part:04d}.parquet", compression="zstd")
            part += 1
            buf = []

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(process_file, f) for f in files]
        for fut in as_completed(futs):
            r = fut.result()
            wbs.append(r["workbook"])
            sheets += r["sheets"]
            names += r["names"]
            links += r["links"]
            comments += r["comments"]
            buf += r["cells"]
            total_cells += len(r["cells"])
            if len(buf) >= cells_per_part:
                flush()
    flush()
    import pandas as pd
    pd.DataFrame(wbs).to_parquet(OUT / "workbooks.parquet", index=False)
    pd.DataFrame(sheets).to_parquet(OUT / "sheets.parquet", index=False)
    pd.DataFrame(names, columns=["file_id", "name", "refers_to", "local_sheet_id", "hidden"]).to_parquet(OUT / "defined_names.parquet", index=False)
    pd.DataFrame(links, columns=["file_id", "link_part", "target", "link_type"]).to_parquet(OUT / "external_links.parquet", index=False)
    pd.DataFrame(comments, columns=["file_id", "sheet_idx", "ref", "author", "text"]).to_parquet(OUT / "comments.parquet", index=False)
    return {"files": len(wbs), "sheets": len(sheets), "cells": total_cells,
            "errors": sum(w["parse_status"] != "ok" for w in wbs)}
