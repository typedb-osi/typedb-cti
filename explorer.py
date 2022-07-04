#
# Copyright (C) 2022 Priam Cyber AI
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

from utils.queries import TiExplorer

parser = argparse.ArgumentParser(description='Useful threat intel queries for attribution determination')
parser.add_argument('--uri', dest='uri', default='localhost:1729', help='URI of TypeDB server')
parser.add_argument('--database', dest='database', default='cti', help='Database to migrate data to.')

parser.add_argument('--stats', dest='stats', default=False, action="store_true",
                    help='Provide entity stats.')

parser.add_argument('-ttp','--ttp', nargs='+', help='List of MITRE TTPs', required=False)

parser.add_argument('--infer_group', dest='infer_group', default=False, action="store_true",
                    help='Infer group from relationships.')

args = parser.parse_args()
logging.basicConfig(level=logging.INFO)  # when debugging, set to logging.DEBUG

if args.stats:
    ti = TiExplorer(args.uri,args.database)
    ti.get_stats()

if args.infer_group:
    if args.ttp is None:
        logging.error('Provide list of MITRE TTP')
    else:
        ti = TiExplorer(args.uri,args.database)
        ti.ttp_to_intrusion(args.ttp)
