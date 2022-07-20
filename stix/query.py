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

import logging

from stix.type_mapping import stix_entity_to_typedb, stix_attributes_to_typedb, stix_relation_to_typedb


def sanitise_string(string_value):
    return string_value.replace("'", "")


class StixInsertGenerator:

    def __init__(self, stix_objects_json,ignore_conditions):
        self.stix_objects_json = stix_objects_json
        self.ignore_conditions = ignore_conditions

    def referenced_stix_objects(self):
        referenced_ids = set()
        for stix_object in self.stix_objects_json:
            if 'created_by_ref' in stix_object:
                referenced_ids.add(stix_object['created_by_ref'])

        queries = set()
        for stix_object in self.stix_objects_json:
            for referenced_id in referenced_ids:
                if stix_object['id'] == referenced_id:
                    entity_type = stix_entity_to_typedb(stix_object['type'])['type']
                    if entity_type == "identity":
                        entity_type = stix_object['identity_class']
                    query = "$x isa " + entity_type + "," + self._attributes(stix_object)
                    query = "insert " + query + ";"
                    queries.add(query)
        logging.debug(f"Generated {len(queries)} insert queries for referenced stix entities")
        return {
            "queries": queries,
            "processed_ids": referenced_ids
        }

    def statement_markings(self):
        queries = set()
        processed_ids = set()
        for stix_object in self.stix_objects_json:
            if stix_object['type'] == "marking-definition" and stix_object['definition_type'] == "statement":
                processed_ids.add(stix_object['id'])
                queries.add(f"insert $x isa statement-marking, "
                            f"has stix-id '{stix_object['id']}', "
                            f"has statement '{sanitise_string(stix_object['definition']['statement'])}', "
                            f"has created '{sanitise_string(stix_object['created'])}',"
                            f" has spec-version '{sanitise_string(stix_object['spec_version'])}';")
        logging.debug(f"Generated {len(queries)} insert queries for markings")
        return {
            "queries": queries,
            "processed_ids": processed_ids
        }

    def stix_objects_and_marking_relations(self, exclude_ids):
        stix_entity_queries = set()
        stix_objects_with_marking_refs = []
        ignored = []
        for stix_object in self.stix_objects_json:
            stix_object_type = stix_object['type']

            skip_check = False
            #skip the object if if deprecated which is default behaviour
            for check in self.ignore_conditions:
                # atomic filter check
                conditions = []
                for attr_name in check.keys():
                    if attr_name in stix_object:
                        atom_check = stix_object[attr_name] == check[attr_name]
                        conditions.append(atom_check)
                # we can skip the entire object
                if all(conditions): 
                    
                    skip_check = True
                    break
            
            if skip_check: 
                ignored.append(stix_object['id'])
                continue

            if stix_object_type != "relationship" and not stix_object['id'] in exclude_ids:
                stix_type = stix_entity_to_typedb(stix_object_type)
                if not stix_type['ignore']:
                    if 'object_marking_refs' in stix_object and len(stix_object['object_marking_refs']) > 0:
                        stix_objects_with_marking_refs.append(stix_object)

                    if stix_type['custom-type']:
                        query = f"$stix isa custom-object, has stix-type '{stix_type['type']}'"
                    else:
                        if stix_object['type'] == "identity":
                            ent_type = stix_object['identity_class']
                        else:
                            ent_type = stix_object['type']
                        query = f"$stix isa {ent_type}"

                    query = "insert " + query + "," + self._attributes(stix_object) + ";"
                    if 'created_by_ref' in stix_object:
                        insert_created_by_refs_relation = "(created: $stix, creator: $creator) isa creation;"
                        # we expect creating stix objects to be inserted before
                        match_creator = f"$creator isa thing, has stix-id '{stix_object['created_by_ref']}';"
                        query = "match " + match_creator + query + insert_created_by_refs_relation
                    stix_entity_queries.add(query)

        marking_relations_queries = self._markings_relations(stix_objects_with_marking_refs)
        logging.debug(f"Generated {len(stix_entity_queries)} insert queries for stix entities")
        logging.debug(f"Generated {len(marking_relations_queries)} insert queries for marking relations")
        print(f"Skipped {len(ignored)} objects based on conditions")
        return {
            "stix_entities": stix_entity_queries,
            "marking_relations": marking_relations_queries
        }

    def _markings_relations(self, objects_with_marking_refs):
        queries = set()
        for stix_object in objects_with_marking_refs:
            match_marked_object = f"$x isa thing, has stix-id '{stix_object['id']}'; "
            match_object_marking = f"$marking isa marking-definition, has stix-id '{stix_object['object_marking_refs'][0]}'; "
            marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
            query = "match " + match_marked_object + match_object_marking + "insert " + marking_rel
            queries.add(query)
        return queries

    def stix_relationships(self):
        relations = set()
        for stix_object in self.stix_objects_json:
            if stix_object['type'] == "relationship":
                match = f"$source has stix-id '{sanitise_string(stix_object['source_ref'])}'; " \
                        f"$target has stix-id '{sanitise_string(stix_object['target_ref'])}';"

                relation = stix_relation_to_typedb(stix_object['relationship_type'])
                if relation['type'] == "stix-core-relationship":
                    insert = f"({relation['active-role']}: $source, {relation['passive-role']}: $target) " \
                             f"isa {relation['type']}, has stix-type '{sanitise_string(relation['stix-type'])}', "
                else:
                    insert = f"({relation['active-role']}: $source, {relation['passive-role']}: $target) " \
                             f"isa {relation['type']}, "
                insert += self._attributes(stix_object)
                query = "match " + match + " insert " + insert + ";"
                relations.add(query)
        logging.debug(f"Generated {len(relations)} insert queries for stix relationships")
        return relations

    def kill_chain_phases(self):
        kill_chain_usages = []
        kill_chain_usages_flattened = set()
        for stix_object in self.stix_objects_json:
            if 'kill_chain_phases' in stix_object:
                for kc in stix_object['kill_chain_phases']:
                    kill_chain_usages.append({
                        "used_id": stix_object['id'],
                        "kill_chain": kc
                    })
                    kill_chain_usages_flattened.add((kc['kill_chain_name'], kc['phase_name']))

        kill_chain_phase_entities = set()
        for kill_chain_usage in kill_chain_usages_flattened:
            query = f"insert $x isa kill-chain-phase, " \
                    f"has kill-chain-name '{kill_chain_usage[0]}', " \
                    f"has phase-name '{kill_chain_usage[1]}';"
            kill_chain_phase_entities.add(query)

        kill_chain_phase_usage_relations = set()
        for kill_chain_usage in kill_chain_usages:
            kill_chain_name = sanitise_string(kill_chain_usage["kill_chain"]['kill_chain_name'])
            kill_chain_phase = sanitise_string(kill_chain_usage["kill_chain"]["phase_name"])
            relation_query = f"match " \
                             f"$x isa thing, has stix-id '{kill_chain_usage['used_id']}'; " \
                             f"$kill-chain-phase isa kill-chain-phase, has kill-chain-name '{kill_chain_name}', " \
                             f"has phase-name '{kill_chain_phase}'; " \
                             f"insert (kill-chain-used: $x, kill-chain-using: $kill-chain-phase) isa kill-chain-usage;"
            kill_chain_phase_usage_relations.add(relation_query)

        logging.debug(f"Generated {len(kill_chain_phase_entities)} insert queries for kill chain phase entities")
        logging.debug(
            f"Generated {len(kill_chain_phase_usage_relations)} insert queries for kill chain phase usage relations"
        )
        return {
            "kill_chain_phases": kill_chain_phase_entities,
            "kill_chain_phase_usages": kill_chain_phase_usage_relations
        }

    def _attributes(self, stix_object):
        query = ""
        for stix_key, typeql_definition in stix_attributes_to_typedb().items():
            if stix_key in stix_object:
                typeql_attr_type = typeql_definition['type']
                stix_value_type = typeql_definition['value']
                stix_value = stix_object[stix_key]
                if stix_value_type == "string":
                    string_value = sanitise_string(stix_value.replace("'", ""))
                    attribute_query = f" has {typeql_attr_type} '{string_value}',"
                elif stix_value_type == "boolean":
                    boolean_value = str(stix_value).lower()
                    attribute_query = f" has {typeql_attr_type} {boolean_value},"
                elif stix_value_type == "list":
                    attribute_query = ""
                    for value in stix_value:
                        attribute_query += f" has {typeql_attr_type} '{sanitise_string(value)}',"
                else:
                    logging.info(f"Unrecognised stix attribute value type: '{stix_value_type}'")
                    attribute_query = ""
                query += attribute_query
        return query[:-1]

    def external_references(self):
        attribute_mapping = stix_attributes_to_typedb()
        external_reference_entities = set()
        external_reference_relations = set()
        for stix_object in self.stix_objects_json:
            if 'external_references' not in stix_object:
                continue
            match_owner = f"match $x has stix-id '{stix_object['id']}'"
            for external_reference in stix_object['external_references']:
                external_reference_attrs = ""
                for stix_key, stix_value in external_reference.items():
                    if stix_key in attribute_mapping:
                        typeql_mapping = attribute_mapping.get(stix_key, {})
                        assert typeql_mapping["value"] == "string"
                        external_reference_attrs += f" has {typeql_mapping['type']} '{sanitise_string(stix_value)}',"
                external_reference_entity = "insert $er isa external-reference," + external_reference_attrs[:-1] + ';'
                external_reference_entities.add(external_reference_entity)
                external_reference_relation = f"{match_owner}; " \
                                              f"$er isa external-reference, {external_reference_attrs[:-1]}; " \
                                              f"insert (referencing: $x, referenced: $er) isa external-referencing;"
                external_reference_relations.add(external_reference_relation)
        logging.debug(f"Generated {len(external_reference_entities)} insert queries for external reference entities")
        logging.debug(f"Generated {len(external_reference_relations)} insert queries for external reference relations")
        return {
            "external_references": external_reference_entities,
            "external_reference_relations": external_reference_relations
        }
