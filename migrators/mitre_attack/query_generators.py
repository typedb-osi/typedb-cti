import logging

from migrators.mitre_attack.concept_mapper import entity_mapper, attribute_definitions


class InsertQueriesGenerator:

    def __init__(self, mitre_objects_json):
        self.mitre_objects_json = mitre_objects_json

    def created_by_refs(self):
        created_by_refs = set()
        for mitre_object in self.mitre_objects_json:
            try:
                created_by_refs.add(mitre_object['created_by_ref'])
            except:
                logging.info("Skipping json data since it is missing key")

        queries = set()
        for mitre_object in self.mitre_objects_json:
            for referenced_id in created_by_refs:
                if mitre_object['id'] == referenced_id:
                    entity_type = entity_mapper(mitre_object['type'])['type']
                    if entity_type == "identity":
                        entity_type = mitre_object['identity_class']
                    query = "$x isa " + entity_type + ","
                    query = self.attribute_builder(mitre_object, query)

                    query = "insert " + query[:-1] + ";"
                    queries.add(query)
        return queries

    def createMarkings(file):
        queries = []
        for obj in file:
            if obj['type'] == "marking-definition":
                if obj['definition_type'] == "statement":
                    query = "insert $x isa statement-marking, has stix-id '" + obj['id'] + "', has statement '" + \
                            obj['definition']['statement'] + "', has created '" + obj[
                                'created'] + "', has spec-version '" + \
                            obj['spec_version'] + "';"
                    queries.append(query)
        return set(queries)

    def createEntitiesQuery(file, uri, batch_size, num_threads):
        queries = []
        entities = []
        marking_relations = []

        for obj in file:

            if obj['type'] != "relationship" and obj['id'] != "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5":

                stix_type = entity_mapper(obj['type'])

                if stix_type['ignore'] == False:
                    try:
                        obj['object_marking_refs'][0]
                        marking_relations.append(obj)
                    except:
                        pass

                    if stix_type['custom-type'] == True:

                        query = "$x isa custom-object, has stix-type '" + stix_type['type'] + "',"
                        entities.append(stix_type['type'])

                    else:

                        if obj['type'] == "identity":
                            ent_type = obj['identity_class']
                        else:
                            ent_type = obj['type']

                        query = "$x isa " + ent_type + ","
                        entities.append(stix_type['type'])

                    query = attributeBuilder(obj, query)

                    query = "insert " + query[:-1] + ";"
                    try:
                        created_by_refs_rel = "(created: $x, creator: $creator) isa creation;"
                        created_by_refs_match = "$creator isa thing, has stix-id '" + obj['created_by_ref'] + "';"
                        query = "match " + created_by_refs_match + query + created_by_refs_rel
                    except Exception:
                        pass

                    queries.append(query)

        queries = set(queries)
        insertQueries(queries, uri, batch_size, num_threads)

        createMarkingsRelations(marking_relations, uri, batch_size, num_threads)

        return queries

    def createMarkingsRelations(marking_relations, uri, batch_size, num_threads):
        queries = []
        for o in marking_relations:
            match_marked_object = "$x isa thing, has stix-id '" + o['id'] + "'; "
            match_object_marking = "$marking isa marking-definition, has stix-id '" + o['object_marking_refs'][
                0] + "'; "
            insert_marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
            query = "match " + match_marked_object + match_object_marking + "insert " + insert_marking_rel
            queries.append(query)
        insertQueries(queries, uri, batch_size, num_threads)

    def attribute_builder(self, mitre_object):
        query = ""
        for mitre_key, typeql_definition in attribute_definitions():
            try:
                typeql_attr_type = typeql_definition['type']
                mitre_value_type = typeql_definition['value']
                mitre_value = mitre_object[mitre_key]
                if mitre_value_type == "string":
                    string_value = mitre_value.replace("'", "")
                    attribute_query = f" has {typeql_attr_type} '{string_value}',"
                elif mitre_value_type == 'boolean':
                    boolean_value = str(mitre_value).lower()
                    attribute_query = f" has {typeql_attr_type} {boolean_value},"
                elif mitre_value_type == "list":
                    attribute_query = ""
                    for l in mitre_value:
                        # TODO do we have to assume this is a string? If so, we should do the same ' replacement
                        attribute_query += f" has {typeql_attr_type} '{l}',"
                else:
                    logging.info(f"Unrecognised mitre attribute value type: '{mitre_value_type}'")
                    attribute_query = ""
                query += attribute_query
            except KeyError:
                logging.info(f"Key error loading '{mitre_key}' from {mitre_object}")
        pass


return query


def createRelationQueries(file):
    queries = []
    relations = []
    for obj in file:
        if obj['type'] == "relationship":

            relations.append(obj['relationship_type'])
            relation = relationship_mapper(obj['relationship_type'])

            match_query = "match $source isa thing, has stix-id '" + obj[
                'source_ref'] + "'; $target isa thing, has stix-id '" + obj['target_ref'] + "'; "
            if relation['relation-name'] == "stix-core-relationship":
                insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation[
                    'passive-role'] + ": $target) isa " + relation['relation-name'] + ", has stix-type '" + \
                               relation[
                                   'stix-type'] + "',"
            else:
                insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation[
                    'passive-role'] + ": $target) isa " + relation['relation-name'] + ","

            insert_query = attributeBuilder(obj, insert_query)

            query = match_query + insert_query[:-1] + ";"
            queries.append(query)

    return set(queries)


