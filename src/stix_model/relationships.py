from stix_model.loaders import TypeDBDocumentMapping, PropertyMappings
from stix_model.embedded_relationships import embedded_created_by_properties

stix_relationship_properties = PropertyMappings() \
    .key(doc_key="id", attribute="id", quoted=True) \
    .has(doc_key="type", attribute="type", quoted=True) \
    .has(doc_key="spec_version", attribute="spec-version", quoted=True) \
    .has(doc_key="created", attribute="created") \
    .has(doc_key="modified", attribute="modified") \
    .has(doc_key="revoked", attribute="revoked", quoted=True) \
    .has(doc_key="confidence", attribute="confidence", quoted=True) \
    .has(doc_key="lang", attribute="lang", quoted=True) \
    .has(doc_key="label", attribute="label_", quoted=True) \
    .has(doc_key="relationship_type", attribute="relationship-type", quoted=True) \
    .has(doc_key="description", attribute="description", quoted=True) \
    .has(doc_key="start_time", attribute="start-time") \
    .has(doc_key="stop_time", attribute="stop-time") \
    .include(embedded_created_by_properties) 


derived_from_mapping = TypeDBDocumentMapping(type_="derived-from") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="deriving-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="derived-target",
        quoted=True
    )

duplicate_of_mapping = TypeDBDocumentMapping(type_="duplicate-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="duplicating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="duplicated-target",
        quoted=True
    )

related_to_mapping = TypeDBDocumentMapping(type_="related-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="relating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="related-target",
        quoted=True
    )

delivers_mapping = TypeDBDocumentMapping(type_="delivers") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="delivering-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="delivered-target",
        quoted=True
    )

targets_mapping = TypeDBDocumentMapping(type_="targets") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="targeting-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="targeted-target",
        quoted=True
    )

attributed_to_mapping = TypeDBDocumentMapping(type_="attributed-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="attributing-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="attributed-target",
        quoted=True
    )

mitigates_mapping = TypeDBDocumentMapping(type_="mitigates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="mitigating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="mitigated-target",
        quoted=True
    )

indicates_mapping = TypeDBDocumentMapping(type_="indicates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="indicating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="indicated-target",
        quoted=True
    )

reference_mapping = TypeDBDocumentMapping(type_="reference") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="referencing-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="referenced-target",
        quoted=True
    )

uses_mapping = TypeDBDocumentMapping(type_="uses") \
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

located_at_mapping = TypeDBDocumentMapping(type_="located-at") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="locating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="location-target",
        quoted=True
    )

originates_from_mapping = TypeDBDocumentMapping(type_="originates-from") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="originating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="origin-target",
        quoted=True
    )

has_mapping = TypeDBDocumentMapping(type_="has_") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="having-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="had-target",
        quoted=True
    )

hosts_mapping = TypeDBDocumentMapping(type_="hosts") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="hosting-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="hosted-target",
        quoted=True
    )

ownership_mapping = TypeDBDocumentMapping(type_="ownership") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="owning-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="owned-target",
        quoted=True
    )

compromises_mapping = TypeDBDocumentMapping(type_="compromises") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="compromising-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="compromised-target",
        quoted=True
    )

authored_by_mapping = TypeDBDocumentMapping(type_="authored-by") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="authored-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="author-target",
        quoted=True
    )

drops_mapping = TypeDBDocumentMapping(type_="drops") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="dropping-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="dropped-target",
        quoted=True
    )

downloads_mapping = TypeDBDocumentMapping(type_="downloads") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="downloading-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="downloaded-target",
        quoted=True
    )

exploits_mapping = TypeDBDocumentMapping(type_="exploits") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="exploiting-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="exploited-target",
        quoted=True
    )

investigates_mapping = TypeDBDocumentMapping(type_="investigates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="investigating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="investigated-target",
        quoted=True
    )

remediates_mapping = TypeDBDocumentMapping(type_="remediates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="remediating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="remediated-target",
        quoted=True
    )

based_on_mapping = TypeDBDocumentMapping(type_="based-on") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="basing-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="based-target",
        quoted=True
    )

communicates_with_mapping = TypeDBDocumentMapping(type_="communicates-with") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="communicating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="communicated-target",
        quoted=True
    )

consists_of_mapping = TypeDBDocumentMapping(type_="consists-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="consisting-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="consisted-target",
        quoted=True
    )

controls_mapping = TypeDBDocumentMapping(type_="controls") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="controlling-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="controlled-target",
        quoted=True
    )

beacons_to_mapping = TypeDBDocumentMapping(type_="beacons-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="beaconing-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="beaconed-target",
        quoted=True
    )

exfiltrates_to_mapping = TypeDBDocumentMapping(type_="exfiltrates-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="exfiltrating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="exfiltrated-target",
        quoted=True
    )

variant_of_mapping = TypeDBDocumentMapping(type_="variant-of") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="varying-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="varied-target",
        quoted=True
    )

characterizes_mapping = TypeDBDocumentMapping(type_="characterizes") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="characterizing-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="characterized-target",
        quoted=True
    )

impersonates_mapping = TypeDBDocumentMapping(type_="impersonates") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="impersonating-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="impersonated-target",
        quoted=True
    )

resolves_to_mapping = TypeDBDocumentMapping(type_="resolves-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="resolving-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="resolved-target",
        quoted=True
    )

belongs_to_mapping = TypeDBDocumentMapping(type_="belongs-to") \
    .include(stix_relationship_properties) \
    .links(
        player_attribute_doc_key="source_ref",
        player_attribute="id",
        role="owned-source",
        quoted=True
    ) \
    .links(
        player_attribute_doc_key="target_ref",
        player_attribute="id",
        role="owner-target",
        quoted=True
    )

