from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.embedded_relationships import (
    embedded_created_by_properties, embedded_object_marking_properties,
    embedded_object_reference_properties, embedded_host_vm_properties,
    embedded_operating_system_properties, embedded_installed_software_properties,
    embedded_analysis_sco_properties, embedded_sample_properties
)


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
    

kill_chain_phase_mapping = TypeDBDocumentMapping("kill-chain-phase") \
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
    .has(doc_key="defanged", attribute="defanged") \
    .include(embedded_created_by_properties) \
    .include(embedded_object_marking_properties) 

# TODO: extensions, external references, object markings, granular markings, extensions


attack_pattern_mapping = TypeDBDocumentMapping("attack-pattern") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases", 
        other_player_mapping=kill_chain_phase_mapping, 
        relation_type="kill-chain-phase-ownership", 
        self_role="owner", 
        other_player_role="kill-chain-phase"
    )

campaign_mapping = TypeDBDocumentMapping("campaign") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .has(doc_key="objective", attribute="objective", quoted=True)

course_of_action_mapping = TypeDBDocumentMapping("course-of-action") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True)

grouping_mapping = TypeDBDocumentMapping("grouping") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="context", attribute="context", quoted=True) \
    .include(embedded_object_reference_properties)

identity_mapping = TypeDBDocumentMapping("identity") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="roles", attribute="role_", quoted=True) \
    .has(doc_key="identity_class", attribute="identity-class", quoted=True) \
    .has(doc_key="sectors", attribute="sector", quoted=True) \
    .has(doc_key="contact_information", attribute="contact-information", quoted=True)

incident_mapping = TypeDBDocumentMapping("incident") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) 

indicator_mapping = TypeDBDocumentMapping("indicator") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="indicator_types", attribute="indicator-type", quoted=True) \
    .has(doc_key="pattern", attribute="pattern", quoted=True) \
    .has(doc_key="pattern_type", attribute="pattern-type", quoted=True) \
    .has(doc_key="pattern_version", attribute="pattern-version", quoted=True) \
    .has(doc_key="valid_from", attribute="valid-from") \
    .has(doc_key="valid_until", attribute="valid-until") \
    .relation_and_new_player(
        doc_key="kill_chain_phases", 
        other_player_mapping=kill_chain_phase_mapping, 
        relation_type="kill-chain-phase-ownership", 
        self_role="owner", 
        other_player_role="kill-chain-phase"
    )

infrastructure_mapping = TypeDBDocumentMapping("infrastructure") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="infrastructure_types", attribute="infrastructure-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen") \
    .has(doc_key="last_seen", attribute="last-seen") \
    .relation_and_new_player(
        doc_key="kill_chain_phases", 
        other_player_mapping=kill_chain_phase_mapping, 
        relation_type="kill-chain-phase-ownership", 
        self_role="owner", 
        other_player_role="kill-chain-phase"
    )

intrusion_set_mapping = TypeDBDocumentMapping("intrusion-set") \
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

location_mapping = TypeDBDocumentMapping("location") \
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

malware_mapping = TypeDBDocumentMapping("malware") \
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
    .relation_and_new_player(
        doc_key="kill_chain_phases", 
        other_player_mapping=kill_chain_phase_mapping, 
        relation_type="kill-chain-phase-ownership", 
        self_role="owner", 
        other_player_role="kill-chain-phase"
    ) \
    .include(embedded_operating_system_properties) \
    .include(embedded_sample_properties) 


malware_analysis_mapping = TypeDBDocumentMapping("malware-analysis") \
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
    .has(doc_key="result", attribute="result", quoted=True)\
    .include(embedded_host_vm_properties) \
    .include(embedded_operating_system_properties) \
    .include(embedded_installed_software_properties) \
    .include(embedded_analysis_sco_properties) \
    .include(embedded_sample_properties) 


note_mapping = TypeDBDocumentMapping("note") \
    .include(stix_object_properties) \
    .has(doc_key="abstract", attribute="abstract_", quoted=True) \
    .has(doc_key="content", attribute="content", quoted=True) \
    .has(doc_key="authors", attribute="author", quoted=True) \
    .include(embedded_object_reference_properties)

observed_data_mapping = TypeDBDocumentMapping("observed-data") \
    .include(stix_object_properties) \
    .has(doc_key="first_observed", attribute="first-observed") \
    .has(doc_key="last_observed", attribute="last-observed") \
    .has(doc_key="number_observed", attribute="number-observed") \
    .include(embedded_object_reference_properties)

opinion_mapping = TypeDBDocumentMapping("opinion") \
    .include(stix_object_properties) \
    .has(doc_key="explanation", attribute="explanation", quoted=True) \
    .has(doc_key="authors", attribute="author", quoted=True) \
    .has(doc_key="opinion", attribute="opinion", quoted=True) \
    .include(embedded_object_reference_properties)

report_mapping = TypeDBDocumentMapping("report") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="report_types", attribute="report-type", quoted=True) \
    .has(doc_key="published", attribute="published") \
    .include(embedded_object_reference_properties)

threat_actor_mapping = TypeDBDocumentMapping("threat-actor") \
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

tool_mapping = TypeDBDocumentMapping("tool") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="tool_types", attribute="tool-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="tool_version", attribute="tool-version", quoted=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases", 
        other_player_mapping=kill_chain_phase_mapping, 
        relation_type="kill-chain-phase-ownership", 
        self_role="owner",
        other_player_role="kill-chain-phase"
    )

vulnerability_mapping = TypeDBDocumentMapping("vulnerability") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True)

# # TODO: relationship loader

# pipeline = attack_pattern_mapping.apply(test_doc)
# query = "\n".join(pipeline)
# print(query)
