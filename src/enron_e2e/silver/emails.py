"""Silver: conformed people, messages and email-to-workbook links.

silver/persons.parquet            one row per @enron.com address seen, custodians flagged
silver/messages.parquet           one row per unique Message-ID (copies across mailboxes collapsed)
silver/message_recipients.parquet message x person x role (to/cc/bcc)
silver/workbook_email_links.parquet   attachment reference -> workbook file, scored
"""
from __future__ import annotations

import hashlib
import re

import duckdb

from .. import paths

MSG = (paths.BRONZE / "cmu_email" / "messages" / "*.parquet").as_posix()
REFS = (paths.BRONZE / "cmu_email" / "attachment_refs.parquet").as_posix()
WB = (paths.BRONZE / "hermans" / "workbooks.parquet").as_posix()


def msg_iri(message_id: str) -> str:
    return "enroni:msg/" + hashlib.sha1(message_id.encode()).hexdigest()[:16]


def build(con: duckdb.DuckDBPyConnection | None = None) -> dict:
    out = paths.SILVER
    out.mkdir(parents=True, exist_ok=True)
    con = con or duckdb.connect()
    con.execute("set enable_progress_bar = false")
    con.create_function("msg_iri", msg_iri, ["VARCHAR"], "VARCHAR")
    con.execute(f"create or replace view bm as select * from read_parquet('{MSG}')")

    # ---- messages: the CMU release minted a unique Message-ID per *file*, so the same
    # email in a sender's "sent" folder and five inboxes has six IDs. Collapse on content.
    con.execute(r"""
        create or replace table bm_keyed as
        select *, md5(coalesce(from_addr, '') || '|' || coalesce(date_utc::varchar, '') || '|' ||
                      coalesce(subject, '') || '|' || left(regexp_replace(coalesce(body, ''), '\s+', ' ', 'g'), 4000)) as content_key
        from bm where message_id is not null
    """)
    con.execute("""
        create or replace table msg_map as
        select message_id, min(message_id) over (partition by content_key) as canonical_id from bm_keyed
    """)
    con.execute(r"""
        create or replace table messages as
        select min(message_id)                              as message_id,
               msg_iri(min(message_id))                     as message_iri,
               content_key,
               any_value(date_utc)                          as sent_at,
               any_value(from_addr)                         as from_addr,
               any_value(to_addrs)                          as to_addrs,
               any_value(cc_addrs)                          as cc_addrs,
               any_value(bcc_addrs)                         as bcc_addrs,
               any_value(subject)                           as subject,
               regexp_replace(lower(coalesce(any_value(subject), '')), '^((re|fw|fwd)\s*:\s*)+', '') as thread_subject,
               any_value(x_from)                            as x_from,
               arg_max(body, body_chars)                    as body,
               list(distinct custodian order by custodian)  as custodians,
               list(path order by path)                     as paths,
               list(message_id order by message_id)         as source_message_ids,
               count(*)                                     as n_copies,
               bool_or(lower(folder) like '%sent%')         as in_sent_folder
        from bm_keyed
        group by content_key
    """)
    con.execute(f"copy messages to '{(out / 'messages.parquet').as_posix()}' (format parquet, compression zstd)")

    # ---- recipients
    con.execute("""
        create or replace table message_recipients as
        select message_id, unnest(to_addrs) as addr, 'to' as role from messages
        union all select message_id, unnest(cc_addrs), 'cc' from messages
        union all select message_id, unnest(bcc_addrs), 'bcc' from messages
    """)
    con.execute("delete from message_recipients where addr is null or addr = ''")
    con.execute(f"copy message_recipients to '{(out / 'message_recipients.parquet').as_posix()}' (format parquet)")

    # ---- persons: every enron.com address, with display name from X-From where available
    con.execute("""
        create or replace table persons as
        with addrs as (
            select from_addr as addr, x_from as display from messages where from_addr like '%@enron.com'
            union all select addr, null from message_recipients where addr like '%@enron.com'
        ), names as (
            select addr, mode(regexp_extract(display, '^([^<]+?)\\s*<', 1)) as display_name, count(*) as n
            from addrs group by addr
        )
        select 'enroni:person/' || split_part(addr, '@', 1) as person_iri, addr as email,
               nullif(trim(display_name), '') as display_name, n as n_messages
        from names
    """)
    # custodians: maildir folder "lokay-m" -> the address they send from most in their sent folders
    con.execute("""
        create or replace table custodians as
        with sent as (
            select custodian, from_addr, count(*) n
            from bm where lower(folder) like '%sent%' and from_addr like '%@enron.com'
            group by custodian, from_addr
        )
        select custodian as maildir_name, arg_max(from_addr, n) as email, max(n) as n_sent
        from sent group by custodian
    """)
    con.execute(f"copy msg_map to '{(out / 'message_id_map.parquet').as_posix()}' (format parquet)")
    con.execute(f"copy persons to '{(out / 'persons.parquet').as_posix()}' (format parquet)")
    con.execute(f"copy custodians to '{(out / 'custodians.parquet').as_posix()}' (format parquet)")

    # ---- workbook <-> email links
    con.execute(f"create or replace view wb as select * from read_parquet('{WB}')")
    con.execute(f"""
        create or replace table refs as
        select r.* exclude (message_id), mm.canonical_id as message_id, m.custodians, m.sent_at, m.from_addr
        from read_parquet('{REFS}') r join msg_map mm using (message_id) join messages m on m.message_id = mm.canonical_id
    """)
    # Hermans converted .xls to .xlsx and prefixed custodian/id; compare on stem.
    con.execute("""
        create or replace table workbook_email_links as
        with w as (
            select file_id, custodian as wb_custodian,
                   lower(regexp_replace(original_filename, '\\.(xlsx|xls|xlsm)$', '')) as stem
            from wb
        ), r as (
            select *, lower(regexp_replace(filename, '\\.(xlsx|xls|xlsm|xlt|csv)$', '', 'i')) as stem from refs
        ), cand as (
            select r.message_id, r.filename, r.marker, r.sent_at, r.from_addr, w.file_id, w.wb_custodian,
                   r.custodians,
                   count(*) over (partition by r.message_id, r.filename) as n_candidates
            from r join w using (stem)
        )
        select *,
               -- Hermans' custodian "michelle_lokay" vs maildir "lokay-m": compare surname + initial
               list_contains(list_transform(custodians, lambda c: split_part(c, '-', 1) || '_' || split_part(c, '-', 2)),
                             split_part(wb_custodian, '_', -1) || '_' || left(wb_custodian, 1)) as custodian_match,
               case when n_candidates = 1 then 0.9 else 0.9 / n_candidates end
                 + case when list_contains(list_transform(custodians, lambda c: split_part(c, '-', 1) || '_' || split_part(c, '-', 2)),
                                           split_part(wb_custodian, '_', -1) || '_' || left(wb_custodian, 1)) then 0.1 else 0 end
                 as score
        from cand
    """)
    con.execute(f"copy workbook_email_links to '{(out / 'workbook_email_links.parquet').as_posix()}' (format parquet)")
    stats = {
        "messages": con.execute("select count(*) from messages").fetchone()[0],
        "persons": con.execute("select count(*) from persons").fetchone()[0],
        "custodians": con.execute("select count(*) from custodians").fetchone()[0],
        "links": con.execute("select count(*) from workbook_email_links").fetchone()[0],
        "linked_workbooks": con.execute("select count(distinct file_id) from workbook_email_links").fetchone()[0],
        "custodian_matched_links": con.execute("select count(*) from workbook_email_links where custodian_match").fetchone()[0],
    }
    return stats
