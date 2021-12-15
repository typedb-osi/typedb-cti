import json
from typedb.client import *
from Migrators.Helpers.ConceptMapper import entity_mapper, relationship_mapper, attribute_map
from os import listdir
from os.path import join, isfile
from Migrators.Helpers.batchLoader import write_batch
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

def openFiles(data_folder):
	file_paths = []
	for f in listdir(data_folder):
		file_paths.append(data_folder + f)

	data = []
	for file in file_paths:
		with open (file) as f: 
			for obj in json.load(f)['objects']:
				data.append(obj)
	return data

def createdByRefs(files):
	created_by_refs = []
	queries = []

	for obj in files: 
		try: 
			created_by_refs.append(obj['created_by_ref'])
		except:
			pass
	created_by_refs = set(created_by_refs)

	for obj in files: 
		for c in created_by_refs:
			if obj['id'] == c: 

				ent_type = entity_mapper(obj['type'])['type']
				
				if entity_mapper(obj['type'])['type'] == "identity": 
					ent_type = obj['identity_class']

				query = "$x isa " + ent_type + ","

				query = attributeBuilder(obj, query)

				query = "insert " + query[:-1] + ";"
				queries.append(query)
	return set(queries)


def createMarkings(file):
	queries = []
	for obj in file: 
		if obj['type'] == "marking-definition":
			if obj['definition_type'] == "statement":
				query = "insert $x isa statement-marking, has stix-id '" + obj['id'] + "', has statement '" + obj['definition']['statement'] + "', has created '" + obj['created'] + "', has spec-version '" + obj['spec_version'] + "';"
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
		match_object_marking = "$marking isa marking-definition, has stix-id '" + o['object_marking_refs'][0] + "'; "
		insert_marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
		query = "match " + match_marked_object + match_object_marking + "insert " + insert_marking_rel
		queries.append(query)
	insertQueries(queries, uri, batch_size, num_threads)


def attributeBuilder(obj, query):
	list_of_attributes = []
	for k, v in attribute_map().items():
		try: 
			list_of_attributes.append({'type': v['type'], 'type_data':obj[k].replace("'", ""), "value": v['value']}) 
			for attr in list_of_attributes: 
				if attr['value'] == "string":
					attribute_query = " has " + attr['type'] + " '" + attr['type_data'] + "'" + ","
				if attr['value'] == 'boolean':
					attribute_query = " has " + attr['type'] + " " + str(attr['type_data']).lower() + ","
				if attr['value'] == "list":
					attribute_query = ""
					for l in attr['type_data']: # TODO: Check if this is inserting 
						attribute_query = attribute_query + " has " + attr['type'] + " '" + l + "'" + ","
			query = query + attribute_query
		except Exception:
			pass
	return query


def insertQueries(queries, uri, batch_size, num_threads):
	batch = []
	batches = []
	client = TypeDB.core_client(uri)
	with client.session("cti", SessionType.DATA) as session:
		with session.transaction(TransactionType.WRITE) as tx:
			for q in queries:
				batch.append(q)
				if len(batch) == batch_size:
					batches.append(batch)
					batch = []

			batches.append(batch)
			pool = ThreadPool(num_threads)
			pool.map(partial(write_batch, session), batches)
			pool.close()
			pool.join()


def createRelationQueries(file):
	queries = []
	relations = []
	for obj in file: 
		if obj['type'] == "relationship":
			
			relations.append(obj['relationship_type'])
			relation = relationship_mapper(obj['relationship_type'])

			match_query = "match $source isa thing, has stix-id '" + obj['source_ref'] + "'; $target isa thing, has stix-id '" + obj['target_ref'] + "'; "
			if relation['relation-name'] == "stix-core-relationship":
				insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation['passive-role'] + ": $target) isa " + relation['relation-name'] + ", has stix-type '" + relation['stix-type'] + "',"
			else: 
				insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation['passive-role'] + ": $target) isa " + relation['relation-name'] + ","

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
			relation_query = "match $x isa thing, has stix-id '" + i['id'] + "'; $kill-chain-phase isa kill-chain-phase, has kill-chain-name '" + i['kill_chain_name'] + "', has phase-name '" + i['phase_name'] + "'; insert (kill-chain-used: $x, kill-chain-using: $kill-chain-phase) isa kill-chain-usage;"
			relation_queries.append(relation_query)
	kill_chain_names = set(kill_chain_names)

	entities_queries = []
	for instances in kill_chain_names:
		query = "insert $x isa kill-chain-phase, has kill-chain-name '" + instances[0] + "', has phase-name '" + instances[1] + "';"
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
				attribute_query_2 = attribute_query_2 + "$" + str(var) + " has attribute-type '" + att + "'; $" + str(var) + " '" + obj[att].replace("'","") + "'; "
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
						attributes = attributes + " has " + mapping['type'] + " '" + e[p].replace("'","") + "',"
					except Exception:
						pass
				insert_rel_query = match_query_1 + ' $er isa external-reference,' + attributes[:-1] + '; insert (referencing: $x, referenced: $er) isa external-referencing;'
			insert_ref_query = "insert $er isa external-reference," + attributes[:-1] + ';'
			insert_queries.append(insert_rel_query)
			list_external_references_queries.append(insert_ref_query)
		except Exception:
			pass
	unique_list_external_references_queries = set(list_external_references_queries)

	insertQueries(unique_list_external_references_queries, uri, batch_size, num_threads)
	insertQueries(insert_queries, uri, batch_size, num_threads)


def migrate_mitre(uri, batch_size, num_threads):
	data_folder = 'Data/'
	file = openFiles(data_folder)
	created_by = createdByRefs(file)
	insertQueries(created_by, uri, batch_size, num_threads)
	markings = createMarkings(file)
	insertQueries(markings, uri, batch_size, num_threads)
	createEntitiesQuery(file, uri, batch_size, num_threads)
	relations = createRelationQueries(file)
	insertQueries(relations, uri, batch_size, num_threads)
	insertKillChainPhases(file, uri, batch_size, num_threads)
	insertCustomAttributes(file, uri, batch_size, num_threads)
	insertExternalReferences(file, uri, batch_size, num_threads)
