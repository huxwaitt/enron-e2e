# enron-e2e

`enron-e2e` builds a finance data lake on your computer from two public Enron data sets:

- The Enron spreadsheet corpus: 15,929 workbook files that Enron employees sent by email.
- The CMU Enron email corpus: 517,401 mail files from 149 mailboxes.

The spreadsheets show how the trading, settlement and accounting teams did their work. This project puts the two data sets into tables that you can query with SQL. Then it adds the context that the files do not contain:

- A label for each workbook. The label gives the process area (for example, settlement or credit) and the words that caused it.
- A catalog of 59 accounting, regulatory and contract standards from 1997 to 2001. Each record shows the rule that applies today.
- A link from each workbook to the standards that were in force on its creation date.
- Synthetic copies of 11 Enron source systems, from deal capture to the general ledger.
- A process log in OCEL 2.0 format and a knowledge graph in Turtle format.
- An ontology in LinkML with mappings to FIBO, OMG Commons, W3C vocabularies and schema.org.
- Data contracts, quality rules and lineage events.

The repository contains code and reference files only. The build downloads the data.

## Real data and synthetic data

The lake contains two types of data. Do not mix them.

**Observed data** comes from the two corpora. This includes the workbooks, the cells, the emails, the persons, and the links between emails and workbooks.

**Synthetic data** comes from a generator. The trades, nominations, invoices, payments and ledger postings are fiction. They are not the content of the Enron databases. The generator uses counterparty names, desks and locations that it finds in the corpus. It sets gas prices from the monthly Henry Hub averages that EIA publishes. Each synthetic trader is an ID without a name, so a real person is never attached to a synthetic trade.

You can always identify synthetic data:

- Each table from a synthetic system has a `_source_system` column. The observed tables are in `bronze/hermans/` and `bronze/cmu_email/` only.
- In the process log, the `provenance` column starts with `observed:` or `synthetic:`.

`ontology/ID_POLICY.md` keeps the prefix `enroni:syn/` for the IDs of synthetic records.

## Requirements

- Python 3.11 or later
- Approximately 5 GB of free disk space
- An internet connection for the first step, which downloads 1.4 GB

## Install

```
git clone https://github.com/huxwaitt/enron-e2e
cd enron-e2e
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux and macOS
pip install -e .
```

Use the `-e` option. The tool finds `sources.yaml` and the `ontology` folder from the location of the source files. If you install without `-e`, set `ENRON_E2E_ROOT` to the repository folder.

## Build the lake

```
enron-e2e all
```

This command runs 14 steps in sequence. Each step prints one JSON line with its name, its time in seconds and its result.

| Step | What it does | Output |
|---|---|---|
| `fetch` | Downloads the two archives. Compares each file with the MD5 in `sources.yaml` and stops if they are different. Extracts the spreadsheets. | `data/landing/` |
| `emails` | Reads each message in the CMU archive. Finds the spreadsheet file names in the message text. | `lake/bronze/cmu_email/` |
| `workbooks` | Reads each workbook: cells, formulas, number formats, sheets, defined names, external links, comments and document properties. | `lake/bronze/hermans/` |
| `silver` | Makes one row for each person and for each unique message. Links attachment names to workbook files and gives each link a score. | `lake/silver/` |
| `classify` | Gives each workbook a process area and a document role. | `lake/gold/workbook_labels.parquet` |
| `standards` | Finds the standards that were in force for each workbook on its creation date. | `lake/gold/workbook_standards.parquet` |
| `reference` | Collects counterparties, traders, books, desks, deal number formats, and price and volume ranges from the workbook columns. | `lake/gold/reference/` |
| `synth` | Generates the synthetic source systems. | `data/sources/*.duckdb` |
| `extract` | Copies each synthetic table into the lake. | `lake/bronze/<system>/` |
| `ocel` | Writes the process log. | `lake/gold/process_log/` |
| `graph` | Writes the knowledge graph and the SSSOM mappings. | `lake/gold/graph/` |
| `contracts` | Writes a data contract (ODCS v3) for each registered table. | `contracts/` |
| `catalog` | Creates a DuckDB database with one view for each table. | `lake/enron.duckdb` |
| `dq` | Runs each quality rule and records the result. | `lake/_meta/dq_results.parquet` |

You can also run one step or some steps:

```
enron-e2e classify standards catalog
```

The steps run in the sequence that you give. Keep the sequence of the table, because each step reads the output of the steps before it.

`fetch` does not download a file again if the file is there and its MD5 is correct.

### Options

| Option | Default | Effect |
|---|---|---|
| `--seed` | `2001` | Seed for the generator. The same seed gives the same synthetic data. |
| `--scale` | `1.0` | Multiplies the quantity of synthetic data. |
| `--workers` | `8` | Number of processes that read workbooks at the same time. |
| `--with-eml` | off | Also downloads the 8.8 GB archive of the emails that carried the spreadsheets. |

### Environment variables

| Variable | Default | Effect |
|---|---|---|
| `ENRON_E2E_ROOT` | the repository folder | The folder that contains `sources.yaml`, `ontology/` and `data/`. |
| `ENRON_E2E_LAKE` | `<root>/lake` | The folder for the lake. |

## Query the lake

The `catalog` step writes `lake/enron.duckdb`. The database has three schemas: `bronze`, `silver` and `gold`. Each view reads the Parquet files directly.

