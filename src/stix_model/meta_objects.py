from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.sdos import stix_object_properties
from stix_model.embedded_relationships import embedded_created_by_properties, embedded_object_marking_properties


stix_meta_object_properties = PropertyMappings() \
    .include(stix_object_properties) \
    .include(embedded_created_by_properties) \
    .include(embedded_object_marking_properties)


marking_definition_mapping = TypeDBDocumentMapping("marking-definition") \
    .include(stix_meta_object_properties) \
    .has(doc_key="created", attribute="created", single=True) \
    .has(doc_key="name", attribute="name", quoted=True, single=True) \
    .stub("definition_type") \
    .stub("definition")
