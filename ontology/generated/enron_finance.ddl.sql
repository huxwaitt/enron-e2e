-- # Abstract Class: NamedThing Description: Anything with a persistent identifier in the estate.
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Evidence Description: Provenance pointer from an assertion back to the corpus or to a synthetic generator. Lets every fact in the lake be traced to a cell, an email or a rule.
--     * Slot: id
--     * Slot: source_kind
--     * Slot: source_id Description: workbook file_id, email message_id, filing accession, or generator run id
--     * Slot: locator Description: sheet!cell range, header field, or rule name
--     * Slot: quote Description: verbatim snippet supporting the assertion
--     * Slot: confidence
--     * Slot: NamedThing_id Description: Autocreated FK slot
--     * Slot: Agent_id Description: Autocreated FK slot
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: LegalEntity_id Description: Autocreated FK slot
--     * Slot: SpecialPurposeEntity_id Description: Autocreated FK slot
--     * Slot: BusinessUnit_id Description: Autocreated FK slot
--     * Slot: TradingDesk_id Description: Autocreated FK slot
--     * Slot: Counterparty_id Description: Autocreated FK slot
--     * Slot: MarketInfrastructure_id Description: Autocreated FK slot
--     * Slot: InformationSystem_id Description: Autocreated FK slot
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: Control_id Description: Autocreated FK slot
--     * Slot: Standard_id Description: Autocreated FK slot
--     * Slot: Commodity_id Description: Autocreated FK slot
--     * Slot: Location_id Description: Autocreated FK slot
--     * Slot: TradingHub_id Description: Autocreated FK slot
--     * Slot: DeliveryPoint_id Description: Autocreated FK slot
--     * Slot: Pipeline_id Description: Autocreated FK slot
--     * Slot: PowerControlArea_id Description: Autocreated FK slot
--     * Slot: PriceIndex_id Description: Autocreated FK slot
--     * Slot: PriceCurve_id Description: Autocreated FK slot
--     * Slot: MasterAgreement_id Description: Autocreated FK slot
--     * Slot: Trade_id Description: Autocreated FK slot
--     * Slot: Book_id Description: Autocreated FK slot
--     * Slot: Position_id Description: Autocreated FK slot
--     * Slot: Valuation_id Description: Autocreated FK slot
--     * Slot: Nomination_id Description: Autocreated FK slot
--     * Slot: Imbalance_id Description: Autocreated FK slot
--     * Slot: Invoice_id Description: Autocreated FK slot
--     * Slot: Payment_id Description: Autocreated FK slot
--     * Slot: GLAccount_id Description: Autocreated FK slot
--     * Slot: CostCenter_id Description: Autocreated FK slot
--     * Slot: JournalEntry_id Description: Autocreated FK slot
--     * Slot: Document_id Description: Autocreated FK slot
--     * Slot: Workbook_id Description: Autocreated FK slot
--     * Slot: Worksheet_id Description: Autocreated FK slot
--     * Slot: TableRegion_id Description: Autocreated FK slot
--     * Slot: EmailMessage_id Description: Autocreated FK slot
-- # Abstract Class: Agent
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Person
--     * Slot: job_title
--     * Slot: is_custodian Description: Person is one of the mailbox custodians in the corpus.
--     * Slot: maildir_name
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Abstract Class: Organization
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: LegalEntity Description: A legally registered Enron affiliate (e.g. Enron North America Corp.).
--     * Slot: parent_entity
--     * Slot: jurisdiction
--     * Slot: segment Description: Reportable segment per FAS 131 in the 2000 Form 10-K.
--     * Slot: sec_registrant
--     * Slot: ferc_regulated
--     * Slot: special_purpose
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: SpecialPurposeEntity Description: Off-balance-sheet or structured vehicle (e.g. LJM2, Chewco, Whitewing, Raptor vehicles). Kept distinct because consolidation treatment is the point of interest.
--     * Slot: parent_entity
--     * Slot: jurisdiction
--     * Slot: segment Description: Reportable segment per FAS 131 in the 2000 Form 10-K.
--     * Slot: sec_registrant
--     * Slot: ferc_regulated
--     * Slot: special_purpose
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: BusinessUnit Description: Management unit (segment, business unit, department) that is not itself a legal entity.
--     * Slot: parent_unit
--     * Slot: legal_entity
--     * Slot: unit_type
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: TradingDesk Description: Commercial desk owning books and traders (e.g. "West Power", "Texas Gas", "NW desk").
--     * Slot: commodity
--     * Slot: region
--     * Slot: parent_unit
--     * Slot: legal_entity
--     * Slot: unit_type
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Counterparty Description: External trading counterparty, as mastered in Global Counterparty (GCP).
--     * Slot: gcp_cp_id Description: Global Counterparty CP ID.
--     * Slot: short_name Description: ERMS/GCP short name.
--     * Slot: credit_rating
--     * Slot: counterparty_type
--     * Slot: parent_counterparty
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: MarketInfrastructure Description: Exchange, ISO/RTO, pipeline operator or price publisher.
--     * Slot: infrastructure_type
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: InformationSystem Description: An application in the trade-to-ledger chain (Sitara, EnPower, ERMS, Unify, SAP ...).
--     * Slot: system_code
--     * Slot: platform
--     * Slot: owning_unit
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: ProcessStep Description: A step in a front-to-back process (e.g. "Actualize volumes", "Run DPR").
--     * Slot: process_area
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Control Description: A check that existed (or should have) at the time, e.g. daily P&L sign-off, deal-entry verification, RAC credit approval. Pre-SOX; mapped to modern control objectives.
--     * Slot: process_area
--     * Slot: control_type
--     * Slot: modern_equivalent Description: e.g. SOX 404 key control, COSO 2013 principle.
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Standard Description: Accounting, regulatory, contractual or market standard; records live in standards/era_standards.yaml.
--     * Slot: designation
--     * Slot: issuer
--     * Slot: effective_date
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Commodity
--     * Slot: commodity_kind
--     * Slot: default_unit
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Abstract Class: Location
--     * Slot: location_type
--     * Slot: region
--     * Slot: commodity
--     * Slot: operator
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: TradingHub Description: Liquid pricing point (Henry Hub, Waha, Mid-C, Palo Verde, PJM West ...).
--     * Slot: location_type
--     * Slot: region
--     * Slot: commodity
--     * Slot: operator
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: DeliveryPoint Description: Physical meter/interconnect or pool where title transfers.
--     * Slot: pipeline
--     * Slot: meter_number
--     * Slot: location_type
--     * Slot: region
--     * Slot: commodity
--     * Slot: operator
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Pipeline Description: Interstate or intrastate pipeline system (Transwestern, Northern Natural, El Paso ...).
--     * Slot: ferc_regulated
--     * Slot: location_type
--     * Slot: region
--     * Slot: commodity
--     * Slot: operator
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: PowerControlArea Description: Power control area, ISO zone or transmission path (NP15, SP15, COB, ERCOT ...).
--     * Slot: location_type
--     * Slot: region
--     * Slot: commodity
--     * Slot: operator
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: PriceIndex Description: Published or exchange price used to settle index deals (IFERC monthly, Gas Daily, NYMEX).
--     * Slot: publisher
--     * Slot: index_frequency
--     * Slot: location
--     * Slot: commodity
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: PriceCurve Description: Forward curve maintained in ERMS/TDS for valuation (price, basis, volatility).
--     * Slot: curve_code
--     * Slot: curve_type
--     * Slot: commodity
--     * Slot: location
--     * Slot: index
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: CurvePoint Description: One marked value of a curve for a delivery period on a valuation date.
--     * Slot: id
--     * Slot: curve
--     * Slot: valuation_date
--     * Slot: delivery_start
--     * Slot: value
--     * Slot: unit
--     * Slot: is_synthetic
-- # Class: MasterAgreement Description: Governing master (ISDA 1992, GISB 1996 base contract, EEI 2000 master, enabling agreements).
--     * Slot: agreement_form
--     * Slot: counterparty
--     * Slot: legal_entity
--     * Slot: effective_date
--     * Slot: netting
--     * Slot: collateral_threshold
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Trade Description: A deal as captured in a front-office system (Sitara, EnPower, TAGG) or on EnronOnline.
--     * Slot: deal_number
--     * Slot: source_system
--     * Slot: eol_transaction_id
--     * Slot: trade_date
--     * Slot: legal_entity
--     * Slot: counterparty
--     * Slot: book
--     * Slot: trader
--     * Slot: commodity
--     * Slot: instrument_type
--     * Slot: buy_sell
--     * Slot: volume
--     * Slot: volume_unit
--     * Slot: volume_frequency
--     * Slot: price
--     * Slot: price_type
--     * Slot: price_index
--     * Slot: premium_or_adder
--     * Slot: delivery_location
--     * Slot: delivery_start
--     * Slot: delivery_end
--     * Slot: deal_status
--     * Slot: master_agreement
--     * Slot: confirmation_status
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Book Description: Portfolio/book in ERMS/RisktRAC that positions roll up to (e.g. "ENA-FT-WEST-PHY").
--     * Slot: book_code
--     * Slot: desk
--     * Slot: legal_entity
--     * Slot: commodity
--     * Slot: book_type
--     * Slot: region
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Position Description: Net open position by book, curve and delivery period on a date (DPR input).
--     * Slot: book
--     * Slot: curve
--     * Slot: as_of_date
--     * Slot: delivery_start
--     * Slot: quantity
--     * Slot: volume_unit
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Valuation Description: Mark-to-market result (DPR line) by book on a date, incl. new-deal and curve-shift P&L.
--     * Slot: book
--     * Slot: as_of_date
--     * Slot: mtm_value
--     * Slot: daily_pnl
--     * Slot: new_deal_pnl
--     * Slot: curve_shift_pnl
--     * Slot: var_95
--     * Slot: currency
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Nomination Description: Gas nomination / power schedule submitted to a pipeline or ISO.
--     * Slot: trade
--     * Slot: pipeline
--     * Slot: delivery_location
--     * Slot: flow_date
--     * Slot: nominated_volume
--     * Slot: scheduled_volume
--     * Slot: actual_volume
--     * Slot: volume_unit
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Imbalance
--     * Slot: pipeline
--     * Slot: delivery_location
--     * Slot: flow_month
--     * Slot: imbalance_volume
--     * Slot: volume_unit
--     * Slot: counterparty
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Invoice Description: Settlement invoice/statement produced by Unify for a counterparty and production month.
--     * Slot: invoice_number
--     * Slot: counterparty
--     * Slot: legal_entity
--     * Slot: production_month
--     * Slot: invoice_date
--     * Slot: due_date
--     * Slot: amount
--     * Slot: currency
--     * Slot: invoice_status
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Payment
--     * Slot: counterparty
--     * Slot: legal_entity
--     * Slot: payment_date
--     * Slot: amount
--     * Slot: currency
--     * Slot: direction
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: GLAccount Description: SAP R/3 general ledger account.
--     * Slot: account_number
--     * Slot: account_type
--     * Slot: fs_line
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: CostCenter
--     * Slot: cost_center_code
--     * Slot: legal_entity
--     * Slot: business_unit
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: JournalEntry Description: SAP FI document (BKPF header with BSEG lines).
--     * Slot: document_number
--     * Slot: company_code
--     * Slot: fiscal_year
--     * Slot: posting_date
--     * Slot: document_type
--     * Slot: header_text
--     * Slot: entered_by
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: JournalLine
--     * Slot: id
--     * Slot: gl_account
--     * Slot: debit_credit
--     * Slot: amount
--     * Slot: cost_center
--     * Slot: counterparty
--     * Slot: trading_partner
--     * Slot: JournalEntry_id Description: Autocreated FK slot
-- # Abstract Class: Document
--     * Slot: created
--     * Slot: author
--     * Slot: custodian
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Workbook Description: One spreadsheet file from the Hermans corpus (deduplicated by MD5).
--     * Slot: file_id Description: MD5 of the file bytes.
--     * Slot: original_filename
--     * Slot: process_area
--     * Slot: document_role
--     * Slot: version_family Description: Groups files that are versions of the same recurring report.
--     * Slot: as_of_date
--     * Slot: created
--     * Slot: author
--     * Slot: custodian
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: Worksheet
--     * Slot: workbook
--     * Slot: sheet_name
--     * Slot: sheet_state
--     * Slot: sheet_role
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: TableRegion Description: A detected rectangular table inside a sheet, with header and data ranges.
--     * Slot: worksheet
--     * Slot: cell_range
--     * Slot: header_range
--     * Slot: table_role
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: EmailMessage
--     * Slot: message_id
--     * Slot: sent_at
--     * Slot: sender
--     * Slot: subject
--     * Slot: thread
--     * Slot: created
--     * Slot: author
--     * Slot: custodian
--     * Slot: id
--     * Slot: label
--     * Slot: description
--     * Slot: is_synthetic Description: True when the record was produced by a generator rather than observed in the corpus.
--     * Slot: valid_from
--     * Slot: valid_to
-- # Class: NamedThing_alt_labels
--     * Slot: NamedThing_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Agent_alt_labels
--     * Slot: Agent_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Person_email_addresses
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: email_addresses
-- # Class: Person_member_of
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: member_of_id
-- # Class: Person_alt_labels
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Organization_alt_labels
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: LegalEntity_alt_labels
--     * Slot: LegalEntity_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: SpecialPurposeEntity_alt_labels
--     * Slot: SpecialPurposeEntity_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: BusinessUnit_alt_labels
--     * Slot: BusinessUnit_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: TradingDesk_alt_labels
--     * Slot: TradingDesk_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Counterparty_alt_labels
--     * Slot: Counterparty_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: MarketInfrastructure_alt_labels
--     * Slot: MarketInfrastructure_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: InformationSystem_process_areas
--     * Slot: InformationSystem_id Description: Autocreated FK slot
--     * Slot: process_areas
-- # Class: InformationSystem_upstream_systems
--     * Slot: InformationSystem_id Description: Autocreated FK slot
--     * Slot: upstream_systems_id
-- # Class: InformationSystem_downstream_systems
--     * Slot: InformationSystem_id Description: Autocreated FK slot
--     * Slot: downstream_systems_id
-- # Class: InformationSystem_alt_labels
--     * Slot: InformationSystem_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: ProcessStep_performed_in
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: performed_in_id
-- # Class: ProcessStep_inputs
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: inputs_id
-- # Class: ProcessStep_outputs
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: outputs_id
-- # Class: ProcessStep_governed_by
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: governed_by_id
-- # Class: ProcessStep_alt_labels
--     * Slot: ProcessStep_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Control_governed_by
--     * Slot: Control_id Description: Autocreated FK slot
--     * Slot: governed_by_id
-- # Class: Control_alt_labels
--     * Slot: Control_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Standard_process_areas
--     * Slot: Standard_id Description: Autocreated FK slot
--     * Slot: process_areas
-- # Class: Standard_alt_labels
--     * Slot: Standard_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Commodity_alt_labels
--     * Slot: Commodity_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Location_alt_labels
--     * Slot: Location_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: TradingHub_alt_labels
--     * Slot: TradingHub_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: DeliveryPoint_alt_labels
--     * Slot: DeliveryPoint_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Pipeline_alt_labels
--     * Slot: Pipeline_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: PowerControlArea_alt_labels
--     * Slot: PowerControlArea_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: PriceIndex_alt_labels
--     * Slot: PriceIndex_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: PriceCurve_alt_labels
--     * Slot: PriceCurve_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: MasterAgreement_alt_labels
--     * Slot: MasterAgreement_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Trade_alt_labels
--     * Slot: Trade_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Book_alt_labels
--     * Slot: Book_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Position_alt_labels
--     * Slot: Position_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Valuation_alt_labels
--     * Slot: Valuation_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Nomination_alt_labels
--     * Slot: Nomination_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Imbalance_alt_labels
--     * Slot: Imbalance_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Invoice_trades
--     * Slot: Invoice_id Description: Autocreated FK slot
--     * Slot: trades_id
-- # Class: Invoice_alt_labels
--     * Slot: Invoice_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Payment_invoices
--     * Slot: Payment_id Description: Autocreated FK slot
--     * Slot: invoices_id
-- # Class: Payment_alt_labels
--     * Slot: Payment_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: GLAccount_alt_labels
--     * Slot: GLAccount_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: CostCenter_alt_labels
--     * Slot: CostCenter_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: JournalEntry_alt_labels
--     * Slot: JournalEntry_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Document_alt_labels
--     * Slot: Document_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Workbook_mentions
--     * Slot: Workbook_id Description: Autocreated FK slot
--     * Slot: mentions_id
-- # Class: Workbook_sheets
--     * Slot: Workbook_id Description: Autocreated FK slot
--     * Slot: sheets_id
-- # Class: Workbook_derived_from
--     * Slot: Workbook_id Description: Autocreated FK slot
--     * Slot: derived_from_id
-- # Class: Workbook_alt_labels
--     * Slot: Workbook_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: Worksheet_alt_labels
--     * Slot: Worksheet_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: TableRegion_alt_labels
--     * Slot: TableRegion_id Description: Autocreated FK slot
--     * Slot: alt_labels
-- # Class: EmailMessage_recipients
--     * Slot: EmailMessage_id Description: Autocreated FK slot
--     * Slot: recipients_id
-- # Class: EmailMessage_attachments
--     * Slot: EmailMessage_id Description: Autocreated FK slot
--     * Slot: attachments_id
-- # Class: EmailMessage_alt_labels
--     * Slot: EmailMessage_id Description: Autocreated FK slot
--     * Slot: alt_labels

