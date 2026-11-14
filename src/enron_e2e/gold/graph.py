"""Gold: instance knowledge graph (Turtle) and SSSOM class mappings.

lake/gold/graph/enron_kg.ttl           instances under enroni:, typed by the LinkML ontology
lake/gold/graph/workbook_mentions.parquet  workbook -> counterparty / system evidence
ontology/mappings/enron_finance.sssom.tsv  class alignments to FIBO / OMG Commons / W3C / schema.org
"""
from __future__ import annotations

import re

import duckdb
import pandas as pd
import yaml
from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, SKOS

from .. import paths
from ..governance import lineage

ONT = Namespace("https://huxwaitt.github.io/enron-e2e/ontology/")
ID = "https://huxwaitt.github.io/enron-e2e/id/"
SCHEMA = Namespace("http://schema.org/")
PROV = Namespace("http://www.w3.org/ns/prov#")
OUT = paths.GOLD / "graph"
SYSTEM_FAMILIES = {"sitara_id": "sitara", "eol_id": "eol", "tagg_id": "tagg"}


def iri(curie: str) -> URIRef:
    return URIRef(ID + curie.split(":", 1)[1]) if curie.startswith("enroni:") else URIRef(curie)


def sssom() -> int:
    schema = yaml.safe_load((paths.ONTOLOGY / "enron_finance.yaml").read_text())
    prefixes = schema["prefixes"]
    rows = []
    for cname, c in schema["classes"].items():
        for pred, key in (("skos:exactMatch", "exact_mappings"), ("skos:closeMatch", "close_mappings"),
                          ("skos:relatedMatch", "related_mappings")):
            for obj in c.get(key, []) or []:
                rows.append({"subject_id": f"enron:{cname}", "subject_label": cname, "predicate_id": pred,
                             "object_id": obj, "object_label": re.sub(r"(?<!^)(?=[A-Z])", " ", obj.split(":")[1]).lower(),
                             "mapping_justification": "semapv:ManualMappingCuration",
                             "confidence": {"skos:exactMatch": 0.95, "skos:closeMatch": 0.8, "skos:relatedMatch": 0.6}[pred]})
        if c.get("class_uri") and not c["class_uri"].startswith("enron:"):
            rows.append({"subject_id": f"enron:{cname}", "subject_label": cname, "predicate_id": "skos:exactMatch",
                         "object_id": c["class_uri"], "object_label": c["class_uri"].split(":")[1],
                         "mapping_justification": "semapv:ManualMappingCuration", "confidence": 0.95})
    df = pd.DataFrame(rows).drop_duplicates(["subject_id", "object_id"])
    used = {r.split(":")[0] for r in pd.concat([df.subject_id, df.object_id, df.predicate_id])} | {"semapv"}
    curie_map = {k: v for k, v in prefixes.items() if k in used}
    curie_map["semapv"] = "https://w3id.org/semapv/vocab/"
    header = {"mapping_set_id": "https://huxwaitt.github.io/enron-e2e/ontology/mappings/enron_finance.sssom.tsv",
              "mapping_set_description": "Alignment of the enron-e2e ontology to FIBO, OMG Commons, W3C ORG/PROV/FOAF and schema.org",
              "license": "https://opensource.org/licenses/MIT", "curie_map": curie_map}
    out = paths.ONTOLOGY / "mappings" / "enron_finance.sssom.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for line in yaml.safe_dump(header, sort_keys=False).splitlines():
            f.write(f"#{line}\n")
        df.to_csv(f, sep="\t", index=False, lineterminator="\n")
    return len(df)


