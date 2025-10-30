from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.sdos import stix_object_properties
from stix_model.embedded_relationships import (
    embedded_analysis_sco_properties,
    embedded_belongs_to_properties,
    embedded_contains_properties,
    embedded_created_by_properties,
    embedded_file_content_properties,
    embedded_header_bcc_properties,
    embedded_header_cc_properties,
    embedded_header_from_properties,
    embedded_header_sender_properties,
    embedded_header_to_properties,
    embedded_host_vm_properties,
    embedded_installed_software_properties,
    embedded_multiple_operating_system_properties,
    embedded_multiple_sample_properties,
    embedded_object_marking_properties,
    embedded_object_reference_properties,
    embedded_operating_system_properties,
    embedded_raw_email_properties,
    embedded_resolves_to_properties,
    embedded_sample_properties
)


# TODO: hashes additional component
stix_cyber_observable_object_properties = PropertyMappings() \
    .include(stix_object_properties) \
    .include(embedded_object_marking_properties) \
    .has(doc_key="defanged", attribute="defanged", single=True) \
# TODO: extensions, granular markings


artifact_mapping = TypeDBDocumentMapping("artifact") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="mime_type", attribute="mime-type", quoted=True, single=True) \
    .has(doc_key="payload_bin", attribute="payload-bin", quoted=True, single=True) \
    .has(doc_key="url", attribute="url-value", quoted=True, single=True) \
    .stub(doc_key="hashes") \
    .has(doc_key="encryption_algorithm", attribute="encryption-algorithm", quoted=True, single=True) \
    .has(doc_key="decryption_key", attribute="decryption-key", quoted=True, single=True)


autonomous_system_mapping = TypeDBDocumentMapping("autonomous-system") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="number", attribute="system-number", single=True) \
    .has(doc_key="name", attribute="system-name", quoted=True, single=True) \
    .has(doc_key="rir", attribute="rir", quoted=True, single=True)


directory_mapping = TypeDBDocumentMapping("directory") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="path", attribute="path", quoted=True, single=True) \
    .has(doc_key="path_enc", attribute="path-enc", quoted=True, single=True) \
    .has(doc_key="ctime", attribute="ctime", single=True) \
    .has(doc_key="mtime", attribute="mtime", single=True) \
    .has(doc_key="atime", attribute="atime", single=True) \
    .include(embedded_contains_properties)


domain_name_mapping = TypeDBDocumentMapping("domain-name") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="domain-value", quoted=True) \
    .include(embedded_resolves_to_properties)


email_address_mapping = TypeDBDocumentMapping("email-addr") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="email-value", quoted=True) \
    .has(doc_key="display_name", attribute="display-name", quoted=True) \
    .include(embedded_belongs_to_properties)


email_message_mapping = TypeDBDocumentMapping("email-message") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="is_multipart", attribute="is-multipart", single=True) \
    .has(doc_key="date", attribute="date_", single=True) \
    .has(doc_key="content_type", attribute="content-type", quoted=True, single=True) \
    .include(embedded_header_from_properties) \
    .include(embedded_header_sender_properties) \
    .include(embedded_header_to_properties) \
    .include(embedded_header_cc_properties) \
    .include(embedded_header_bcc_properties) \
    .has(doc_key="message_id", attribute="message-id", quoted=True, single=True) \
    .has(doc_key="subject", attribute="subject", quoted=True, single=True) \
    .has(doc_key="received_lines", attribute="received-line", quoted=True) \
    .has(doc_key="body", attribute="body", quoted=True, single=True) \
    .stub("body_multipart") \
    .include(embedded_raw_email_properties)


file_mapping = TypeDBDocumentMapping("file") \
    .include(stix_cyber_observable_object_properties) \
    .stub("hashes") \
    .has(doc_key="size", attribute="size", single=True) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="name_enc", attribute="name-enc", quoted=True, single=True) \
    .has(doc_key="magic_number_hex", attribute="magic-number-hex", quoted=True, single=True) \
    .has(doc_key="mime_type", attribute="mime-type", quoted=True, single=True) \
    .has(doc_key="ctime", attribute="ctime", single=True) \
    .has(doc_key="mtime", attribute="mtime", single=True) \
    .has(doc_key="atime", attribute="atime", single=True) \
    .include(embedded_contains_properties) \
    .include(embedded_file_content_properties) \
    .relation_existing_player(
        player_attribute_doc_key="parent_directory_ref",
        player_attribute="id",
        relation_type="contains_",
        self_role="contained",
        player_role="container",
        quoted=True,
        single=True,
    )


# TODO: decide how we want to model extensions

ipv4_addr_mapping = TypeDBDocumentMapping("ipv4-addr") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="ipv4-value", quoted=True, single=True) \
    .include(embedded_resolves_to_properties) \
    .include(embedded_belongs_to_properties)


ipv6_addr_mapping = TypeDBDocumentMapping("ipv6-addr") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="ipv6-value", quoted=True, single=True) \
    .include(embedded_resolves_to_properties) \
    .include(embedded_belongs_to_properties)


mac_addr_mapping = TypeDBDocumentMapping("mac-addr") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="mac-value", quoted=True, single=True)


mutex_mapping = TypeDBDocumentMapping("mutex") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True)


