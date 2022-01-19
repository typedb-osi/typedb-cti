import json
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from os import listdir

from typedb.client import *

from migrators.helpers.BatchLoader import write_batch
from migrators.mitre_attack.query_generators import InsertQueriesGenerator


def read_mitre_objects_json(data_folder):
    file_paths = []
    for f in listdir(data_folder):
        file_paths.append(data_folder + f)

    data = []
    for file in file_paths:
        with open(file) as f:
            for obj in json.load(f)['objects']:
                data.append(obj)
    return data


class TypeDBInserter:

    def __init__(self, uri, database, batch_size, num_threads):
        self.database = database
        self.batch_size = batch_size
        self.num_threads = num_threads
        self.client = TypeDB.core_client(uri)

    def insert(self, queries):
        batch = []
        batches = []
        for q in queries:
            batch.append(q)
            if len(batch) == self.batch_size:
                batches.append(batch)
                batch = []
        batches.append(batch)

        with self.client.session(self.database, SessionType.DATA) as session:
            pool = ThreadPool(self.num_threads)
            pool.map(partial(self.write_batch, session), batches)
            pool.close()
            pool.join()

    def write_batch(self, session, batch):
        with session.transaction(TransactionType.WRITE) as tx:
            for query in batch:
                tx.query().insert(query)
            tx.commit()


def migrate_mitre_objects(batch_inserter, queries_generator):
    referenced = queries_generator.mitre_objects_referenced()
    batch_inserter.insert(referenced["queries"])
    markings = queries_generator.mitre_objects_markings_definition()
    batch_inserter.insert(markings["queries"])
    mitre_ids_processed = referenced["processed_ids"].union(markings["processed_ids"])
    mitre_and_markings = queries_generator.mitre_objects_and_marking_relations(exclude_ids=mitre_ids_processed)
    batch_inserter.insert(mitre_and_markings)


def migrate_mitre(uri, database, batch_size, num_threads):
    print('.....')
    print('Inserting data...')
    print('.....')

    typedb_inserter = TypeDBInserter(uri, database, batch_size, num_threads)

    data_folder = 'data/'
    json_objects = read_mitre_objects_json(data_folder)
    queries_generator = InsertQueriesGenerator(json_objects)
    migrate_mitre_objects(typedb_inserter, queries_generator)
    # relations = createRelationQueries(json_objects)
    # insert_queries(relations, uri, batch_size, num_threads)
    # insertKillChainPhases(json_objects, uri, batch_size, num_threads)
    # insertCustomAttributes(json_objects, uri, batch_size, num_threads)
    # insertExternalReferences(json_objects, uri, batch_size, num_threads)

    print('.....')
    print('Successfully inserted data!')
    print('.....')
