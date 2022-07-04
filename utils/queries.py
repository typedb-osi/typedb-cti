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

import json
import os

from typedb.client import *
import networkx as nx
from tabulate import tabulate

import logging
logger = logging.getLogger(__name__)

class TiExplorer:

    def __init__(self, uri, database):
        self.database = database
        self.client = TypeDB.core_client(uri)

    def ttp_to_intrusion(self,ttp_list):
        with self.client.session("cti", SessionType.DATA) as session:
            ## get various count stats
            with session.transaction(TransactionType.READ) as read_transaction:
                DG = nx.DiGraph()

                if len(ttp_list) == 1:
                    or_conditions = f'has external-id "{ttp_list[0]}"'
                else:
                    fmt_cnd = ['{{$e has external-id "{0}";}}'.format(t) for t in ttp_list]
                    or_conditions = ' or '.join(fmt_cnd)
                    
                q_ttp = 'match $e isa external-reference, has source-name "mitre-attack";\
                {0};\
                $e has external-id $eid;\
                $a isa attack-pattern, has name $an;\
                $i isa intrusion-set, has name $in;\
                $rel (referencing: $a, referenced: $e) isa external-referencing;\
                $u (used: $a, used-by: $i) isa use;\
                get $an,$eid,$u,$i,$in; '.format(or_conditions)
                
                answer_iterator = read_transaction.query().match(q_ttp)
                
                for q in answer_iterator:
                    #attack_id = q.get('a').get_iid()
                    attack_name = q.get('an').get_value()
                    ttp_id = q.get('eid').get_value()
                    group_name = q.get('in').get_value()
                    
                    DG.add_node(ttp_id, type='ttp')
                    DG.add_node(group_name, type='group')
                    DG.add_edge(ttp_id, group_name)
                    
            logger.info('Total threat groups %d ' % len(DG.edges))
            logger.info('Total nodes %d ' % len(DG.nodes))
            
            deg_counts = [(n_id,DG.degree(n_id)) for n_id,n_att in DG.nodes(data=True) if n_att['type']=='group']
            

            match_all = filter(lambda deg: deg[1]==len(ttp_list), deg_counts)
            
            logger.info('\n'+tabulate(match_all, ["Group Name", "TTP count"], tablefmt="grid"))    

    def get_stats(self):
        with self.client.session("cti", SessionType.DATA) as session:
            ## get various count stats
            with session.transaction(TransactionType.READ) as read_transaction:
                
                total_groups = read_transaction.query().match_aggregate("match $x isa intrusion-set; get $x; count;").get().as_int()
                logger.info('Total Intrusions Sets %d' % total_groups)
                
                total_ttp = read_transaction.query().match_aggregate("match $x isa attack-pattern; get $x; count;").get().as_int()
                logger.info('Total Attack Patterns %d' % total_ttp)
                
                q_ttp = 'match $e isa external-reference, has source-name "mitre-attack", has external-id like "T[0-9]+";\
                $e has external-id $eid;$a isa attack-pattern, has name $an;\
                $rel (referencing: $a, referenced: $e) isa external-referencing;\
                get $a; count;'
                
                total_ttp = read_transaction.query().match_aggregate(q_ttp).get().as_int()

                logger.info('Total Mitre Techniques %d' % total_ttp)
                
                q_subttp = 'match $e isa external-reference, has source-name "mitre-attack", has external-id like "T[0-9]+\.[0-9]+";\
                $e has external-id $eid;$a isa attack-pattern, has name $an;\
                $rel (referencing: $a, referenced: $e) isa external-referencing;\
                get $a; count;'
                
                total_sub = read_transaction.query().match_aggregate(q_subttp).get().as_int()

                logger.info('Total Mitre Sub Techniques %d' % total_sub)
                
                total_malware = read_transaction.query().match_aggregate("match $x isa malware; get $x; count;").get().as_int()
                logger.info('Total Malware %d' % total_malware)
                
                total_tools = read_transaction.query().match_aggregate("match $x isa tool; get $x; count;").get().as_int()
                logger.info('Total Tools %d' % total_tools)
                