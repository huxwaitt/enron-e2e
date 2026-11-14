# Standards catalog: sources

This is the bibliography for `standards/era_standards.yaml`. Each record there also lists the specific URLs used to verify it. This page groups the main references and records the conventions the catalog follows.

## Conventions

- **Dates** are ISO-8601 strings. When a source gives only the month or year, the value is truncated (for example `"1998-06"` or `"1992"`).
- **`effective`** is the first period the standard applied to a calendar-year SEC registrant like Enron, or the first transaction date for transaction-based standards. The official wording is kept in `effective_note`.
- **Unverified values.** A value that no source confirmed is `null`, and the record is flagged `unverified: true` with an `unverified_fields` list. Nothing is filled in from memory.
- **Master agreements and frameworks** (ISDA, EEI, GISB, COSO) have no regulatory effective date, so `effective` is `null` and `effective_note` explains why.
- **`post_enron: true`** marks reforms that came after Enron's bankruptcy: EITF 02-3, FIN 45, FIN 46/46(R), SFAS 157, SFAS 167, SEC FR-61, SOX, PCAOB AS 2201, FERC Order 2001, the 2003 FERC price-index policy and Dodd-Frank Title VII.

## Enron primary documents (SEC EDGAR, CIK 0001024401)

- Enron Corp. Form 10-K for fiscal year 2000, filed April 2, 2001. Used for the accounting policies (mark-to-market, SAB 51, equity method, SFAS 71), SFAS 133 adoption, segments, securitizations, related-party note, VaR and APB 25. https://www.sec.gov/Archives/edgar/data/1024401/000102440101500010/ene10-k.txt
- Enron Corp. Form 8-K, filed November 8, 2001. Covers the 1997-2001 restatement: Chewco/JEDI and LJM1 consolidation, and the Raptor notes receivable. https://www.sec.gov/Archives/edgar/data/1024401/000095012901503835/0000950129-01-503835.txt
- *Report of Investigation by the Special Investigative Committee of the Board of Directors of Enron Corp.* (the Powers Report), dated February 1, 2002. Filed as an exhibit to Enron's 8-K of February 7, 2002. Covers the SPE 3% test, ARB 51, SFAS 57, S-K Item 404, Rule 4-08(k), the Andersen fees, the qualitative materiality conclusion and the "fundamentally inadequate" disclosure finding. https://www.sec.gov/Archives/edgar/data/1024401/000090951802000089/0000909518-02-000089.txt
- EDGAR filing index for Enron. It shows no 10-K for fiscal 2001. https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001024401&type=10-K
- SEC, Holding Co. Act Release No. 35-27809 (March 9, 2004). Covers Enron's PUHCA status. https://www.sec.gov/files/rules/other/35-27809.pdf

## FASB / AICPA original pronouncements (storage.fasb.org)

Issue and effective dates were read from the original documents:

- SFAS 5, 57, 71, 94, 107, 109, 121, 123, 125, 131, 133, 137, 138, 140, 142, 144, 157, 167 and 168
- ARB 51
- FIN 46 and FIN 46(R)

The URL pattern is `https://storage.fasb.org/fasNNN.pdf`, `https://storage.fasb.org/ARB%2051.pdf` and `https://storage.fasb.org/fin46.pdf` / `fin46r.pdf`. FIN 46 is also the source for the nullification of EITF 90-15, Topic D-14 and 96-21, and SFAS 157 for the nullification of EITF 02-3 footnote 3.

## EITF and secondary accounting sources

- EITF 98-10 consensus text, hosted by R. Jensen at Trinity University: https://www.cs.trinity.edu/rjensen/000overview/mp3/bookout.htm
- CFO.com, "Enron's derivative accounting legacy" (EITF 02-3): https://www.cfo.com/news/enrons-derivative-accounting-legacy/678056/
- Deloitte DART: ASC 850, ASC 606 principal-versus-agent, and the history of guarantee guidance (FIN 45): https://dart.deloitte.com/
- FY2000 SEC filings by other registrants that describe the EITF 00-19 consensus date (for example USA Education Inc. 10-Q): https://www.sec.gov/Archives/edgar/data/0001032033/000091205700050216/a2030171z10-q.txt
- Wikipedia, used for orientation only: Enron scandal, FIN 46, List of APB Opinions, and SAS 99.

## SEC releases and staff guidance

