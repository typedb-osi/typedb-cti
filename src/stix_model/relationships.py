from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.embedded_relationships import embedded_created_by_properties
from stix_model.embedded_relationships import embedded_object_marking_properties

stix_relationship_properties = PropertyMappings() \
    .key(doc_key="id", attribute="id", quoted=True) \
    .has(doc_key="type", attribute="type", quoted=True, single=True) \
    .has(doc_key="spec_version", attribute="spec-version", quoted=True, single=True) \
    .has(doc_key="created", attribute="created", single=True) \
    .has(doc_key="modified", attribute="modified", single=True) \
    .has(doc_key="revoked", attribute="revoked", quoted=True, single=True) \
    .has(doc_key="confidence", attribute="confidence", quoted=True, single=True) \
    .has(doc_key="lang", attribute="lang", quoted=True, single=True) \
    .has(doc_key="label", attribute="label_", quoted=True, single=True) \
    .has(doc_key="relationship_type", attribute="relationship-type", quoted=True, single=True) \
    .has(doc_key="description", attribute="description", quoted=True, single=True) \
    .has(doc_key="start_time", attribute="start-time", single=True) \
    .has(doc_key="stop_time", attribute="stop-time", single=True) \
    .include(embedded_created_by_properties) 


derived_from_mapping = TypeDBDocumentMapping(type_="derived-from") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="deriving-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="derived-target",
        quoted=True,
        single=True,
    )

duplicate_of_mapping = TypeDBDocumentMapping(type_="duplicate-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="duplicating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="duplicated-target",
        quoted=True,
        single=True,
    )

related_to_mapping = TypeDBDocumentMapping(type_="related-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="relating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="related-target",
        quoted=True,
        single=True,
    )

delivers_mapping = TypeDBDocumentMapping(type_="delivers") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="delivering-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="delivered-target",
        quoted=True,
        single=True,
    )

targets_mapping = TypeDBDocumentMapping(type_="targets") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="targeting-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="targeted-target",
        quoted=True,
        single=True,
    )

attributed_to_mapping = TypeDBDocumentMapping(type_="attributed-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="attributing-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="attributed-target",
        quoted=True,
        single=True,
    )

mitigates_mapping = TypeDBDocumentMapping(type_="mitigates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="mitigating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="mitigated-target",
        quoted=True,
        single=True,
    )

indicates_mapping = TypeDBDocumentMapping(type_="indicates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="indicating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="indicated-target",
        quoted=True,
        single=True,
    )

reference_mapping = TypeDBDocumentMapping(type_="reference") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="referencing-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="referenced-target",
        quoted=True,
        single=True,
    )

uses_mapping = TypeDBDocumentMapping(type_="uses") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="using-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref", 
        player_attribute="id",
        role="used-target",
        quoted=True,
        single=True,
    )

located_at_mapping = TypeDBDocumentMapping(type_="located-at") \
    .include(stix_relationship_properties) \
    .include(embedded_object_marking_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="locating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="location-target",
        quoted=True,
        single=True,
    )

originates_from_mapping = TypeDBDocumentMapping(type_="originates-from") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="originating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="origin-target",
        quoted=True,
        single=True,
    )

has_mapping = TypeDBDocumentMapping(type_="has_") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="having-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="had-target",
        quoted=True,
        single=True,
    )

hosts_mapping = TypeDBDocumentMapping(type_="hosts") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="hosting-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="hosted-target",
        quoted=True,
        single=True,
    )

ownership_mapping = TypeDBDocumentMapping(type_="ownership") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="owning-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="owned-target",
        quoted=True,
        single=True,
    )

compromises_mapping = TypeDBDocumentMapping(type_="compromises") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="compromising-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="compromised-target",
        quoted=True,
        single=True,
    )

authored_by_mapping = TypeDBDocumentMapping(type_="authored-by") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="authored-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="author-target",
        quoted=True,
        single=True,
    )

drops_mapping = TypeDBDocumentMapping(type_="drops") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="dropping-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="dropped-target",
        quoted=True,
        single=True,
    )

downloads_mapping = TypeDBDocumentMapping(type_="downloads") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="downloading-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="downloaded-target",
        quoted=True,
        single=True,
    )

exploits_mapping = TypeDBDocumentMapping(type_="exploits") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="exploiting-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="exploited-target",
        quoted=True,
        single=True,
    )

investigates_mapping = TypeDBDocumentMapping(type_="investigates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="investigating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="investigated-target",
        quoted=True,
        single=True,
    )

remediates_mapping = TypeDBDocumentMapping(type_="remediates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="remediating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="remediated-target",
        quoted=True,
        single=True,
    )

based_on_mapping = TypeDBDocumentMapping(type_="based-on") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="basing-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="based-target",
        quoted=True,
        single=True,
    )

communicates_with_mapping = TypeDBDocumentMapping(type_="communicates-with") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="communicating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="communicated-target",
        quoted=True,
        single=True,
    )

consists_of_mapping = TypeDBDocumentMapping(type_="consists-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="consisting-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="consisted-target",
        quoted=True,
        single=True,
    )

controls_mapping = TypeDBDocumentMapping(type_="controls") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="controlling-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="controlled-target",
        quoted=True,
        single=True,
    )

beacons_to_mapping = TypeDBDocumentMapping(type_="beacons-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="beaconing-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="beaconed-target",
        quoted=True,
        single=True,
    )

exfiltrates_to_mapping = TypeDBDocumentMapping(type_="exfiltrates-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="exfiltrating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="exfiltrated-target",
        quoted=True,
        single=True,
    )

variant_of_mapping = TypeDBDocumentMapping(type_="variant-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="varying-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="varied-target",
        quoted=True,
        single=True,
    )

characterizes_mapping = TypeDBDocumentMapping(type_="characterizes") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="characterizing-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="characterized-target",
        quoted=True,
        single=True,
    )

impersonates_mapping = TypeDBDocumentMapping(type_="impersonates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="impersonating-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="impersonated-target",
        quoted=True,
        single=True,
    )

resolves_to_mapping = TypeDBDocumentMapping(type_="resolves-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="resolving-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="resolved-target",
        quoted=True,
        single=True,
    )

belongs_to_mapping = TypeDBDocumentMapping(type_="belongs-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="owned-source",
        quoted=True,
        single=True,
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="owner-target",
        quoted=True,
        single=True,
    )

