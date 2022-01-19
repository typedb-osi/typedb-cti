import logging

from migrators.mitre.mitre_typedb_mapping import mitre_entity_to_typedb, mitre_attributes_to_typedb, \
    mitre_relation_to_typedb


def sanitise_string(string_value):
    return string_value.replace("'", "")


class MitreInsertGenerator:

    def __init__(self, mitre_objects_json):
        self.mitre_objects_json = mitre_objects_json

    def mitre_objects_referenced(self):
        referenced_ids = set()
        for mitre_object in self.mitre_objects_json:
            if 'created_by_ref' in mitre_object:
                referenced_ids.add(mitre_object['created_by_ref'])

        queries = set()
        for mitre_object in self.mitre_objects_json:
            for referenced_id in referenced_ids:
                if mitre_object['id'] == referenced_id:
                    entity_type = mitre_entity_to_typedb(mitre_object['type'])['type']
                    if entity_type == "identity":
                        entity_type = mitre_object['identity_class']
                    query = "$x isa " + entity_type + "," + self._attributes(mitre_object)
                    query = "insert " + query + ";"
                    queries.add(query)
        logging.debug(f"Generated {len(queries)} insert queries for referenced mitre entities")
        return {
            "queries": queries,
            "processed_ids": referenced_ids
        }

    def statement_markings(self):
        queries = set()
        processed_ids = set()
        for mitre_object in self.mitre_objects_json:
            if mitre_object['type'] == "marking-definition" and mitre_object['definition_type'] == "statement":
                mitre_id = sanitise_string(mitre_object['id'])
                processed_ids.add(mitre_id)
                queries.add(f"insert $x isa statement-marking, "
                            f"has stix-id '{mitre_id}', "
                            f"has statement '{sanitise_string(mitre_object['definition']['statement'])}', "
                            f"has created '{sanitise_string(mitre_object['created'])}',"
                            f" has spec-version '{sanitise_string(mitre_object['spec_version'])}';")
        logging.debug(f"Generated {len(queries)} insert queries for markings")
        return {
            "queries": queries,
            "processed_ids": processed_ids
        }

    def mitre_objects_and_marking_relations(self, exclude_ids):
        mitre_entity_queries = set()
        mitre_objects_with_marking_refs = []

        for mitre_object in self.mitre_objects_json:
            mitre_object_type = mitre_object['type']
            if mitre_object_type != "relationship" and not mitre_object['id'] in exclude_ids:
                stix_type = mitre_entity_to_typedb(mitre_object_type)
                if not stix_type['ignore']:
                    if 'object_marking_refs' in mitre_object and len(mitre_object['object_marking_refs']) > 0:
                        mitre_objects_with_marking_refs.append(mitre_object)

                    if stix_type['custom-type']:
                        query = f"$mitre isa custom-object, has stix-type '{stix_type['type']}'"
                    else:
                        if mitre_object['type'] == "identity":
                            ent_type = mitre_object['identity_class']
                        else:
                            ent_type = mitre_object['type']
                        query = f"$mitre isa {ent_type}"

                    query = "insert " + query + "," + self._attributes(mitre_object) + ";"
                    if 'created_by_ref' in mitre_object:
                        insert_created_by_refs_relation = "(created: $mitre, creator: $creator) isa creation;"
                        # we expect creating stix objects to be inserted before
                        match_creator = f"$creator isa thing, has stix-id '{mitre_object['created_by_ref']}';"
                        query = "match " + match_creator + query + insert_created_by_refs_relation
                    mitre_entity_queries.add(query)

        marking_relations_queries = self._markings_relations(mitre_objects_with_marking_refs)
        queries = mitre_entity_queries.union(marking_relations_queries)
        logging.debug(f"Generated {len(queries)} insert queries for mitre entities and marking relations")
        return queries

    def _markings_relations(self, objects_with_marking_refs):
        queries = set()
        for mitre_object in objects_with_marking_refs:
            match_marked_object = f"$x isa thing, has stix-id '{mitre_object['id']}'; "
            match_object_marking = f"$marking isa marking-definition, has stix-id '{mitre_object['object_marking_refs'][0]}'; "
            marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
            query = "match " + match_marked_object + match_object_marking + "insert " + marking_rel
            queries.add(query)
        return queries

    def _attributes(self, mitre_object):
        query = ""
        for mitre_key, typeql_definition in mitre_attributes_to_typedb().items():
            if mitre_key in mitre_object:
                typeql_attr_type = typeql_definition['type']
                mitre_value_type = typeql_definition['value']
                mitre_value = mitre_object[mitre_key]
                if mitre_value_type == "string":
                    string_value = sanitise_string(mitre_value.replace("'", ""))
                    attribute_query = f" has {typeql_attr_type} '{string_value}',"
                elif mitre_value_type == "boolean":
                    boolean_value = str(mitre_value).lower()
                    attribute_query = f" has {typeql_attr_type} {boolean_value},"
                elif mitre_value_type == "list":
                    attribute_query = ""
                    for value in mitre_value:
                        attribute_query += f" has {typeql_attr_type} '{sanitise_string(value)}',"
                else:
                    logging.info(f"Unrecognised mitre attribute value type: '{mitre_value_type}'")
                    attribute_query = ""
                query += attribute_query
        return query[:-1]

    def mitre_relationships(self):
        relations = set()
        for mitre_object in self.mitre_objects_json:
            if mitre_object['type'] == "relationship":
                match = f"$source has stix-id '{sanitise_string(mitre_object['source_ref'])}'; " \
                        f"$target has stix-id '{sanitise_string(mitre_object['target_ref'])}';"

                relation = mitre_relation_to_typedb(mitre_object['relationship_type'])
                if relation['type'] == "stix-core-relationship":
                    insert = f"({relation['active-role']}: $source, {relation['passive-role']}: $target) " \
                             f"isa {relation['type']}, has stix-type '{sanitise_string(relation['stix-type'])}', "
                else:
                    insert = f"({relation['active-role']}: $source, {relation['passive-role']}: $target) " \
                             f"isa {relation['type']}, "
                insert += self._attributes(mitre_object)
                query = "match " + match + " insert " + insert + ";"
                relations.add(query)
        logging.debug(f"Generated {len(relations)} insert queries for mitre relationships")
        return relations

    def kill_chain_phases(self):
        kill_chain_usages = []
        kill_chain_usages_flattened = set()
        for mitre_object in self.mitre_objects_json:
            if 'kill_chain_phases' in mitre_object:
                for kc in mitre_object['kill_chain_phases']:
                    kill_chain_usages.append({
                        "used_id": mitre_object['id'],
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

    def external_references(self):
        attribute_mapping = mitre_attributes_to_typedb()
        external_reference_entities = set()
        external_reference_relations = set()
        for mitre_object in self.mitre_objects_json:
            if 'external_references' not in mitre_object:
                continue
            match_owner = f"match $x has stix-id '{mitre_object['id']}'"
            for external_reference in mitre_object['external_references']:
                external_reference_attrs = ""
                for mitre_key, mitre_value in external_reference.items():
                    if mitre_key in attribute_mapping:
                        typeql_mapping = attribute_mapping.get(mitre_key, {})
                        assert typeql_mapping["value"] == "string"
                        external_reference_attrs += f" has {typeql_mapping['type']} '{sanitise_string(mitre_value)}',"
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
