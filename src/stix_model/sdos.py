from stix_model.loaders import TypeDBDocumentLoader, PropertyLoaders


# @dataclass
# class AttackPattern:
#     spec_version: str
#     id: str
#     created: str
#     modified: str
    
#     revoked: Optional[bool] = None
#     confidence: Optional[int] = None
#     lang: Optional[str] = None
#     labels: List[str] = field(default_factory=list)
    
#     aliases: List[str] = field(default_factory=list)
    

kill_chain_phase_loader = TypeDBDocumentLoader("kcp", "isa kill-chain-phase") \
    .key("phase_name", "has phase-name {value}", quoted=True) \
    .has("kill_chain_name", "has kill-chain-name {value}", quoted=True)


stix_object_properties = PropertyLoaders() \
    .key("id", "has id {value}", quoted=True) \
    .has("type", "has type {value}", quoted=True) \
    .has("spec_version", "has spec-version {value}", quoted=True) \
    .has("created", "has created {value}") \
    .has("modified", "has modified {value}") \
    .has("revoked", "has revoked {value}") \
    .has("labels", "has label_ {value}", quoted=True) \
    .has("lang", "has lang {value}", quoted=True) \
    .has("defanged", "has defanged {value}")

    # TODO: external references, object markings, granular markings, extensions


attack_pattern_loader = TypeDBDocumentLoader("ap", "isa attack-pattern") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .relation("kill_chain_phases", kill_chain_phase_loader, "kill-chain-phase-ownership (owner: ${var}, kill-chain-phase: ${other_var})")

campaign_loader = TypeDBDocumentLoader("c", "isa campaign") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("first_seen", "has first-seen {value}") \
    .has("last_seen", "has last-seen {value}") \
    .has("objective", "has objective {value}", quoted=True)

course_of_action_loader = TypeDBDocumentLoader("coa", "isa course-of-action") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True)

grouping_loader = TypeDBDocumentLoader("g", "isa grouping") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("context", "has context {value}", quoted=True)

identity_loader = TypeDBDocumentLoader("i", "isa identity") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("roles", "has role_ {value}", quoted=True) \
    .has("identity_class", "has identity-class {value}", quoted=True) \
    .has("sectors", "has sector {value}", quoted=True) \
    .has("contact_information", "has contact-information {value}", quoted=True)

incident_loader = TypeDBDocumentLoader("inc", "isa incident") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) 

indicator_loader = TypeDBDocumentLoader("ind", "isa indicator") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("indicator_types", "has indicator-type {value}", quoted=True) \
    .has("pattern", "has pattern {value}", quoted=True) \
    .has("pattern_type", "has pattern-type {value}", quoted=True) \
    .has("pattern_version", "has pattern-version {value}", quoted=True) \
    .has("valid_from", "has valid-from {value}") \
    .has("valid_until", "has valid-until {value}") \
    .relation("kill_chain_phases", kill_chain_phase_loader, "kill-chain-phase-ownership (owner: ${var}, kill-chain-phase: ${other_var})")