CREATE TABLE "NamedThing" (
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_NamedThing_id" ON "NamedThing" (id);

CREATE TABLE "Agent" (
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Agent_id" ON "Agent" (id);

CREATE TABLE "Person" (
	job_title TEXT,
	is_custodian BOOLEAN,
	maildir_name TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Person_id" ON "Person" (id);

CREATE TABLE "Organization" (
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Organization_id" ON "Organization" (id);

CREATE TABLE "LegalEntity" (
	parent_entity TEXT,
	jurisdiction TEXT,
	segment TEXT,
	sec_registrant BOOLEAN,
	ferc_regulated BOOLEAN,
	special_purpose BOOLEAN,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_entity) REFERENCES "LegalEntity" (id),
	FOREIGN KEY(segment) REFERENCES "BusinessUnit" (id)
);
CREATE INDEX "ix_LegalEntity_id" ON "LegalEntity" (id);

CREATE TABLE "BusinessUnit" (
	parent_unit TEXT,
	legal_entity TEXT,
	unit_type VARCHAR(13),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_unit) REFERENCES "BusinessUnit" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_BusinessUnit_id" ON "BusinessUnit" (id);

CREATE TABLE "Counterparty" (
	gcp_cp_id TEXT,
	short_name TEXT,
	credit_rating TEXT,
	counterparty_type TEXT,
	parent_counterparty TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_counterparty) REFERENCES "Counterparty" (id)
);
CREATE INDEX "ix_Counterparty_id" ON "Counterparty" (id);

CREATE TABLE "MarketInfrastructure" (
	infrastructure_type VARCHAR(17),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_MarketInfrastructure_id" ON "MarketInfrastructure" (id);

CREATE TABLE "ProcessStep" (
	process_area VARCHAR(23),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_ProcessStep_id" ON "ProcessStep" (id);

CREATE TABLE "Control" (
	process_area VARCHAR(23),
	control_type TEXT,
	modern_equivalent TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Control_id" ON "Control" (id);

CREATE TABLE "Standard" (
	designation TEXT,
	issuer TEXT,
	effective_date DATE,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Standard_id" ON "Standard" (id);

CREATE TABLE "Commodity" (
	commodity_kind VARCHAR(18),
	default_unit VARCHAR(5),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Commodity_id" ON "Commodity" (id);

CREATE TABLE "GLAccount" (
	account_number TEXT,
	account_type TEXT,
	fs_line TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_GLAccount_id" ON "GLAccount" (id);

CREATE TABLE "SpecialPurposeEntity" (
	parent_entity TEXT,
	jurisdiction TEXT,
	segment TEXT,
	sec_registrant BOOLEAN,
	ferc_regulated BOOLEAN,
	special_purpose BOOLEAN,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_entity) REFERENCES "LegalEntity" (id),
	FOREIGN KEY(segment) REFERENCES "BusinessUnit" (id)
);
CREATE INDEX "ix_SpecialPurposeEntity_id" ON "SpecialPurposeEntity" (id);

CREATE TABLE "TradingDesk" (
	commodity TEXT,
	region TEXT,
	parent_unit TEXT,
	legal_entity TEXT,
	unit_type VARCHAR(13),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(parent_unit) REFERENCES "BusinessUnit" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_TradingDesk_id" ON "TradingDesk" (id);

CREATE TABLE "InformationSystem" (
	system_code TEXT,
	platform TEXT,
	owning_unit TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(owning_unit) REFERENCES "BusinessUnit" (id)
);
CREATE INDEX "ix_InformationSystem_id" ON "InformationSystem" (id);

CREATE TABLE "Location" (
	location_type TEXT,
	region TEXT,
	commodity TEXT,
	operator TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(operator) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_Location_id" ON "Location" (id);

CREATE TABLE "TradingHub" (
	location_type TEXT,
	region TEXT,
	commodity TEXT,
	operator TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(operator) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_TradingHub_id" ON "TradingHub" (id);

CREATE TABLE "Pipeline" (
	ferc_regulated BOOLEAN,
	location_type TEXT,
	region TEXT,
	commodity TEXT,
	operator TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(operator) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_Pipeline_id" ON "Pipeline" (id);

CREATE TABLE "PowerControlArea" (
	location_type TEXT,
	region TEXT,
	commodity TEXT,
	operator TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(operator) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_PowerControlArea_id" ON "PowerControlArea" (id);

CREATE TABLE "MasterAgreement" (
	agreement_form VARCHAR(10),
	counterparty TEXT,
	legal_entity TEXT,
	effective_date DATE,
	netting BOOLEAN,
	collateral_threshold FLOAT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_MasterAgreement_id" ON "MasterAgreement" (id);

CREATE TABLE "Invoice" (
	invoice_number TEXT,
	counterparty TEXT,
	legal_entity TEXT,
	production_month TEXT,
	invoice_date DATE,
	due_date DATE,
	amount FLOAT,
	currency TEXT,
	invoice_status TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_Invoice_id" ON "Invoice" (id);

CREATE TABLE "Payment" (
	counterparty TEXT,
	legal_entity TEXT,
	payment_date DATE,
	amount FLOAT,
	currency TEXT,
	direction TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_Payment_id" ON "Payment" (id);

CREATE TABLE "CostCenter" (
	cost_center_code TEXT,
	legal_entity TEXT,
	business_unit TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id),
	FOREIGN KEY(business_unit) REFERENCES "BusinessUnit" (id)
);
CREATE INDEX "ix_CostCenter_id" ON "CostCenter" (id);

CREATE TABLE "JournalEntry" (
	document_number TEXT,
	company_code TEXT,
	fiscal_year INTEGER,
	posting_date DATE,
	document_type TEXT,
	header_text TEXT,
	entered_by TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(entered_by) REFERENCES "Person" (id)
);
CREATE INDEX "ix_JournalEntry_id" ON "JournalEntry" (id);

CREATE TABLE "Document" (
	created DATETIME,
	author TEXT,
	custodian TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(custodian) REFERENCES "Person" (id)
);
CREATE INDEX "ix_Document_id" ON "Document" (id);

CREATE TABLE "Workbook" (
	file_id TEXT,
	original_filename TEXT,
	process_area VARCHAR(23),
	document_role VARCHAR(14),
	version_family TEXT,
	as_of_date DATE,
	created DATETIME,
	author TEXT,
	custodian TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(custodian) REFERENCES "Person" (id)
);
CREATE INDEX "ix_Workbook_id" ON "Workbook" (id);

CREATE TABLE "EmailMessage" (
	message_id TEXT,
	sent_at DATETIME,
	sender TEXT,
	subject TEXT,
	thread TEXT,
	created DATETIME,
	author TEXT,
	custodian TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(sender) REFERENCES "Person" (id),
	FOREIGN KEY(custodian) REFERENCES "Person" (id)
);
CREATE INDEX "ix_EmailMessage_id" ON "EmailMessage" (id);

CREATE TABLE "NamedThing_alt_labels" (
	"NamedThing_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("NamedThing_id", alt_labels),
	FOREIGN KEY("NamedThing_id") REFERENCES "NamedThing" (id)
);
CREATE INDEX "ix_NamedThing_alt_labels_alt_labels" ON "NamedThing_alt_labels" (alt_labels);
CREATE INDEX "ix_NamedThing_alt_labels_NamedThing_id" ON "NamedThing_alt_labels" ("NamedThing_id");

CREATE TABLE "Agent_alt_labels" (
	"Agent_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Agent_id", alt_labels),
	FOREIGN KEY("Agent_id") REFERENCES "Agent" (id)
);
CREATE INDEX "ix_Agent_alt_labels_Agent_id" ON "Agent_alt_labels" ("Agent_id");
CREATE INDEX "ix_Agent_alt_labels_alt_labels" ON "Agent_alt_labels" (alt_labels);

CREATE TABLE "Person_email_addresses" (
	"Person_id" TEXT,
	email_addresses TEXT,
	PRIMARY KEY ("Person_id", email_addresses),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE INDEX "ix_Person_email_addresses_email_addresses" ON "Person_email_addresses" (email_addresses);
CREATE INDEX "ix_Person_email_addresses_Person_id" ON "Person_email_addresses" ("Person_id");

CREATE TABLE "Person_member_of" (
	"Person_id" TEXT,
	member_of_id TEXT,
	PRIMARY KEY ("Person_id", member_of_id),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id),
	FOREIGN KEY(member_of_id) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_Person_member_of_Person_id" ON "Person_member_of" ("Person_id");
CREATE INDEX "ix_Person_member_of_member_of_id" ON "Person_member_of" (member_of_id);

CREATE TABLE "Person_alt_labels" (
	"Person_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Person_id", alt_labels),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE INDEX "ix_Person_alt_labels_alt_labels" ON "Person_alt_labels" (alt_labels);
CREATE INDEX "ix_Person_alt_labels_Person_id" ON "Person_alt_labels" ("Person_id");

CREATE TABLE "Organization_alt_labels" (
	"Organization_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Organization_id", alt_labels),
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id)
);
CREATE INDEX "ix_Organization_alt_labels_alt_labels" ON "Organization_alt_labels" (alt_labels);
CREATE INDEX "ix_Organization_alt_labels_Organization_id" ON "Organization_alt_labels" ("Organization_id");

CREATE TABLE "LegalEntity_alt_labels" (
	"LegalEntity_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("LegalEntity_id", alt_labels),
	FOREIGN KEY("LegalEntity_id") REFERENCES "LegalEntity" (id)
);
CREATE INDEX "ix_LegalEntity_alt_labels_LegalEntity_id" ON "LegalEntity_alt_labels" ("LegalEntity_id");
CREATE INDEX "ix_LegalEntity_alt_labels_alt_labels" ON "LegalEntity_alt_labels" (alt_labels);

CREATE TABLE "BusinessUnit_alt_labels" (
	"BusinessUnit_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("BusinessUnit_id", alt_labels),
	FOREIGN KEY("BusinessUnit_id") REFERENCES "BusinessUnit" (id)
);
CREATE INDEX "ix_BusinessUnit_alt_labels_alt_labels" ON "BusinessUnit_alt_labels" (alt_labels);
CREATE INDEX "ix_BusinessUnit_alt_labels_BusinessUnit_id" ON "BusinessUnit_alt_labels" ("BusinessUnit_id");

CREATE TABLE "Counterparty_alt_labels" (
	"Counterparty_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Counterparty_id", alt_labels),
	FOREIGN KEY("Counterparty_id") REFERENCES "Counterparty" (id)
);
CREATE INDEX "ix_Counterparty_alt_labels_alt_labels" ON "Counterparty_alt_labels" (alt_labels);
CREATE INDEX "ix_Counterparty_alt_labels_Counterparty_id" ON "Counterparty_alt_labels" ("Counterparty_id");

CREATE TABLE "MarketInfrastructure_alt_labels" (
	"MarketInfrastructure_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("MarketInfrastructure_id", alt_labels),
	FOREIGN KEY("MarketInfrastructure_id") REFERENCES "MarketInfrastructure" (id)
);
CREATE INDEX "ix_MarketInfrastructure_alt_labels_alt_labels" ON "MarketInfrastructure_alt_labels" (alt_labels);
CREATE INDEX "ix_MarketInfrastructure_alt_labels_MarketInfrastructure_id" ON "MarketInfrastructure_alt_labels" ("MarketInfrastructure_id");

CREATE TABLE "ProcessStep_inputs" (
	"ProcessStep_id" TEXT,
	inputs_id TEXT,
	PRIMARY KEY ("ProcessStep_id", inputs_id),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id),
	FOREIGN KEY(inputs_id) REFERENCES "NamedThing" (id)
);
CREATE INDEX "ix_ProcessStep_inputs_ProcessStep_id" ON "ProcessStep_inputs" ("ProcessStep_id");
CREATE INDEX "ix_ProcessStep_inputs_inputs_id" ON "ProcessStep_inputs" (inputs_id);

CREATE TABLE "ProcessStep_outputs" (
	"ProcessStep_id" TEXT,
	outputs_id TEXT,
	PRIMARY KEY ("ProcessStep_id", outputs_id),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id),
	FOREIGN KEY(outputs_id) REFERENCES "NamedThing" (id)
);
CREATE INDEX "ix_ProcessStep_outputs_ProcessStep_id" ON "ProcessStep_outputs" ("ProcessStep_id");
CREATE INDEX "ix_ProcessStep_outputs_outputs_id" ON "ProcessStep_outputs" (outputs_id);

CREATE TABLE "ProcessStep_governed_by" (
	"ProcessStep_id" TEXT,
	governed_by_id TEXT,
	PRIMARY KEY ("ProcessStep_id", governed_by_id),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id),
	FOREIGN KEY(governed_by_id) REFERENCES "Standard" (id)
);
CREATE INDEX "ix_ProcessStep_governed_by_governed_by_id" ON "ProcessStep_governed_by" (governed_by_id);
CREATE INDEX "ix_ProcessStep_governed_by_ProcessStep_id" ON "ProcessStep_governed_by" ("ProcessStep_id");

CREATE TABLE "ProcessStep_alt_labels" (
	"ProcessStep_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("ProcessStep_id", alt_labels),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id)
);
CREATE INDEX "ix_ProcessStep_alt_labels_ProcessStep_id" ON "ProcessStep_alt_labels" ("ProcessStep_id");
CREATE INDEX "ix_ProcessStep_alt_labels_alt_labels" ON "ProcessStep_alt_labels" (alt_labels);

CREATE TABLE "Control_governed_by" (
	"Control_id" TEXT,
	governed_by_id TEXT,
	PRIMARY KEY ("Control_id", governed_by_id),
	FOREIGN KEY("Control_id") REFERENCES "Control" (id),
	FOREIGN KEY(governed_by_id) REFERENCES "Standard" (id)
);
CREATE INDEX "ix_Control_governed_by_governed_by_id" ON "Control_governed_by" (governed_by_id);
CREATE INDEX "ix_Control_governed_by_Control_id" ON "Control_governed_by" ("Control_id");

CREATE TABLE "Control_alt_labels" (
	"Control_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Control_id", alt_labels),
	FOREIGN KEY("Control_id") REFERENCES "Control" (id)
);
CREATE INDEX "ix_Control_alt_labels_alt_labels" ON "Control_alt_labels" (alt_labels);
CREATE INDEX "ix_Control_alt_labels_Control_id" ON "Control_alt_labels" ("Control_id");

CREATE TABLE "Standard_process_areas" (
	"Standard_id" TEXT,
	process_areas VARCHAR(23),
	PRIMARY KEY ("Standard_id", process_areas),
	FOREIGN KEY("Standard_id") REFERENCES "Standard" (id)
);
CREATE INDEX "ix_Standard_process_areas_Standard_id" ON "Standard_process_areas" ("Standard_id");
CREATE INDEX "ix_Standard_process_areas_process_areas" ON "Standard_process_areas" (process_areas);

CREATE TABLE "Standard_alt_labels" (
	"Standard_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Standard_id", alt_labels),
	FOREIGN KEY("Standard_id") REFERENCES "Standard" (id)
);
CREATE INDEX "ix_Standard_alt_labels_alt_labels" ON "Standard_alt_labels" (alt_labels);
CREATE INDEX "ix_Standard_alt_labels_Standard_id" ON "Standard_alt_labels" ("Standard_id");

CREATE TABLE "Commodity_alt_labels" (
	"Commodity_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Commodity_id", alt_labels),
	FOREIGN KEY("Commodity_id") REFERENCES "Commodity" (id)
);
CREATE INDEX "ix_Commodity_alt_labels_Commodity_id" ON "Commodity_alt_labels" ("Commodity_id");
CREATE INDEX "ix_Commodity_alt_labels_alt_labels" ON "Commodity_alt_labels" (alt_labels);

CREATE TABLE "GLAccount_alt_labels" (
	"GLAccount_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("GLAccount_id", alt_labels),
	FOREIGN KEY("GLAccount_id") REFERENCES "GLAccount" (id)
);
CREATE INDEX "ix_GLAccount_alt_labels_alt_labels" ON "GLAccount_alt_labels" (alt_labels);
CREATE INDEX "ix_GLAccount_alt_labels_GLAccount_id" ON "GLAccount_alt_labels" ("GLAccount_id");

CREATE TABLE "DeliveryPoint" (
	pipeline TEXT,
	meter_number TEXT,
	location_type TEXT,
	region TEXT,
	commodity TEXT,
	operator TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(pipeline) REFERENCES "Pipeline" (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(operator) REFERENCES "Organization" (id)
);
CREATE INDEX "ix_DeliveryPoint_id" ON "DeliveryPoint" (id);

CREATE TABLE "PriceIndex" (
	publisher TEXT,
	index_frequency TEXT,
	location TEXT,
	commodity TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(publisher) REFERENCES "MarketInfrastructure" (id),
	FOREIGN KEY(location) REFERENCES "Location" (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id)
);
CREATE INDEX "ix_PriceIndex_id" ON "PriceIndex" (id);

CREATE TABLE "Book" (
	book_code TEXT,
	desk TEXT,
	legal_entity TEXT,
	commodity TEXT,
	book_type TEXT,
	region TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(desk) REFERENCES "TradingDesk" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id)
);
CREATE INDEX "ix_Book_id" ON "Book" (id);

CREATE TABLE "Imbalance" (
	pipeline TEXT,
	delivery_location TEXT,
	flow_month TEXT,
	imbalance_volume FLOAT,
	volume_unit VARCHAR(5),
	counterparty TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(pipeline) REFERENCES "Pipeline" (id),
	FOREIGN KEY(delivery_location) REFERENCES "Location" (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id)
);
CREATE INDEX "ix_Imbalance_id" ON "Imbalance" (id);

CREATE TABLE "JournalLine" (
	id INTEGER NOT NULL,
	gl_account TEXT NOT NULL,
	debit_credit VARCHAR(1) NOT NULL,
	amount FLOAT NOT NULL,
	cost_center TEXT,
	counterparty TEXT,
	trading_partner TEXT,
	"JournalEntry_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(gl_account) REFERENCES "GLAccount" (id),
	FOREIGN KEY(cost_center) REFERENCES "CostCenter" (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id),
	FOREIGN KEY(trading_partner) REFERENCES "LegalEntity" (id),
	FOREIGN KEY("JournalEntry_id") REFERENCES "JournalEntry" (id)
);
CREATE INDEX "ix_JournalLine_id" ON "JournalLine" (id);

CREATE TABLE "Worksheet" (
	workbook TEXT,
	sheet_name TEXT,
	sheet_state TEXT,
	sheet_role TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(workbook) REFERENCES "Workbook" (id)
);
CREATE INDEX "ix_Worksheet_id" ON "Worksheet" (id);

CREATE TABLE "SpecialPurposeEntity_alt_labels" (
	"SpecialPurposeEntity_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("SpecialPurposeEntity_id", alt_labels),
	FOREIGN KEY("SpecialPurposeEntity_id") REFERENCES "SpecialPurposeEntity" (id)
);
CREATE INDEX "ix_SpecialPurposeEntity_alt_labels_alt_labels" ON "SpecialPurposeEntity_alt_labels" (alt_labels);
CREATE INDEX "ix_SpecialPurposeEntity_alt_labels_SpecialPurposeEntity_id" ON "SpecialPurposeEntity_alt_labels" ("SpecialPurposeEntity_id");

CREATE TABLE "TradingDesk_alt_labels" (
	"TradingDesk_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("TradingDesk_id", alt_labels),
	FOREIGN KEY("TradingDesk_id") REFERENCES "TradingDesk" (id)
);
CREATE INDEX "ix_TradingDesk_alt_labels_alt_labels" ON "TradingDesk_alt_labels" (alt_labels);
CREATE INDEX "ix_TradingDesk_alt_labels_TradingDesk_id" ON "TradingDesk_alt_labels" ("TradingDesk_id");

CREATE TABLE "InformationSystem_process_areas" (
	"InformationSystem_id" TEXT,
	process_areas VARCHAR(23),
	PRIMARY KEY ("InformationSystem_id", process_areas),
	FOREIGN KEY("InformationSystem_id") REFERENCES "InformationSystem" (id)
);
CREATE INDEX "ix_InformationSystem_process_areas_process_areas" ON "InformationSystem_process_areas" (process_areas);
CREATE INDEX "ix_InformationSystem_process_areas_InformationSystem_id" ON "InformationSystem_process_areas" ("InformationSystem_id");

CREATE TABLE "InformationSystem_upstream_systems" (
	"InformationSystem_id" TEXT,
	upstream_systems_id TEXT,
	PRIMARY KEY ("InformationSystem_id", upstream_systems_id),
	FOREIGN KEY("InformationSystem_id") REFERENCES "InformationSystem" (id),
	FOREIGN KEY(upstream_systems_id) REFERENCES "InformationSystem" (id)
);
CREATE INDEX "ix_InformationSystem_upstream_systems_upstream_systems_id" ON "InformationSystem_upstream_systems" (upstream_systems_id);
CREATE INDEX "ix_InformationSystem_upstream_systems_InformationSystem_id" ON "InformationSystem_upstream_systems" ("InformationSystem_id");

CREATE TABLE "InformationSystem_downstream_systems" (
	"InformationSystem_id" TEXT,
	downstream_systems_id TEXT,
	PRIMARY KEY ("InformationSystem_id", downstream_systems_id),
	FOREIGN KEY("InformationSystem_id") REFERENCES "InformationSystem" (id),
	FOREIGN KEY(downstream_systems_id) REFERENCES "InformationSystem" (id)
);
CREATE INDEX "ix_InformationSystem_downstream_systems_downstream_systems_id" ON "InformationSystem_downstream_systems" (downstream_systems_id);
CREATE INDEX "ix_InformationSystem_downstream_systems_InformationSystem_id" ON "InformationSystem_downstream_systems" ("InformationSystem_id");

CREATE TABLE "InformationSystem_alt_labels" (
	"InformationSystem_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("InformationSystem_id", alt_labels),
	FOREIGN KEY("InformationSystem_id") REFERENCES "InformationSystem" (id)
);
CREATE INDEX "ix_InformationSystem_alt_labels_alt_labels" ON "InformationSystem_alt_labels" (alt_labels);
CREATE INDEX "ix_InformationSystem_alt_labels_InformationSystem_id" ON "InformationSystem_alt_labels" ("InformationSystem_id");

CREATE TABLE "ProcessStep_performed_in" (
	"ProcessStep_id" TEXT,
	performed_in_id TEXT,
	PRIMARY KEY ("ProcessStep_id", performed_in_id),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id),
	FOREIGN KEY(performed_in_id) REFERENCES "InformationSystem" (id)
);
CREATE INDEX "ix_ProcessStep_performed_in_ProcessStep_id" ON "ProcessStep_performed_in" ("ProcessStep_id");
CREATE INDEX "ix_ProcessStep_performed_in_performed_in_id" ON "ProcessStep_performed_in" (performed_in_id);

CREATE TABLE "Location_alt_labels" (
	"Location_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Location_id", alt_labels),
	FOREIGN KEY("Location_id") REFERENCES "Location" (id)
);
CREATE INDEX "ix_Location_alt_labels_alt_labels" ON "Location_alt_labels" (alt_labels);
CREATE INDEX "ix_Location_alt_labels_Location_id" ON "Location_alt_labels" ("Location_id");

CREATE TABLE "TradingHub_alt_labels" (
	"TradingHub_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("TradingHub_id", alt_labels),
	FOREIGN KEY("TradingHub_id") REFERENCES "TradingHub" (id)
);
CREATE INDEX "ix_TradingHub_alt_labels_alt_labels" ON "TradingHub_alt_labels" (alt_labels);
CREATE INDEX "ix_TradingHub_alt_labels_TradingHub_id" ON "TradingHub_alt_labels" ("TradingHub_id");

CREATE TABLE "Pipeline_alt_labels" (
	"Pipeline_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Pipeline_id", alt_labels),
	FOREIGN KEY("Pipeline_id") REFERENCES "Pipeline" (id)
);
CREATE INDEX "ix_Pipeline_alt_labels_alt_labels" ON "Pipeline_alt_labels" (alt_labels);
CREATE INDEX "ix_Pipeline_alt_labels_Pipeline_id" ON "Pipeline_alt_labels" ("Pipeline_id");

CREATE TABLE "PowerControlArea_alt_labels" (
	"PowerControlArea_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("PowerControlArea_id", alt_labels),
	FOREIGN KEY("PowerControlArea_id") REFERENCES "PowerControlArea" (id)
);
CREATE INDEX "ix_PowerControlArea_alt_labels_alt_labels" ON "PowerControlArea_alt_labels" (alt_labels);
CREATE INDEX "ix_PowerControlArea_alt_labels_PowerControlArea_id" ON "PowerControlArea_alt_labels" ("PowerControlArea_id");

CREATE TABLE "MasterAgreement_alt_labels" (
	"MasterAgreement_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("MasterAgreement_id", alt_labels),
	FOREIGN KEY("MasterAgreement_id") REFERENCES "MasterAgreement" (id)
);
CREATE INDEX "ix_MasterAgreement_alt_labels_alt_labels" ON "MasterAgreement_alt_labels" (alt_labels);
CREATE INDEX "ix_MasterAgreement_alt_labels_MasterAgreement_id" ON "MasterAgreement_alt_labels" ("MasterAgreement_id");

CREATE TABLE "Invoice_alt_labels" (
	"Invoice_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Invoice_id", alt_labels),
	FOREIGN KEY("Invoice_id") REFERENCES "Invoice" (id)
);
CREATE INDEX "ix_Invoice_alt_labels_alt_labels" ON "Invoice_alt_labels" (alt_labels);
CREATE INDEX "ix_Invoice_alt_labels_Invoice_id" ON "Invoice_alt_labels" ("Invoice_id");

CREATE TABLE "Payment_invoices" (
	"Payment_id" TEXT,
	invoices_id TEXT,
	PRIMARY KEY ("Payment_id", invoices_id),
	FOREIGN KEY("Payment_id") REFERENCES "Payment" (id),
	FOREIGN KEY(invoices_id) REFERENCES "Invoice" (id)
);
CREATE INDEX "ix_Payment_invoices_invoices_id" ON "Payment_invoices" (invoices_id);
CREATE INDEX "ix_Payment_invoices_Payment_id" ON "Payment_invoices" ("Payment_id");

CREATE TABLE "Payment_alt_labels" (
	"Payment_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Payment_id", alt_labels),
	FOREIGN KEY("Payment_id") REFERENCES "Payment" (id)
);
CREATE INDEX "ix_Payment_alt_labels_Payment_id" ON "Payment_alt_labels" ("Payment_id");
CREATE INDEX "ix_Payment_alt_labels_alt_labels" ON "Payment_alt_labels" (alt_labels);

