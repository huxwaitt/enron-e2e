# Identifier policy

Instance IRIs live under `https://huxwaitt.github.io/enron-e2e/id/` (prefix `enroni:`).

| Kind | Pattern | Derived from | Example |
|---|---|---|---|
| Workbook | `enroni:wb/{md5}` | MD5 of file bytes | `enroni:wb/1952351d9c833fe475ef7f2f645f28ca` |
| Worksheet | `enroni:wb/{md5}/sheet/{index}` | workbook + 0-based sheet index | `enroni:wb/1952…/sheet/0` |
| Email | `enroni:msg/{sha1(Message-ID)[:16]}` | RFC 822 Message-ID | `enroni:msg/3f0c9a1e2b7d4410` |
| Person | `enroni:person/{local-part}` | canonical @enron.com address | `enroni:person/kate.symes` |
| Legal entity / unit / desk / system | `enroni:org/{slug}`, `enroni:sys/{slug}` | curated reference data | `enroni:sys/sitara` |
| Counterparty | `enroni:cp/{slug}` | normalized name; aliases kept as `skos:altLabel` | `enroni:cp/reliant-energy-services` |
| Location / index / curve | `enroni:loc/{slug}`, `enroni:idx/{slug}`, `enroni:curve/{code}` | curated + corpus-mined | `enroni:loc/henry-hub` |
| Synthetic record | `enroni:syn/{system}/{table}/{key}` | generator run + natural key | `enroni:syn/sitara/deal/1043217` |

Rules:

1. IDs are content- or key-derived, so rebuilding the lake reproduces them.
2. An ID is never reassigned. Merged entities keep both IDs, linked with `owl:sameAs`, and the older one becomes canonical.
3. Anything synthetic is minted under `enroni:syn/`, so observed and generated facts can't be confused.
4. External alignment is recorded in `ontology/mappings/*.sssom.tsv` (SSSOM). It is never done by reusing external IRIs as our IDs.
