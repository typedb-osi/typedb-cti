from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings

stix_relationship_properties = PropertyMappings() \
	.key(doc_key="id", attribute="id", quoted=True) \
	.has(doc_key="type", attribute="type", quoted=True) \
	.has(doc_key="spec-version", attribute="spec-version", quoted=True) \
	.has(doc_key="created", attribute="created") \
	.has(doc_key="modified", attribute="modified") \
	.has(doc_key="revoked", attribute="revoked", quoted=True) \
	.has(doc_key="confidence", attribute="confidence", quoted=True) \
	.has(doc_key="lang", attribute="lang", quoted=True) \
	.has(doc_key="label", attribute="label_", quoted=True) \
	.has(doc_key="relationship-type", attribute="relationship-type", quoted=True) \
	.has(doc_key="description", attribute="description", quoted=True) \
	.has(doc_key="start-time", attribute="start-time") \
	.has(doc_key="stop-time", attribute="stop-time")

uses_loader = TypeDBDocumentMapping(type_="uses") \
	.include(stix_relationship_properties) \
	.links(
		player_attribute_doc_key="source_ref",
		player_attribute="id",
		role="using-source",
		quoted=True
	) \
	.links(
		player_attribute_doc_key="target_ref", 
		player_attribute="id",
		role="used-target",
		quoted=True
	)