def build(min_cp_files: int = 3) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    g = Graph()
    g.bind("enron", ONT)
    g.bind("enroni", Namespace(ID))
    g.bind("schema", SCHEMA)
    g.bind("prov", PROV)
    g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS)
    ref = paths.ONTOLOGY / "reference"

    sysd = yaml.safe_load((ref / "systems.yaml").read_text())
    for s in sysd["systems"]:
        u = iri(s["id"])
        g.add((u, RDF.type, ONT.InformationSystem))
        g.add((u, SKOS.prefLabel, Literal(s["label"])))
        for a in s.get("alt_labels", []):
            g.add((u, SKOS.altLabel, Literal(a)))
        if s.get("description"):
            g.add((u, DCTERMS.description, Literal(s["description"])))
        for pa in s.get("process_areas", []):
            g.add((u, ONT.process_areas, ONT[f"ProcessArea#{pa}"]))
        for d in s.get("downstream_systems", []):
            g.add((u, ONT.downstream_systems, iri(d)))
        for up in s.get("upstream_systems", []):
            g.add((u, ONT.upstream_systems, iri(up)))
    for st in sysd["process_steps"]:
        u = iri(st["id"])
        g.add((u, RDF.type, ONT.ProcessStep))
        g.add((u, SKOS.prefLabel, Literal(st["label"])))
        g.add((u, ONT.process_area, ONT[f"ProcessArea#{st['process_area']}"]))
        for p in st.get("performed_in", []):
            g.add((u, ONT.performed_in, iri(p)))

    orgs = yaml.safe_load((ref / "organizations.yaml").read_text())
    for kind, cls in (("segments", ONT.BusinessUnit), ("legal_entities", ONT.LegalEntity),
                      ("special_purpose_entities", ONT.SpecialPurposeEntity)):
        for o in orgs[kind]:
            u = iri(o["id"])
            g.add((u, RDF.type, cls))
            g.add((u, SKOS.prefLabel, Literal(o["label"])))
            for a in o.get("alt_labels", []):
                g.add((u, SKOS.altLabel, Literal(a)))
            if o.get("parent_entity"):
                g.add((u, ONT.parent_entity, iri(o["parent_entity"])))
            if o.get("segment"):
                g.add((u, ONT.segment, iri(o["segment"])))
            if o.get("email_mentions"):
                g.add((u, ONT.corpus_email_mentions, Literal(o["email_mentions"], datatype=XSD.integer)))
    for c in orgs.get("sap_company_codes", []):
        if c.get("entity"):
            g.add((iri(c["entity"]), ONT.company_code, Literal(c["code"])))

    lex = yaml.safe_load((ref / "lexicon.yaml").read_text())
    hits = pd.read_parquet(paths.GOLD / "reference" / "lexicon_hits.parquet").set_index(["group", "slug"])
    cls_for = {"pipelines": ONT.Pipeline, "gas_hubs": ONT.TradingHub, "power_points": ONT.PowerControlArea,
               "price_indices": ONT.PriceIndex, "exchanges_isos": ONT.MarketInfrastructure}
    prefix = {"pipelines": "loc", "gas_hubs": "loc", "power_points": "loc", "price_indices": "idx", "exchanges_isos": "org"}
    for group, entries in lex.items():
        for e in entries:
            h = hits.loc[(group, e["slug"])]
            if not bool(h.observed):
                continue
            u = URIRef(f"{ID}{prefix[group]}/{e['slug']}")
            g.add((u, RDF.type, cls_for[group]))
            g.add((u, SKOS.prefLabel, Literal(e["label"])))
            g.add((u, ONT.corpus_cell_mentions, Literal(int(h.cells), datatype=XSD.integer)))

    cps = pd.read_parquet(paths.GOLD / "reference" / "counterparties.parquet")
    cps = cps[(cps.n_files >= min_cp_files) & ~cps.is_enron_affiliate]
    for r in cps.itertuples(index=False):
        u = iri(r.cp_iri)
        g.add((u, RDF.type, ONT.Counterparty))
        g.add((u, SKOS.prefLabel, Literal(r.name_norm)))
        for a in list(r.aliases)[:10]:
            g.add((u, SKOS.altLabel, Literal(a)))
        g.add((u, ONT.corpus_file_count, Literal(int(r.n_files), datatype=XSD.integer)))

    con = duckdb.connect()
    con.execute("set enable_progress_bar = false")
    cust = pd.read_parquet(paths.SILVER / "custodians.parquet")
    for r in cust.itertuples(index=False):
        u = URIRef(f"{ID}person/{r.email.split('@')[0]}")
        g.add((u, RDF.type, ONT.Person))
        g.add((u, ONT.is_custodian, Literal(True)))
        g.add((u, ONT.maildir_name, Literal(r.maildir_name)))

    wb = pd.read_parquet(paths.BRONZE / "hermans" / "workbooks.parquet",
                         columns=["file_id", "original_filename", "custodian", "created", "author"])
    labels = pd.read_parquet(paths.GOLD / "workbook_labels.parquet", columns=["file_id", "process_area", "document_role"])
    wb = wb.drop_duplicates("file_id").merge(labels.drop_duplicates("file_id"), how="left")
    for r in wb.itertuples(index=False):
        u = URIRef(f"{ID}wb/{r.file_id}")
        g.add((u, RDF.type, ONT.Workbook))
        g.add((u, ONT.file_id, Literal(r.file_id)))
        g.add((u, ONT.original_filename, Literal(r.original_filename)))
        if r.created and str(r.created)[:4] < "2003":
            g.add((u, DCTERMS.created, Literal(r.created, datatype=XSD.dateTime)))
        if r.author:
            g.add((u, DCTERMS.creator, Literal(r.author)))
        if isinstance(r.process_area, str):
            g.add((u, ONT.process_area, ONT[f"ProcessArea#{r.process_area}"]))
            g.add((u, ONT.document_role, ONT[f"DocumentRole#{r.document_role}"]))
        g.add((u, ONT.custodian_name, Literal(r.custodian)))

    fv = (paths.GOLD / "reference" / "field_values.parquet").as_posix()
    con.register("cps", cps[["name_norm", "cp_iri"]])
    from .reference import norm_name
    con.create_function("norm_name", norm_name, ["VARCHAR"], "VARCHAR")
    mentions = con.execute(f"""
        select file_id, cps.cp_iri as target, 'counterparty' as kind, count(*) as n
        from '{fv}' v join cps on norm_name(v.value) = cps.name_norm
        where v.family = 'counterparty' and v.value_num is null group by 1, 2, 3
        union all
        select file_id, 'enroni:sys/' || case family {' '.join(f"when '{k}' then '{v}'" for k, v in SYSTEM_FAMILIES.items())} end,
               'system_identifier_column', count(*)
        from '{fv}' where family in ({', '.join(repr(k) for k in SYSTEM_FAMILIES)}) group by 1, 2, 3
    """).df()
    mentions.to_parquet(OUT / "workbook_mentions.parquet", index=False)
    for r in mentions.itertuples(index=False):
        pred = SCHEMA.mentions if r.kind == "counterparty" else PROV.wasDerivedFrom
        g.add((URIRef(f"{ID}wb/{r.file_id}"), pred, iri(r.target)))
    g.serialize(OUT / "enron_kg.ttl", format="turtle")
    n_map = sssom()
    lineage("build_knowledge_graph", ["ontology/reference", "gold/reference", "gold/workbook_labels", "bronze/hermans/workbooks"],
            ["gold/graph/enron_kg.ttl", "ontology/mappings/enron_finance.sssom.tsv"])
    return {"triples": len(g), "workbook_mentions": len(mentions), "sssom_mappings": n_map,
            "counterparties": len(cps), "workbooks": len(wb)}
