import logging

from migrators.mitre_attack.concept_mapper import mitre_object_entity_definitions, mitre_object_attribute_definitions


def sanitise_string(string_value):
    return string_value.replace("'", "")


class InsertQueriesGenerator:

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
                    entity_type = mitre_object_entity_definitions(mitre_object['type'])['type']
                    if entity_type == "identity":
                        entity_type = mitre_object['identity_class']
                    query = "$x isa " + entity_type + "," + self.attributes(mitre_object)
                    query = "insert " + query + ";"
                    queries.add(query)
        logging.debug(f"Generated {len(queries)} insert queries for created_by_refs")
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
                stix_type = mitre_object_entity_definitions(mitre_object_type)
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

                    query = "insert " + query + "," + self.attributes(mitre_object) + ";"
                    if 'created_by_ref' in mitre_object:
                        insert_created_by_refs_relation = "(created: $mitre, creator: $creator) isa creation;"
                        # we expect creating stix objects to be inserted before
                        match_creator = f"$creator isa thing, has stix-id '{mitre_object['created_by_ref']}';"
                        query = "match " + match_creator + query + insert_created_by_refs_relation
                    mitre_entity_queries.add(query)

        marking_relations_queries = self.markings_relations(mitre_objects_with_marking_refs)
        queries = mitre_entity_queries.union(marking_relations_queries)
        logging.debug(f"Generated {len(queries)} insert queries for mitre entities and marking relations")
        return queries

    def markings_relations(self, objects_with_marking_refs):
        queries = set()
        for mitre_object in objects_with_marking_refs:
            match_marked_object = f"$x isa thing, has stix-id '{mitre_object['id']}'; "
            match_object_marking = f"$marking isa marking-definition, has stix-id '{mitre_object['object_marking_refs'][0]}'; "
            marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
            query = "match " + match_marked_object + match_object_marking + "insert " + marking_rel
            queries.add(query)
        return queries

    def attributes(self, mitre_object):
        query = ""
        for mitre_key, typeql_definition in mitre_object_attribute_definitions().items():
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

    #
    # def createRelationQueries(file):
    #     queries = []
    #     relations = []
    #     for obj in file:
    #         if obj['type'] == "relationship":
    #
    #             relations.append(obj['relationship_type'])
    #             relation = relationship_mapper(obj['relationship_type'])
    #
    #             match_query = "match $source isa thing, has stix-id '" + obj[
    #                 'source_ref'] + "'; $target isa thing, has stix-id '" + obj['target_ref'] + "'; "
    #             if relation['relation-name'] == "stix-core-relationship":
    #                 insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation[
    #                     'passive-role'] + ": $target) isa " + relation['relation-name'] + ", has stix-type '" + \
    #                                relation[
    #                                    'stix-type'] + "',"
    #             else:
    #                 insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation[
    #                     'passive-role'] + ": $target) isa " + relation['relation-name'] + ","
    #
    #             insert_query = attributeBuilder(obj, insert_query)
    #
    #             query = match_query + insert_query[:-1] + ";"
    #             queries.append(query)
    #
    #     return set(queries)
    #
    # def insertKillChainPhases(file, uri, batch_size, num_threads):
    #     kill_chain_usage = []
    #     for obj in file:
    #         try:
    #             for k in obj:
    #
    #                 for kc in obj['kill_chain_phases']:
    #                     kc['id'] = obj['id']
    #                 kill_chain_usage.append(obj['kill_chain_phases'])
    #         except Exception:
    #             pass
    #
    #     kill_chain_names = []
    #     relation_queries = []
    #     for k in kill_chain_usage:
    #         for i in k:
    #             kill_chain_names.append((i['kill_chain_name'], i['phase_name']))
    #             relation_query = "match $x isa thing, has stix-id '" + i[
    #                 'id'] + "'; $kill-chain-phase isa kill-chain-phase, has kill-chain-name '" + i[
    #                                  'kill_chain_name'] + "', has phase-name '" + i[
    #                                  'phase_name'] + "'; insert (kill-chain-used: $x, kill-chain-using: $kill-chain-phase) isa kill-chain-usage;"
    #             relation_queries.append(relation_query)
    #     kill_chain_names = set(kill_chain_names)
    #
    #     entities_queries = []
    #     for instances in kill_chain_names:
    #         query = "insert $x isa kill-chain-phase, has kill-chain-name '" + instances[0] + "', has phase-name '" + \
    #                 instances[1] + "';"
    #         entities_queries.append(query)
    #     relation_queries = set(relation_queries)
    #
    #     insertQueries(entities_queries, uri, batch_size, num_threads)
    #     insertQueries(relation_queries, uri, batch_size, num_threads)
    #
    # def filterAttributeTypes(file):
    #     all_attr = []
    #     for obj in file:
    #         for k in obj:
    #             all_attr.append(k)
    #
    #     unique_list_of_attributes = sorted(set(all_attr))
    #
    #     for k, v in attribute_map().items():
    #         try:
    #             unique_list_of_attributes.remove(k)
    #         except Exception:
    #             pass
    #     unique_list_of_attributes.remove("created_by_ref")
    #     unique_list_of_attributes.remove("definition")
    #     unique_list_of_attributes.remove("definition_type")
    #     unique_list_of_attributes.remove("external_references")
    #     unique_list_of_attributes.remove("identity_class")
    #     unique_list_of_attributes.remove("kill_chain_phases")
    #     unique_list_of_attributes.remove("relationship_type")
    #     unique_list_of_attributes.remove("source_ref")
    #     unique_list_of_attributes.remove("target_ref")
    #     unique_list_of_attributes.remove("type")
    #     unique_list_of_attributes.remove("object_marking_refs")
    #     unique_list_of_attributes.remove("tactic_refs")
    #     return unique_list_of_attributes
    #
    # def insertCustomAttributes(file, uri, batch_size, num_threads):
    #     attributes = filterAttributeTypes(file)
    #     queries = []
    #     relations = []
    #     for obj in file:
    #         match = "match $x isa thing, has stix-id '" + obj['id'] + "'; "
    #         var = 0
    #         attribute_query_1 = ""
    #         attribute_query_2 = ""
    #         for att in attributes:
    #             try:
    #                 attribute_query_2 = attribute_query_2 + "$" + str(
    #                     var) + " has attribute-type '" + att + "'; $" + str(
    #                     var) + " '" + obj[att].replace("'", "") + "'; "
    #                 attribute_query_1 = attribute_query_1 + "has custom-attribute $" + str(var) + ", "
    #                 var = var + 1
    #             except Exception:
    #                 pass
    #         query = match + "insert $x " + attribute_query_1[:-2] + "; " + attribute_query_2
    #         queries.append(query)
    #
    #     insertQueries(queries, uri, batch_size, num_threads)
    #
    # def insertExternalReferences(file, uri, batch_size, num_threads):
    #     external_references = []
    #     for obj in file:
    #         try:
    #             for e in obj['external_references']:
    #                 external_references.append(e)
    #         except Exception:
    #             pass
    #
    #     properties = []
    #     for e in external_references:
    #         for k, v in e.items():
    #             properties.append(k)
    #     unique_properties = set(properties)
    #
    #     list_external_references_queries = []
    #     insert_queries = []
    #
    #     for obj in file:
    #         attributes = ''
    #         try:
    #             match_query_1 = "match $x isa thing, has stix-id '" + obj['id'] + "';"
    #             for e in obj['external_references']:
    #                 for p in unique_properties:
    #                     mapping = attribute_map().get(p, {})
    #                     try:
    #                         attributes = attributes + " has " + mapping['type'] + " '" + e[p].replace("'", "") + "',"
    #                     except Exception:
    #                         pass
    #                 insert_rel_query = match_query_1 + ' $er isa external-reference,' + attributes[
    #                                                                                     :-1] + '; insert (referencing: $x, referenced: $er) isa external-referencing;'
    #             insert_ref_query = "insert $er isa external-reference," + attributes[:-1] + ';'
    #             insert_queries.append(insert_rel_query)
    #             list_external_references_queries.append(insert_ref_query)
    #         except Exception:
    #             pass
    #     unique_list_external_references_queries = set(list_external_references_queries)
    #
    #     insertQueries(unique_list_external_references_queries, uri, batch_size, num_threads)
    #     insertQueries(insert_queries, uri, batch_size, num_threads)
