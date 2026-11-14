# Auto generated from enron_finance.yaml by pythongen.py version: 0.0.1
# Schema: enron_finance
#
# id: https://huxwaitt.github.io/enron-e2e/ontology/enron_finance
# description: Conceptual model for Enron Corp's trading, logistics, settlement and accounting estate circa 1999-2001, as evidenced by the Enron spreadsheet and email corpora. Every class maps to external standards (FIBO, OMG Commons, W3C ORG/PROV, schema.org) so lake records can be joined to other finance knowledge graphs. Instance IRIs are minted under the `enroni:` namespace and never reused (see ontology/ID_POLICY.md).
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate, XSDDateTime

metamodel_version = "1.12.0"
version = "0.1.0"

# Namespaces
CMNS_ORG = CurieNamespace('cmns-org', 'https://www.omg.org/spec/Commons/Organizations/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
ENRON = CurieNamespace('enron', 'https://huxwaitt.github.io/enron-e2e/ontology/')
ENRONI = CurieNamespace('enroni', 'https://huxwaitt.github.io/enron-e2e/id/')
FIBO_BE_LE_CB = CurieNamespace('fibo-be-le-cb', 'https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/CorporateBodies/')
FIBO_BE_LE_LP = CurieNamespace('fibo-be-le-lp', 'https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/LegalPersons/')
FIBO_DER_DRC_COMM = CurieNamespace('fibo-der-drc-comm', 'https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/CommoditiesContracts/')
FIBO_DER_DRC_FF = CurieNamespace('fibo-der-drc-ff', 'https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/FuturesAndForwards/')
FIBO_DER_DRC_MA = CurieNamespace('fibo-der-drc-ma', 'https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/DerivativesMasterAgreements/')
FIBO_DER_DRC_OPT = CurieNamespace('fibo-der-drc-opt', 'https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/Options/')
FIBO_DER_DRC_SWP = CurieNamespace('fibo-der-drc-swp', 'https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/Swaps/')
FIBO_FBC_FCT_MKT = CurieNamespace('fibo-fbc-fct-mkt', 'https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/Markets/')
FIBO_FBC_FI_FI = CurieNamespace('fibo-fbc-fi-fi', 'https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/')
FIBO_FBC_FI_IP = CurieNamespace('fibo-fbc-fi-ip', 'https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/InstrumentPricing/')
FIBO_FBC_FI_STL = CurieNamespace('fibo-fbc-fi-stl', 'https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/Settlement/')
FIBO_FBC_PAS_CAA = CurieNamespace('fibo-fbc-pas-caa', 'https://spec.edmcouncil.org/fibo/ontology/FBC/ProductsAndServices/ClientsAndAccounts/')
FIBO_FND_AGR_CTR = CurieNamespace('fibo-fnd-agr-ctr', 'https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/')
FIBO_FND_PAS_PSCH = CurieNamespace('fibo-fnd-pas-psch', 'https://spec.edmcouncil.org/fibo/ontology/FND/ProductsAndServices/PaymentsAndSchedules/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
ORG = CurieNamespace('org', 'http://www.w3.org/ns/org#')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = ENRON


# Types

# Class references
class NamedThingId(URIorCURIE):
    pass


class AgentId(NamedThingId):
    pass


class PersonId(AgentId):
    pass


class OrganizationId(AgentId):
    pass


class LegalEntityId(OrganizationId):
    pass


class SpecialPurposeEntityId(LegalEntityId):
    pass


class BusinessUnitId(OrganizationId):
    pass


class TradingDeskId(BusinessUnitId):
    pass


class CounterpartyId(OrganizationId):
    pass


class MarketInfrastructureId(OrganizationId):
    pass


class InformationSystemId(NamedThingId):
    pass


class ProcessStepId(NamedThingId):
    pass


class ControlId(NamedThingId):
    pass


class StandardId(NamedThingId):
    pass


class CommodityId(NamedThingId):
    pass


class LocationId(NamedThingId):
    pass


class TradingHubId(LocationId):
    pass


class DeliveryPointId(LocationId):
    pass


class PipelineId(LocationId):
    pass


class PowerControlAreaId(LocationId):
    pass


class PriceIndexId(NamedThingId):
    pass


class PriceCurveId(NamedThingId):
    pass


class MasterAgreementId(NamedThingId):
    pass


class TradeId(NamedThingId):
    pass


class BookId(NamedThingId):
    pass


class PositionId(NamedThingId):
    pass


class ValuationId(NamedThingId):
    pass


class NominationId(NamedThingId):
    pass


class ImbalanceId(NamedThingId):
    pass


class InvoiceId(NamedThingId):
    pass


class PaymentId(NamedThingId):
    pass


class GLAccountId(NamedThingId):
    pass


class CostCenterId(NamedThingId):
    pass


class JournalEntryId(NamedThingId):
    pass


class DocumentId(NamedThingId):
    pass


class WorkbookId(DocumentId):
    pass


class WorksheetId(NamedThingId):
    pass


class TableRegionId(NamedThingId):
    pass


class EmailMessageId(DocumentId):
    pass


@dataclass(repr=False)
class NamedThing(YAMLRoot):
    """
    Anything with a persistent identifier in the estate.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["NamedThing"]
    class_class_curie: ClassVar[str] = "enron:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = ENRON.NamedThing

    id: Union[str, NamedThingId] = None
    label: Optional[str] = None
    alt_labels: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[str] = None
    evidence: Optional[Union[Union[dict, "Evidence"], list[Union[dict, "Evidence"]]]] = empty_list()
    is_synthetic: Optional[Union[bool, Bool]] = None
    valid_from: Optional[Union[str, XSDDate]] = None
    valid_to: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if not isinstance(self.alt_labels, list):
            self.alt_labels = [self.alt_labels] if self.alt_labels is not None else []
        self.alt_labels = [v if isinstance(v, str) else str(v) for v in self.alt_labels]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="evidence", slot_type=Evidence, key_name="source_kind", keyed=False)

        if self.is_synthetic is not None and not isinstance(self.is_synthetic, Bool):
            self.is_synthetic = Bool(self.is_synthetic)

        if self.valid_from is not None and not isinstance(self.valid_from, XSDDate):
            self.valid_from = XSDDate(self.valid_from)

        if self.valid_to is not None and not isinstance(self.valid_to, XSDDate):
            self.valid_to = XSDDate(self.valid_to)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Evidence(YAMLRoot):
    """
    Provenance pointer from an assertion back to the corpus or to a synthetic generator. Lets every fact in the lake
    be traced to a cell, an email or a rule.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "Evidence"
    class_model_uri: ClassVar[URIRef] = ENRON.Evidence

    source_kind: Union[str, "EvidenceSourceKind"] = None
    source_id: Optional[str] = None
    locator: Optional[str] = None
    quote: Optional[str] = None
    confidence: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.source_kind):
            self.MissingRequiredField("source_kind")
        if not isinstance(self.source_kind, EvidenceSourceKind):
            self.source_kind = EvidenceSourceKind(self.source_kind)

        if self.source_id is not None and not isinstance(self.source_id, str):
            self.source_id = str(self.source_id)

        if self.locator is not None and not isinstance(self.locator, str):
            self.locator = str(self.locator)

        if self.quote is not None and not isinstance(self.quote, str):
            self.quote = str(self.quote)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Agent(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = ENRON.Agent

    id: Union[str, AgentId] = None

@dataclass(repr=False)
class Person(Agent):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Person"]
    class_class_curie: ClassVar[str] = "foaf:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = ENRON.Person

    id: Union[str, PersonId] = None
    email_addresses: Optional[Union[str, list[str]]] = empty_list()
    job_title: Optional[str] = None
    member_of: Optional[Union[Union[str, OrganizationId], list[Union[str, OrganizationId]]]] = empty_list()
    is_custodian: Optional[Union[bool, Bool]] = None
    maildir_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if not isinstance(self.email_addresses, list):
            self.email_addresses = [self.email_addresses] if self.email_addresses is not None else []
        self.email_addresses = [v if isinstance(v, str) else str(v) for v in self.email_addresses]

        if self.job_title is not None and not isinstance(self.job_title, str):
            self.job_title = str(self.job_title)

        if not isinstance(self.member_of, list):
            self.member_of = [self.member_of] if self.member_of is not None else []
        self.member_of = [v if isinstance(v, OrganizationId) else OrganizationId(v) for v in self.member_of]

        if self.is_custodian is not None and not isinstance(self.is_custodian, Bool):
            self.is_custodian = Bool(self.is_custodian)

        if self.maildir_name is not None and not isinstance(self.maildir_name, str):
            self.maildir_name = str(self.maildir_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Organization(Agent):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ORG["Organization"]
    class_class_curie: ClassVar[str] = "org:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = ENRON.Organization

    id: Union[str, OrganizationId] = None

@dataclass(repr=False)
class LegalEntity(Organization):
    """
    A legally registered Enron affiliate (e.g. Enron North America Corp.).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMNS_ORG["LegalEntity"]
    class_class_curie: ClassVar[str] = "cmns-org:LegalEntity"
    class_name: ClassVar[str] = "LegalEntity"
    class_model_uri: ClassVar[URIRef] = ENRON.LegalEntity

    id: Union[str, LegalEntityId] = None
    parent_entity: Optional[Union[str, LegalEntityId]] = None
    jurisdiction: Optional[str] = None
    segment: Optional[Union[str, BusinessUnitId]] = None
    sec_registrant: Optional[Union[bool, Bool]] = None
    ferc_regulated: Optional[Union[bool, Bool]] = None
    special_purpose: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LegalEntityId):
            self.id = LegalEntityId(self.id)

        if self.parent_entity is not None and not isinstance(self.parent_entity, LegalEntityId):
            self.parent_entity = LegalEntityId(self.parent_entity)

        if self.jurisdiction is not None and not isinstance(self.jurisdiction, str):
            self.jurisdiction = str(self.jurisdiction)

        if self.segment is not None and not isinstance(self.segment, BusinessUnitId):
            self.segment = BusinessUnitId(self.segment)

        if self.sec_registrant is not None and not isinstance(self.sec_registrant, Bool):
            self.sec_registrant = Bool(self.sec_registrant)

        if self.ferc_regulated is not None and not isinstance(self.ferc_regulated, Bool):
            self.ferc_regulated = Bool(self.ferc_regulated)

        if self.special_purpose is not None and not isinstance(self.special_purpose, Bool):
            self.special_purpose = Bool(self.special_purpose)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SpecialPurposeEntity(LegalEntity):
    """
    Off-balance-sheet or structured vehicle (e.g. LJM2, Chewco, Whitewing, Raptor vehicles). Kept distinct because
    consolidation treatment is the point of interest.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["SpecialPurposeEntity"]
    class_class_curie: ClassVar[str] = "enron:SpecialPurposeEntity"
    class_name: ClassVar[str] = "SpecialPurposeEntity"
    class_model_uri: ClassVar[URIRef] = ENRON.SpecialPurposeEntity

    id: Union[str, SpecialPurposeEntityId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SpecialPurposeEntityId):
            self.id = SpecialPurposeEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BusinessUnit(Organization):
    """
    Management unit (segment, business unit, department) that is not itself a legal entity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ORG["OrganizationalUnit"]
    class_class_curie: ClassVar[str] = "org:OrganizationalUnit"
    class_name: ClassVar[str] = "BusinessUnit"
    class_model_uri: ClassVar[URIRef] = ENRON.BusinessUnit

    id: Union[str, BusinessUnitId] = None
    parent_unit: Optional[Union[str, BusinessUnitId]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    unit_type: Optional[Union[str, "UnitType"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BusinessUnitId):
            self.id = BusinessUnitId(self.id)

        if self.parent_unit is not None and not isinstance(self.parent_unit, BusinessUnitId):
            self.parent_unit = BusinessUnitId(self.parent_unit)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.unit_type is not None and not isinstance(self.unit_type, UnitType):
            self.unit_type = UnitType(self.unit_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TradingDesk(BusinessUnit):
    """
    Commercial desk owning books and traders (e.g. "West Power", "Texas Gas", "NW desk").
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["TradingDesk"]
    class_class_curie: ClassVar[str] = "enron:TradingDesk"
    class_name: ClassVar[str] = "TradingDesk"
    class_model_uri: ClassVar[URIRef] = ENRON.TradingDesk

    id: Union[str, TradingDeskId] = None
    commodity: Optional[Union[str, CommodityId]] = None
    region: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TradingDeskId):
            self.id = TradingDeskId(self.id)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        if self.region is not None and not isinstance(self.region, str):
            self.region = str(self.region)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Counterparty(Organization):
    """
    External trading counterparty, as mastered in Global Counterparty (GCP).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIBO_FND_AGR_CTR["Counterparty"]
    class_class_curie: ClassVar[str] = "fibo-fnd-agr-ctr:Counterparty"
    class_name: ClassVar[str] = "Counterparty"
    class_model_uri: ClassVar[URIRef] = ENRON.Counterparty

    id: Union[str, CounterpartyId] = None
    gcp_cp_id: Optional[str] = None
    short_name: Optional[str] = None
    credit_rating: Optional[str] = None
    counterparty_type: Optional[str] = None
    parent_counterparty: Optional[Union[str, CounterpartyId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CounterpartyId):
            self.id = CounterpartyId(self.id)

        if self.gcp_cp_id is not None and not isinstance(self.gcp_cp_id, str):
            self.gcp_cp_id = str(self.gcp_cp_id)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.credit_rating is not None and not isinstance(self.credit_rating, str):
            self.credit_rating = str(self.credit_rating)

        if self.counterparty_type is not None and not isinstance(self.counterparty_type, str):
            self.counterparty_type = str(self.counterparty_type)

        if self.parent_counterparty is not None and not isinstance(self.parent_counterparty, CounterpartyId):
            self.parent_counterparty = CounterpartyId(self.parent_counterparty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MarketInfrastructure(Organization):
    """
    Exchange, ISO/RTO, pipeline operator or price publisher.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["MarketInfrastructure"]
    class_class_curie: ClassVar[str] = "enron:MarketInfrastructure"
    class_name: ClassVar[str] = "MarketInfrastructure"
    class_model_uri: ClassVar[URIRef] = ENRON.MarketInfrastructure

    id: Union[str, MarketInfrastructureId] = None
    infrastructure_type: Optional[Union[str, "InfrastructureType"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MarketInfrastructureId):
            self.id = MarketInfrastructureId(self.id)

        if self.infrastructure_type is not None and not isinstance(self.infrastructure_type, InfrastructureType):
            self.infrastructure_type = InfrastructureType(self.infrastructure_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class InformationSystem(NamedThing):
    """
    An application in the trade-to-ledger chain (Sitara, EnPower, ERMS, Unify, SAP ...).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["SoftwareApplication"]
    class_class_curie: ClassVar[str] = "schema:SoftwareApplication"
    class_name: ClassVar[str] = "InformationSystem"
    class_model_uri: ClassVar[URIRef] = ENRON.InformationSystem

    id: Union[str, InformationSystemId] = None
    system_code: Optional[str] = None
    platform: Optional[str] = None
    process_areas: Optional[Union[Union[str, "ProcessArea"], list[Union[str, "ProcessArea"]]]] = empty_list()
    owning_unit: Optional[Union[str, BusinessUnitId]] = None
    upstream_systems: Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]] = empty_list()
    downstream_systems: Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InformationSystemId):
            self.id = InformationSystemId(self.id)

        if self.system_code is not None and not isinstance(self.system_code, str):
            self.system_code = str(self.system_code)

        if self.platform is not None and not isinstance(self.platform, str):
            self.platform = str(self.platform)

        if not isinstance(self.process_areas, list):
            self.process_areas = [self.process_areas] if self.process_areas is not None else []
        self.process_areas = [v if isinstance(v, ProcessArea) else ProcessArea(v) for v in self.process_areas]

        if self.owning_unit is not None and not isinstance(self.owning_unit, BusinessUnitId):
            self.owning_unit = BusinessUnitId(self.owning_unit)

        if not isinstance(self.upstream_systems, list):
            self.upstream_systems = [self.upstream_systems] if self.upstream_systems is not None else []
        self.upstream_systems = [v if isinstance(v, InformationSystemId) else InformationSystemId(v) for v in self.upstream_systems]

        if not isinstance(self.downstream_systems, list):
            self.downstream_systems = [self.downstream_systems] if self.downstream_systems is not None else []
        self.downstream_systems = [v if isinstance(v, InformationSystemId) else InformationSystemId(v) for v in self.downstream_systems]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProcessStep(NamedThing):
    """
    A step in a front-to-back process (e.g. "Actualize volumes", "Run DPR").
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Plan"]
    class_class_curie: ClassVar[str] = "prov:Plan"
    class_name: ClassVar[str] = "ProcessStep"
    class_model_uri: ClassVar[URIRef] = ENRON.ProcessStep

    id: Union[str, ProcessStepId] = None
    process_area: Optional[Union[str, "ProcessArea"]] = None
    performed_in: Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]] = empty_list()
    inputs: Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]] = empty_list()
    outputs: Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]] = empty_list()
    governed_by: Optional[Union[Union[str, StandardId], list[Union[str, StandardId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessStepId):
            self.id = ProcessStepId(self.id)

        if self.process_area is not None and not isinstance(self.process_area, ProcessArea):
            self.process_area = ProcessArea(self.process_area)

        if not isinstance(self.performed_in, list):
            self.performed_in = [self.performed_in] if self.performed_in is not None else []
        self.performed_in = [v if isinstance(v, InformationSystemId) else InformationSystemId(v) for v in self.performed_in]

        if not isinstance(self.inputs, list):
            self.inputs = [self.inputs] if self.inputs is not None else []
        self.inputs = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.inputs]

        if not isinstance(self.outputs, list):
            self.outputs = [self.outputs] if self.outputs is not None else []
        self.outputs = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.outputs]

        if not isinstance(self.governed_by, list):
            self.governed_by = [self.governed_by] if self.governed_by is not None else []
        self.governed_by = [v if isinstance(v, StandardId) else StandardId(v) for v in self.governed_by]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Control(NamedThing):
    """
    A check that existed (or should have) at the time, e.g. daily P&L sign-off, deal-entry verification, RAC credit
    approval. Pre-SOX; mapped to modern control objectives.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Control"]
    class_class_curie: ClassVar[str] = "enron:Control"
    class_name: ClassVar[str] = "Control"
    class_model_uri: ClassVar[URIRef] = ENRON.Control

    id: Union[str, ControlId] = None
    process_area: Optional[Union[str, "ProcessArea"]] = None
    control_type: Optional[str] = None
    governed_by: Optional[Union[Union[str, StandardId], list[Union[str, StandardId]]]] = empty_list()
    modern_equivalent: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ControlId):
            self.id = ControlId(self.id)

        if self.process_area is not None and not isinstance(self.process_area, ProcessArea):
            self.process_area = ProcessArea(self.process_area)

        if self.control_type is not None and not isinstance(self.control_type, str):
            self.control_type = str(self.control_type)

        if not isinstance(self.governed_by, list):
            self.governed_by = [self.governed_by] if self.governed_by is not None else []
        self.governed_by = [v if isinstance(v, StandardId) else StandardId(v) for v in self.governed_by]

        if self.modern_equivalent is not None and not isinstance(self.modern_equivalent, str):
            self.modern_equivalent = str(self.modern_equivalent)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Standard(NamedThing):
    """
    Accounting, regulatory, contractual or market standard; records live in standards/era_standards.yaml.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Standard"]
    class_class_curie: ClassVar[str] = "dcterms:Standard"
    class_name: ClassVar[str] = "Standard"
    class_model_uri: ClassVar[URIRef] = ENRON.Standard

    id: Union[str, StandardId] = None
    designation: Optional[str] = None
    issuer: Optional[str] = None
    effective_date: Optional[Union[str, XSDDate]] = None
    process_areas: Optional[Union[Union[str, "ProcessArea"], list[Union[str, "ProcessArea"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StandardId):
            self.id = StandardId(self.id)

        if self.designation is not None and not isinstance(self.designation, str):
            self.designation = str(self.designation)

        if self.issuer is not None and not isinstance(self.issuer, str):
            self.issuer = str(self.issuer)

        if self.effective_date is not None and not isinstance(self.effective_date, XSDDate):
            self.effective_date = XSDDate(self.effective_date)

        if not isinstance(self.process_areas, list):
            self.process_areas = [self.process_areas] if self.process_areas is not None else []
        self.process_areas = [v if isinstance(v, ProcessArea) else ProcessArea(v) for v in self.process_areas]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Commodity(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Commodity"]
    class_class_curie: ClassVar[str] = "enron:Commodity"
    class_name: ClassVar[str] = "Commodity"
    class_model_uri: ClassVar[URIRef] = ENRON.Commodity

    id: Union[str, CommodityId] = None
    commodity_kind: Optional[Union[str, "CommodityKind"]] = None
    default_unit: Optional[Union[str, "VolumeUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CommodityId):
            self.id = CommodityId(self.id)

        if self.commodity_kind is not None and not isinstance(self.commodity_kind, CommodityKind):
            self.commodity_kind = CommodityKind(self.commodity_kind)

        if self.default_unit is not None and not isinstance(self.default_unit, VolumeUnit):
            self.default_unit = VolumeUnit(self.default_unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Location(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Place"]
    class_class_curie: ClassVar[str] = "schema:Place"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = ENRON.Location

    id: Union[str, LocationId] = None
    location_type: Optional[str] = None
    region: Optional[str] = None
    commodity: Optional[Union[str, CommodityId]] = None
    operator: Optional[Union[str, OrganizationId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.location_type is not None and not isinstance(self.location_type, str):
            self.location_type = str(self.location_type)

        if self.region is not None and not isinstance(self.region, str):
            self.region = str(self.region)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        if self.operator is not None and not isinstance(self.operator, OrganizationId):
            self.operator = OrganizationId(self.operator)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TradingHub(Location):
    """
    Liquid pricing point (Henry Hub, Waha, Mid-C, Palo Verde, PJM West ...).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["TradingHub"]
    class_class_curie: ClassVar[str] = "enron:TradingHub"
    class_name: ClassVar[str] = "TradingHub"
    class_model_uri: ClassVar[URIRef] = ENRON.TradingHub

    id: Union[str, TradingHubId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TradingHubId):
            self.id = TradingHubId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DeliveryPoint(Location):
    """
    Physical meter/interconnect or pool where title transfers.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["DeliveryPoint"]
    class_class_curie: ClassVar[str] = "enron:DeliveryPoint"
    class_name: ClassVar[str] = "DeliveryPoint"
    class_model_uri: ClassVar[URIRef] = ENRON.DeliveryPoint

    id: Union[str, DeliveryPointId] = None
    pipeline: Optional[Union[str, PipelineId]] = None
    meter_number: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DeliveryPointId):
            self.id = DeliveryPointId(self.id)

        if self.pipeline is not None and not isinstance(self.pipeline, PipelineId):
            self.pipeline = PipelineId(self.pipeline)

        if self.meter_number is not None and not isinstance(self.meter_number, str):
            self.meter_number = str(self.meter_number)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Pipeline(Location):
    """
    Interstate or intrastate pipeline system (Transwestern, Northern Natural, El Paso ...).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Pipeline"]
    class_class_curie: ClassVar[str] = "enron:Pipeline"
    class_name: ClassVar[str] = "Pipeline"
    class_model_uri: ClassVar[URIRef] = ENRON.Pipeline

    id: Union[str, PipelineId] = None
    ferc_regulated: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PipelineId):
            self.id = PipelineId(self.id)

        if self.ferc_regulated is not None and not isinstance(self.ferc_regulated, Bool):
            self.ferc_regulated = Bool(self.ferc_regulated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerControlArea(Location):
    """
    Power control area, ISO zone or transmission path (NP15, SP15, COB, ERCOT ...).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["PowerControlArea"]
    class_class_curie: ClassVar[str] = "enron:PowerControlArea"
    class_name: ClassVar[str] = "PowerControlArea"
    class_model_uri: ClassVar[URIRef] = ENRON.PowerControlArea

    id: Union[str, PowerControlAreaId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PowerControlAreaId):
            self.id = PowerControlAreaId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PriceIndex(NamedThing):
    """
    Published or exchange price used to settle index deals (IFERC monthly, Gas Daily, NYMEX).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["PriceIndex"]
    class_class_curie: ClassVar[str] = "enron:PriceIndex"
    class_name: ClassVar[str] = "PriceIndex"
    class_model_uri: ClassVar[URIRef] = ENRON.PriceIndex

    id: Union[str, PriceIndexId] = None
    publisher: Optional[Union[str, MarketInfrastructureId]] = None
    index_frequency: Optional[str] = None
    location: Optional[Union[str, LocationId]] = None
    commodity: Optional[Union[str, CommodityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PriceIndexId):
            self.id = PriceIndexId(self.id)

        if self.publisher is not None and not isinstance(self.publisher, MarketInfrastructureId):
            self.publisher = MarketInfrastructureId(self.publisher)

        if self.index_frequency is not None and not isinstance(self.index_frequency, str):
            self.index_frequency = str(self.index_frequency)

        if self.location is not None and not isinstance(self.location, LocationId):
            self.location = LocationId(self.location)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PriceCurve(NamedThing):
    """
    Forward curve maintained in ERMS/TDS for valuation (price, basis, volatility).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["PriceCurve"]
    class_class_curie: ClassVar[str] = "enron:PriceCurve"
    class_name: ClassVar[str] = "PriceCurve"
    class_model_uri: ClassVar[URIRef] = ENRON.PriceCurve

    id: Union[str, PriceCurveId] = None
    curve_code: Optional[str] = None
    curve_type: Optional[Union[str, "CurveType"]] = None
    commodity: Optional[Union[str, CommodityId]] = None
    location: Optional[Union[str, LocationId]] = None
    index: Optional[Union[str, PriceIndexId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PriceCurveId):
            self.id = PriceCurveId(self.id)

        if self.curve_code is not None and not isinstance(self.curve_code, str):
            self.curve_code = str(self.curve_code)

        if self.curve_type is not None and not isinstance(self.curve_type, CurveType):
            self.curve_type = CurveType(self.curve_type)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        if self.location is not None and not isinstance(self.location, LocationId):
            self.location = LocationId(self.location)

        if self.index is not None and not isinstance(self.index, PriceIndexId):
            self.index = PriceIndexId(self.index)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CurvePoint(YAMLRoot):
    """
    One marked value of a curve for a delivery period on a valuation date.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["CurvePoint"]
    class_class_curie: ClassVar[str] = "enron:CurvePoint"
    class_name: ClassVar[str] = "CurvePoint"
    class_model_uri: ClassVar[URIRef] = ENRON.CurvePoint

    curve: Union[str, PriceCurveId] = None
    valuation_date: Union[str, XSDDate] = None
    delivery_start: Union[str, XSDDate] = None
    value: float = None
    unit: Optional[str] = None
    is_synthetic: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.curve):
            self.MissingRequiredField("curve")
        if not isinstance(self.curve, PriceCurveId):
            self.curve = PriceCurveId(self.curve)

        if self._is_empty(self.valuation_date):
            self.MissingRequiredField("valuation_date")
        if not isinstance(self.valuation_date, XSDDate):
            self.valuation_date = XSDDate(self.valuation_date)

        if self._is_empty(self.delivery_start):
            self.MissingRequiredField("delivery_start")
        if not isinstance(self.delivery_start, XSDDate):
            self.delivery_start = XSDDate(self.delivery_start)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, float):
            self.value = float(self.value)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.is_synthetic is not None and not isinstance(self.is_synthetic, Bool):
            self.is_synthetic = Bool(self.is_synthetic)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MasterAgreement(NamedThing):
    """
    Governing master (ISDA 1992, GISB 1996 base contract, EEI 2000 master, enabling agreements).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["MasterAgreement"]
    class_class_curie: ClassVar[str] = "enron:MasterAgreement"
    class_name: ClassVar[str] = "MasterAgreement"
    class_model_uri: ClassVar[URIRef] = ENRON.MasterAgreement

    id: Union[str, MasterAgreementId] = None
    agreement_form: Optional[Union[str, "AgreementForm"]] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    effective_date: Optional[Union[str, XSDDate]] = None
    netting: Optional[Union[bool, Bool]] = None
    collateral_threshold: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MasterAgreementId):
            self.id = MasterAgreementId(self.id)

        if self.agreement_form is not None and not isinstance(self.agreement_form, AgreementForm):
            self.agreement_form = AgreementForm(self.agreement_form)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.effective_date is not None and not isinstance(self.effective_date, XSDDate):
            self.effective_date = XSDDate(self.effective_date)

        if self.netting is not None and not isinstance(self.netting, Bool):
            self.netting = Bool(self.netting)

        if self.collateral_threshold is not None and not isinstance(self.collateral_threshold, float):
            self.collateral_threshold = float(self.collateral_threshold)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Trade(NamedThing):
    """
    A deal as captured in a front-office system (Sitara, EnPower, TAGG) or on EnronOnline.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Trade"]
    class_class_curie: ClassVar[str] = "enron:Trade"
    class_name: ClassVar[str] = "Trade"
    class_model_uri: ClassVar[URIRef] = ENRON.Trade

    id: Union[str, TradeId] = None
    deal_number: Optional[str] = None
    source_system: Optional[Union[str, InformationSystemId]] = None
    eol_transaction_id: Optional[str] = None
    trade_date: Optional[Union[str, XSDDate]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None
    book: Optional[Union[str, BookId]] = None
    trader: Optional[Union[str, PersonId]] = None
    commodity: Optional[Union[str, CommodityId]] = None
    instrument_type: Optional[Union[str, "InstrumentType"]] = None
    buy_sell: Optional[Union[str, "BuySell"]] = None
    volume: Optional[float] = None
    volume_unit: Optional[Union[str, "VolumeUnit"]] = None
    volume_frequency: Optional[str] = None
    price: Optional[float] = None
    price_type: Optional[Union[str, "PriceType"]] = None
    price_index: Optional[Union[str, PriceIndexId]] = None
    premium_or_adder: Optional[float] = None
    delivery_location: Optional[Union[str, LocationId]] = None
    delivery_start: Optional[Union[str, XSDDate]] = None
    delivery_end: Optional[Union[str, XSDDate]] = None
    deal_status: Optional[str] = None
    master_agreement: Optional[Union[str, MasterAgreementId]] = None
    confirmation_status: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TradeId):
            self.id = TradeId(self.id)

        if self.deal_number is not None and not isinstance(self.deal_number, str):
            self.deal_number = str(self.deal_number)

        if self.source_system is not None and not isinstance(self.source_system, InformationSystemId):
            self.source_system = InformationSystemId(self.source_system)

        if self.eol_transaction_id is not None and not isinstance(self.eol_transaction_id, str):
            self.eol_transaction_id = str(self.eol_transaction_id)

        if self.trade_date is not None and not isinstance(self.trade_date, XSDDate):
            self.trade_date = XSDDate(self.trade_date)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        if self.book is not None and not isinstance(self.book, BookId):
            self.book = BookId(self.book)

        if self.trader is not None and not isinstance(self.trader, PersonId):
            self.trader = PersonId(self.trader)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        if self.instrument_type is not None and not isinstance(self.instrument_type, InstrumentType):
            self.instrument_type = InstrumentType(self.instrument_type)

        if self.buy_sell is not None and not isinstance(self.buy_sell, BuySell):
            self.buy_sell = BuySell(self.buy_sell)

        if self.volume is not None and not isinstance(self.volume, float):
            self.volume = float(self.volume)

        if self.volume_unit is not None and not isinstance(self.volume_unit, VolumeUnit):
            self.volume_unit = VolumeUnit(self.volume_unit)

        if self.volume_frequency is not None and not isinstance(self.volume_frequency, str):
            self.volume_frequency = str(self.volume_frequency)

        if self.price is not None and not isinstance(self.price, float):
            self.price = float(self.price)

        if self.price_type is not None and not isinstance(self.price_type, PriceType):
            self.price_type = PriceType(self.price_type)

        if self.price_index is not None and not isinstance(self.price_index, PriceIndexId):
            self.price_index = PriceIndexId(self.price_index)

        if self.premium_or_adder is not None and not isinstance(self.premium_or_adder, float):
            self.premium_or_adder = float(self.premium_or_adder)

        if self.delivery_location is not None and not isinstance(self.delivery_location, LocationId):
            self.delivery_location = LocationId(self.delivery_location)

        if self.delivery_start is not None and not isinstance(self.delivery_start, XSDDate):
            self.delivery_start = XSDDate(self.delivery_start)

        if self.delivery_end is not None and not isinstance(self.delivery_end, XSDDate):
            self.delivery_end = XSDDate(self.delivery_end)

        if self.deal_status is not None and not isinstance(self.deal_status, str):
            self.deal_status = str(self.deal_status)

        if self.master_agreement is not None and not isinstance(self.master_agreement, MasterAgreementId):
            self.master_agreement = MasterAgreementId(self.master_agreement)

        if self.confirmation_status is not None and not isinstance(self.confirmation_status, str):
            self.confirmation_status = str(self.confirmation_status)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Book(NamedThing):
    """
    Portfolio/book in ERMS/RisktRAC that positions roll up to (e.g. "ENA-FT-WEST-PHY").
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Book"]
    class_class_curie: ClassVar[str] = "enron:Book"
    class_name: ClassVar[str] = "Book"
    class_model_uri: ClassVar[URIRef] = ENRON.Book

    id: Union[str, BookId] = None
    book_code: Optional[str] = None
    desk: Optional[Union[str, TradingDeskId]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    commodity: Optional[Union[str, CommodityId]] = None
    book_type: Optional[str] = None
    region: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookId):
            self.id = BookId(self.id)

        if self.book_code is not None and not isinstance(self.book_code, str):
            self.book_code = str(self.book_code)

        if self.desk is not None and not isinstance(self.desk, TradingDeskId):
            self.desk = TradingDeskId(self.desk)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.commodity is not None and not isinstance(self.commodity, CommodityId):
            self.commodity = CommodityId(self.commodity)

        if self.book_type is not None and not isinstance(self.book_type, str):
            self.book_type = str(self.book_type)

        if self.region is not None and not isinstance(self.region, str):
            self.region = str(self.region)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Position(NamedThing):
    """
    Net open position by book, curve and delivery period on a date (DPR input).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Position"]
    class_class_curie: ClassVar[str] = "enron:Position"
    class_name: ClassVar[str] = "Position"
    class_model_uri: ClassVar[URIRef] = ENRON.Position

    id: Union[str, PositionId] = None
    book: Optional[Union[str, BookId]] = None
    curve: Optional[Union[str, PriceCurveId]] = None
    as_of_date: Optional[Union[str, XSDDate]] = None
    delivery_start: Optional[Union[str, XSDDate]] = None
    quantity: Optional[float] = None
    volume_unit: Optional[Union[str, "VolumeUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PositionId):
            self.id = PositionId(self.id)

        if self.book is not None and not isinstance(self.book, BookId):
            self.book = BookId(self.book)

        if self.curve is not None and not isinstance(self.curve, PriceCurveId):
            self.curve = PriceCurveId(self.curve)

        if self.as_of_date is not None and not isinstance(self.as_of_date, XSDDate):
            self.as_of_date = XSDDate(self.as_of_date)

        if self.delivery_start is not None and not isinstance(self.delivery_start, XSDDate):
            self.delivery_start = XSDDate(self.delivery_start)

        if self.quantity is not None and not isinstance(self.quantity, float):
            self.quantity = float(self.quantity)

        if self.volume_unit is not None and not isinstance(self.volume_unit, VolumeUnit):
            self.volume_unit = VolumeUnit(self.volume_unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Valuation(NamedThing):
    """
    Mark-to-market result (DPR line) by book on a date, incl. new-deal and curve-shift P&L.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Valuation"]
    class_class_curie: ClassVar[str] = "enron:Valuation"
    class_name: ClassVar[str] = "Valuation"
    class_model_uri: ClassVar[URIRef] = ENRON.Valuation

    id: Union[str, ValuationId] = None
    book: Optional[Union[str, BookId]] = None
    as_of_date: Optional[Union[str, XSDDate]] = None
    mtm_value: Optional[float] = None
    daily_pnl: Optional[float] = None
    new_deal_pnl: Optional[float] = None
    curve_shift_pnl: Optional[float] = None
    var_95: Optional[float] = None
    currency: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ValuationId):
            self.id = ValuationId(self.id)

        if self.book is not None and not isinstance(self.book, BookId):
            self.book = BookId(self.book)

        if self.as_of_date is not None and not isinstance(self.as_of_date, XSDDate):
            self.as_of_date = XSDDate(self.as_of_date)

        if self.mtm_value is not None and not isinstance(self.mtm_value, float):
            self.mtm_value = float(self.mtm_value)

        if self.daily_pnl is not None and not isinstance(self.daily_pnl, float):
            self.daily_pnl = float(self.daily_pnl)

        if self.new_deal_pnl is not None and not isinstance(self.new_deal_pnl, float):
            self.new_deal_pnl = float(self.new_deal_pnl)

        if self.curve_shift_pnl is not None and not isinstance(self.curve_shift_pnl, float):
            self.curve_shift_pnl = float(self.curve_shift_pnl)

        if self.var_95 is not None and not isinstance(self.var_95, float):
            self.var_95 = float(self.var_95)

        if self.currency is not None and not isinstance(self.currency, str):
            self.currency = str(self.currency)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Nomination(NamedThing):
    """
    Gas nomination / power schedule submitted to a pipeline or ISO.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Nomination"]
    class_class_curie: ClassVar[str] = "enron:Nomination"
    class_name: ClassVar[str] = "Nomination"
    class_model_uri: ClassVar[URIRef] = ENRON.Nomination

    id: Union[str, NominationId] = None
    trade: Optional[Union[str, TradeId]] = None
    pipeline: Optional[Union[str, PipelineId]] = None
    delivery_location: Optional[Union[str, LocationId]] = None
    flow_date: Optional[Union[str, XSDDate]] = None
    nominated_volume: Optional[float] = None
    scheduled_volume: Optional[float] = None
    actual_volume: Optional[float] = None
    volume_unit: Optional[Union[str, "VolumeUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NominationId):
            self.id = NominationId(self.id)

        if self.trade is not None and not isinstance(self.trade, TradeId):
            self.trade = TradeId(self.trade)

        if self.pipeline is not None and not isinstance(self.pipeline, PipelineId):
            self.pipeline = PipelineId(self.pipeline)

        if self.delivery_location is not None and not isinstance(self.delivery_location, LocationId):
            self.delivery_location = LocationId(self.delivery_location)

        if self.flow_date is not None and not isinstance(self.flow_date, XSDDate):
            self.flow_date = XSDDate(self.flow_date)

        if self.nominated_volume is not None and not isinstance(self.nominated_volume, float):
            self.nominated_volume = float(self.nominated_volume)

        if self.scheduled_volume is not None and not isinstance(self.scheduled_volume, float):
            self.scheduled_volume = float(self.scheduled_volume)

        if self.actual_volume is not None and not isinstance(self.actual_volume, float):
            self.actual_volume = float(self.actual_volume)

        if self.volume_unit is not None and not isinstance(self.volume_unit, VolumeUnit):
            self.volume_unit = VolumeUnit(self.volume_unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Imbalance(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Imbalance"]
    class_class_curie: ClassVar[str] = "enron:Imbalance"
    class_name: ClassVar[str] = "Imbalance"
    class_model_uri: ClassVar[URIRef] = ENRON.Imbalance

    id: Union[str, ImbalanceId] = None
    pipeline: Optional[Union[str, PipelineId]] = None
    delivery_location: Optional[Union[str, LocationId]] = None
    flow_month: Optional[str] = None
    imbalance_volume: Optional[float] = None
    volume_unit: Optional[Union[str, "VolumeUnit"]] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ImbalanceId):
            self.id = ImbalanceId(self.id)

        if self.pipeline is not None and not isinstance(self.pipeline, PipelineId):
            self.pipeline = PipelineId(self.pipeline)

        if self.delivery_location is not None and not isinstance(self.delivery_location, LocationId):
            self.delivery_location = LocationId(self.delivery_location)

        if self.flow_month is not None and not isinstance(self.flow_month, str):
            self.flow_month = str(self.flow_month)

        if self.imbalance_volume is not None and not isinstance(self.imbalance_volume, float):
            self.imbalance_volume = float(self.imbalance_volume)

        if self.volume_unit is not None and not isinstance(self.volume_unit, VolumeUnit):
            self.volume_unit = VolumeUnit(self.volume_unit)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Invoice(NamedThing):
    """
    Settlement invoice/statement produced by Unify for a counterparty and production month.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Invoice"]
    class_class_curie: ClassVar[str] = "enron:Invoice"
    class_name: ClassVar[str] = "Invoice"
    class_model_uri: ClassVar[URIRef] = ENRON.Invoice

    id: Union[str, InvoiceId] = None
    invoice_number: Optional[str] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    production_month: Optional[str] = None
    invoice_date: Optional[Union[str, XSDDate]] = None
    due_date: Optional[Union[str, XSDDate]] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    trades: Optional[Union[Union[str, TradeId], list[Union[str, TradeId]]]] = empty_list()
    invoice_status: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InvoiceId):
            self.id = InvoiceId(self.id)

        if self.invoice_number is not None and not isinstance(self.invoice_number, str):
            self.invoice_number = str(self.invoice_number)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.production_month is not None and not isinstance(self.production_month, str):
            self.production_month = str(self.production_month)

        if self.invoice_date is not None and not isinstance(self.invoice_date, XSDDate):
            self.invoice_date = XSDDate(self.invoice_date)

        if self.due_date is not None and not isinstance(self.due_date, XSDDate):
            self.due_date = XSDDate(self.due_date)

        if self.amount is not None and not isinstance(self.amount, float):
            self.amount = float(self.amount)

        if self.currency is not None and not isinstance(self.currency, str):
            self.currency = str(self.currency)

        if not isinstance(self.trades, list):
            self.trades = [self.trades] if self.trades is not None else []
        self.trades = [v if isinstance(v, TradeId) else TradeId(v) for v in self.trades]

        if self.invoice_status is not None and not isinstance(self.invoice_status, str):
            self.invoice_status = str(self.invoice_status)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Payment(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Payment"]
    class_class_curie: ClassVar[str] = "enron:Payment"
    class_name: ClassVar[str] = "Payment"
    class_model_uri: ClassVar[URIRef] = ENRON.Payment

    id: Union[str, PaymentId] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    payment_date: Optional[Union[str, XSDDate]] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    invoices: Optional[Union[Union[str, InvoiceId], list[Union[str, InvoiceId]]]] = empty_list()
    direction: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PaymentId):
            self.id = PaymentId(self.id)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.payment_date is not None and not isinstance(self.payment_date, XSDDate):
            self.payment_date = XSDDate(self.payment_date)

        if self.amount is not None and not isinstance(self.amount, float):
            self.amount = float(self.amount)

        if self.currency is not None and not isinstance(self.currency, str):
            self.currency = str(self.currency)

        if not isinstance(self.invoices, list):
            self.invoices = [self.invoices] if self.invoices is not None else []
        self.invoices = [v if isinstance(v, InvoiceId) else InvoiceId(v) for v in self.invoices]

        if self.direction is not None and not isinstance(self.direction, str):
            self.direction = str(self.direction)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GLAccount(NamedThing):
    """
    SAP R/3 general ledger account.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["GLAccount"]
    class_class_curie: ClassVar[str] = "enron:GLAccount"
    class_name: ClassVar[str] = "GLAccount"
    class_model_uri: ClassVar[URIRef] = ENRON.GLAccount

    id: Union[str, GLAccountId] = None
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    fs_line: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GLAccountId):
            self.id = GLAccountId(self.id)

        if self.account_number is not None and not isinstance(self.account_number, str):
            self.account_number = str(self.account_number)

        if self.account_type is not None and not isinstance(self.account_type, str):
            self.account_type = str(self.account_type)

        if self.fs_line is not None and not isinstance(self.fs_line, str):
            self.fs_line = str(self.fs_line)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CostCenter(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["CostCenter"]
    class_class_curie: ClassVar[str] = "enron:CostCenter"
    class_name: ClassVar[str] = "CostCenter"
    class_model_uri: ClassVar[URIRef] = ENRON.CostCenter

    id: Union[str, CostCenterId] = None
    cost_center_code: Optional[str] = None
    legal_entity: Optional[Union[str, LegalEntityId]] = None
    business_unit: Optional[Union[str, BusinessUnitId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CostCenterId):
            self.id = CostCenterId(self.id)

        if self.cost_center_code is not None and not isinstance(self.cost_center_code, str):
            self.cost_center_code = str(self.cost_center_code)

        if self.legal_entity is not None and not isinstance(self.legal_entity, LegalEntityId):
            self.legal_entity = LegalEntityId(self.legal_entity)

        if self.business_unit is not None and not isinstance(self.business_unit, BusinessUnitId):
            self.business_unit = BusinessUnitId(self.business_unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class JournalEntry(NamedThing):
    """
    SAP FI document (BKPF header with BSEG lines).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["JournalEntry"]
    class_class_curie: ClassVar[str] = "enron:JournalEntry"
    class_name: ClassVar[str] = "JournalEntry"
    class_model_uri: ClassVar[URIRef] = ENRON.JournalEntry

    id: Union[str, JournalEntryId] = None
    document_number: Optional[str] = None
    company_code: Optional[str] = None
    fiscal_year: Optional[int] = None
    posting_date: Optional[Union[str, XSDDate]] = None
    document_type: Optional[str] = None
    header_text: Optional[str] = None
    entered_by: Optional[Union[str, PersonId]] = None
    lines: Optional[Union[Union[dict, "JournalLine"], list[Union[dict, "JournalLine"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, JournalEntryId):
            self.id = JournalEntryId(self.id)

        if self.document_number is not None and not isinstance(self.document_number, str):
            self.document_number = str(self.document_number)

        if self.company_code is not None and not isinstance(self.company_code, str):
            self.company_code = str(self.company_code)

        if self.fiscal_year is not None and not isinstance(self.fiscal_year, int):
            self.fiscal_year = int(self.fiscal_year)

        if self.posting_date is not None and not isinstance(self.posting_date, XSDDate):
            self.posting_date = XSDDate(self.posting_date)

        if self.document_type is not None and not isinstance(self.document_type, str):
            self.document_type = str(self.document_type)

        if self.header_text is not None and not isinstance(self.header_text, str):
            self.header_text = str(self.header_text)

        if self.entered_by is not None and not isinstance(self.entered_by, PersonId):
            self.entered_by = PersonId(self.entered_by)

        self._normalize_inlined_as_list(slot_name="lines", slot_type=JournalLine, key_name="debit_credit", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class JournalLine(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["JournalLine"]
    class_class_curie: ClassVar[str] = "enron:JournalLine"
    class_name: ClassVar[str] = "JournalLine"
    class_model_uri: ClassVar[URIRef] = ENRON.JournalLine

    gl_account: Union[str, GLAccountId] = None
    debit_credit: Union[str, "DebitCredit"] = None
    amount: float = None
    cost_center: Optional[Union[str, CostCenterId]] = None
    counterparty: Optional[Union[str, CounterpartyId]] = None
    trading_partner: Optional[Union[str, LegalEntityId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gl_account):
            self.MissingRequiredField("gl_account")
        if not isinstance(self.gl_account, GLAccountId):
            self.gl_account = GLAccountId(self.gl_account)

        if self._is_empty(self.debit_credit):
            self.MissingRequiredField("debit_credit")
        if not isinstance(self.debit_credit, DebitCredit):
            self.debit_credit = DebitCredit(self.debit_credit)

        if self._is_empty(self.amount):
            self.MissingRequiredField("amount")
        if not isinstance(self.amount, float):
            self.amount = float(self.amount)

        if self.cost_center is not None and not isinstance(self.cost_center, CostCenterId):
            self.cost_center = CostCenterId(self.cost_center)

        if self.counterparty is not None and not isinstance(self.counterparty, CounterpartyId):
            self.counterparty = CounterpartyId(self.counterparty)

        if self.trading_partner is not None and not isinstance(self.trading_partner, LegalEntityId):
            self.trading_partner = LegalEntityId(self.trading_partner)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Document(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["DigitalDocument"]
    class_class_curie: ClassVar[str] = "schema:DigitalDocument"
    class_name: ClassVar[str] = "Document"
    class_model_uri: ClassVar[URIRef] = ENRON.Document

    id: Union[str, DocumentId] = None
    created: Optional[Union[str, XSDDateTime]] = None
    author: Optional[str] = None
    custodian: Optional[Union[str, PersonId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.created is not None and not isinstance(self.created, XSDDateTime):
            self.created = XSDDateTime(self.created)

        if self.author is not None and not isinstance(self.author, str):
            self.author = str(self.author)

        if self.custodian is not None and not isinstance(self.custodian, PersonId):
            self.custodian = PersonId(self.custodian)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Workbook(Document):
    """
    One spreadsheet file from the Hermans corpus (deduplicated by MD5).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["SpreadsheetDigitalDocument"]
    class_class_curie: ClassVar[str] = "schema:SpreadsheetDigitalDocument"
    class_name: ClassVar[str] = "Workbook"
    class_model_uri: ClassVar[URIRef] = ENRON.Workbook

    id: Union[str, WorkbookId] = None
    file_id: Optional[str] = None
    original_filename: Optional[str] = None
    process_area: Optional[Union[str, "ProcessArea"]] = None
    document_role: Optional[Union[str, "DocumentRole"]] = None
    mentions: Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]] = empty_list()
    sheets: Optional[Union[Union[str, WorksheetId], list[Union[str, WorksheetId]]]] = empty_list()
    derived_from: Optional[Union[Union[str, WorkbookId], list[Union[str, WorkbookId]]]] = empty_list()
    version_family: Optional[str] = None
    as_of_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, WorkbookId):
            self.id = WorkbookId(self.id)

        if self.file_id is not None and not isinstance(self.file_id, str):
            self.file_id = str(self.file_id)

        if self.original_filename is not None and not isinstance(self.original_filename, str):
            self.original_filename = str(self.original_filename)

        if self.process_area is not None and not isinstance(self.process_area, ProcessArea):
            self.process_area = ProcessArea(self.process_area)

        if self.document_role is not None and not isinstance(self.document_role, DocumentRole):
            self.document_role = DocumentRole(self.document_role)

        if not isinstance(self.mentions, list):
            self.mentions = [self.mentions] if self.mentions is not None else []
        self.mentions = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.mentions]

        if not isinstance(self.sheets, list):
            self.sheets = [self.sheets] if self.sheets is not None else []
        self.sheets = [v if isinstance(v, WorksheetId) else WorksheetId(v) for v in self.sheets]

        if not isinstance(self.derived_from, list):
            self.derived_from = [self.derived_from] if self.derived_from is not None else []
        self.derived_from = [v if isinstance(v, WorkbookId) else WorkbookId(v) for v in self.derived_from]

        if self.version_family is not None and not isinstance(self.version_family, str):
            self.version_family = str(self.version_family)

        if self.as_of_date is not None and not isinstance(self.as_of_date, XSDDate):
            self.as_of_date = XSDDate(self.as_of_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Worksheet(NamedThing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["Worksheet"]
    class_class_curie: ClassVar[str] = "enron:Worksheet"
    class_name: ClassVar[str] = "Worksheet"
    class_model_uri: ClassVar[URIRef] = ENRON.Worksheet

    id: Union[str, WorksheetId] = None
    workbook: Optional[Union[str, WorkbookId]] = None
    sheet_name: Optional[str] = None
    sheet_state: Optional[str] = None
    sheet_role: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, WorksheetId):
            self.id = WorksheetId(self.id)

        if self.workbook is not None and not isinstance(self.workbook, WorkbookId):
            self.workbook = WorkbookId(self.workbook)

        if self.sheet_name is not None and not isinstance(self.sheet_name, str):
            self.sheet_name = str(self.sheet_name)

        if self.sheet_state is not None and not isinstance(self.sheet_state, str):
            self.sheet_state = str(self.sheet_state)

        if self.sheet_role is not None and not isinstance(self.sheet_role, str):
            self.sheet_role = str(self.sheet_role)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TableRegion(NamedThing):
    """
    A detected rectangular table inside a sheet, with header and data ranges.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENRON["TableRegion"]
    class_class_curie: ClassVar[str] = "enron:TableRegion"
    class_name: ClassVar[str] = "TableRegion"
    class_model_uri: ClassVar[URIRef] = ENRON.TableRegion

    id: Union[str, TableRegionId] = None
    worksheet: Optional[Union[str, WorksheetId]] = None
    cell_range: Optional[str] = None
    header_range: Optional[str] = None
    table_role: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TableRegionId):
            self.id = TableRegionId(self.id)

        if self.worksheet is not None and not isinstance(self.worksheet, WorksheetId):
            self.worksheet = WorksheetId(self.worksheet)

        if self.cell_range is not None and not isinstance(self.cell_range, str):
            self.cell_range = str(self.cell_range)

        if self.header_range is not None and not isinstance(self.header_range, str):
            self.header_range = str(self.header_range)

        if self.table_role is not None and not isinstance(self.table_role, str):
            self.table_role = str(self.table_role)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EmailMessage(Document):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["EmailMessage"]
    class_class_curie: ClassVar[str] = "schema:EmailMessage"
    class_name: ClassVar[str] = "EmailMessage"
    class_model_uri: ClassVar[URIRef] = ENRON.EmailMessage

    id: Union[str, EmailMessageId] = None
    message_id: Optional[str] = None
    sent_at: Optional[Union[str, XSDDateTime]] = None
    sender: Optional[Union[str, PersonId]] = None
    recipients: Optional[Union[Union[str, PersonId], list[Union[str, PersonId]]]] = empty_list()
    subject: Optional[str] = None
    attachments: Optional[Union[Union[str, WorkbookId], list[Union[str, WorkbookId]]]] = empty_list()
    thread: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EmailMessageId):
            self.id = EmailMessageId(self.id)

        if self.message_id is not None and not isinstance(self.message_id, str):
            self.message_id = str(self.message_id)

        if self.sent_at is not None and not isinstance(self.sent_at, XSDDateTime):
            self.sent_at = XSDDateTime(self.sent_at)

        if self.sender is not None and not isinstance(self.sender, PersonId):
            self.sender = PersonId(self.sender)

        if not isinstance(self.recipients, list):
            self.recipients = [self.recipients] if self.recipients is not None else []
        self.recipients = [v if isinstance(v, PersonId) else PersonId(v) for v in self.recipients]

        if self.subject is not None and not isinstance(self.subject, str):
            self.subject = str(self.subject)

        if not isinstance(self.attachments, list):
            self.attachments = [self.attachments] if self.attachments is not None else []
        self.attachments = [v if isinstance(v, WorkbookId) else WorkbookId(v) for v in self.attachments]

        if self.thread is not None and not isinstance(self.thread, str):
            self.thread = str(self.thread)

        super().__post_init__(**kwargs)


# Enumerations
class EvidenceSourceKind(EnumDefinitionImpl):

    workbook_cell = PermissibleValue(text="workbook_cell")
    workbook_metadata = PermissibleValue(text="workbook_metadata")
    email = PermissibleValue(text="email")
    email_header = PermissibleValue(text="email_header")
    public_filing = PermissibleValue(text="public_filing")
    ferc_record = PermissibleValue(text="ferc_record")
    synthetic_generator = PermissibleValue(text="synthetic_generator")
    curated = PermissibleValue(
        text="curated",
        description="Hand-curated reference fact with a cited source.")

    _defn = EnumDefinition(
        name="EvidenceSourceKind",
    )

class ProcessArea(EnumDefinitionImpl):
    """
    Front-to-back process areas of a merchant energy company. The same vocabulary is used by the standards catalog,
    the workbook classifier and the process log.
    """
    deal_capture = PermissibleValue(
        text="deal_capture",
        description="Trade entry and EnronOnline transactions (Sitara, EnPower, TAGG, EOL).")
    confirmation = PermissibleValue(
        text="confirmation",
        description="Trade confirmations and contract administration (Global Contracts).")
    credit = PermissibleValue(
        text="credit",
        description="Counterparty credit, limits, collateral, master netting (GCP, RAC credit).")
    risk_and_valuation = PermissibleValue(
        text="risk_and_valuation",
        description="Curves, positions, MTM, VaR, DPR (ERMS, RisktRAC, TDS).")
    scheduling_logistics = PermissibleValue(
        text="scheduling_logistics",
        description="Gas nominations, pipeline scheduling, power scheduling and tagging.")
    settlement = PermissibleValue(
        text="settlement",
        description="Actualization, invoicing, payments, imbalances (Unify).")
    accounting_r2r = PermissibleValue(
        text="accounting_r2r",
        description="GL, accruals, reconciliations, close (SAP).")
    consolidation_reporting = PermissibleValue(
        text="consolidation_reporting",
        description="Consolidation, SEC and segment reporting.")
    regulatory_reporting = PermissibleValue(
        text="regulatory_reporting",
        description="FERC, state commission and ISO reporting.")
    fpa = PermissibleValue(
        text="fpa",
        description="Plans, budgets, forecasts, management reporting.")
    treasury = PermissibleValue(
        text="treasury",
        description="Cash, funding, liquidity, bank and payment operations.")
    tax = PermissibleValue(text="tax")
    audit_controls = PermissibleValue(
        text="audit_controls",
        description="Internal audit, RAC oversight, external audit (Andersen).")
    structured_finance = PermissibleValue(
        text="structured_finance",
        description="SPEs, prepays, monetizations, FAS 125/140 transactions.")
    origination_assets = PermissibleValue(
        text="origination_assets",
        description="Origination, asset development, project finance models.")
    hr_admin = PermissibleValue(
        text="hr_admin",
        description="People, PRC, expenses, facilities.")
    it_projects = PermissibleValue(text="it_projects")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="ProcessArea",
        description="""Front-to-back process areas of a merchant energy company. The same vocabulary is used by the standards catalog, the workbook classifier and the process log.""",
    )

class UnitType(EnumDefinitionImpl):

    segment = PermissibleValue(text="segment")
    business_unit = PermissibleValue(text="business_unit")
    department = PermissibleValue(text="department")
    desk = PermissibleValue(text="desk")
    team = PermissibleValue(text="team")

    _defn = EnumDefinition(
        name="UnitType",
    )

class InfrastructureType(EnumDefinitionImpl):

    exchange = PermissibleValue(text="exchange")
    iso_rto = PermissibleValue(text="iso_rto")
    pipeline_operator = PermissibleValue(text="pipeline_operator")
    price_publisher = PermissibleValue(text="price_publisher")
    utility = PermissibleValue(text="utility")
    regulator = PermissibleValue(text="regulator")

    _defn = EnumDefinition(
        name="InfrastructureType",
    )

class CommodityKind(EnumDefinitionImpl):

    natural_gas = PermissibleValue(
        text="natural_gas",
        meaning=FIBO_DER_DRC_COMM["GasCommodity"])
    power = PermissibleValue(
        text="power",
        meaning=FIBO_DER_DRC_COMM["GeneratedResource"])
    crude_oil = PermissibleValue(
        text="crude_oil",
        meaning=FIBO_DER_DRC_COMM["OilCommodity"])
    refined_products = PermissibleValue(text="refined_products")
    ngl = PermissibleValue(text="ngl")
    coal = PermissibleValue(text="coal")
    emissions = PermissibleValue(
        text="emissions",
        meaning=FIBO_DER_DRC_COMM["EnvironmentalResource"])
    weather = PermissibleValue(
        text="weather",
        meaning=FIBO_DER_DRC_COMM["WeatherDerivative"])
    metals = PermissibleValue(
        text="metals",
        meaning=FIBO_DER_DRC_COMM["Metal"])
    pulp_paper = PermissibleValue(
        text="pulp_paper",
        meaning=FIBO_DER_DRC_COMM["PaperResource"])
    bandwidth = PermissibleValue(text="bandwidth")
    transport_capacity = PermissibleValue(text="transport_capacity")
    interest_rate = PermissibleValue(text="interest_rate")
    fx = PermissibleValue(text="fx")
    equity = PermissibleValue(text="equity")
    credit = PermissibleValue(text="credit")

    _defn = EnumDefinition(
        name="CommodityKind",
    )

class InstrumentType(EnumDefinitionImpl):

    physical_forward = PermissibleValue(
        text="physical_forward",
        meaning=FIBO_DER_DRC_COMM["CommodityForward"])
    physical_spot = PermissibleValue(
        text="physical_spot",
        meaning=FIBO_DER_DRC_COMM["CommoditySpotContract"])
    financial_swap = PermissibleValue(
        text="financial_swap",
        meaning=FIBO_DER_DRC_COMM["CommoditySwap"])
    basis_swap = PermissibleValue(
        text="basis_swap",
        meaning=FIBO_DER_DRC_SWP["BasisSwap"])
    index_swap = PermissibleValue(text="index_swap")
    option = PermissibleValue(
        text="option",
        meaning=FIBO_DER_DRC_COMM["CommodityOption"])
    futures = PermissibleValue(
        text="futures",
        meaning=FIBO_DER_DRC_COMM["CommodityFuture"])
    transport = PermissibleValue(text="transport")
    storage = PermissibleValue(text="storage")
    tolling = PermissibleValue(text="tolling")
    prepay = PermissibleValue(
        text="prepay",
        description="Prepaid forward used as financing (cf. Mahonia-style structures).")

    _defn = EnumDefinition(
        name="InstrumentType",
    )

class BuySell(EnumDefinitionImpl):

    buy = PermissibleValue(text="buy")
    sell = PermissibleValue(text="sell")

    _defn = EnumDefinition(
        name="BuySell",
    )

class PriceType(EnumDefinitionImpl):

    fixed = PermissibleValue(text="fixed")
    index = PermissibleValue(text="index")
    index_plus = PermissibleValue(text="index_plus")
    formula = PermissibleValue(text="formula")

    _defn = EnumDefinition(
        name="PriceType",
    )

class VolumeUnit(EnumDefinitionImpl):

    MMBtu = PermissibleValue(text="MMBtu")
    Dth = PermissibleValue(text="Dth")
    Mcf = PermissibleValue(text="Mcf")
    MWh = PermissibleValue(text="MWh")
    MW = PermissibleValue(text="MW")
    bbl = PermissibleValue(text="bbl")
    ton = PermissibleValue(text="ton")
    USD = PermissibleValue(text="USD")

    _defn = EnumDefinition(
        name="VolumeUnit",
    )

class CurveType(EnumDefinitionImpl):

    price = PermissibleValue(text="price")
    basis = PermissibleValue(text="basis")
    index = PermissibleValue(text="index")
    volatility = PermissibleValue(text="volatility")
    interest_rate = PermissibleValue(text="interest_rate")

    _defn = EnumDefinition(
        name="CurveType",
    )

class AgreementForm(EnumDefinitionImpl):

    isda_1992 = PermissibleValue(text="isda_1992")
    gisb_1996 = PermissibleValue(text="gisb_1996")
    eei_2000 = PermissibleValue(text="eei_2000")
    enfolio = PermissibleValue(
        text="enfolio",
        description="Enron master firm purchase/sale agreement.")
    online_gtc = PermissibleValue(
        text="online_gtc",
        description="EnronOnline general terms and conditions.")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="AgreementForm",
    )

class DebitCredit(EnumDefinitionImpl):

    S = PermissibleValue(
        text="S",
        description="Soll (debit)")
    H = PermissibleValue(
        text="H",
        description="Haben (credit)")

    _defn = EnumDefinition(
        name="DebitCredit",
    )

class DocumentRole(EnumDefinitionImpl):
    """
    What job a workbook does in the process (independent of process area).
    """
    report = PermissibleValue(text="report")
    reconciliation = PermissibleValue(text="reconciliation")
    schedule = PermissibleValue(
        text="schedule",
        description="Supporting schedule/roll-forward.")
    model = PermissibleValue(
        text="model",
        description="Valuation or deal model.")
    extract = PermissibleValue(
        text="extract",
        description="Raw system dump.")
    template = PermissibleValue(text="template")
    form = PermissibleValue(text="form")
    tracker = PermissibleValue(text="tracker")
    list = PermissibleValue(text="list")
    plan_budget = PermissibleValue(text="plan_budget")
    calculation = PermissibleValue(text="calculation")
    other = PermissibleValue(text="other")

    _defn = EnumDefinition(
        name="DocumentRole",
        description="What job a workbook does in the process (independent of process area).",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=ENRON.id, name="id", curie=ENRON.curie('id'),
                   model_uri=ENRON.id, domain=None, range=URIRef)

slots.label = Slot(uri=SKOS.prefLabel, name="label", curie=SKOS.curie('prefLabel'),
                   model_uri=ENRON.label, domain=None, range=Optional[str])

slots.alt_labels = Slot(uri=SKOS.altLabel, name="alt_labels", curie=SKOS.curie('altLabel'),
                   model_uri=ENRON.alt_labels, domain=None, range=Optional[Union[str, list[str]]])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=ENRON.description, domain=None, range=Optional[str])

slots.evidence = Slot(uri=PROV.wasDerivedFrom, name="evidence", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=ENRON.evidence, domain=None, range=Optional[Union[Union[dict, Evidence], list[Union[dict, Evidence]]]])

slots.is_synthetic = Slot(uri=ENRON.is_synthetic, name="is_synthetic", curie=ENRON.curie('is_synthetic'),
                   model_uri=ENRON.is_synthetic, domain=None, range=Optional[Union[bool, Bool]])

slots.valid_from = Slot(uri=ENRON.valid_from, name="valid_from", curie=ENRON.curie('valid_from'),
                   model_uri=ENRON.valid_from, domain=None, range=Optional[Union[str, XSDDate]])

slots.valid_to = Slot(uri=ENRON.valid_to, name="valid_to", curie=ENRON.curie('valid_to'),
                   model_uri=ENRON.valid_to, domain=None, range=Optional[Union[str, XSDDate]])

slots.email_addresses = Slot(uri=ENRON.email_addresses, name="email_addresses", curie=ENRON.curie('email_addresses'),
                   model_uri=ENRON.email_addresses, domain=None, range=Optional[Union[str, list[str]]])

slots.job_title = Slot(uri=ENRON.job_title, name="job_title", curie=ENRON.curie('job_title'),
                   model_uri=ENRON.job_title, domain=None, range=Optional[str])

slots.member_of = Slot(uri=ORG.memberOf, name="member_of", curie=ORG.curie('memberOf'),
                   model_uri=ENRON.member_of, domain=None, range=Optional[Union[Union[str, OrganizationId], list[Union[str, OrganizationId]]]])

slots.is_custodian = Slot(uri=ENRON.is_custodian, name="is_custodian", curie=ENRON.curie('is_custodian'),
                   model_uri=ENRON.is_custodian, domain=None, range=Optional[Union[bool, Bool]])

slots.maildir_name = Slot(uri=ENRON.maildir_name, name="maildir_name", curie=ENRON.curie('maildir_name'),
                   model_uri=ENRON.maildir_name, domain=None, range=Optional[str])

slots.parent_entity = Slot(uri=ORG.subOrganizationOf, name="parent_entity", curie=ORG.curie('subOrganizationOf'),
                   model_uri=ENRON.parent_entity, domain=None, range=Optional[Union[str, LegalEntityId]])

slots.parent_unit = Slot(uri=ORG.subOrganizationOf, name="parent_unit", curie=ORG.curie('subOrganizationOf'),
                   model_uri=ENRON.parent_unit, domain=None, range=Optional[Union[str, BusinessUnitId]])

slots.legal_entity = Slot(uri=ENRON.legal_entity, name="legal_entity", curie=ENRON.curie('legal_entity'),
                   model_uri=ENRON.legal_entity, domain=None, range=Optional[Union[str, LegalEntityId]])

slots.jurisdiction = Slot(uri=ENRON.jurisdiction, name="jurisdiction", curie=ENRON.curie('jurisdiction'),
                   model_uri=ENRON.jurisdiction, domain=None, range=Optional[str])

slots.segment = Slot(uri=ENRON.segment, name="segment", curie=ENRON.curie('segment'),
                   model_uri=ENRON.segment, domain=None, range=Optional[Union[str, BusinessUnitId]])

slots.sec_registrant = Slot(uri=ENRON.sec_registrant, name="sec_registrant", curie=ENRON.curie('sec_registrant'),
                   model_uri=ENRON.sec_registrant, domain=None, range=Optional[Union[bool, Bool]])

slots.ferc_regulated = Slot(uri=ENRON.ferc_regulated, name="ferc_regulated", curie=ENRON.curie('ferc_regulated'),
                   model_uri=ENRON.ferc_regulated, domain=None, range=Optional[Union[bool, Bool]])

slots.special_purpose = Slot(uri=ENRON.special_purpose, name="special_purpose", curie=ENRON.curie('special_purpose'),
                   model_uri=ENRON.special_purpose, domain=None, range=Optional[Union[bool, Bool]])

slots.unit_type = Slot(uri=ENRON.unit_type, name="unit_type", curie=ENRON.curie('unit_type'),
                   model_uri=ENRON.unit_type, domain=None, range=Optional[Union[str, "UnitType"]])

slots.region = Slot(uri=ENRON.region, name="region", curie=ENRON.curie('region'),
                   model_uri=ENRON.region, domain=None, range=Optional[str])

slots.commodity = Slot(uri=ENRON.commodity, name="commodity", curie=ENRON.curie('commodity'),
                   model_uri=ENRON.commodity, domain=None, range=Optional[Union[str, CommodityId]])

slots.gcp_cp_id = Slot(uri=ENRON.gcp_cp_id, name="gcp_cp_id", curie=ENRON.curie('gcp_cp_id'),
                   model_uri=ENRON.gcp_cp_id, domain=None, range=Optional[str])

slots.short_name = Slot(uri=ENRON.short_name, name="short_name", curie=ENRON.curie('short_name'),
                   model_uri=ENRON.short_name, domain=None, range=Optional[str])

slots.credit_rating = Slot(uri=ENRON.credit_rating, name="credit_rating", curie=ENRON.curie('credit_rating'),
                   model_uri=ENRON.credit_rating, domain=None, range=Optional[str])

slots.counterparty_type = Slot(uri=ENRON.counterparty_type, name="counterparty_type", curie=ENRON.curie('counterparty_type'),
                   model_uri=ENRON.counterparty_type, domain=None, range=Optional[str])

slots.parent_counterparty = Slot(uri=ENRON.parent_counterparty, name="parent_counterparty", curie=ENRON.curie('parent_counterparty'),
                   model_uri=ENRON.parent_counterparty, domain=None, range=Optional[Union[str, CounterpartyId]])

slots.infrastructure_type = Slot(uri=ENRON.infrastructure_type, name="infrastructure_type", curie=ENRON.curie('infrastructure_type'),
                   model_uri=ENRON.infrastructure_type, domain=None, range=Optional[Union[str, "InfrastructureType"]])

slots.system_code = Slot(uri=ENRON.system_code, name="system_code", curie=ENRON.curie('system_code'),
                   model_uri=ENRON.system_code, domain=None, range=Optional[str])

slots.platform = Slot(uri=ENRON.platform, name="platform", curie=ENRON.curie('platform'),
                   model_uri=ENRON.platform, domain=None, range=Optional[str])

slots.process_areas = Slot(uri=ENRON.process_areas, name="process_areas", curie=ENRON.curie('process_areas'),
                   model_uri=ENRON.process_areas, domain=None, range=Optional[Union[Union[str, "ProcessArea"], list[Union[str, "ProcessArea"]]]])

slots.process_area = Slot(uri=ENRON.process_area, name="process_area", curie=ENRON.curie('process_area'),
                   model_uri=ENRON.process_area, domain=None, range=Optional[Union[str, "ProcessArea"]])

slots.owning_unit = Slot(uri=ENRON.owning_unit, name="owning_unit", curie=ENRON.curie('owning_unit'),
                   model_uri=ENRON.owning_unit, domain=None, range=Optional[Union[str, BusinessUnitId]])

slots.upstream_systems = Slot(uri=ENRON.upstream_systems, name="upstream_systems", curie=ENRON.curie('upstream_systems'),
                   model_uri=ENRON.upstream_systems, domain=None, range=Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]])

slots.downstream_systems = Slot(uri=ENRON.downstream_systems, name="downstream_systems", curie=ENRON.curie('downstream_systems'),
                   model_uri=ENRON.downstream_systems, domain=None, range=Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]])

slots.performed_in = Slot(uri=ENRON.performed_in, name="performed_in", curie=ENRON.curie('performed_in'),
                   model_uri=ENRON.performed_in, domain=None, range=Optional[Union[Union[str, InformationSystemId], list[Union[str, InformationSystemId]]]])

slots.inputs = Slot(uri=PROV.used, name="inputs", curie=PROV.curie('used'),
                   model_uri=ENRON.inputs, domain=None, range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]])

slots.outputs = Slot(uri=PROV.generated, name="outputs", curie=PROV.curie('generated'),
                   model_uri=ENRON.outputs, domain=None, range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]])

slots.governed_by = Slot(uri=ENRON.governed_by, name="governed_by", curie=ENRON.curie('governed_by'),
                   model_uri=ENRON.governed_by, domain=None, range=Optional[Union[Union[str, StandardId], list[Union[str, StandardId]]]])

slots.control_type = Slot(uri=ENRON.control_type, name="control_type", curie=ENRON.curie('control_type'),
                   model_uri=ENRON.control_type, domain=None, range=Optional[str])

slots.modern_equivalent = Slot(uri=ENRON.modern_equivalent, name="modern_equivalent", curie=ENRON.curie('modern_equivalent'),
                   model_uri=ENRON.modern_equivalent, domain=None, range=Optional[str])

slots.designation = Slot(uri=ENRON.designation, name="designation", curie=ENRON.curie('designation'),
                   model_uri=ENRON.designation, domain=None, range=Optional[str])

slots.issuer = Slot(uri=ENRON.issuer, name="issuer", curie=ENRON.curie('issuer'),
                   model_uri=ENRON.issuer, domain=None, range=Optional[str])

slots.effective_date = Slot(uri=ENRON.effective_date, name="effective_date", curie=ENRON.curie('effective_date'),
                   model_uri=ENRON.effective_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.commodity_kind = Slot(uri=ENRON.commodity_kind, name="commodity_kind", curie=ENRON.curie('commodity_kind'),
                   model_uri=ENRON.commodity_kind, domain=None, range=Optional[Union[str, "CommodityKind"]])

slots.default_unit = Slot(uri=ENRON.default_unit, name="default_unit", curie=ENRON.curie('default_unit'),
                   model_uri=ENRON.default_unit, domain=None, range=Optional[Union[str, "VolumeUnit"]])

slots.location_type = Slot(uri=ENRON.location_type, name="location_type", curie=ENRON.curie('location_type'),
                   model_uri=ENRON.location_type, domain=None, range=Optional[str])

slots.operator = Slot(uri=ENRON.operator, name="operator", curie=ENRON.curie('operator'),
                   model_uri=ENRON.operator, domain=None, range=Optional[Union[str, OrganizationId]])

slots.pipeline = Slot(uri=ENRON.pipeline, name="pipeline", curie=ENRON.curie('pipeline'),
                   model_uri=ENRON.pipeline, domain=None, range=Optional[Union[str, PipelineId]])

slots.meter_number = Slot(uri=ENRON.meter_number, name="meter_number", curie=ENRON.curie('meter_number'),
                   model_uri=ENRON.meter_number, domain=None, range=Optional[str])

slots.publisher = Slot(uri=ENRON.publisher, name="publisher", curie=ENRON.curie('publisher'),
                   model_uri=ENRON.publisher, domain=None, range=Optional[Union[str, MarketInfrastructureId]])

slots.index_frequency = Slot(uri=ENRON.index_frequency, name="index_frequency", curie=ENRON.curie('index_frequency'),
                   model_uri=ENRON.index_frequency, domain=None, range=Optional[str])

slots.location = Slot(uri=ENRON.location, name="location", curie=ENRON.curie('location'),
                   model_uri=ENRON.location, domain=None, range=Optional[Union[str, LocationId]])

slots.curve_code = Slot(uri=ENRON.curve_code, name="curve_code", curie=ENRON.curie('curve_code'),
                   model_uri=ENRON.curve_code, domain=None, range=Optional[str])

slots.curve_type = Slot(uri=ENRON.curve_type, name="curve_type", curie=ENRON.curie('curve_type'),
                   model_uri=ENRON.curve_type, domain=None, range=Optional[Union[str, "CurveType"]])

slots.index = Slot(uri=ENRON.index, name="index", curie=ENRON.curie('index'),
                   model_uri=ENRON.index, domain=None, range=Optional[Union[str, PriceIndexId]])

slots.agreement_form = Slot(uri=ENRON.agreement_form, name="agreement_form", curie=ENRON.curie('agreement_form'),
                   model_uri=ENRON.agreement_form, domain=None, range=Optional[Union[str, "AgreementForm"]])

slots.counterparty = Slot(uri=ENRON.counterparty, name="counterparty", curie=ENRON.curie('counterparty'),
                   model_uri=ENRON.counterparty, domain=None, range=Optional[Union[str, CounterpartyId]])

slots.netting = Slot(uri=ENRON.netting, name="netting", curie=ENRON.curie('netting'),
                   model_uri=ENRON.netting, domain=None, range=Optional[Union[bool, Bool]])

slots.collateral_threshold = Slot(uri=ENRON.collateral_threshold, name="collateral_threshold", curie=ENRON.curie('collateral_threshold'),
                   model_uri=ENRON.collateral_threshold, domain=None, range=Optional[float])

slots.deal_number = Slot(uri=ENRON.deal_number, name="deal_number", curie=ENRON.curie('deal_number'),
                   model_uri=ENRON.deal_number, domain=None, range=Optional[str])

slots.source_system = Slot(uri=ENRON.source_system, name="source_system", curie=ENRON.curie('source_system'),
                   model_uri=ENRON.source_system, domain=None, range=Optional[Union[str, InformationSystemId]])

slots.eol_transaction_id = Slot(uri=ENRON.eol_transaction_id, name="eol_transaction_id", curie=ENRON.curie('eol_transaction_id'),
                   model_uri=ENRON.eol_transaction_id, domain=None, range=Optional[str])

slots.trade_date = Slot(uri=ENRON.trade_date, name="trade_date", curie=ENRON.curie('trade_date'),
                   model_uri=ENRON.trade_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.book = Slot(uri=ENRON.book, name="book", curie=ENRON.curie('book'),
                   model_uri=ENRON.book, domain=None, range=Optional[Union[str, BookId]])

slots.trader = Slot(uri=ENRON.trader, name="trader", curie=ENRON.curie('trader'),
                   model_uri=ENRON.trader, domain=None, range=Optional[Union[str, PersonId]])

slots.instrument_type = Slot(uri=ENRON.instrument_type, name="instrument_type", curie=ENRON.curie('instrument_type'),
                   model_uri=ENRON.instrument_type, domain=None, range=Optional[Union[str, "InstrumentType"]])

slots.buy_sell = Slot(uri=ENRON.buy_sell, name="buy_sell", curie=ENRON.curie('buy_sell'),
                   model_uri=ENRON.buy_sell, domain=None, range=Optional[Union[str, "BuySell"]])

slots.volume = Slot(uri=ENRON.volume, name="volume", curie=ENRON.curie('volume'),
                   model_uri=ENRON.volume, domain=None, range=Optional[float])

slots.volume_unit = Slot(uri=ENRON.volume_unit, name="volume_unit", curie=ENRON.curie('volume_unit'),
                   model_uri=ENRON.volume_unit, domain=None, range=Optional[Union[str, "VolumeUnit"]])

slots.volume_frequency = Slot(uri=ENRON.volume_frequency, name="volume_frequency", curie=ENRON.curie('volume_frequency'),
                   model_uri=ENRON.volume_frequency, domain=None, range=Optional[str])

slots.price = Slot(uri=ENRON.price, name="price", curie=ENRON.curie('price'),
                   model_uri=ENRON.price, domain=None, range=Optional[float])

slots.price_type = Slot(uri=ENRON.price_type, name="price_type", curie=ENRON.curie('price_type'),
                   model_uri=ENRON.price_type, domain=None, range=Optional[Union[str, "PriceType"]])

slots.price_index = Slot(uri=ENRON.price_index, name="price_index", curie=ENRON.curie('price_index'),
                   model_uri=ENRON.price_index, domain=None, range=Optional[Union[str, PriceIndexId]])

slots.premium_or_adder = Slot(uri=ENRON.premium_or_adder, name="premium_or_adder", curie=ENRON.curie('premium_or_adder'),
                   model_uri=ENRON.premium_or_adder, domain=None, range=Optional[float])

slots.delivery_location = Slot(uri=ENRON.delivery_location, name="delivery_location", curie=ENRON.curie('delivery_location'),
                   model_uri=ENRON.delivery_location, domain=None, range=Optional[Union[str, LocationId]])

slots.delivery_start = Slot(uri=ENRON.delivery_start, name="delivery_start", curie=ENRON.curie('delivery_start'),
                   model_uri=ENRON.delivery_start, domain=None, range=Optional[Union[str, XSDDate]])

slots.delivery_end = Slot(uri=ENRON.delivery_end, name="delivery_end", curie=ENRON.curie('delivery_end'),
                   model_uri=ENRON.delivery_end, domain=None, range=Optional[Union[str, XSDDate]])

slots.deal_status = Slot(uri=ENRON.deal_status, name="deal_status", curie=ENRON.curie('deal_status'),
                   model_uri=ENRON.deal_status, domain=None, range=Optional[str])

slots.master_agreement = Slot(uri=ENRON.master_agreement, name="master_agreement", curie=ENRON.curie('master_agreement'),
                   model_uri=ENRON.master_agreement, domain=None, range=Optional[Union[str, MasterAgreementId]])

slots.confirmation_status = Slot(uri=ENRON.confirmation_status, name="confirmation_status", curie=ENRON.curie('confirmation_status'),
                   model_uri=ENRON.confirmation_status, domain=None, range=Optional[str])

slots.book_code = Slot(uri=ENRON.book_code, name="book_code", curie=ENRON.curie('book_code'),
                   model_uri=ENRON.book_code, domain=None, range=Optional[str])

slots.desk = Slot(uri=ENRON.desk, name="desk", curie=ENRON.curie('desk'),
                   model_uri=ENRON.desk, domain=None, range=Optional[Union[str, TradingDeskId]])

slots.book_type = Slot(uri=ENRON.book_type, name="book_type", curie=ENRON.curie('book_type'),
                   model_uri=ENRON.book_type, domain=None, range=Optional[str])

slots.curve = Slot(uri=ENRON.curve, name="curve", curie=ENRON.curie('curve'),
                   model_uri=ENRON.curve, domain=None, range=Optional[Union[str, PriceCurveId]])

slots.as_of_date = Slot(uri=ENRON.as_of_date, name="as_of_date", curie=ENRON.curie('as_of_date'),
                   model_uri=ENRON.as_of_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.quantity = Slot(uri=ENRON.quantity, name="quantity", curie=ENRON.curie('quantity'),
                   model_uri=ENRON.quantity, domain=None, range=Optional[float])

slots.mtm_value = Slot(uri=ENRON.mtm_value, name="mtm_value", curie=ENRON.curie('mtm_value'),
                   model_uri=ENRON.mtm_value, domain=None, range=Optional[float])

slots.daily_pnl = Slot(uri=ENRON.daily_pnl, name="daily_pnl", curie=ENRON.curie('daily_pnl'),
                   model_uri=ENRON.daily_pnl, domain=None, range=Optional[float])

slots.new_deal_pnl = Slot(uri=ENRON.new_deal_pnl, name="new_deal_pnl", curie=ENRON.curie('new_deal_pnl'),
                   model_uri=ENRON.new_deal_pnl, domain=None, range=Optional[float])

slots.curve_shift_pnl = Slot(uri=ENRON.curve_shift_pnl, name="curve_shift_pnl", curie=ENRON.curie('curve_shift_pnl'),
                   model_uri=ENRON.curve_shift_pnl, domain=None, range=Optional[float])

slots.var_95 = Slot(uri=ENRON.var_95, name="var_95", curie=ENRON.curie('var_95'),
                   model_uri=ENRON.var_95, domain=None, range=Optional[float])

slots.currency = Slot(uri=ENRON.currency, name="currency", curie=ENRON.curie('currency'),
                   model_uri=ENRON.currency, domain=None, range=Optional[str])

slots.trade = Slot(uri=ENRON.trade, name="trade", curie=ENRON.curie('trade'),
                   model_uri=ENRON.trade, domain=None, range=Optional[Union[str, TradeId]])

slots.flow_date = Slot(uri=ENRON.flow_date, name="flow_date", curie=ENRON.curie('flow_date'),
                   model_uri=ENRON.flow_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.flow_month = Slot(uri=ENRON.flow_month, name="flow_month", curie=ENRON.curie('flow_month'),
                   model_uri=ENRON.flow_month, domain=None, range=Optional[str])

slots.nominated_volume = Slot(uri=ENRON.nominated_volume, name="nominated_volume", curie=ENRON.curie('nominated_volume'),
                   model_uri=ENRON.nominated_volume, domain=None, range=Optional[float])

slots.scheduled_volume = Slot(uri=ENRON.scheduled_volume, name="scheduled_volume", curie=ENRON.curie('scheduled_volume'),
                   model_uri=ENRON.scheduled_volume, domain=None, range=Optional[float])

slots.actual_volume = Slot(uri=ENRON.actual_volume, name="actual_volume", curie=ENRON.curie('actual_volume'),
                   model_uri=ENRON.actual_volume, domain=None, range=Optional[float])

slots.imbalance_volume = Slot(uri=ENRON.imbalance_volume, name="imbalance_volume", curie=ENRON.curie('imbalance_volume'),
                   model_uri=ENRON.imbalance_volume, domain=None, range=Optional[float])

slots.invoice_number = Slot(uri=ENRON.invoice_number, name="invoice_number", curie=ENRON.curie('invoice_number'),
                   model_uri=ENRON.invoice_number, domain=None, range=Optional[str])

slots.production_month = Slot(uri=ENRON.production_month, name="production_month", curie=ENRON.curie('production_month'),
                   model_uri=ENRON.production_month, domain=None, range=Optional[str])

slots.invoice_date = Slot(uri=ENRON.invoice_date, name="invoice_date", curie=ENRON.curie('invoice_date'),
                   model_uri=ENRON.invoice_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.due_date = Slot(uri=ENRON.due_date, name="due_date", curie=ENRON.curie('due_date'),
                   model_uri=ENRON.due_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.amount = Slot(uri=ENRON.amount, name="amount", curie=ENRON.curie('amount'),
                   model_uri=ENRON.amount, domain=None, range=Optional[float])

slots.trades = Slot(uri=ENRON.trades, name="trades", curie=ENRON.curie('trades'),
                   model_uri=ENRON.trades, domain=None, range=Optional[Union[Union[str, TradeId], list[Union[str, TradeId]]]])

slots.invoice_status = Slot(uri=ENRON.invoice_status, name="invoice_status", curie=ENRON.curie('invoice_status'),
                   model_uri=ENRON.invoice_status, domain=None, range=Optional[str])

slots.payment_date = Slot(uri=ENRON.payment_date, name="payment_date", curie=ENRON.curie('payment_date'),
                   model_uri=ENRON.payment_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.invoices = Slot(uri=ENRON.invoices, name="invoices", curie=ENRON.curie('invoices'),
                   model_uri=ENRON.invoices, domain=None, range=Optional[Union[Union[str, InvoiceId], list[Union[str, InvoiceId]]]])

slots.direction = Slot(uri=ENRON.direction, name="direction", curie=ENRON.curie('direction'),
                   model_uri=ENRON.direction, domain=None, range=Optional[str])

slots.account_number = Slot(uri=ENRON.account_number, name="account_number", curie=ENRON.curie('account_number'),
                   model_uri=ENRON.account_number, domain=None, range=Optional[str])

slots.account_type = Slot(uri=ENRON.account_type, name="account_type", curie=ENRON.curie('account_type'),
                   model_uri=ENRON.account_type, domain=None, range=Optional[str])

slots.fs_line = Slot(uri=ENRON.fs_line, name="fs_line", curie=ENRON.curie('fs_line'),
                   model_uri=ENRON.fs_line, domain=None, range=Optional[str])

slots.cost_center_code = Slot(uri=ENRON.cost_center_code, name="cost_center_code", curie=ENRON.curie('cost_center_code'),
                   model_uri=ENRON.cost_center_code, domain=None, range=Optional[str])

slots.business_unit = Slot(uri=ENRON.business_unit, name="business_unit", curie=ENRON.curie('business_unit'),
                   model_uri=ENRON.business_unit, domain=None, range=Optional[Union[str, BusinessUnitId]])

slots.document_number = Slot(uri=ENRON.document_number, name="document_number", curie=ENRON.curie('document_number'),
                   model_uri=ENRON.document_number, domain=None, range=Optional[str])

slots.company_code = Slot(uri=ENRON.company_code, name="company_code", curie=ENRON.curie('company_code'),
                   model_uri=ENRON.company_code, domain=None, range=Optional[str])

slots.fiscal_year = Slot(uri=ENRON.fiscal_year, name="fiscal_year", curie=ENRON.curie('fiscal_year'),
                   model_uri=ENRON.fiscal_year, domain=None, range=Optional[int])

slots.posting_date = Slot(uri=ENRON.posting_date, name="posting_date", curie=ENRON.curie('posting_date'),
                   model_uri=ENRON.posting_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.document_type = Slot(uri=ENRON.document_type, name="document_type", curie=ENRON.curie('document_type'),
                   model_uri=ENRON.document_type, domain=None, range=Optional[str])

slots.header_text = Slot(uri=ENRON.header_text, name="header_text", curie=ENRON.curie('header_text'),
                   model_uri=ENRON.header_text, domain=None, range=Optional[str])

slots.entered_by = Slot(uri=ENRON.entered_by, name="entered_by", curie=ENRON.curie('entered_by'),
                   model_uri=ENRON.entered_by, domain=None, range=Optional[Union[str, PersonId]])

slots.lines = Slot(uri=ENRON.lines, name="lines", curie=ENRON.curie('lines'),
                   model_uri=ENRON.lines, domain=None, range=Optional[Union[Union[dict, JournalLine], list[Union[dict, JournalLine]]]])

slots.created = Slot(uri=DCTERMS.created, name="created", curie=DCTERMS.curie('created'),
                   model_uri=ENRON.created, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.author = Slot(uri=DCTERMS.creator, name="author", curie=DCTERMS.curie('creator'),
                   model_uri=ENRON.author, domain=None, range=Optional[str])

slots.custodian = Slot(uri=ENRON.custodian, name="custodian", curie=ENRON.curie('custodian'),
                   model_uri=ENRON.custodian, domain=None, range=Optional[Union[str, PersonId]])

slots.file_id = Slot(uri=ENRON.file_id, name="file_id", curie=ENRON.curie('file_id'),
                   model_uri=ENRON.file_id, domain=None, range=Optional[str])

slots.original_filename = Slot(uri=ENRON.original_filename, name="original_filename", curie=ENRON.curie('original_filename'),
                   model_uri=ENRON.original_filename, domain=None, range=Optional[str])

slots.document_role = Slot(uri=ENRON.document_role, name="document_role", curie=ENRON.curie('document_role'),
                   model_uri=ENRON.document_role, domain=None, range=Optional[Union[str, "DocumentRole"]])

slots.mentions = Slot(uri=SCHEMA.mentions, name="mentions", curie=SCHEMA.curie('mentions'),
                   model_uri=ENRON.mentions, domain=None, range=Optional[Union[Union[str, NamedThingId], list[Union[str, NamedThingId]]]])

slots.sheets = Slot(uri=ENRON.sheets, name="sheets", curie=ENRON.curie('sheets'),
                   model_uri=ENRON.sheets, domain=None, range=Optional[Union[Union[str, WorksheetId], list[Union[str, WorksheetId]]]])

slots.derived_from = Slot(uri=PROV.wasDerivedFrom, name="derived_from", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=ENRON.derived_from, domain=None, range=Optional[Union[Union[str, WorkbookId], list[Union[str, WorkbookId]]]])

slots.version_family = Slot(uri=ENRON.version_family, name="version_family", curie=ENRON.curie('version_family'),
                   model_uri=ENRON.version_family, domain=None, range=Optional[str])

slots.workbook = Slot(uri=ENRON.workbook, name="workbook", curie=ENRON.curie('workbook'),
                   model_uri=ENRON.workbook, domain=None, range=Optional[Union[str, WorkbookId]])

slots.sheet_name = Slot(uri=ENRON.sheet_name, name="sheet_name", curie=ENRON.curie('sheet_name'),
                   model_uri=ENRON.sheet_name, domain=None, range=Optional[str])

slots.sheet_state = Slot(uri=ENRON.sheet_state, name="sheet_state", curie=ENRON.curie('sheet_state'),
                   model_uri=ENRON.sheet_state, domain=None, range=Optional[str])

slots.sheet_role = Slot(uri=ENRON.sheet_role, name="sheet_role", curie=ENRON.curie('sheet_role'),
                   model_uri=ENRON.sheet_role, domain=None, range=Optional[str])

slots.worksheet = Slot(uri=ENRON.worksheet, name="worksheet", curie=ENRON.curie('worksheet'),
                   model_uri=ENRON.worksheet, domain=None, range=Optional[Union[str, WorksheetId]])

slots.cell_range = Slot(uri=ENRON.cell_range, name="cell_range", curie=ENRON.curie('cell_range'),
                   model_uri=ENRON.cell_range, domain=None, range=Optional[str])

slots.header_range = Slot(uri=ENRON.header_range, name="header_range", curie=ENRON.curie('header_range'),
                   model_uri=ENRON.header_range, domain=None, range=Optional[str])

slots.table_role = Slot(uri=ENRON.table_role, name="table_role", curie=ENRON.curie('table_role'),
                   model_uri=ENRON.table_role, domain=None, range=Optional[str])

slots.message_id = Slot(uri=ENRON.message_id, name="message_id", curie=ENRON.curie('message_id'),
                   model_uri=ENRON.message_id, domain=None, range=Optional[str])

slots.sent_at = Slot(uri=ENRON.sent_at, name="sent_at", curie=ENRON.curie('sent_at'),
                   model_uri=ENRON.sent_at, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.sender = Slot(uri=ENRON.sender, name="sender", curie=ENRON.curie('sender'),
                   model_uri=ENRON.sender, domain=None, range=Optional[Union[str, PersonId]])

slots.recipients = Slot(uri=ENRON.recipients, name="recipients", curie=ENRON.curie('recipients'),
                   model_uri=ENRON.recipients, domain=None, range=Optional[Union[Union[str, PersonId], list[Union[str, PersonId]]]])

slots.subject = Slot(uri=ENRON.subject, name="subject", curie=ENRON.curie('subject'),
                   model_uri=ENRON.subject, domain=None, range=Optional[str])

slots.attachments = Slot(uri=ENRON.attachments, name="attachments", curie=ENRON.curie('attachments'),
                   model_uri=ENRON.attachments, domain=None, range=Optional[Union[Union[str, WorkbookId], list[Union[str, WorkbookId]]]])

slots.thread = Slot(uri=ENRON.thread, name="thread", curie=ENRON.curie('thread'),
                   model_uri=ENRON.thread, domain=None, range=Optional[str])

slots.evidence__source_kind = Slot(uri=ENRON.source_kind, name="evidence__source_kind", curie=ENRON.curie('source_kind'),
                   model_uri=ENRON.evidence__source_kind, domain=None, range=Union[str, "EvidenceSourceKind"])

slots.evidence__source_id = Slot(uri=ENRON.source_id, name="evidence__source_id", curie=ENRON.curie('source_id'),
                   model_uri=ENRON.evidence__source_id, domain=None, range=Optional[str])

slots.evidence__locator = Slot(uri=ENRON.locator, name="evidence__locator", curie=ENRON.curie('locator'),
                   model_uri=ENRON.evidence__locator, domain=None, range=Optional[str])

slots.evidence__quote = Slot(uri=ENRON.quote, name="evidence__quote", curie=ENRON.curie('quote'),
                   model_uri=ENRON.evidence__quote, domain=None, range=Optional[str])

slots.evidence__confidence = Slot(uri=ENRON.confidence, name="evidence__confidence", curie=ENRON.curie('confidence'),
                   model_uri=ENRON.evidence__confidence, domain=None, range=Optional[float])

slots.curvePoint__curve = Slot(uri=ENRON.curve, name="curvePoint__curve", curie=ENRON.curie('curve'),
                   model_uri=ENRON.curvePoint__curve, domain=None, range=Union[str, PriceCurveId])

slots.curvePoint__valuation_date = Slot(uri=ENRON.valuation_date, name="curvePoint__valuation_date", curie=ENRON.curie('valuation_date'),
                   model_uri=ENRON.curvePoint__valuation_date, domain=None, range=Union[str, XSDDate])

slots.curvePoint__delivery_start = Slot(uri=ENRON.delivery_start, name="curvePoint__delivery_start", curie=ENRON.curie('delivery_start'),
                   model_uri=ENRON.curvePoint__delivery_start, domain=None, range=Union[str, XSDDate])

slots.curvePoint__value = Slot(uri=ENRON.value, name="curvePoint__value", curie=ENRON.curie('value'),
                   model_uri=ENRON.curvePoint__value, domain=None, range=float)

slots.curvePoint__unit = Slot(uri=ENRON.unit, name="curvePoint__unit", curie=ENRON.curie('unit'),
                   model_uri=ENRON.curvePoint__unit, domain=None, range=Optional[str])

slots.curvePoint__is_synthetic = Slot(uri=ENRON.is_synthetic, name="curvePoint__is_synthetic", curie=ENRON.curie('is_synthetic'),
                   model_uri=ENRON.curvePoint__is_synthetic, domain=None, range=Optional[Union[bool, Bool]])

slots.journalLine__gl_account = Slot(uri=ENRON.gl_account, name="journalLine__gl_account", curie=ENRON.curie('gl_account'),
                   model_uri=ENRON.journalLine__gl_account, domain=None, range=Union[str, GLAccountId])

slots.journalLine__debit_credit = Slot(uri=ENRON.debit_credit, name="journalLine__debit_credit", curie=ENRON.curie('debit_credit'),
                   model_uri=ENRON.journalLine__debit_credit, domain=None, range=Union[str, "DebitCredit"])

slots.journalLine__amount = Slot(uri=ENRON.amount, name="journalLine__amount", curie=ENRON.curie('amount'),
                   model_uri=ENRON.journalLine__amount, domain=None, range=float)

slots.journalLine__cost_center = Slot(uri=ENRON.cost_center, name="journalLine__cost_center", curie=ENRON.curie('cost_center'),
                   model_uri=ENRON.journalLine__cost_center, domain=None, range=Optional[Union[str, CostCenterId]])

slots.journalLine__counterparty = Slot(uri=ENRON.counterparty, name="journalLine__counterparty", curie=ENRON.curie('counterparty'),
                   model_uri=ENRON.journalLine__counterparty, domain=None, range=Optional[Union[str, CounterpartyId]])

slots.journalLine__trading_partner = Slot(uri=ENRON.trading_partner, name="journalLine__trading_partner", curie=ENRON.curie('trading_partner'),
                   model_uri=ENRON.journalLine__trading_partner, domain=None, range=Optional[Union[str, LegalEntityId]])

