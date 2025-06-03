from stix_model.loaders import TypeDBDocumentLoader, PropertyLoaders
from stix_model.sdos import stix_object_properties

# TODO: hashes additional component

artifact_loader = TypeDBDocumentLoader("a", "isa artifact") \
    .include(stix_object_properties) \
    .has("mime_type", "has mime-type {value}", quoted=True) \
    .has("payload_bin", "has payload-bin {value}", quoted=True) \
    .has("url", "has url {value}", quoted=True) \
    .has("encryption_algorithm", "has encryption-algorithm {value}", quoted=True) \
    .has("decryption_key", "has decryption-key {value}", quoted=True)

autonomous_system_loader = TypeDBDocumentLoader("as", "isa autonomous-system") \
    .include(stix_object_properties) \
    .key("number", "has system-number {value}") \
    .has("name", "has system-name {value}", quoted=True) \
    .has("rir", "has rir {value}", quoted=True)

directory_loader = TypeDBDocumentLoader("d", "isa directory") \
    .include(stix_object_properties) \
    .key("path", "has path {value}", quoted=True) \
    .has("path_enc", "has path-enc {value}", quoted=True) \
    .has("ctime", "has ctime {value}") \
    .has("mtime", "has mtime {value}") \
    .has("atime", "has atime {value}")

domain_name_loader = TypeDBDocumentLoader("dn", "isa domain-name") \
    .include(stix_object_properties) \
    .key("value", "has domain-value {value}", quoted=True)

email_address_loader = TypeDBDocumentLoader("ea", "isa email-addr") \
    .include(stix_object_properties) \
    .key("value", "has email-value {value}", quoted=True) \
    .has("display_name", "has display-name {value}", quoted=True)

email_message_loader = TypeDBDocumentLoader("em", "isa email-message") \
    .include(stix_object_properties) \
    .has("is_multipart", "has is-multipart {value}") \
    .has("date", "has date_ {value}") \
    .has("content_type", "has content-type {value}", quoted=True) \
    .has("message_id", "has message-id {value}", quoted=True) \
    .has("subject", "has subject {value}", quoted=True) \
    .has("received_lines", "has received-line {value}", quoted=True) \
    .has("body", "has body {value}", quoted=True)

file_loader = TypeDBDocumentLoader("f", "isa file") \
    .include(stix_object_properties) \
    .has("size", "has size {value}") \
    .has("name", "has name {value}", quoted=True) \
    .has("name_enc", "has name-enc {value}", quoted=True) \
    .has("magic_number_hex", "has magic-number-hex {value}", quoted=True) \
    .has("mime_type", "has mime-type {value}", quoted=True) \
    .has("ctime", "has ctime {value}") \
    .has("mtime", "has mtime {value}") \
    .has("atime", "has atime {value}") 
