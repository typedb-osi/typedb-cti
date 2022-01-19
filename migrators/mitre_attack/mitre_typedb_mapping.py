def mitre_entity_to_typedb(mitre_type: str):
    mapper = {
        "attack-pattern": {"type": "attack-pattern", "custom-type": False, 'ignore': False},
        "tool": {"type": "tool", "custom-type": False, 'ignore': False},
        "identity": {"type": "identity", "custom-type": False, 'ignore': False},
        "course-of-action": {"type": "course-of-action", "custom-type": False, 'ignore': False},
        "malware": {"type": "malware", "custom-type": False, 'ignore': False},
        "intrusion-set": {"type": "intrusion-set", "custom-type": False, 'ignore': False},
        "marking_definition": {"type": "marking-definition", "custom-type": False, 'ignore': True}
    }

    mapping = mapper.get(mitre_type, {})

    if mapping == {}:
        mapping = {"type": str(mitre_type), 'custom-type': True, 'ignore': False}
    if mapping['type'] == "marking-definition":
        mapping['ignore'] = True

    return mapping


def mitre_relation_to_typedb(mitre_relation_type: str):
    mapper = {
        "uses": {"type": "use", "active-role": "used-by", "passive-role": "used"},
        "mitigates": {"type": "mitigation", "active-role": "mitigating", "passive-role": "mitigated"},
        "delivers": {"type": "delivery", "active-role": "delivering", "passive-role": "delivered"},
        "targets": {"type": "target", "active-role": "targetting", "passive-role": "targetted"},
        "attributed-to": {"type": "attribution", "active-role": "attributing", "passive-role": "attributed"},
        "indicates": {"type": "indication", "active-role": "indicating", "passive-role": "indicated"},
        "derives": {"type": "derivation", "active-role": "deriving", "passive-role": "derived-from"},
        "duplicate-of": {"type": "duplicate", "active-role": "duplicate-object", "passive-role": "duplicate-object"},
        "related-to": {"type": "relatedness", "active-role": "related-to", "passive-role": "related-to"}
    }

    mapping = mapper.get(mitre_relation_type, {})
    if mapping == {}:
        mapping = {"type": "stix-core-relationship", "active-role": "active-role",
                   "passive-role": "passive-role", "stix-type": mitre_relation_type}
    return mapping


def mitre_attributes_to_typedb():
    mapper = {
        "id": {"type": "stix-id", "value": "string"},
        "created": {"type": "created", "value": "string"},
        "modified": {"type": "modified", "value": "string"},
        "spec_version": {"type": "spec-version", "value": "string"},
        "description": {"type": "description", "value": "string"},
        "name": {"type": "name", "value": "string"},
        "aliases": {"type": "alias", "value": "list"},
        "revoked": {"type": "revoked", "value": "boolean"},
        "is_family": {"type": "is-family", "value": "boolean"},
        "source_name": {"type": "source-name", "value": "string"},
        "url": {"type": "url", "value": "string"},
        "external_id": {"type": "external-id", "value": "string"}
    }
    return mapper