- SAB 101B and the Federal Register notice: https://www.sec.gov/interps/account/sab101b1.htm and https://www.govinfo.gov/content/pkg/FR-2000-07-03/pdf/00-16580.pdf
- SAB 104 press release: https://www.sec.gov/news/press/2003-174.htm
- SAB 99: https://www.sec.gov/interps/account/sab99.htm
- SAB 112: https://www.sec.gov/interps/account/sab112.htm
- Release 33-7386 (market risk, Item 305): https://www.sec.gov/rules/final/33-7386.htm
- Release 33-7919 (auditor independence): https://www.sec.gov/rules/final/33-7919.htm
- Release 33-8056 (FR-61): https://www.sec.gov/rules/other/33-8056.htm
- SOX §302 rules (press release 2002-128) and the §404 CorpFin alert: https://www.sec.gov/divisions/corpfin/cfalerts/cfalert030405.htm
- PCAOB AS 5 and AS 2201 pages: https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201

## FERC, CFTC and energy regulation

- FERC major orders list (archived) and FERC OATT history (Orders 636, 888, 889 and 2000): https://www.ferc.gov/history-oatt-reform
- FERC Order 587 Federal Register notices: https://www.govinfo.gov/content/pkg/FR-1996-10-25/html/96-27432.htm
- FERC Order 2001 EQR filing guide (archived): https://webarchive.library.unt.edu/web/20080916192326/http://ferc.gov/docs-filing/eqr/news-help/require-guide.pdf
- FERC price index policy statement, July 2003: https://webarchive.library.unt.edu/eot2008/20090114222131/http:/www.ferc.gov/news/news-releases/2003/2003-3/07-23-03-indexgas.pdf
- FERC staff final report on price manipulation in western markets, March 26, 2003 (archived release): https://webarchive.library.unt.edu/eot2008/20090114221159/http:/www.ferc.gov/news/news-releases/2003/2003-1/report3-26x.pdf
- FERC Form No. 1 page, and Order 627 (RM02-3) on the Uniform System of Accounts: https://www.ferc.gov/industries-data/electric/resources/industry-forms/form-no-1-annual-report-major-electric-utility
- CFTC history of the 1990s (1993 swap and energy exemptions): https://www.cftc.gov/About/HistoryoftheCFTC/history_1990s.html
- CRS Report RS22912, *The Enron Loophole* (2008): https://www.everycrsreport.com/reports/RS22912.html
- CFTC Part 43 and Part 45 final rules (2012): https://www.cftc.gov/LawRegulation/FederalRegister/FinalRules/2011-33199.html
- EIA summary of California AB 1890: https://www.eia.gov/electricity/policies/legislation/california/assemblybill.html
- PUHCA repeal: https://www.wiley.law/newsletter-936 and https://www.projectfinance.law/publications/2004/february/sec-signals-tougher-stance-on-puhca-exemptions

## Contracts and market conventions

- ISDA 1992 vs 2002 comparison: https://isda.org/book/comparison-between-the-1992-and-2002-isda-master-agreement
- ISDA 2000 Supplement to the 1993 Commodity Definitions: https://www.isda.org/book/2000-supplement-to-1993-commodity-definitions/
- EEI Master Contract page (Version 2.1, April 25, 2000): https://eei.org/resources-and-media/master-contract
- GISB Base Contract form (GISB-BC-2/13/96): https://naesb.org//pdf/Gisbsale.pdf
- NAESB press release on the 2002 Base Contract: https://www.naesb.org/pdf/042302pr.pdf
- CME Group, Henry Hub futures as a global benchmark: https://www.cmegroup.com/articles/whitepapers/henry-hub-natural-gas-futures-global-benchmark.html
- OSTI record on the start of NYMEX electricity futures (March 29, 1996): https://www.osti.gov/biblio/319013
- NGI on Inside FERC index testimony: https://www.naturalgasintel.com/price-editors-testify-to-editorial-checks-against-bogus-trades/

## Tax

- Federal Register, 1999 (IRC §475(e)/(f) regulations): https://www.govinfo.gov/content/pkg/FR-1999-01-28/html/99-1787.htm
- Joint Committee on Taxation, *Report of Investigation of Enron Corporation and Related Entities Regarding Federal Tax and Compensation Issues* (JCS-3-03, February 2003), via Senate Finance: https://www.finance.senate.gov/download/enron-the-joint-committee-on-taxations-investigative-report&download=1
