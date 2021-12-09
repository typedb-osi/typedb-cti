def entity_mapper(entity: str):

    mapper = {
    	"attack-pattern": {"type": "attack-pattern", "custom-type": False, 'ignore': False},
        "tool": {"type": "tool", "custom-type": False, 'ignore': False},
        "identity": {"type": "identity", "custom-type": False, 'ignore': False},
        "course-of-action": {"type": "course-of-action", "custom-type": False, 'ignore': False},
        "malware": {"type": "malware", "custom-type": False, 'ignore': False},
        "intrusion-set": {"type": "intrusion-set", "custom-type": False, 'ignore': False},
        "marking_definition": {"type": "marking-definition", "custom-type": False, 'ignore': True}    

    }
    mapping = mapper.get(entity, {})

    if mapping == {}:
        mapping = {"type": str(entity), 'custom-type': True, 'ignore': False}
    if mapping['type'] == "marking-definition":
        mapping['ignore'] = True

    return mapping


def relationship_mapper(relationship: str):

    mapper = {
    	"uses": {"relation-name": "use", "active-role": "used-by", "passive-role": "used"},
    	"mitigates": {"relation-name": "mitigation", "active-role": "mitigating", "passive-role": "mitigated"},
        "delivers": {"relation-name": "delivery", "active-role": "delivering", "passive-role": "delivered"},
        "targets": {"relation-name": "target", "active-role": "targetting", "passive-role": "targetted"},
        "attributed-to": {"relation-name": "attribution", "active-role": "attributing", "passive-role": "attributed"},
        "mitigates": {"relation-name": "mitigation", "active-role": "mitigating", "passive-role": "mitigated"},
        "indicates": {"relation-name": "indication", "active-role": "indicating", "passive-role": "indicated"},
        "uses": {"relation-name": "use", "active-role": "used-by", "passive-role": "used"},
        "derives": {"relation-name": "derivation", "active-role": "deriving", "passive-role": "derived-from"},
        "duplicate-of": {"relation-name": "duplicate", "active-role": "duplicate-object", "passive-role": "duplicate-object"},
        "related-to": {"relation-name": "relatedness", "active-role": "related-to", "passive-role": "related-to"}
    }

    mapping = mapper.get(relationship, {})
    if mapping == {}:
        mapping = {"relation-name": "stix-core-relationship", "active-role": "active-role", "passive-role": "passive-role", "stix-type": relationship}
    return mapping


def attribute_map():
    mapper = {
        "id": {"type": "stix-id", "value": "string"},
        "created": {"type": "created", "value": "string"},
        "modified": {"type": "modified", "value": "string"},
        "spec_version": {"type": "spec-version", "value": "string"},
        "description": {"type": "description", "value": "string"},
        "name": {"type": "name", "value": "string"},
        "aliases": {"type": "alias", "value": "list"},
        "revoked": {"type": "revoked", "value": "boolean"},
        "is_family": {"type": "is-family", "value": "boolean"}
    }
    return mapper






















