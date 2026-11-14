"""Bronze ingest of the CMU Enron maildir, streamed straight from the tarball.

Output: lake/bronze/cmu_email/messages/part-*.parquet  (one row per file in the maildir)
        lake/bronze/cmu_email/attachment_refs.parquet  (spreadsheet-like filenames referenced in bodies)

The CMU release strips attachment payloads but leaves their names in the body
(Outlook/Notes markers like "<<1-25act.xls>>" or " - Book1.xls"). Those markers are
how emails are joined to the Hermans spreadsheet files downstream.
"""
from __future__ import annotations

import datetime as dt
import email
import email.policy
import email.utils
import re
import tarfile
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from .. import paths

TARBALL = paths.LANDING / "cmu_email" / "enron_mail_20150507.tar.gz"
OUT = paths.BRONZE / "cmu_email"

ATTACH_RE = re.compile(
    r"""(?:<<\s*(?:File:\s*)?(?P<a>[^<>\r\n]{1,200}?\.(?:xls|xlsx|xlsm|xlt|csv|wk[134s]|123))\s*>>)"""
    r"""|(?:^[ \t]*-[ \t]+(?P<b>[^\r\n]{1,200}?\.(?:xls|xlsx|xlsm|xlt|csv|wk[134s]|123))[ \t]*$)"""
    r"""|(?:(?:attached|attachment)[^\r\n]{0,60}?\b(?P<c>[\w\-\. &()]{1,120}?\.(?:xls|xlsx|xlsm|csv)))""",
    re.IGNORECASE | re.MULTILINE,
)
SCHEMA = pa.schema([
    ("path", pa.string()), ("custodian", pa.string()), ("folder", pa.string()),
    ("message_id", pa.string()), ("date_raw", pa.string()), ("date_utc", pa.timestamp("s", tz="UTC")),
    ("from_addr", pa.string()), ("to_addrs", pa.list_(pa.string())), ("cc_addrs", pa.list_(pa.string())),
    ("bcc_addrs", pa.list_(pa.string())), ("subject", pa.string()), ("x_from", pa.string()),
    ("x_to", pa.string()), ("x_cc", pa.string()), ("x_folder", pa.string()), ("x_origin", pa.string()),
    ("x_filename", pa.string()), ("body", pa.string()), ("body_chars", pa.int32()),
])


def _addrs(v: str | None) -> list[str]:
    if not v:
        return []
    return [a.strip().lower() for a in re.split(r",\s*", v.replace("\n", " ").replace("\t", " ")) if a.strip()]


def _date(v: str | None):
    if not v:
        return None
    try:
        return email.utils.parsedate_to_datetime(v).astimezone(dt.timezone.utc)
    except Exception:
        return None


def parse_message(path: str, raw: bytes) -> dict:
    msg = email.message_from_bytes(raw, policy=email.policy.compat32)

    def h(name: str) -> str | None:
        v = msg.get(name)
        return None if v is None else str(v)
    body = msg.get_payload(decode=False)
    if isinstance(body, list):
        body = "\n".join(str(p.get_payload()) for p in body)
    body = body if isinstance(body, str) else ""
    parts = path.split("/")
    return {
        "path": path, "custodian": parts[1] if len(parts) > 1 else None,
        "folder": "/".join(parts[2:-1]) if len(parts) > 3 else None,
        "message_id": h("Message-ID"), "date_raw": h("Date"), "date_utc": _date(h("Date")),
        "from_addr": (h("From") or "").strip().lower() or None,
        "to_addrs": _addrs(h("To")), "cc_addrs": _addrs(h("Cc")), "bcc_addrs": _addrs(h("Bcc")),
        "subject": h("Subject"), "x_from": h("X-From"), "x_to": h("X-To"),
        "x_cc": h("X-cc"), "x_folder": h("X-Folder"), "x_origin": h("X-Origin"),
        "x_filename": h("X-FileName"), "body": body, "body_chars": len(body),
    }


def attachment_refs(row: dict) -> list[dict]:
    out, seen = [], set()
    for m in ATTACH_RE.finditer(row["body"] or ""):
        name = (m.group("a") or m.group("b") or m.group("c") or "").strip().strip('"')
        key = name.lower()
        if name and key not in seen:
            seen.add(key)
            out.append({"path": row["path"], "message_id": row["message_id"], "filename": name,
                        "filename_norm": key, "marker": "angle" if m.group("a") else "dash" if m.group("b") else "prose"})
    return out


def ingest(limit: int | None = None, batch: int = 50_000) -> dict:
    (OUT / "messages").mkdir(parents=True, exist_ok=True)
    for old in (OUT / "messages").glob("part-*.parquet"):
        old.unlink()
    rows, refs, part, n = [], [], 0, 0
    with tarfile.open(TARBALL, "r:gz") as tar:
        for m in tar:
            if not m.isfile():
                continue
            raw = tar.extractfile(m).read()
            row = parse_message(m.name, raw)
            rows.append(row)
            refs.extend(attachment_refs(row))
            n += 1
            if len(rows) >= batch:
                pq.write_table(pa.Table.from_pylist(rows, SCHEMA), OUT / "messages" / f"part-{part:04d}.parquet")
                rows, part = [], part + 1
            if limit and n >= limit:
                break
    if rows:
        pq.write_table(pa.Table.from_pylist(rows, SCHEMA), OUT / "messages" / f"part-{part:04d}.parquet")
    ref_schema = pa.schema([("path", pa.string()), ("message_id", pa.string()), ("filename", pa.string()),
                            ("filename_norm", pa.string()), ("marker", pa.string())])
    pq.write_table(pa.Table.from_pylist(refs, ref_schema), OUT / "attachment_refs.parquet")
    return {"messages": n, "attachment_refs": len(refs)}