infrastructure_loader = TypeDBDocumentLoader("inf", "isa infrastructure") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("infrastructure_types", "has infrastructure-type {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("first_seen", "has first-seen {value}") \
    .has("last_seen", "has last-seen {value}") \
    .relation("kill_chain_phases", kill_chain_phase_loader, "kill-chain-phase-ownership (owner: ${var}, kill-chain-phase: ${other_var})")

intrusion_set_loader = TypeDBDocumentLoader("is", "isa intrusion-set") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("first_seen", "has first-seen {value}") \
    .has("last_seen", "has last-seen {value}") \
    .has("goals", "has goal {value}", quoted=True) \
    .has("resource_level", "has resource-level {value}", quoted=True) \
    .has("primary_motivation", "has primary-motivation {value}", quoted=True) \
    .has("secondary_motivations", "has secondary-motivation {value}", quoted=True)

location_loader = TypeDBDocumentLoader("loc", "isa location") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("latitude", "has latitude {value}") \
    .has("longitude", "has longitude {value}") \
    .has("precision", "has precision {value}") \
    .has("region", "has region {value}", quoted=True) \
    .has("country", "has country {value}", quoted=True) \
    .has("administrative_area", "has administrative-area {value}", quoted=True) \
    .has("city", "has city {value}", quoted=True) \
    .has("street_address", "has street-address {value}", quoted=True) \
    .has("postal_code", "has postal-code {value}", quoted=True)

malware_loader = TypeDBDocumentLoader("m", "isa malware") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("malware_types", "has malware-type {value}", quoted=True) \
    .has("is_family", "has is-family {value}") \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("first_seen", "has first-seen {value}") \
    .has("last_seen", "has last-seen {value}") \
    .has("architecture_execution_envs", "has architecture-execution-env {value}", quoted=True) \
    .has("implementation_languages", "has implementation-language {value}", quoted=True) \
    .has("capabilities", "has capability {value}", quoted=True) \
    .relation("kill_chain_phases", kill_chain_phase_loader, "kill-chain-phase-ownership (owner: ${var}, kill-chain-phase: ${other_var})")

malware_analysis_loader = TypeDBDocumentLoader("ma", "isa malware-analysis") \
    .include(stix_object_properties) \
    .has("product", "has product {value}", quoted=True) \
    .has("version", "has version {value}", quoted=True) \
    .has("configuration_version", "has configuration-version {value}", quoted=True) \
    .has("modules", "has module {value}", quoted=True) \
    .has("analysis_engine_version", "has analysis-engine-version {value}", quoted=True) \
    .has("analysis_definition_version", "has analysis-definition-version {value}", quoted=True) \
    .has("submitted", "has submitted {value}") \
    .has("analysis_started", "has analysis-started {value}") \
    .has("analysis_ended", "has analysis-ended {value}") \
    .has("result_name", "has result-name {value}", quoted=True) \
    .has("result", "has result {value}", quoted=True)

note_loader = TypeDBDocumentLoader("n", "isa note") \
    .include(stix_object_properties) \
    .has("abstract", "has abstract_ {value}", quoted=True) \
    .has("content", "has content {value}", quoted=True) \
    .has("authors", "has author {value}", quoted=True)

observed_data_loader = TypeDBDocumentLoader("od", "isa observed-data") \
    .include(stix_object_properties) \
    .has("first_observed", "has first-observed {value}") \
    .has("last_observed", "has last-observed {value}") \
    .has("number_observed", "has number-observed {value}")

opinion_loader = TypeDBDocumentLoader("op", "isa opinion") \
    .include(stix_object_properties) \
    .has("explanation", "has explanation {value}", quoted=True) \
    .has("authors", "has author {value}", quoted=True) \
    .has("opinion", "has opinion {value}", quoted=True)

report_loader = TypeDBDocumentLoader("r", "isa report") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("report_types", "has report-type {value}", quoted=True) \
    .has("published", "has published {value}")

threat_actor_loader = TypeDBDocumentLoader("ta", "isa threat-actor") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("threat_actor_types", "has threat-actor-type {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("first_seen", "has first-seen {value}") \
    .has("last_seen", "has last-seen {value}") \
    .has("roles", "has role_ {value}", quoted=True) \
    .has("goals", "has goal {value}", quoted=True) \
    .has("sophistication", "has sophistication {value}", quoted=True) \
    .has("resource_level", "has resource-level {value}", quoted=True) \
    .has("primary_motivation", "has primary-motivation {value}", quoted=True) \
    .has("secondary_motivations", "has secondary-motivation {value}", quoted=True) \
    .has("personal_motivations", "has personal-motivation {value}", quoted=True)

tool_loader = TypeDBDocumentLoader("t", "isa tool") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True) \
    .has("tool_types", "has tool-type {value}", quoted=True) \
    .has("aliases", "has alias_ {value}", quoted=True) \
    .has("tool_version", "has tool-version {value}", quoted=True) \
    .relation("kill_chain_phases", kill_chain_phase_loader, "kill-chain-phase-ownership (owner: ${var}, kill-chain-phase: ${other_var})")

vulnerability_loader = TypeDBDocumentLoader("v", "isa vulnerability") \
    .include(stix_object_properties) \
    .has("name", "has name {value}", quoted=True) \
    .has("description", "has description {value}", quoted=True)

# # TODO: relationship loader

# pipeline = attack_pattern_loader.apply(test_doc)
# query = "\n".join(pipeline)
# print(query)