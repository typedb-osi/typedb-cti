from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.embedded_relationships import (
        embedded_created_by_properties, embedded_multiple_sample_properties,
        embedded_object_marking_properties, embedded_object_reference_properties,
        embedded_host_vm_properties, embedded_operating_system_properties,
        embedded_installed_software_properties, embedded_analysis_sco_properties,
        embedded_sample_properties
)


kill_chain_phase_mapping = TypeDBDocumentMapping("kill-chain-phase") \
    .key(doc_key="phase_name", attribute="phase-name", quoted=True) \
    .has(doc_key="kill_chain_name", attribute="kill-chain-name", quoted=True, single=True)


external_reference_mapping = TypeDBDocumentMapping("external-reference") \
    .has(doc_key="source_name", attribute="source-name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="url", attribute="url-value", quoted=True, single=True) \
    .has(doc_key="external_id", attribute="external-id", quoted=True, single=True) \
    .stub(doc_key="hashes")


stix_object_properties = PropertyMappings() \
    .key(doc_key="id", attribute="id", quoted=True) \
    .has(doc_key="type", attribute="type", quoted=True, single=True) \
    .has(doc_key="spec_version", attribute="spec-version", quoted=True, single=True)


stix_domain_object_properties = PropertyMappings() \
    .include(stix_object_properties) \
    .has(doc_key="created", attribute="created", single=True) \
    .has(doc_key="modified", attribute="modified", single=True) \
    .has(doc_key="revoked", attribute="revoked", single=True) \
    .has(doc_key="confidence", attribute="confidence", single=True) \
    .has(doc_key="lang", attribute="lang", quoted=True, single=True) \
    .has(doc_key="labels", attribute="label_", quoted=True) \
    .include(embedded_created_by_properties) \
    .include(embedded_object_marking_properties) \
    .relation_and_new_player(
        doc_key="external_references",
        other_player_mapping=external_reference_mapping,
        relation_type="external-reference-ownership",
        self_role="owner",
        other_player_role="external-reference"
    )
# TODO: extensions, granular markings


attack_pattern_mapping = TypeDBDocumentMapping("attack-pattern") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases",
        other_player_mapping=kill_chain_phase_mapping,
        relation_type="kill-chain-phase-ownership",
        self_role="owner",
        other_player_role="kill-chain-phase"
    )


campaign_mapping = TypeDBDocumentMapping("campaign") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen", single=True) \
    .has(doc_key="last_seen", attribute="last-seen", single=True) \
    .has(doc_key="objective", attribute="objective", quoted=True, single=True)


course_of_action_mapping = TypeDBDocumentMapping("course-of-action") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .stub("action") # RESERVED


grouping_mapping = TypeDBDocumentMapping("grouping") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="context", attribute="context", quoted=True, single=True) \
    .include(embedded_object_reference_properties)


identity_mapping = TypeDBDocumentMapping("identity") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="roles", attribute="role_", quoted=True) \
    .has(doc_key="identity_class", attribute="identity-class", quoted=True, single=True) \
    .has(doc_key="sectors", attribute="sector", quoted=True) \
    .has(doc_key="contact_information", attribute="contact-information", quoted=True, single=True)


incident_mapping = TypeDBDocumentMapping("incident") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True)


indicator_mapping = TypeDBDocumentMapping("indicator") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="indicator_types", attribute="indicator-type", quoted=True) \
    .has(doc_key="pattern", attribute="pattern", quoted=True, single=True) \
    .has(doc_key="pattern_type", attribute="pattern-type", quoted=True, single=True) \
    .has(doc_key="pattern_version", attribute="pattern-version", quoted=True, single=True) \
    .has(doc_key="valid_from", attribute="valid-from", single=True) \
    .has(doc_key="valid_until", attribute="valid-until", single=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases",
        other_player_mapping=kill_chain_phase_mapping,
        relation_type="kill-chain-phase-ownership",
        self_role="owner",
        other_player_role="kill-chain-phase"
    )


infrastructure_mapping = TypeDBDocumentMapping("infrastructure") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="infrastructure_types", attribute="infrastructure-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen", single=True) \
    .has(doc_key="last_seen", attribute="last-seen", single=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases",
        other_player_mapping=kill_chain_phase_mapping,
        relation_type="kill-chain-phase-ownership",
        self_role="owner",
        other_player_role="kill-chain-phase"
    )


intrusion_set_mapping = TypeDBDocumentMapping("intrusion-set") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen", single=True) \
    .has(doc_key="last_seen", attribute="last-seen", single=True) \
    .has(doc_key="goals", attribute="goal", quoted=True) \
    .has(doc_key="resource_level", attribute="resource-level", quoted=True, single=True) \
    .has(doc_key="primary_motivation", attribute="primary-motivation", quoted=True, single=True) \
    .has(doc_key="secondary_motivations", attribute="secondary-motivation", quoted=True)


location_mapping = TypeDBDocumentMapping("location") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="latitude", attribute="latitude", single=True) \
    .has(doc_key="longitude", attribute="longitude", single=True) \
    .has(doc_key="precision", attribute="precision", single=True) \
    .has(doc_key="region", attribute="region", quoted=True, single=True) \
    .has(doc_key="country", attribute="country", quoted=True, single=True) \
    .has(doc_key="administrative_area", attribute="administrative-area", quoted=True, single=True) \
    .has(doc_key="city", attribute="city", quoted=True, single=True) \
    .has(doc_key="street_address", attribute="street-address", quoted=True, single=True) \
    .has(doc_key="postal_code", attribute="postal-code", quoted=True, single=True)


