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
	for f in listdir('Data/'):
		file_paths.append('Data/' + f)

	data = []
	for file in file_paths:
		with open (file) as f: 
			data.append(json.load(f)['objects'])
	
	return data

def createdByRefs(files):
	created_by_refs = []
	queries = []
	for f in files:
		for obj in f: 
			try: 
				created_by_refs.append(obj['created_by_ref'])
			except:
				pass
	created_by_refs = set(created_by_refs)
	for f in files:
		for obj in f: 
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


def createMarkings(files):
	queries = []
	for f in files:
		for obj in f: 
			if obj['type'] == "marking-definition":
				if obj['definition_type'] == "statement":
					query = "insert $x isa statement-marking, has stix-id '" + obj['id'] + "', has statement '" + obj['definition']['statement'] + "', has created '" + obj['created'] + "', has spec-version '" + obj['spec_version'] + "';"
					queries.append(query)
	return set(queries)
	

def createEntitiesQuery(files):
	queries = []
	entities = []
	for f in files:
		for obj in f: 

			if obj['type'] != "relationship" and obj['id'] != "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5":

				stix_type = entity_mapper(obj['type'])

				if stix_type['ignore'] == False:
					has_marking = False
					try: 
						match_object_marking = "$marking isa marking-definition, has stix-id '" + obj['object_marking_refs'][0] + "'; "
						insert_marking_rel = " (marked: $x, marking: $marking) isa object-marking;"
						has_marking = True
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
							attribute_query = " has " + k + ' "' + v + '"' + ","
							query = query + attribute_query

					if has_marking == True:
						query = match_object_marking + "insert " + query[:-1] + ";"	+ insert_marking_rel

						try: 
							created_by_refs_rel = "(created: $x, creator: $creator) isa creation;"
							created_by_refs_match = "$creator isa thing, has stix-id '" + obj['created_by_ref'] + "';"
							query = "match " + created_by_refs_match + query + created_by_refs_rel
						except Exception: 
							query = "match " + query
					else: 
						query = "insert " + query[:-1] + ";"
						try: 
							created_by_refs_rel = "(created: $x, creator: $creator) isa creation;"
							created_by_refs_match = "$creator isa thing, has stix-id '" + obj['created_by_ref'] + "';"
							query = "match " + created_by_refs_match + query + created_by_refs_rel
						except Exception:
							pass

					queries.append(query)

	# print(set(entities))
	return queries


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
		stix_description = {"description": obj['description'].replace('"', "'")}
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
	for f in file:
		for obj in f: 
			if obj['type'] == "relationship":
				
				relations.append(obj['relationship_type'])
				relation = relationship_mapper(obj['relationship_type'])

				match_query = "match $source isa thing, has stix-id '" + obj['source_ref'] + "'; $target isa thing, has stix-id '" + obj['target_ref'] + "'; "
				if relation['relation-name'] == "stix-core-relationship":
					insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation['passive-role'] + ": $target) isa " + relation['relation-name'] + ", has stix-type '" + relation['stix-type'] + "',"
				else: 
					insert_query = "insert $a (" + relation['active-role'] + ": $source, " + relation['passive-role'] + ": $target) isa " + relation['relation-name'] + ","

				# Attributes
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



	# print(set(relations))
	return queries



uri = "localhost:1729"
data_folder = 'Data/'
batch_size = 50
num_threads = 8
files = openFiles(data_folder)
created_by = createdByRefs(files)
insertQueries(created_by, uri, batch_size, num_threads)
markings = createMarkings(files)
insertQueries(markings, uri, batch_size, num_threads)
entities = createEntitiesQuery(files)
insertQueries(entities, uri, batch_size, num_threads)
relations = createRelationQueries(files)
insertQueries(relations, uri, batch_size, num_threads)