CREATE TABLE "CostCenter_alt_labels" (
	"CostCenter_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("CostCenter_id", alt_labels),
	FOREIGN KEY("CostCenter_id") REFERENCES "CostCenter" (id)
);
CREATE INDEX "ix_CostCenter_alt_labels_alt_labels" ON "CostCenter_alt_labels" (alt_labels);
CREATE INDEX "ix_CostCenter_alt_labels_CostCenter_id" ON "CostCenter_alt_labels" ("CostCenter_id");

CREATE TABLE "JournalEntry_alt_labels" (
	"JournalEntry_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("JournalEntry_id", alt_labels),
	FOREIGN KEY("JournalEntry_id") REFERENCES "JournalEntry" (id)
);
CREATE INDEX "ix_JournalEntry_alt_labels_alt_labels" ON "JournalEntry_alt_labels" (alt_labels);
CREATE INDEX "ix_JournalEntry_alt_labels_JournalEntry_id" ON "JournalEntry_alt_labels" ("JournalEntry_id");

CREATE TABLE "Document_alt_labels" (
	"Document_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Document_id", alt_labels),
	FOREIGN KEY("Document_id") REFERENCES "Document" (id)
);
CREATE INDEX "ix_Document_alt_labels_Document_id" ON "Document_alt_labels" ("Document_id");
CREATE INDEX "ix_Document_alt_labels_alt_labels" ON "Document_alt_labels" (alt_labels);