network_traffic_mapping = TypeDBDocumentMapping("network-traffic") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="start", attribute="start", single=True) \
    .has(doc_key="end", attribute="end_", single=True) \
    .has(doc_key="is_active", attribute="is-active", single=True) \
    .has(doc_key="src_ref", attribute="src-ref", quoted=True, single=True) \
    .has(doc_key="dst_ref", attribute="dst-ref", quoted=True, single=True) \
    .has(doc_key="src_port", attribute="src-port", single=True) \
    .has(doc_key="dst_port", attribute="dst-port", single=True) \
    .has(doc_key="protocols", attribute="protocol", quoted=True) \
    .has(doc_key="src_byte_count", attribute="src-byte-count", single=True) \
    .has(doc_key="dst_byte_count", attribute="dst-byte-count", single=True) \
    .has(doc_key="src_packets", attribute="src-packets", single=True) \
    .has(doc_key="dst_packets", attribute="dst-packets", single=True) \
    .has(doc_key="src_payload_ref", attribute="src-payload-ref", quoted=True, single=True) \
    .has(doc_key="dst_payload_ref", attribute="dst-payload-ref", quoted=True, single=True) \
    .has(doc_key="encapsulates_refs", attribute="encapsulates-ref", quoted=True) \
    .has(doc_key="encapsulated_by_ref", attribute="encapsulated-by-ref", quoted=True, single=True)
# TODO: decide how we want to model extensions


process_mapping = TypeDBDocumentMapping("process") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="is_hidden", attribute="is-hidden", single=True) \
    .has(doc_key="pid", attribute="pid", single=True) \
    .has(doc_key="created_time", attribute="created-time", single=True) \
    .has(doc_key="cwd", attribute="cwd", quoted=True, single=True) \
    .has(doc_key="command_line", attribute="command-line", quoted=True, single=True) \
    .stub("environment_variables") \
    .stub("opened_connection_refs") \
    .stub("creator_user_ref") \
    .stub("image_ref") \
    .stub("parent_ref") \
    .stub("child_refs")


software_mapping = TypeDBDocumentMapping("software") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .has(doc_key="cpe", attribute="cpe", quoted=True, single=True) \
    .has(doc_key="swid", attribute="swid", quoted=True, single=True) \
    .has(doc_key="languages", attribute="language", quoted=True) \
    .has(doc_key="vendor", attribute="vendor", quoted=True, single=True) \
    .has(doc_key="version", attribute="version", quoted=True, single=True)


url_mapping = TypeDBDocumentMapping("url") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="value", attribute="url-value", quoted=True, single=True)


user_account_mapping = TypeDBDocumentMapping("user-account") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="user_id", attribute="user-id", quoted=True, single=True) \
    .has(doc_key="credential", attribute="credential", quoted=True, single=True) \
    .has(doc_key="account_login", attribute="account-login", quoted=True, single=True) \
    .has(doc_key="account_type", attribute="account-type", quoted=True, single=True) \
    .has(doc_key="display_name", attribute="display-name", quoted=True, single=True) \
    .has(doc_key="is_service_account", attribute="is-service-account", single=True) \
    .has(doc_key="is_privileged", attribute="is-privileged", single=True) \
    .has(doc_key="can_escalate_privs", attribute="can-escalate-privs", single=True) \
    .has(doc_key="is_disabled", attribute="is-disabled", single=True) \
    .has(doc_key="account_created", attribute="account-created", single=True) \
    .has(doc_key="account_expires", attribute="account-expires", single=True) \
    .has(doc_key="credential_last_changed", attribute="credential-last-changed", single=True) \
    .has(doc_key="account_first_login", attribute="account-first-login", single=True) \
    .has(doc_key="account_last_login", attribute="account-last-login", single=True)


windows_registry_key_mapping = TypeDBDocumentMapping("windows-registry-key") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="key", attribute="windows-registry-key-string", quoted=True, single=True) \
    .stub("values") \
    .has(doc_key="modified_time", attribute="modified-time", single=True) \
    .stub("creator_user_ref") \
    .has(doc_key="number_of_subkeys", attribute="number-of-subkeys", single=True)
# TODO: ownership relationship


windows_registry_value_mapping = TypeDBDocumentMapping("windows-registry-value") \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="data", attribute="registry-value-data", quoted=True) \
    .has(doc_key="type", attribute="registry-value-data-type", quoted=True)


x509_certificate_mapping = TypeDBDocumentMapping("x509-certificate") \
    .include(stix_cyber_observable_object_properties) \
    .has(doc_key="is_self_signed", attribute="is-self-signed", single=True) \
    .stub("hashes") \
    .has(doc_key="version", attribute="version", quoted=True, single=True) \
    .has(doc_key="serial_number", attribute="serial-number", quoted=True, single=True) \
    .has(doc_key="signature_algorithm", attribute="signature-algorithm", quoted=True, single=True) \
    .has(doc_key="issuer", attribute="issuer", quoted=True, single=True) \
    .has(doc_key="validity_not_before", attribute="validity-not-before", single=True) \
    .has(doc_key="validity_not_after", attribute="validity-not-after", single=True) \
    .has(doc_key="subject", attribute="subject", quoted=True, single=True) \
    .has(doc_key="subject_public_key_algorithm", attribute="subject-public-key-algorithm", quoted=True, single=True) \
    .has(doc_key="subject_public_key_modulus", attribute="subject-public-key-modulus", quoted=True, single=True) \
    .has(doc_key="subject_public_key_exponent", attribute="subject-public-key-exponent", single=True)

