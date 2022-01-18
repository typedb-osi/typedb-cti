import json
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from os import listdir

from typedb.client import *

from migrators.helpers.BatchLoader import write_batch
from migrators.mitre_attack.query_generators import InsertQueriesGenerator


def read_objects_json(data_folder):
    file_paths = []
    for f in listdir(data_folder):
        file_paths.append(data_folder + f)

    data = []
    for file in file_paths:
        with open(file) as f:
            for obj in json.load(f)['objects']:
                data.append(obj)
    return data


def insert_queries(database, queries, uri, batch_size, num_threads):
    batch = []
    batches = []
    client = TypeDB.core_client(uri)
    with client.session(database, SessionType.DATA) as session:
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


def migrate_mitre(uri, database, batch_size, num_threads):
    print('.....')
    print('Inserting data...')
    print('.....')

    data_folder = 'data/'
    json_objects = read_objects_json(data_folder)
    queries_generator = InsertQueriesGenerator(json_objects)
    created_by = queries_generator.created_by_refs()
    insert_queries(database, created_by, uri, batch_size, num_threads)
    # markings = createMarkings(json_objects)
    # insert_queries(markings, uri, batch_size, num_threads)
    # createEntitiesQuery(json_objects, uri, batch_size, num_threads)
    # relations = createRelationQueries(json_objects)
    # insert_queries(relations, uri, batch_size, num_threads)
    # insertKillChainPhases(json_objects, uri, batch_size, num_threads)
    # insertCustomAttributes(json_objects, uri, batch_size, num_threads)
    # insertExternalReferences(json_objects, uri, batch_size, num_threads)

    print('.....')
    print('Successfully inserted data!')
    print('.....')
