import json
import logging
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
from os import listdir
from timeit import default_timer as timer

from typedb.client import *

from migrators.mitre_attack.query_generators import MitreInsertGenerator


class TypeDBInserter:

    def __init__(self, uri, database, batch_size, num_threads):
        self.database = database
        self.batch_size = batch_size
        self.num_threads = num_threads
        self.client = TypeDB.core_client(uri)

    def insert(self, queries):
        start = timer()
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
            pool.map(partial(self._insert_query_batch, session), batches)
            pool.close()
            pool.join()
        end = timer()
        logging.debug(f"Executed '{len(queries)}' inserts in {end - start} seconds")

    def _insert_query_batch(self, session, batch):
        with session.transaction(TransactionType.WRITE) as tx:
            for query in batch:
                tx.query().insert(query)
            tx.commit()


class MitreMigrator:

    def __init__(self, typedb_uri, database, batch_size, num_threads, data_path='data/'):
        self.inserter = TypeDBInserter(typedb_uri, database, batch_size, num_threads)
        self.data_path = data_path

    def migrate(self):
        print('.....')
        print('Inserting data...')
        print('.....')
        mitre_json_objects = self._read_mitre_objects_json()
        insert_generator = MitreInsertGenerator(mitre_json_objects)
        self._migrate_mitre_entities(insert_generator)
        self._migrate_mitre_relations(insert_generator)
        self._migrate_kill_chain_phases(insert_generator)
        self._migrate_external_references(insert_generator)
        print('.....')
        print('Successfully inserted data!')
        print('.....')

    def _read_mitre_objects_json(self):
        file_paths = []
        for f in listdir(self.data_path):
            file_paths.append(self.data_path + f)

        data = []
        for file in file_paths:
            with open(file) as f:
                for obj in json.load(f)['objects']:
                    data.append(obj)
        return data

    def _migrate_mitre_entities(self, insert_generator):
        referenced = insert_generator.mitre_objects_referenced()
        self.inserter.insert(referenced["queries"])
        markings = insert_generator.statement_markings()
        self.inserter.insert(markings["queries"])
        mitre_ids_processed = referenced["processed_ids"].union(markings["processed_ids"])
        mitre_and_markings = insert_generator.mitre_objects_and_marking_relations(exclude_ids=mitre_ids_processed)
        self.inserter.insert(mitre_and_markings)

    def _migrate_mitre_relations(self, insert_generator):
        relations = insert_generator.mitre_relationships()
        self.inserter.insert(relations)

    def _migrate_kill_chain_phases(self, insert_generator):
        phases_and_usages = insert_generator.kill_chain_phases()
        # We must insert the phases before phase usages
        self.inserter.insert(phases_and_usages["kill_chain_phases"])
        self.inserter.insert(phases_and_usages["kill_chain_phase_usages"])

    def _migrate_external_references(self, insert_generator):
        external_references = insert_generator.external_references()
        # We must insert external references before relations to them
        self.inserter.insert(external_references["external_references"])
        self.inserter.insert(external_references["external_reference_relations"])
