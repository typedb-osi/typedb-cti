from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings


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
    

kill_chain_phase_loader = TypeDBDocumentMapping("kill-chain-phase") \
    .key(doc_key="phase_name", attribute="phase-name", quoted=True) \
    .has(doc_key="kill_chain_name", attribute="kill-chain-name", quoted=True)


stix_object_properties = PropertyMappings() \
    .key(doc_key="id", attribute="id", quoted=True) \
    .has(doc_key="type", attribute="type", quoted=True) \
    .has(doc_key="spec_version", attribute="spec-version", quoted=True) \
    .has(doc_key="created", attribute="created") \
    .has(doc_key="modified", attribute="modified") \
    .has(doc_key="revoked", attribute="revoked") \
    .has(doc_key="labels", attribute="label_", quoted=True) \
    .has(doc_key="lang", attribute="lang", quoted=True) \
    .has(doc_key="defanged", attribute="defanged")

    # TODO: external references, object markings, granular markings, extensions


attack_pattern_loader = TypeDBDocumentMapping("attack-pattern") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .embedded_relation(doc_key="kill_chain_phases", embedded_loader=kill_chain_phase_loader, relation_type="kill-chain-phase-ownership", self_role="owner", embedded_role="kill-chain-phase")

campaign_loader = TypeDBDocumentMapping("campaign") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .has(doc_key="objective", attribute="objective", quoted=True)

course_of_action_loader = TypeDBDocumentMapping("course-of-action") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True)

grouping_loader = TypeDBDocumentMapping("grouping") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="context", attribute="context", quoted=True)

identity_loader = TypeDBDocumentMapping("identity") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="roles", attribute="role_", quoted=True) \
    .has(doc_key="identity_class", attribute="identity-class", quoted=True) \
    .has(doc_key="sectors", attribute="sector", quoted=True) \
    .has(doc_key="contact_information", attribute="contact-information", quoted=True)

incident_loader = TypeDBDocumentMapping("incident") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) 

indicator_loader = TypeDBDocumentMapping("indicator") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="indicator_types", attribute="indicator-type", quoted=True) \
    .has(doc_key="pattern", attribute="pattern", quoted=True) \
    .has(doc_key="pattern_type", attribute="pattern-type", quoted=True) \
    .has(doc_key="pattern_version", attribute="pattern-version", quoted=True) \
    .has(doc_key="valid_from", attribute="valid-from") \
    .has(doc_key="valid_until", attribute="valid-until") \
    .embedded_relation(doc_key="kill_chain_phases", embedded_loader=kill_chain_phase_loader, relation_type="kill-chain-phase-ownership", self_role="owner", embedded_role="kill-chain-phase")

infrastructure_loader = TypeDBDocumentMapping("infrastructure") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="infrastructure_types", attribute="infrastructure-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .embedded_relation(doc_key="kill_chain_phases", embedded_loader=kill_chain_phase_loader, relation_type="kill-chain-phase-ownership", self_role="owner", embedded_role="kill-chain-phase")

intrusion_set_loader = TypeDBDocumentMapping("intrusion-set") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .has(doc_key="goals", attribute="goal", quoted=True) \
    .has(doc_key="resource_level", attribute="resource-level", quoted=True) \
    .has(doc_key="primary_motivation", attribute="primary-motivation", quoted=True) \
    .has(doc_key="secondary_motivations", attribute="secondary-motivation", quoted=True)

location_loader = TypeDBDocumentMapping("location") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="latitude", attribute="latitude") \
    .has(doc_key="longitude", attribute="longitude") \
    .has(doc_key="precision", attribute="precision") \
    .has(doc_key="region", attribute="region", quoted=True) \
    .has(doc_key="country", attribute="country", quoted=True) \
    .has(doc_key="administrative_area", attribute="administrative-area", quoted=True) \
    .has(doc_key="city", attribute="city", quoted=True) \
    .has(doc_key="street_address", attribute="street-address", quoted=True) \
    .has(doc_key="postal_code", attribute="postal-code", quoted=True)