CREATE TABLE "Workbook_mentions" (
	"Workbook_id" TEXT,
	mentions_id TEXT,
	PRIMARY KEY ("Workbook_id", mentions_id),
	FOREIGN KEY("Workbook_id") REFERENCES "Workbook" (id),
	FOREIGN KEY(mentions_id) REFERENCES "NamedThing" (id)
);
CREATE INDEX "ix_Workbook_mentions_mentions_id" ON "Workbook_mentions" (mentions_id);
CREATE INDEX "ix_Workbook_mentions_Workbook_id" ON "Workbook_mentions" ("Workbook_id");

CREATE TABLE "Workbook_derived_from" (
	"Workbook_id" TEXT,
	derived_from_id TEXT,
	PRIMARY KEY ("Workbook_id", derived_from_id),
	FOREIGN KEY("Workbook_id") REFERENCES "Workbook" (id),
	FOREIGN KEY(derived_from_id) REFERENCES "Workbook" (id)
);
CREATE INDEX "ix_Workbook_derived_from_derived_from_id" ON "Workbook_derived_from" (derived_from_id);
CREATE INDEX "ix_Workbook_derived_from_Workbook_id" ON "Workbook_derived_from" ("Workbook_id");

CREATE TABLE "Workbook_alt_labels" (
	"Workbook_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Workbook_id", alt_labels),
	FOREIGN KEY("Workbook_id") REFERENCES "Workbook" (id)
);
CREATE INDEX "ix_Workbook_alt_labels_alt_labels" ON "Workbook_alt_labels" (alt_labels);
CREATE INDEX "ix_Workbook_alt_labels_Workbook_id" ON "Workbook_alt_labels" ("Workbook_id");

