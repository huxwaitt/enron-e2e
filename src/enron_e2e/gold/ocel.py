"""Gold: OCEL 2.0 object-centric event log spanning observed and synthetic activity.

Observed (provenance = observed:*):
  "Create Workbook"         docProps created timestamp + author (Hermans corpus)
  "Send Workbook by Email"  email carrying a linked workbook (CMU corpus x Hermans corpus)
Synthetic (provenance = synthetic:<system>):
  Capture Trade -> Confirm Trade / Dispute Confirmation -> Nominate -> Actualize Volumes
  -> Issue Invoice -> Receive Payment | Make Payment -> Post to GL ; Run DPR ; Call Collateral

Writes the OCEL 2.0 SQLite layout (event, object, event_object, object_object,
event_map_type, object_map_type, event_<type>, object_<type>) to
lake/gold/process_log/enron_ocel2.sqlite, plus flat Parquet for lake queries.
"""
from __future__ import annotations

import re
import sqlite3

import duckdb
import pandas as pd

from .. import paths
from ..governance import lineage

OUT = paths.GOLD / "process_log"


def _b(system: str, table: str) -> str:
    return (paths.BRONZE / system / f"{table}.parquet").as_posix()


def _snake(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def build(min_link_score: float = 0.45) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("set enable_progress_bar = false")
    ev, eo = [], []  # event frames, event-object frames

    def add(sql_events: str, sql_rel: str):
        e = con.execute(sql_events).df()
        e.columns = ["ocel_id", "ocel_type", "ocel_time", "provenance", "resource", "detail"]
        r = con.execute(sql_rel).df()
        r.columns = ["ocel_event_id", "ocel_object_id", "ocel_qualifier"]
        ev.append(e.astype({"resource": "string", "detail": "string"}))
        eo.append(r)

    # ---------- observed: workbook creation
    wb = (paths.BRONZE / "hermans" / "workbooks.parquet").as_posix()
    add(f"""select 'wbc:' || file_id as ocel_id, 'Create Workbook' as ocel_type, try_cast(created as timestamp) as ocel_time,
               'observed:hermans' as provenance, author as resource, original_filename as detail
            from '{wb}' where try_cast(created as timestamp) between '1995-01-01' and '2002-12-31'""",
        f"""select 'wbc:' || file_id ocel_event_id, 'wb:' || file_id ocel_object_id, 'created' ocel_qualifier
            from '{wb}' where try_cast(created as timestamp) between '1995-01-01' and '2002-12-31'""")
    # ---------- observed: workbook sent by email
    links = (paths.SILVER / "workbook_email_links.parquet").as_posix()
    msgs = (paths.SILVER / "messages.parquet").as_posix()
    con.execute(f"""create table sends as
        select distinct l.message_id, l.file_id, m.sent_at, m.from_addr, m.subject, m.to_addrs, m.cc_addrs
        from '{links}' l join '{msgs}' m using (message_id) where l.score >= {min_link_score} and m.sent_at is not null""")
    add("""select distinct 'mail:' || md5(message_id) ocel_id, 'Send Workbook by Email' ocel_type, sent_at::timestamp ocel_time,
               'observed:cmu_email' provenance, from_addr resource, subject detail from sends""",
        """select 'mail:' || md5(message_id), 'wb:' || file_id, 'attachment' from sends
           union all select distinct 'mail:' || md5(message_id), 'person:' || split_part(from_addr, '@', 1), 'sender' from sends where from_addr like '%@enron.com'
           union all select distinct 'mail:' || md5(message_id), 'person:' || split_part(unnest(to_addrs), '@', 1), 'recipient' from sends
           union all select distinct 'mail:' || md5(message_id), 'email:' || md5(message_id), 'message' from sends""")

    # ---------- synthetic: trade lifecycle
    for sysname, table in (("sitara", "DEAL"), ("enpower", "PWR_DEAL"), ("tagg", "FIN_DEAL")):
        p = _b(sysname, table)
        add(f"""select 'cap:' || DEAL_NUM ocel_id, 'Capture Trade' ocel_type, TRADE_TS::timestamp ocel_time,
                   'synthetic:{sysname}' provenance, TRADER_ID resource, INSTRUMENT || ' ' || LOCATION_CD detail from '{p}'""",
            f"""select 'cap:' || DEAL_NUM, 'deal:' || DEAL_NUM, 'captured' from '{p}'
                union all select 'cap:' || DEAL_NUM, 'cp:' || CP_ID, 'counterparty' from '{p}'
                union all select 'cap:' || DEAL_NUM, 'book:' || BOOK_CD, 'book' from '{p}'
                union all select 'cap:' || DEAL_NUM, 'eol:' || EOL_TXN_ID::bigint, 'eol_transaction' from '{p}' where EOL_TXN_ID is not null""")
    c = _b("global_contracts", "CONFIRMATION")
    add(f"""select 'cnf:' || CONFIRM_ID, case when STATUS = 'DISPUTED' then 'Dispute Confirmation' else 'Confirm Trade' end,
               coalesce(RETURNED_DT, SENT_DT)::timestamp + interval 16 hour, 'synthetic:global_contracts', AGMT_TYPE, STATUS
            from '{c}' where STATUS <> 'OUTSTANDING'""",
        f"""select 'cnf:' || CONFIRM_ID, 'deal:' || DEAL_NUM, 'confirms' from '{c}' where STATUS <> 'OUTSTANDING'
            union all select 'cnf:' || CONFIRM_ID, 'agmt:' || AGMT_ID, 'master_agreement' from '{c}' where STATUS <> 'OUTSTANDING' and AGMT_ID is not null""")
    n = _b("sitara", "NOMINATION")
    add(f"""select 'nom:' || NOM_ID, 'Nominate', (FLOW_START - interval 2 day)::timestamp + interval 11 hour, 'synthetic:sitara', PIPELINE_CD, LOCATION_CD from '{n}'
            union all select 'act:' || NOM_ID, 'Actualize Volumes', ACTUALIZED_DT::timestamp + interval 10 hour, 'synthetic:unify_gas', PIPELINE_CD, LOCATION_CD from '{n}' where ACTUALIZED_DT is not null""",
        f"""select 'nom:' || NOM_ID, 'deal:' || DEAL_NUM, 'nominates' from '{n}'
            union all select 'act:' || NOM_ID, 'deal:' || DEAL_NUM, 'actualizes' from '{n}' where ACTUALIZED_DT is not null""")
    s = _b("enpower", "SCHEDULE")
    add(f"""select 'sch:' || SCHED_ID, 'Actualize Volumes', ACTUALIZED_DT::timestamp + interval 10 hour, 'synthetic:unify_power', LOCATION_CD, HOURS_PROFILE from '{s}' where ACTUALIZED_DT is not null""",
        f"""select 'sch:' || SCHED_ID, 'deal:' || DEAL_NUM, 'actualizes' from '{s}' where ACTUALIZED_DT is not null""")
    for u in ("unify_gas", "unify_power", "unify_financial"):
        h, l, p = _b(u, "INVOICE_HDR"), _b(u, "INVOICE_LINE"), _b(u, "PAYMENT")
        add(f"""select 'inv:' || INVOICE_NUM, 'Issue Invoice', INVOICE_DT::timestamp + interval 9 hour, 'synthetic:{u}', DOC_TYPE, SETTLE_CLASS from '{h}'
                union all select 'pay:' || PAYMENT_ID, case DIRECTION when 'RECEIPT' then 'Receive Payment' else 'Make Payment' end,
                       PAY_DT::timestamp + interval 14 hour, 'synthetic:{u}', METHOD, BANK_REF from '{p}'""",
            f"""select 'inv:' || INVOICE_NUM, 'invoice:' || INVOICE_NUM, 'issued' from '{h}'
                union all select 'inv:' || INVOICE_NUM, 'cp:' || CP_ID, 'counterparty' from '{h}'
                union all select distinct 'inv:' || INVOICE_NUM, 'deal:' || DEAL_NUM, 'settles' from '{l}'
                union all select 'pay:' || PAYMENT_ID, 'invoice:' || INVOICE_NUM, 'pays' from '{p}'
                union all select 'pay:' || PAYMENT_ID, 'payment:' || PAYMENT_ID, 'payment' from '{p}'""")
    bk, bs = _b("sap", "BKPF"), _b("sap", "BSEG")
    add(f"""select 'gl:' || BUKRS || '-' || BELNR || '-' || GJAHR, 'Post to GL', CPUDT::timestamp + interval 18 hour, 'synthetic:sap', USNAM, BLART || ' ' || coalesce(BKTXT, '') from '{bk}'""",
        f"""select 'gl:' || BUKRS || '-' || BELNR || '-' || GJAHR, 'gldoc:' || BUKRS || '-' || BELNR || '-' || GJAHR, 'document' from '{bk}'
            union all select 'gl:' || BUKRS || '-' || BELNR || '-' || GJAHR, 'invoice:' || XBLNR, 'references' from '{bk}' where BLART in ('DR','KR','DZ','KZ')""")
    d = _b("erms", "DPR")
    add(f"""select 'dpr:' || BOOK_CD || ':' || EFF_DT, 'Run DPR', EFF_DT::timestamp + interval 19 hour, 'synthetic:erms', 'DPR batch', BOOK_CD from '{d}'""",
        f"""select 'dpr:' || BOOK_CD || ':' || EFF_DT, 'book:' || BOOK_CD, 'book' from '{d}'""")
    cc = _b("gcp", "COLLATERAL_CALL")
    add(f"""select 'col:' || CALL_ID, 'Call Collateral', CALL_DT::timestamp + interval 15 hour, 'synthetic:gcp', DIRECTION, REASON from '{cc}'""",
        f"""select 'col:' || CALL_ID, 'cp:' || CP_ID, 'counterparty' from '{cc}'""")

    events = pd.concat(ev, ignore_index=True).dropna(subset=["ocel_time"]).drop_duplicates("ocel_id")
    rel = pd.concat(eo, ignore_index=True).dropna()

    rel = rel[rel.ocel_event_id.isin(set(events.ocel_id))].drop_duplicates()
    objects = pd.DataFrame({"ocel_id": rel.ocel_object_id.unique()})
    objects["ocel_type"] = objects.ocel_id.str.split(":").str[0].map({
        "wb": "workbook", "person": "person", "email": "email", "deal": "deal", "cp": "counterparty", "book": "book",
        "eol": "eol_transaction", "agmt": "master_agreement", "invoice": "invoice", "payment": "payment",
        "gldoc": "gl_document"})
    # object-to-object: deal belongs to counterparty/book (from capture events)
    cap = rel[rel.ocel_event_id.str.startswith("cap:")]
    deal_of = cap[cap.ocel_qualifier == "captured"].set_index("ocel_event_id").ocel_object_id
    o2o = cap[cap.ocel_qualifier.isin(["counterparty", "book"])].assign(src=lambda x: x.ocel_event_id.map(deal_of))
    o2o = o2o.rename(columns={"src": "ocel_source_id", "ocel_object_id": "ocel_target_id"})[["ocel_source_id", "ocel_target_id", "ocel_qualifier"]]

    events.to_parquet(OUT / "events.parquet", index=False)
    rel.to_parquet(OUT / "event_object.parquet", index=False)
    objects.to_parquet(OUT / "objects.parquet", index=False)
    o2o.to_parquet(OUT / "object_object.parquet", index=False)

    db = OUT / "enron_ocel2.sqlite"
    if db.exists():
        db.unlink()
    sq = sqlite3.connect(db)
    events[["ocel_id", "ocel_type"]].to_sql("event", sq, index=False)
    objects[["ocel_id", "ocel_type"]].to_sql("object", sq, index=False)
    rel.to_sql("event_object", sq, index=False)
    o2o.to_sql("object_object", sq, index=False)
    et = pd.DataFrame({"ocel_type": sorted(events.ocel_type.unique())})
    et["ocel_type_map"] = et.ocel_type.map(_snake)
    et.to_sql("event_map_type", sq, index=False)
    ot = pd.DataFrame({"ocel_type": sorted(objects.ocel_type.dropna().unique())})
    ot["ocel_type_map"] = ot.ocel_type.map(_snake)
    ot.to_sql("object_map_type", sq, index=False)
    for t, m in zip(et.ocel_type, et.ocel_type_map):
        e = events[events.ocel_type == t][["ocel_id", "ocel_time", "provenance", "resource", "detail"]].copy()
        e["ocel_time"] = pd.to_datetime(e.ocel_time).dt.strftime("%Y-%m-%d %H:%M:%S")
        e.to_sql(f"event_{m}", sq, index=False)
    for t, m in zip(ot.ocel_type, ot.ocel_type_map):
        o = objects[objects.ocel_type == t][["ocel_id"]].assign(ocel_time="1970-01-01 00:00:00", ocel_changed_field=None)
        o.to_sql(f"object_{m}", sq, index=False)
    sq.commit()
    sq.close()
    lineage("build_ocel2_process_log", ["silver/workbook_email_links", "silver/messages", "bronze/hermans/workbooks",
                                        "bronze/sitara", "bronze/enpower", "bronze/tagg", "bronze/unify_*", "bronze/sap"],
            ["gold/process_log/enron_ocel2.sqlite"])
    return {"events": len(events), "objects": len(objects), "event_object": len(rel), "object_object": len(o2o),
            "by_type": events.ocel_type.value_counts().to_dict(),
            "observed_events": int(events.provenance.str.startswith("observed").sum())}
