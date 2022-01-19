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
import argparse
import logging
from timeit import default_timer as timer

from schema.initialise import initialise_database
from stix.migrator import StixMigrator
from stix.typedb_inserter import data_count

parser = argparse.ArgumentParser(description='Demonstration STIX migrator using the MITRE dataset.')
parser.add_argument('--uri', dest='uri', default='localhost:1729', help='URI of TypeDB server')
parser.add_argument('--database', dest='database', default='cti', help='Database to migrate data to.')
parser.add_argument('--batch_size', dest='batch_size', default=50, help='Transaction batch size during migration')
parser.add_argument('--threads', dest='threads', default=16, help='Number of loading threads  with (recommend 2*cores)')
parser.add_argument('--data-path', dest='data_path', default='data/mitre', help='Path to STIX-compliant data files')

args = parser.parse_args()
logging.basicConfig(level=logging.INFO)  # when debugging, set to logging.DEBUG

start = timer()
initialise_database(args.uri, args.database, False)
migrator = StixMigrator(args.uri, args.database, args.batch_size, args.threads)
migrator.migrate(data_path=args.data_path)
migrator.close()
end = timer()
time_in_sec = end - start
inserted = data_count(args.uri, args.database)
print(f"Loaded data points: {inserted}.)")
print(f"Elapsed time: {time_in_sec} seconds.")