CREATE TABLE "EmailMessage_recipients" (
	"EmailMessage_id" TEXT,
	recipients_id TEXT,
	PRIMARY KEY ("EmailMessage_id", recipients_id),
	FOREIGN KEY("EmailMessage_id") REFERENCES "EmailMessage" (id),
	FOREIGN KEY(recipients_id) REFERENCES "Person" (id)
);
CREATE INDEX "ix_EmailMessage_recipients_EmailMessage_id" ON "EmailMessage_recipients" ("EmailMessage_id");
CREATE INDEX "ix_EmailMessage_recipients_recipients_id" ON "EmailMessage_recipients" (recipients_id);

CREATE TABLE "EmailMessage_attachments" (
	"EmailMessage_id" TEXT,
	attachments_id TEXT,
	PRIMARY KEY ("EmailMessage_id", attachments_id),
	FOREIGN KEY("EmailMessage_id") REFERENCES "EmailMessage" (id),
	FOREIGN KEY(attachments_id) REFERENCES "Workbook" (id)
);
CREATE INDEX "ix_EmailMessage_attachments_EmailMessage_id" ON "EmailMessage_attachments" ("EmailMessage_id");
CREATE INDEX "ix_EmailMessage_attachments_attachments_id" ON "EmailMessage_attachments" (attachments_id);