def insertKillChainPhases(file, uri, batch_size, num_threads):
    kill_chain_usage = []
    for obj in file:
        try:
            for k in obj:

                for kc in obj['kill_chain_phases']:
                    kc['id'] = obj['id']
                kill_chain_usage.append(obj['kill_chain_phases'])
        except Exception:
            pass

    kill_chain_names = []
    relation_queries = []
    for k in kill_chain_usage:
        for i in k:
            kill_chain_names.append((i['kill_chain_name'], i['phase_name']))
            relation_query = "match $x isa thing, has stix-id '" + i[
                'id'] + "'; $kill-chain-phase isa kill-chain-phase, has kill-chain-name '" + i[
                                 'kill_chain_name'] + "', has phase-name '" + i[
                                 'phase_name'] + "'; insert (kill-chain-used: $x, kill-chain-using: $kill-chain-phase) isa kill-chain-usage;"
            relation_queries.append(relation_query)
    kill_chain_names = set(kill_chain_names)

    entities_queries = []
    for instances in kill_chain_names:
        query = "insert $x isa kill-chain-phase, has kill-chain-name '" + instances[0] + "', has phase-name '" + \
                instances[1] + "';"
        entities_queries.append(query)
    relation_queries = set(relation_queries)

    insertQueries(entities_queries, uri, batch_size, num_threads)
    insertQueries(relation_queries, uri, batch_size, num_threads)


def filterAttributeTypes(file):
    all_attr = []
    for obj in file:
        for k in obj:
            all_attr.append(k)

    unique_list_of_attributes = sorted(set(all_attr))

    for k, v in attribute_map().items():
        try:
            unique_list_of_attributes.remove(k)
        except Exception:
            pass
    unique_list_of_attributes.remove("created_by_ref")
    unique_list_of_attributes.remove("definition")
    unique_list_of_attributes.remove("definition_type")
    unique_list_of_attributes.remove("external_references")
    unique_list_of_attributes.remove("identity_class")
    unique_list_of_attributes.remove("kill_chain_phases")
    unique_list_of_attributes.remove("relationship_type")
    unique_list_of_attributes.remove("source_ref")
    unique_list_of_attributes.remove("target_ref")
    unique_list_of_attributes.remove("type")
    unique_list_of_attributes.remove("object_marking_refs")
    unique_list_of_attributes.remove("tactic_refs")
    return unique_list_of_attributes


def insertCustomAttributes(file, uri, batch_size, num_threads):
    attributes = filterAttributeTypes(file)
    queries = []
    relations = []
    for obj in file:
        match = "match $x isa thing, has stix-id '" + obj['id'] + "'; "
        var = 0
        attribute_query_1 = ""
        attribute_query_2 = ""
        for att in attributes:
            try:
                attribute_query_2 = attribute_query_2 + "$" + str(
                    var) + " has attribute-type '" + att + "'; $" + str(
                    var) + " '" + obj[att].replace("'", "") + "'; "
                attribute_query_1 = attribute_query_1 + "has custom-attribute $" + str(var) + ", "
                var = var + 1
            except Exception:
                pass
        query = match + "insert $x " + attribute_query_1[:-2] + "; " + attribute_query_2
        queries.append(query)

    insertQueries(queries, uri, batch_size, num_threads)


def insertExternalReferences(file, uri, batch_size, num_threads):
    external_references = []
    for obj in file:
        try:
            for e in obj['external_references']:
                external_references.append(e)
        except Exception:
            pass

    properties = []
    for e in external_references:
        for k, v in e.items():
            properties.append(k)
    unique_properties = set(properties)

    list_external_references_queries = []
    insert_queries = []

    for obj in file:
        attributes = ''
        try:
            match_query_1 = "match $x isa thing, has stix-id '" + obj['id'] + "';"
            for e in obj['external_references']:
                for p in unique_properties:
                    mapping = attribute_map().get(p, {})
                    try:
                        attributes = attributes + " has " + mapping['type'] + " '" + e[p].replace("'", "") + "',"
                    except Exception:
                        pass
                insert_rel_query = match_query_1 + ' $er isa external-reference,' + attributes[
                                                                                    :-1] + '; insert (referencing: $x, referenced: $er) isa external-referencing;'
            insert_ref_query = "insert $er isa external-reference," + attributes[:-1] + ';'
            insert_queries.append(insert_rel_query)
            list_external_references_queries.append(insert_ref_query)
        except Exception:
            pass
    unique_list_external_references_queries = set(list_external_references_queries)

    insertQueries(unique_list_external_references_queries, uri, batch_size, num_threads)
    insertQueries(insert_queries, uri, batch_size, num_threads)
