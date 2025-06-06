from stix_model.loaders import TypeDBDocumentMapping, ProperyMappings

stix_relationship_properties = ProperyMappings() \
	.key("id", "has id {value}", quoted=True) \
	.has("type", "has type {value}", quoted=True) \
	.has("spec-version", "has spec-version {value}", quoted=True) \
	.has("created", "has created {value}", quoted=True) \
	.has("modified", "has modified {value}", quoted=True) \
	.has("revoked", "has revoked {value}", quoted=True) \
	.has("confidence", "has confidence {value}", quoted=True) \
	.has("lang", "has lang {value}", quoted=True) \
	.has("label", "has label_ {value}", quoted=True) \
	.has("relationship-type", "has relationship-type {value}", quoted=True) \
	.has("description", "has description {value}", quoted=True) \
	.has("start-time", "has start-time {value}", quoted=True) \
	.has("stop-time", "has stop-time {value}", quoted=True)

uses_loader = TypeDBDocumentMapping(type_="uses") \
	.include(stix_relationship_properties) \
	.links(
		doc_key="source_ref",
		player_lookup="{other_var} has id {value}"
	)
	.links(
		doc_key="target_ref", 
		player_lookup="{other_var} has id {value}"
	)