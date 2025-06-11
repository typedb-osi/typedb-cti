from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.sdos import stix_object_properties
from stix_model.embedded_relationships import (
    embedded_contains_properties, embedded_header_from_properties,
    embedded_header_sender_properties, embedded_header_to_properties,
    embedded_header_cc_properties, embedded_header_bcc_properties,
    embedded_raw_email_properties, embedded_file_content_properties
)

# TODO: hashes additional component

artifact_mapping = TypeDBDocumentMapping("artifact") \
    .include(stix_object_properties) \
    .has(doc_key="mime_type", attribute="mime-type", quoted=True) \
    .has(doc_key="payload_bin", attribute="payload-bin", quoted=True) \
    .has(doc_key="url", attribute="url", quoted=True) \
    .has(doc_key="encryption_algorithm", attribute="encryption-algorithm", quoted=True) \
    .has(doc_key="decryption_key", attribute="decryption-key", quoted=True)

autonomous_system_mapping = TypeDBDocumentMapping("autonomous-system") \
    .include(stix_object_properties) \
    .key(doc_key="number", attribute="system-number") \
    .has(doc_key="name", attribute="system-name", quoted=True) \
    .has(doc_key="rir", attribute="rir", quoted=True)

directory_mapping = TypeDBDocumentMapping("directory") \
    .include(stix_object_properties) \
    .key(doc_key="path", attribute="path", quoted=True) \
    .has(doc_key="path_enc", attribute="path-enc", quoted=True) \
    .has(doc_key="ctime", attribute="ctime") \
    .has(doc_key="mtime", attribute="mtime") \
    .has(doc_key="atime", attribute="atime") \
	.include(embedded_contains_properties)

domain_name_mapping = TypeDBDocumentMapping("domain-name") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="domain-value", quoted=True)

email_address_mapping = TypeDBDocumentMapping("email-addr") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="email-value", quoted=True) \
    .has(doc_key="display_name", attribute="display-name", quoted=True)

email_message_mapping = TypeDBDocumentMapping("email-message") \
    .include(stix_object_properties) \
    .has(doc_key="is_multipart", attribute="is-multipart") \
    .has(doc_key="date", attribute="date_") \
    .has(doc_key="content_type", attribute="content-type", quoted=True) \
    .has(doc_key="message_id", attribute="message-id", quoted=True) \
    .has(doc_key="subject", attribute="subject", quoted=True) \
    .has(doc_key="received_lines", attribute="received-line", quoted=True) \
    .has(doc_key="body", attribute="body", quoted=True) \
	.include(embedded_header_from_properties) \
	.include(embedded_header_sender_properties) \
	.include(embedded_header_to_properties) \
	.include(embedded_header_cc_properties) \
	.include(embedded_header_bcc_properties) \
	.include(embedded_raw_email_properties) 

# TODO: body-multipart, email-mime-part-body-raw, email-mime-part-type entity

file_mapping = TypeDBDocumentMapping("file") \
    .include(stix_object_properties) \
    .has(doc_key="size", attribute="size") \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="name_enc", attribute="name-enc", quoted=True) \
    .has(doc_key="magic_number_hex", attribute="magic-number-hex", quoted=True) \
    .has(doc_key="mime_type", attribute="mime-type", quoted=True) \
    .has(doc_key="ctime", attribute="ctime") \
    .has(doc_key="mtime", attribute="mtime") \
    .has(doc_key="atime", attribute="atime") \
	.include(embedded_contains_properties) \
    .include(embedded_file_content_properties)
    


# TODO: decide how we want to model extensions

ipv4_addr_mapping = TypeDBDocumentMapping("ipv4-addr") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="ipv4-value", quoted=True)

ipv6_addr_mapping = TypeDBDocumentMapping("ipv6-addr") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="ipv6-value", quoted=True)

mac_addr_mapping = TypeDBDocumentMapping("mac-addr") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="mac-value", quoted=True)

mutex_mapping = TypeDBDocumentMapping("mutex") \
    .include(stix_object_properties) \
    .key(doc_key="name", attribute="name", quoted=True)