CREATE TABLE "EmailMessage_alt_labels" (
	"EmailMessage_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("EmailMessage_id", alt_labels),
	FOREIGN KEY("EmailMessage_id") REFERENCES "EmailMessage" (id)
);
CREATE INDEX "ix_EmailMessage_alt_labels_alt_labels" ON "EmailMessage_alt_labels" (alt_labels);
CREATE INDEX "ix_EmailMessage_alt_labels_EmailMessage_id" ON "EmailMessage_alt_labels" ("EmailMessage_id");

CREATE TABLE "PriceCurve" (
	curve_code TEXT,
	curve_type VARCHAR(13),
	commodity TEXT,
	location TEXT,
	"index" TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(location) REFERENCES "Location" (id),
	FOREIGN KEY("index") REFERENCES "PriceIndex" (id)
);
CREATE INDEX "ix_PriceCurve_id" ON "PriceCurve" (id);

CREATE TABLE "Trade" (
	deal_number TEXT,
	source_system TEXT,
	eol_transaction_id TEXT,
	trade_date DATE,
	legal_entity TEXT,
	counterparty TEXT,
	book TEXT,
	trader TEXT,
	commodity TEXT,
	instrument_type VARCHAR(16),
	buy_sell VARCHAR(4),
	volume FLOAT,
	volume_unit VARCHAR(5),
	volume_frequency TEXT,
	price FLOAT,
	price_type VARCHAR(10),
	price_index TEXT,
	premium_or_adder FLOAT,
	delivery_location TEXT,
	delivery_start DATE,
	delivery_end DATE,
	deal_status TEXT,
	master_agreement TEXT,
	confirmation_status TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(source_system) REFERENCES "InformationSystem" (id),
	FOREIGN KEY(legal_entity) REFERENCES "LegalEntity" (id),
	FOREIGN KEY(counterparty) REFERENCES "Counterparty" (id),
	FOREIGN KEY(book) REFERENCES "Book" (id),
	FOREIGN KEY(trader) REFERENCES "Person" (id),
	FOREIGN KEY(commodity) REFERENCES "Commodity" (id),
	FOREIGN KEY(price_index) REFERENCES "PriceIndex" (id),
	FOREIGN KEY(delivery_location) REFERENCES "Location" (id),
	FOREIGN KEY(master_agreement) REFERENCES "MasterAgreement" (id)
);
CREATE INDEX "ix_Trade_id" ON "Trade" (id);

