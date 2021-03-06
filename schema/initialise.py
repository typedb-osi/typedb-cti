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

from typedb.client import *


def initialise_database(uri, database, force=False):
    client = TypeDB.core_client(uri)
    if client.databases().contains(database):
        if force:
            client.databases().get(database).delete()
        else:
            raise ValueError(f"Database '{database}' already exists")
    client.databases().create(database)
    session = client.session(database, SessionType.SCHEMA)
    with open("schema/cti-schema.tql", "r") as schema_file:
        schema = schema_file.read()
    with open("schema/cti-rules.tql", "r") as rules_file:
        rules = rules_file.read()
    print('.....')
    print('Inserting schema and rules...')
    print('.....')
    with session.transaction(TransactionType.WRITE) as write_transaction:
        write_transaction.query().define(schema)
        write_transaction.commit()
    with session.transaction(TransactionType.WRITE) as write_transaction:
        write_transaction.query().define(rules)
        write_transaction.commit()
    print('.....')
    print('Successfully committed schema!')
    print('.....')
    session.close()
    client.close()