malware_loader = TypeDBDocumentMapping("malware") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="malware_types", attribute="malware-type", quoted=True) \
    .has(doc_key="is_family", attribute="is-family") \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .has(doc_key="architecture_execution_envs", attribute="architecture-execution-env", quoted=True) \
    .has(doc_key="implementation_languages", attribute="implementation-language", quoted=True) \
    .has(doc_key="capabilities", attribute="capability", quoted=True) \
    .embedded_relation(doc_key="kill_chain_phases", embedded_loader=kill_chain_phase_loader, relation_type="kill-chain-phase-ownership", self_role="owner", embedded_role="kill-chain-phase")

malware_analysis_loader = TypeDBDocumentMapping("malware-analysis") \
    .include(stix_object_properties) \
    .has(doc_key="product", attribute="product", quoted=True) \
    .has(doc_key="version", attribute="version", quoted=True) \
    .has(doc_key="configuration_version", attribute="configuration-version", quoted=True) \
    .has(doc_key="modules", attribute="module", quoted=True) \
    .has(doc_key="analysis_engine_version", attribute="analysis-engine-version", quoted=True) \
    .has(doc_key="analysis_definition_version", attribute="analysis-definition-version", quoted=True) \
    .has(doc_key="submitted", attribute="submitted") \
    .has(doc_key="analysis_started", attribute="analysis-started") \
    .has(doc_key="analysis_ended", attribute="analysis-ended") \
    .has(doc_key="result_name", attribute="result-name", quoted=True) \
    .has(doc_key="result", attribute="result", quoted=True)

note_loader = TypeDBDocumentMapping("note") \
    .include(stix_object_properties) \
    .has(doc_key="abstract", attribute="abstract_", quoted=True) \
    .has(doc_key="content", attribute="content", quoted=True) \
    .has(doc_key="authors", attribute="author", quoted=True)

observed_data_loader = TypeDBDocumentMapping("observed-data") \
    .include(stix_object_properties) \
    .has(doc_key="first_observed", attribute="first-observed") \
    .has(doc_key="last_observed", attribute="last-observed") \
    .has(doc_key="number_observed", attribute="number-observed")

opinion_loader = TypeDBDocumentMapping("opinion") \
    .include(stix_object_properties) \
    .has(doc_key="explanation", attribute="explanation", quoted=True) \
    .has(doc_key="authors", attribute="author", quoted=True) \
    .has(doc_key="opinion", attribute="opinion", quoted=True)

report_loader = TypeDBDocumentMapping("report") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="report_types", attribute="report-type", quoted=True) \
    .has(doc_key="published", attribute="published")

threat_actor_loader = TypeDBDocumentMapping("threat-actor") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="threat_actor_types", attribute="threat-actor-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .has(doc_key="roles", attribute="role_", quoted=True) \
    .has(doc_key="goals", attribute="goal", quoted=True) \
    .has(doc_key="sophistication", attribute="sophistication", quoted=True) \
    .has(doc_key="resource_level", attribute="resource-level", quoted=True) \
    .has(doc_key="primary_motivation", attribute="primary-motivation", quoted=True) \
    .has(doc_key="secondary_motivations", attribute="secondary-motivation", quoted=True) \
    .has(doc_key="personal_motivations", attribute="personal-motivation", quoted=True)

tool_loader = TypeDBDocumentMapping("tool") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="tool_types", attribute="tool-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="tool_version", attribute="tool-version", quoted=True) \
    .embedded_relation(doc_key="kill_chain_phases", embedded_loader=kill_chain_phase_loader, relation_type="kill-chain-phase-ownership", self_role="owner", embedded_role="kill-chain-phase")

vulnerability_loader = TypeDBDocumentMapping("vulnerability") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True)

# # TODO: relationship loader

# pipeline = attack_pattern_loader.apply(test_doc)
# query = "\n".join(pipeline)
# print(query)