CREATE TABLE "Valuation" (
	book TEXT,
	as_of_date DATE,
	mtm_value FLOAT,
	daily_pnl FLOAT,
	new_deal_pnl FLOAT,
	curve_shift_pnl FLOAT,
	var_95 FLOAT,
	currency TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(book) REFERENCES "Book" (id)
);
CREATE INDEX "ix_Valuation_id" ON "Valuation" (id);

CREATE TABLE "TableRegion" (
	worksheet TEXT,
	cell_range TEXT,
	header_range TEXT,
	table_role TEXT,
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(worksheet) REFERENCES "Worksheet" (id)
);
CREATE INDEX "ix_TableRegion_id" ON "TableRegion" (id);

CREATE TABLE "DeliveryPoint_alt_labels" (
	"DeliveryPoint_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("DeliveryPoint_id", alt_labels),
	FOREIGN KEY("DeliveryPoint_id") REFERENCES "DeliveryPoint" (id)
);
CREATE INDEX "ix_DeliveryPoint_alt_labels_alt_labels" ON "DeliveryPoint_alt_labels" (alt_labels);
CREATE INDEX "ix_DeliveryPoint_alt_labels_DeliveryPoint_id" ON "DeliveryPoint_alt_labels" ("DeliveryPoint_id");

CREATE TABLE "PriceIndex_alt_labels" (
	"PriceIndex_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("PriceIndex_id", alt_labels),
	FOREIGN KEY("PriceIndex_id") REFERENCES "PriceIndex" (id)
);
CREATE INDEX "ix_PriceIndex_alt_labels_PriceIndex_id" ON "PriceIndex_alt_labels" ("PriceIndex_id");
CREATE INDEX "ix_PriceIndex_alt_labels_alt_labels" ON "PriceIndex_alt_labels" (alt_labels);

CREATE TABLE "Book_alt_labels" (
	"Book_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Book_id", alt_labels),
	FOREIGN KEY("Book_id") REFERENCES "Book" (id)
);
CREATE INDEX "ix_Book_alt_labels_Book_id" ON "Book_alt_labels" ("Book_id");
CREATE INDEX "ix_Book_alt_labels_alt_labels" ON "Book_alt_labels" (alt_labels);

CREATE TABLE "Imbalance_alt_labels" (
	"Imbalance_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Imbalance_id", alt_labels),
	FOREIGN KEY("Imbalance_id") REFERENCES "Imbalance" (id)
);
CREATE INDEX "ix_Imbalance_alt_labels_Imbalance_id" ON "Imbalance_alt_labels" ("Imbalance_id");
CREATE INDEX "ix_Imbalance_alt_labels_alt_labels" ON "Imbalance_alt_labels" (alt_labels);

CREATE TABLE "Workbook_sheets" (
	"Workbook_id" TEXT,
	sheets_id TEXT,
	PRIMARY KEY ("Workbook_id", sheets_id),
	FOREIGN KEY("Workbook_id") REFERENCES "Workbook" (id),
	FOREIGN KEY(sheets_id) REFERENCES "Worksheet" (id)
);
CREATE INDEX "ix_Workbook_sheets_sheets_id" ON "Workbook_sheets" (sheets_id);
CREATE INDEX "ix_Workbook_sheets_Workbook_id" ON "Workbook_sheets" ("Workbook_id");

CREATE TABLE "Worksheet_alt_labels" (
	"Worksheet_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Worksheet_id", alt_labels),
	FOREIGN KEY("Worksheet_id") REFERENCES "Worksheet" (id)
);
CREATE INDEX "ix_Worksheet_alt_labels_Worksheet_id" ON "Worksheet_alt_labels" ("Worksheet_id");
CREATE INDEX "ix_Worksheet_alt_labels_alt_labels" ON "Worksheet_alt_labels" (alt_labels);

CREATE TABLE "CurvePoint" (
	id INTEGER NOT NULL,
	curve TEXT NOT NULL,
	valuation_date DATE NOT NULL,
	delivery_start DATE NOT NULL,
	value FLOAT NOT NULL,
	unit TEXT,
	is_synthetic BOOLEAN,
	PRIMARY KEY (id),
	FOREIGN KEY(curve) REFERENCES "PriceCurve" (id)
);
CREATE INDEX "ix_CurvePoint_id" ON "CurvePoint" (id);

CREATE TABLE "Position" (
	book TEXT,
	curve TEXT,
	as_of_date DATE,
	delivery_start DATE,
	quantity FLOAT,
	volume_unit VARCHAR(5),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(book) REFERENCES "Book" (id),
	FOREIGN KEY(curve) REFERENCES "PriceCurve" (id)
);
CREATE INDEX "ix_Position_id" ON "Position" (id);

CREATE TABLE "Nomination" (
	trade TEXT,
	pipeline TEXT,
	delivery_location TEXT,
	flow_date DATE,
	nominated_volume FLOAT,
	scheduled_volume FLOAT,
	actual_volume FLOAT,
	volume_unit VARCHAR(5),
	id TEXT NOT NULL,
	label TEXT,
	description TEXT,
	is_synthetic BOOLEAN,
	valid_from DATE,
	valid_to DATE,
	PRIMARY KEY (id),
	FOREIGN KEY(trade) REFERENCES "Trade" (id),
	FOREIGN KEY(pipeline) REFERENCES "Pipeline" (id),
	FOREIGN KEY(delivery_location) REFERENCES "Location" (id)
);
CREATE INDEX "ix_Nomination_id" ON "Nomination" (id);

CREATE TABLE "PriceCurve_alt_labels" (
	"PriceCurve_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("PriceCurve_id", alt_labels),
	FOREIGN KEY("PriceCurve_id") REFERENCES "PriceCurve" (id)
);
CREATE INDEX "ix_PriceCurve_alt_labels_alt_labels" ON "PriceCurve_alt_labels" (alt_labels);
CREATE INDEX "ix_PriceCurve_alt_labels_PriceCurve_id" ON "PriceCurve_alt_labels" ("PriceCurve_id");