network_traffic_mapping = TypeDBDocumentMapping("network-traffic") \
    .include(stix_object_properties) \
    .has(doc_key="start", attribute="start") \
    .has(doc_key="end", attribute="end_") \
    .has(doc_key="is_active", attribute="is-active") \
    .has(doc_key="src_ref", attribute="src-ref", quoted=True) \
    .has(doc_key="dst_ref", attribute="dst-ref", quoted=True) \
    .has(doc_key="src_port", attribute="src-port") \
    .has(doc_key="dst_port", attribute="dst-port") \
    .has(doc_key="protocol", attribute="protocol", quoted=True) \
    .has(doc_key="src_byte_count", attribute="src-byte-count") \
    .has(doc_key="dst_byte_count", attribute="dst-byte-count") \
    .has(doc_key="src_packets", attribute="src-packets") \
    .has(doc_key="dst_packets", attribute="dst-packets") \
    .has(doc_key="src_payload_ref", attribute="src-payload-ref", quoted=True) \
    .has(doc_key="dst_payload_ref", attribute="dst-payload-ref", quoted=True) \
    .has(doc_key="encapsulates_ref", attribute="encapsulates-ref", quoted=True) \
    .has(doc_key="encapsulated_by_ref", attribute="encapsulated-by-ref", quoted=True)

# TODO: decide how we want to model extensions

process_mapping = TypeDBDocumentMapping("process") \
    .include(stix_object_properties) \
    .has(doc_key="is_hidden", attribute="is-hidden") \
    .has(doc_key="pid", attribute="pid") \
    .has(doc_key="created_time", attribute="created-time") \
    .has(doc_key="cwd", attribute="cwd", quoted=True) \
    .has(doc_key="command_line", attribute="command-line", quoted=True)

software_mapping = TypeDBDocumentMapping("software") \
    .include(stix_object_properties) \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="cpe", attribute="cpe", quoted=True) \
    .has(doc_key="swid", attribute="swid", quoted=True) \
    .has(doc_key="languages", attribute="language", quoted=True) \
    .has(doc_key="vendor", attribute="vendor", quoted=True) \
    .has(doc_key="version", attribute="version", quoted=True)

url_mapping = TypeDBDocumentMapping("url") \
    .include(stix_object_properties) \
    .key(doc_key="value", attribute="url-value", quoted=True)

user_account_mapping = TypeDBDocumentMapping("user-account") \
    .include(stix_object_properties) \
    .has(doc_key="user_id", attribute="user-id", quoted=True) \
    .has(doc_key="credential", attribute="credential", quoted=True) \
    .has(doc_key="account_login", attribute="account-login", quoted=True) \
    .has(doc_key="account_type", attribute="account-type", quoted=True) \
    .has(doc_key="display_name", attribute="display-name", quoted=True) \
    .has(doc_key="is_service_account", attribute="is-service-account") \
    .has(doc_key="is_privileged", attribute="is-privileged") \
    .has(doc_key="can_escalate_privs", attribute="can-escalate-privs") \
    .has(doc_key="is_disabled", attribute="is-disabled") \
    .has(doc_key="account_created", attribute="account-created") \
    .has(doc_key="account_expires", attribute="account-expires") \
    .has(doc_key="credential_last_changed", attribute="credential-last-changed") \
    .has(doc_key="account_first_login", attribute="account-first-login") \
    .has(doc_key="account_last_login", attribute="account-last-login")

windows_registry_key_mapping = TypeDBDocumentMapping("windows-registry-key") \
    .include(stix_object_properties) \
    .has(doc_key="key", attribute="windows-registry-key-string", quoted=True) \
    .has(doc_key="modified_time", attribute="modified-time") \
    .has(doc_key="number_of_subkeys", attribute="number-of-subkeys")

# TODO: ownership relationship

windows_registry_value_mapping = TypeDBDocumentMapping("windows-registry-value") \
    .has(doc_key="name", attribute="name", quoted=True) \
    .has(doc_key="data", attribute="registry-value-data", quoted=True) \
    .has(doc_key="type", attribute="registry-value-data-type", quoted=True)

x509_certificate_mapping = TypeDBDocumentMapping("x509-certificate") \
    .include(stix_object_properties) \
    .has(doc_key="is_self_signed", attribute="is-self-signed") \
    .has(doc_key="hashes", attribute="hash", quoted=True) \
    .has(doc_key="version", attribute="version", quoted=True) \
    .has(doc_key="serial_number", attribute="serial-number", quoted=True) \
    .has(doc_key="signature_algorithm", attribute="signature-algorithm", quoted=True) \
    .has(doc_key="issuer", attribute="issuer", quoted=True) \
    .has(doc_key="validity_not_before", attribute="validity-not-before") \
    .has(doc_key="validity_not_after", attribute="validity-not-after") \
    .has(doc_key="subject", attribute="subject", quoted=True) \
    .has(doc_key="subject_public_key_algorithm", attribute="subject-public-key-algorithm", quoted=True) \
    .has(doc_key="subject_public_key_modulus", attribute="subject-public-key-modulus", quoted=True) \
    .has(doc_key="subject_public_key_exponent", attribute="subject-public-key-exponent") 