A view name is the file path in lowercase, with underscores between the parts. For example, `lake/bronze/sap/BSEG.parquet` becomes `bronze.sap_bseg`.

```python
import duckdb

con = duckdb.connect("lake/enron.duckdb", read_only=True)
con.sql("""
    select process_area, count(*) as workbooks
    from gold.workbook_labels
    group by 1
    order by 2 desc
    limit 5
""").show()
```

```
risk_and_valuation      3623
scheduling_logistics    3294
unclassified            3280
deal_capture            1648
fpa                      739
```

Two outputs are not in the DuckDB database:

- `lake/gold/process_log/enron_ocel2.sqlite` is the process log in the OCEL 2.0 SQLite layout. Open it with a process mining tool that reads OCEL 2.0.
- `lake/gold/graph/enron_kg.ttl` is the knowledge graph. Load it into an RDF store.

## What is in the lake

| Layer | Folder | Contents |
|---|---|---|
| Landing | `data/landing/` | The downloaded archives. The build does not change them. |
| Bronze | `lake/bronze/` | One table for each source object, with the content as the source gives it. |
| Silver | `lake/silver/` | Persons, unique messages, recipients, and links between emails and workbooks. |
| Gold | `lake/gold/` | Workbook labels, standards, reference data, the process log and the knowledge graph. |
| Metadata | `lake/_meta/` | Lineage events (OpenLineage) and the results of the quality rules. |

A build with the default options gave these counts:

- 15,929 workbook files with more than 70 million non-empty cells
- 517,401 mail files, which become 254,305 unique messages
- 67,159 links between an attachment name in an email and a workbook file
- 36 synthetic tables with 1.46 million rows
- 17,345 observed events and 456,847 synthetic events in the process log

### The synthetic source systems

| System | Function | Tables |
|---|---|---|
| EnronOnline (`eol`) | Online trades | `PRODUCT`, `TRANSACTION` |
| Sitara (`sitara`) | Gas deals and nominations | `DEAL`, `NOMINATION` |
| EnPower (`enpower`) | Power deals and schedules | `PWR_DEAL`, `SCHEDULE` |
| TAGG (`tagg`) | Financial deals | `FIN_DEAL` |
| ERMS (`erms`) | Books, desks, traders, curves, index prices and the daily position report | 9 tables |
| Global Counterparty (`gcp`) | Counterparties, credit limits, master agreements and collateral calls | 4 tables |
| Global Contracts (`global_contracts`) | Trade confirmations | `CONFIRMATION` |
| Unify (`unify_gas`, `unify_power`, `unify_financial`) | Invoices and payments | `INVOICE_HDR`, `INVOICE_LINE`, `PAYMENT` |
| SAP R/3 FI (`sap`) | General ledger | `BKPF`, `BSEG` and 4 master tables |

The synthetic trades stop on November 29, 2001. The timeline follows the collapse of Enron in 2001.

## Repository layout

```
sources.yaml           The source registry: URL, MD5, license and citation for each download
ontology/              The LinkML ontology, the generated OWL, JSON Schema, SQL DDL and Python files,
                       the SSSOM mappings and the ID policy
ontology/reference/    Curated systems, organizations, market words, classifier rules and market history
standards/             The standards catalog and its list of sources
src/enron_e2e/         The pipeline code
tests/                 Unit tests and lake tests
```

To change how the classifier labels workbooks, edit `ontology/reference/classifier_rules.yaml`. Then run `enron-e2e classify` and compare the new `workbook_labels.parquet` with the old one.

## Tests

```
pip install -e ".[dev]"
pytest -q tests/test_units.py
```

The unit tests do not use the downloaded data.

After a full build, run `pytest -q`. This command also runs the lake tests. For example, they make sure that each SAP document balances and that each invoice total agrees with its lines. If `lake/enron.duckdb` is not there, pytest skips the lake tests.

## Known limits

- For old `.xls` files, the build reads cell values only. It cannot read their formulas.
- The classifier is a list of words with weights. Approximately 21% of the workbooks get the label `unclassified`.
- The authors of the spreadsheet corpus changed the `.xls` files to `.xlsx` in 2014. Thus the modified dates and the `last_modified_by` values come from 2014. Use the `created` column.
- The CMU corpus has no attachments. The build links emails to workbooks from the attachment names in the message text. Each link has a score.
- In the standards catalog, a value that no source confirmed is `null`. The record has the flag `unverified: true`.
- The data contracts and the quality rules include 9 tables at this time.
- `--with-eml` downloads the archive, but no step reads it at this time.
- The views in `lake/enron.duckdb` contain full paths. If you move the lake, run `enron-e2e catalog` again.

## Data sources and license

The code has the MIT license. See `LICENSE`.

The data has its own terms:

- F. Hermans and E. Murphy-Hill, "Enron's Spreadsheets and Related Emails: A Dataset and Analysis", ICSE 2015. figshare, [doi:10.6084/m9.figshare.1221767.v2](https://doi.org/10.6084/m9.figshare.1221767.v2). License: CC BY 4.0.
- W. Cohen, Enron Email Dataset, release of May 7, 2015, Carnegie Mellon University. <https://www.cs.cmu.edu/~enron/>. FERC released these emails during its investigation of the Western energy markets.

The two corpora contain the names, email addresses and messages of real persons. The data contracts mark these columns with a `pii:` tag. Be careful if you publish data from the lake.

`NOTICE` gives the full attribution. `standards/sources.md` lists the sources for the standards catalog.