CREATE TABLE "Trade_alt_labels" (
	"Trade_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Trade_id", alt_labels),
	FOREIGN KEY("Trade_id") REFERENCES "Trade" (id)
);
CREATE INDEX "ix_Trade_alt_labels_alt_labels" ON "Trade_alt_labels" (alt_labels);
CREATE INDEX "ix_Trade_alt_labels_Trade_id" ON "Trade_alt_labels" ("Trade_id");

CREATE TABLE "Valuation_alt_labels" (
	"Valuation_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Valuation_id", alt_labels),
	FOREIGN KEY("Valuation_id") REFERENCES "Valuation" (id)
);
CREATE INDEX "ix_Valuation_alt_labels_alt_labels" ON "Valuation_alt_labels" (alt_labels);
CREATE INDEX "ix_Valuation_alt_labels_Valuation_id" ON "Valuation_alt_labels" ("Valuation_id");

CREATE TABLE "Invoice_trades" (
	"Invoice_id" TEXT,
	trades_id TEXT,
	PRIMARY KEY ("Invoice_id", trades_id),
	FOREIGN KEY("Invoice_id") REFERENCES "Invoice" (id),
	FOREIGN KEY(trades_id) REFERENCES "Trade" (id)
);
CREATE INDEX "ix_Invoice_trades_trades_id" ON "Invoice_trades" (trades_id);
CREATE INDEX "ix_Invoice_trades_Invoice_id" ON "Invoice_trades" ("Invoice_id");

CREATE TABLE "TableRegion_alt_labels" (
	"TableRegion_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("TableRegion_id", alt_labels),
	FOREIGN KEY("TableRegion_id") REFERENCES "TableRegion" (id)
);
CREATE INDEX "ix_TableRegion_alt_labels_alt_labels" ON "TableRegion_alt_labels" (alt_labels);
CREATE INDEX "ix_TableRegion_alt_labels_TableRegion_id" ON "TableRegion_alt_labels" ("TableRegion_id");

CREATE TABLE "Evidence" (
	id INTEGER NOT NULL,
	source_kind VARCHAR(19) NOT NULL,
	source_id TEXT,
	locator TEXT,
	quote TEXT,
	confidence FLOAT,
	"NamedThing_id" TEXT,
	"Agent_id" TEXT,
	"Person_id" TEXT,
	"Organization_id" TEXT,
	"LegalEntity_id" TEXT,
	"SpecialPurposeEntity_id" TEXT,
	"BusinessUnit_id" TEXT,
	"TradingDesk_id" TEXT,
	"Counterparty_id" TEXT,
	"MarketInfrastructure_id" TEXT,
	"InformationSystem_id" TEXT,
	"ProcessStep_id" TEXT,
	"Control_id" TEXT,
	"Standard_id" TEXT,
	"Commodity_id" TEXT,
	"Location_id" TEXT,
	"TradingHub_id" TEXT,
	"DeliveryPoint_id" TEXT,
	"Pipeline_id" TEXT,
	"PowerControlArea_id" TEXT,
	"PriceIndex_id" TEXT,
	"PriceCurve_id" TEXT,
	"MasterAgreement_id" TEXT,
	"Trade_id" TEXT,
	"Book_id" TEXT,
	"Position_id" TEXT,
	"Valuation_id" TEXT,
	"Nomination_id" TEXT,
	"Imbalance_id" TEXT,
	"Invoice_id" TEXT,
	"Payment_id" TEXT,
	"GLAccount_id" TEXT,
	"CostCenter_id" TEXT,
	"JournalEntry_id" TEXT,
	"Document_id" TEXT,
	"Workbook_id" TEXT,
	"Worksheet_id" TEXT,
	"TableRegion_id" TEXT,
	"EmailMessage_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("NamedThing_id") REFERENCES "NamedThing" (id),
	FOREIGN KEY("Agent_id") REFERENCES "Agent" (id),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id),
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id),
	FOREIGN KEY("LegalEntity_id") REFERENCES "LegalEntity" (id),
	FOREIGN KEY("SpecialPurposeEntity_id") REFERENCES "SpecialPurposeEntity" (id),
	FOREIGN KEY("BusinessUnit_id") REFERENCES "BusinessUnit" (id),
	FOREIGN KEY("TradingDesk_id") REFERENCES "TradingDesk" (id),
	FOREIGN KEY("Counterparty_id") REFERENCES "Counterparty" (id),
	FOREIGN KEY("MarketInfrastructure_id") REFERENCES "MarketInfrastructure" (id),
	FOREIGN KEY("InformationSystem_id") REFERENCES "InformationSystem" (id),
	FOREIGN KEY("ProcessStep_id") REFERENCES "ProcessStep" (id),
	FOREIGN KEY("Control_id") REFERENCES "Control" (id),
	FOREIGN KEY("Standard_id") REFERENCES "Standard" (id),
	FOREIGN KEY("Commodity_id") REFERENCES "Commodity" (id),
	FOREIGN KEY("Location_id") REFERENCES "Location" (id),
	FOREIGN KEY("TradingHub_id") REFERENCES "TradingHub" (id),
	FOREIGN KEY("DeliveryPoint_id") REFERENCES "DeliveryPoint" (id),
	FOREIGN KEY("Pipeline_id") REFERENCES "Pipeline" (id),
	FOREIGN KEY("PowerControlArea_id") REFERENCES "PowerControlArea" (id),
	FOREIGN KEY("PriceIndex_id") REFERENCES "PriceIndex" (id),
	FOREIGN KEY("PriceCurve_id") REFERENCES "PriceCurve" (id),
	FOREIGN KEY("MasterAgreement_id") REFERENCES "MasterAgreement" (id),
	FOREIGN KEY("Trade_id") REFERENCES "Trade" (id),
	FOREIGN KEY("Book_id") REFERENCES "Book" (id),
	FOREIGN KEY("Position_id") REFERENCES "Position" (id),
	FOREIGN KEY("Valuation_id") REFERENCES "Valuation" (id),
	FOREIGN KEY("Nomination_id") REFERENCES "Nomination" (id),
	FOREIGN KEY("Imbalance_id") REFERENCES "Imbalance" (id),
	FOREIGN KEY("Invoice_id") REFERENCES "Invoice" (id),
	FOREIGN KEY("Payment_id") REFERENCES "Payment" (id),
	FOREIGN KEY("GLAccount_id") REFERENCES "GLAccount" (id),
	FOREIGN KEY("CostCenter_id") REFERENCES "CostCenter" (id),
	FOREIGN KEY("JournalEntry_id") REFERENCES "JournalEntry" (id),
	FOREIGN KEY("Document_id") REFERENCES "Document" (id),
	FOREIGN KEY("Workbook_id") REFERENCES "Workbook" (id),
	FOREIGN KEY("Worksheet_id") REFERENCES "Worksheet" (id),
	FOREIGN KEY("TableRegion_id") REFERENCES "TableRegion" (id),
	FOREIGN KEY("EmailMessage_id") REFERENCES "EmailMessage" (id)
);
CREATE INDEX "ix_Evidence_id" ON "Evidence" (id);

CREATE TABLE "Position_alt_labels" (
	"Position_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Position_id", alt_labels),
	FOREIGN KEY("Position_id") REFERENCES "Position" (id)
);
CREATE INDEX "ix_Position_alt_labels_alt_labels" ON "Position_alt_labels" (alt_labels);
CREATE INDEX "ix_Position_alt_labels_Position_id" ON "Position_alt_labels" ("Position_id");

CREATE TABLE "Nomination_alt_labels" (
	"Nomination_id" TEXT,
	alt_labels TEXT,
	PRIMARY KEY ("Nomination_id", alt_labels),
	FOREIGN KEY("Nomination_id") REFERENCES "Nomination" (id)
);
CREATE INDEX "ix_Nomination_alt_labels_alt_labels" ON "Nomination_alt_labels" (alt_labels);
CREATE INDEX "ix_Nomination_alt_labels_Nomination_id" ON "Nomination_alt_labels" ("Nomination_id");

