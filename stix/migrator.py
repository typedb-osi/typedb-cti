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

import json
import os

from stix.query import StixInsertGenerator
from stix.typedb_inserter import TypeDBInserter


class StixMigrator:

    def __init__(self, typedb_uri, database, batch_size, num_threads):
        self.inserter = TypeDBInserter(typedb_uri, database, batch_size=batch_size, num_threads=num_threads)

    def migrate(self, data_path, ignore_conditions=[]):
        print('.....')
        print('Inserting data...')
        print('.....')
        stix_json_objects = self._read_stix_objects_json(data_path)
        insert_generator = StixInsertGenerator(stix_json_objects,ignore_conditions)
        self._migrate_stix_objects(insert_generator)
        self._migrate_stix_relationships(insert_generator)
        self._migrate_kill_chain_phases(insert_generator)
        self._migrate_external_references(insert_generator)
        print('.....')
        print('Successfully inserted data!')
        print('.....')

    def _read_stix_objects_json(self, data_path):
        file_paths = []
        for f in os.listdir(data_path):
            file_paths.append(os.path.join(data_path, f))

        data = []
        for file in file_paths:
            with open(file) as f:
                for obj in json.load(f)['objects']:
                    data.append(obj)
        return data

    def _migrate_stix_objects(self, insert_generator):
        referenced = insert_generator.referenced_stix_objects()
        self.inserter.insert(referenced["queries"])
        markings = insert_generator.statement_markings()
        self.inserter.insert(markings["queries"])
        stix_ids_processed = referenced["processed_ids"].union(markings["processed_ids"])
        stix_objects_and_markings = insert_generator.stix_objects_and_marking_relations(exclude_ids=stix_ids_processed)
        # We must load stix entities before relations to them
        self.inserter.insert(stix_objects_and_markings["stix_entities"])
        self.inserter.insert(stix_objects_and_markings["marking_relations"])

    def _migrate_stix_relationships(self, insert_generator):
        relations = insert_generator.stix_relationships()
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

    def close(self):
        self.inserter.close()
