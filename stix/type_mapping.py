#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""

This file defines mappings from the STIX types and keys to TypeDB types

"""

def stix_entity_to_typedb(stix_type: str):
    mapper = {
        "attack-pattern": {"type": "attack-pattern", "custom-type": False, 'ignore': False},
        "tool": {"type": "tool", "custom-type": False, 'ignore': False},
        "identity": {"type": "identity", "custom-type": False, 'ignore': False},
        "course-of-action": {"type": "course-of-action", "custom-type": False, 'ignore': False},
        "malware": {"type": "malware", "custom-type": False, 'ignore': False},
        "intrusion-set": {"type": "intrusion-set", "custom-type": False, 'ignore': False},
        "marking_definition": {"type": "marking-definition", "custom-type": False, 'ignore': True}
    }

    mapping = mapper.get(stix_type, {})

    if mapping == {}:
        mapping = {"type": str(stix_type), 'custom-type': True, 'ignore': False}
    if mapping['type'] == "marking-definition":
        mapping['ignore'] = True

    return mapping


def stix_relation_to_typedb(stix_relation_type: str):
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

    mapping = mapper.get(stix_relation_type, {})
    if mapping == {}:
        mapping = {"type": "stix-core-relationship", "active-role": "active-role",
                   "passive-role": "passive-role", "stix-type": stix_relation_type}
    return mapping


def stix_attributes_to_typedb():
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
