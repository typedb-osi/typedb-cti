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

import logging
from timeit import default_timer as timer

from schema.initialise import initialise_database
from stix.migrator import StixMigrator
from stix.typedb_inserter import data_count

# TODO allow setting via CLI run options
uri = "localhost:1729"
database = "cti"
batch_size = 50
num_threads = 16
logging.basicConfig(level=logging.INFO)

start = timer()
initialise_database(uri, database, True)  # TODO don't leave on force = True!!
migrator = StixMigrator(uri, database, batch_size, num_threads)
migrator.migrate(data_path="data/mitre")
migrator.close()
end = timer()
time_in_sec = end - start
inserted = data_count(uri, database)
print(f"Loaded data points: {inserted}. Elapsed time: {time_in_sec} seconds.")