malware_mapping = TypeDBDocumentMapping("malware") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="malware_types", attribute="malware-type", quoted=True) \
    .has(doc_key="is_family", attribute="is-family", single=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases",
        other_player_mapping=kill_chain_phase_mapping,
        relation_type="kill-chain-phase-ownership",
        self_role="owner",
        other_player_role="kill-chain-phase"
    ) \
    .has(doc_key="first_seen", attribute="first-seen", single=True) \
    .has(doc_key="last_seen", attribute="last-seen", single=True) \
    .include(embedded_operating_system_properties) \
    .has(doc_key="architecture_execution_envs", attribute="architecture-execution-env", quoted=True) \
    .has(doc_key="implementation_languages", attribute="implementation-language", quoted=True) \
    .has(doc_key="capabilities", attribute="capability", quoted=True) \
    .include(embedded_multiple_sample_properties)


malware_analysis_mapping = TypeDBDocumentMapping("malware-analysis") \
    .include(stix_domain_object_properties) \
    .has(doc_key="product", attribute="product", quoted=True, single=True) \
    .has(doc_key="version", attribute="version", quoted=True, single=True) \
    .include(embedded_host_vm_properties) \
    .include(embedded_operating_system_properties) \
    .include(embedded_installed_software_properties) \
    .has(doc_key="configuration_version", attribute="configuration-version", quoted=True, single=True) \
    .has(doc_key="modules", attribute="module", quoted=True) \
    .has(doc_key="analysis_engine_version", attribute="analysis-engine-version", quoted=True, single=True) \
    .has(doc_key="analysis_definition_version", attribute="analysis-definition-version", quoted=True, single=True) \
    .has(doc_key="submitted", attribute="submitted", single=True) \
    .has(doc_key="analysis_started", attribute="analysis-started", single=True) \
    .has(doc_key="analysis_ended", attribute="analysis-ended", single=True) \
    .has(doc_key="result_name", attribute="result-name", quoted=True, single=True) \
    .has(doc_key="result", attribute="result", quoted=True, single=True)\
    .include(embedded_analysis_sco_properties) \
    .include(embedded_sample_properties)


note_mapping = TypeDBDocumentMapping("note") \
    .include(stix_domain_object_properties) \
    .has(doc_key="abstract", attribute="abstract_", quoted=True, single=True) \
    .has(doc_key="content", attribute="content", quoted=True, single=True) \
    .has(doc_key="authors", attribute="author", quoted=True) \
    .include(embedded_object_reference_properties)


observed_data_mapping = TypeDBDocumentMapping("observed-data") \
    .include(stix_domain_object_properties) \
    .has(doc_key="first_observed", attribute="first-observed", single=True) \
    .has(doc_key="last_observed", attribute="last-observed", single=True) \
    .has(doc_key="number_observed", attribute="number-observed", single=True) \
    .include(embedded_object_reference_properties)


opinion_mapping = TypeDBDocumentMapping("opinion-object") \
    .include(stix_domain_object_properties) \
    .has(doc_key="explanation", attribute="explanation", quoted=True, single=True) \
    .has(doc_key="authors", attribute="author", quoted=True) \
    .has(doc_key="opinion", attribute="opinion", quoted=True, single=True) \
    .include(embedded_object_reference_properties)


report_mapping = TypeDBDocumentMapping("report") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="report_types", attribute="report-type", quoted=True) \
    .has(doc_key="published", attribute="published", single=True) \
    .include(embedded_object_reference_properties)


threat_actor_mapping = TypeDBDocumentMapping("threat-actor") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="threat_actor_types", attribute="threat-actor-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .has(doc_key="first_seen", attribute="first-seen", single=True) \
    .has(doc_key="last_seen", attribute="last-seen", single=True) \
    .has(doc_key="roles", attribute="role_", quoted=True) \
    .has(doc_key="goals", attribute="goal", quoted=True) \
    .has(doc_key="sophistication", attribute="sophistication", quoted=True, single=True) \
    .has(doc_key="resource_level", attribute="resource-level", quoted=True, single=True) \
    .has(doc_key="primary_motivation", attribute="primary-motivation", quoted=True, single=True) \
    .has(doc_key="secondary_motivations", attribute="secondary-motivation", quoted=True) \
    .has(doc_key="personal_motivations", attribute="personal-motivation", quoted=True)


tool_mapping = TypeDBDocumentMapping("tool") \
    .include(stix_domain_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="tool_types", attribute="tool-type", quoted=True) \
    .has(doc_key="aliases", attribute="alias_", quoted=True) \
    .relation_and_new_player(
        doc_key="kill_chain_phases",
        other_player_mapping=kill_chain_phase_mapping,
        relation_type="kill-chain-phase-ownership",
        self_role="owner",
        other_player_role="kill-chain-phase"
    ) \
    .has(doc_key="tool_version", attribute="tool-version", quoted=True, single=True)


vulnerability_mapping = TypeDBDocumentMapping("vulnerability") \
    .include(stix_domain_object_properties) \
    .relation_and_new_player(
        doc_key="external_references",
        other_player_mapping=external_reference_mapping,
        relation_type="external-reference-ownership",
        self_role="owner",
        other_player_role="external-reference"
    ) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True)
