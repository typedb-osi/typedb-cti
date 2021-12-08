import json
from typedb.client import *
from Migrators.Helpers.ConceptMapper import entity_mapper, relationship_mapper
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
				query = "$x isa " + entity_mapper(obj['type'])['type'] + ","

				list_of_attributes = fetchAttributes(obj)

				for attr in list_of_attributes: 
					for k, v in attr.items(): 
						attribute_query = " has " + k + ' "' + v + '"' + ","
						query = query + attribute_query

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
	

def createEntitiesQuery(file):
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
					query = "$x isa " + stix_type['type'] + ","
					entities.append(stix_type['type'])

				list_of_attributes = fetchAttributes(obj)

				for attr in list_of_attributes: 
					for k, v in attr.items(): 
						attribute_query = " has " + k + " '" + v + "'" + ","
						query = query + attribute_query

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

	createMarkingsRelations(marking_relations)
	
	return queries

def createMarkingsRelations(marking_relations):
	queries = []
	for o in marking_relations:
		match_marked_object = "$x isa thing, has stix-id '" + o['id'] + "'; "
		match_object_marking = "$marking isa marking-definition, has stix-id '" + o['object_marking_refs'][0] + "'; "
		insert_marking_rel = "(marked: $x, marking: $marking) isa object-marking;"
		query = "match " + match_marked_object + match_object_marking + "insert " + insert_marking_rel
		queries.append(query)
	insertQueries(queries, uri, batch_size, num_threads)


def fetchAttributes(obj):
	list_of_attributes = []
	try: 
		stix_id = {"stix-id": obj['id']}
		list_of_attributes.append(stix_id)
	except: 
		pass
	try: 
		stix_created = {"created": obj['created']}
		list_of_attributes.append(stix_created)
	except: 
		pass
	try: 
		stix_modified = {"modified": obj['modified']}
		list_of_attributes.append(stix_modified)
	except:
		pass
	try: 
		stix_description = {"description": obj['description'].replace("'", "")}
		list_of_attributes.append(stix_description)
	except:
		pass
	try: 
		stix_name = {"name": obj['name']}
		list_of_attributes.append(stix_name)
	except: 
		pass
	try: 
		stix_spec_version = {"spec-version": obj['spec_version']}
		list_of_attributes.append(stix_spec_version)
	except: 
		pass
	try: 
		stix_hash = {"hashes": obj['hash']}
		list_of_attributes.append(stix_hash)
	except:
		pass
	return list_of_attributes


def insertQueries(queries, uri, batch_size, num_threads):
	batch = []
	batches = []
	client = TypeDB.core_client(uri)
	with client.session("stix", SessionType.DATA) as session:
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

			list_of_attributes = []

			try: 
				stix_id = {"stix-id": obj['id']}
				list_of_attributes.append(stix_id)
			except: 
				pass
			try: 
				stix_created = {"created": obj['created']}
				list_of_attributes.append(stix_created)
			except: 
				pass
			try: 
				stix_modified = {"modified": obj['modified']}
				list_of_attributes.append(stix_modified)
			except:
				pass
			try: 
				stix_spec_version = {"spec-version": obj['spec_version']}
				list_of_attributes.append(stix_spec_version)
			except: 
				pass

			for attr in list_of_attributes: 
				for k, v in attr.items(): 
					attribute_query = " has " + k + ' "' + v + '"' + ","
					insert_query = insert_query + attribute_query

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

uri = "localhost:1729"
data_folder = 'Data/'
batch_size = 50
num_threads = 8
file = openFiles(data_folder)
created_by = createdByRefs(file)
insertQueries(created_by, uri, batch_size, num_threads)
markings = createMarkings(file)
insertQueries(markings, uri, batch_size, num_threads)
createEntitiesQuery(file)
relations = createRelationQueries(file)
insertQueries(relations, uri, batch_size, num_threads)
insertKillChainPhases(file, uri, batch_size, num_threads)






