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

from functools import reduce
import json
import os

from typedb.client import *
import networkx as nx
from tabulate import tabulate

import logging
logger = logging.getLogger(__name__)

from operator import itemgetter



class TiExplorer:
    '''
    This class contains basic exploration techniques to attribute tactics to threat groups
    '''

    def __init__(self, uri, database,ignoreRevoked=True):
        self.database = database
        self.client = TypeDB.core_client(uri)
        self._ignoreRevoked = ignoreRevoked

    def ttp_to_intrusion(self,ttp_list:list):
        # load a dictionary of all current TTP
        self.get_all_ttp()

        with self.client.session(self.database, SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:
                
                # check the TTP are correct
                for ttp_id in ttp_list:
                    if ttp_id not in self._ttp:
                        logger.error(f'TTP {ttp_id} not in database')
                if len(ttp_list) == 1:
                    or_conditions = f'$e has external-id "{ttp_list[0]}"'
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
                DG = nx.DiGraph()
                for q in answer_iterator:
                    attack_name = q.get('an').get_value()
                    ttp_id = q.get('eid').get_value()
                    group_name = q.get('in').get_value()
                    
                    DG.add_node(ttp_id, type='attack-pattern')
                    DG.add_node(group_name, type='intrusion-set')
                    DG.add_edge(ttp_id, group_name)
                    
            logger.info('Total links %d ' % len(DG.edges))
            logger.info('Total nodes %d ' % len(DG.nodes))
            
            deg_counts = [(n_id,DG.degree(n_id)) for n_id,n_att in DG.nodes(data=True) if n_att['type']=='intrusion-set']
            
            match_all = list(filter(lambda deg: deg[1]==len(ttp_list), deg_counts))

            logger.info('\n'+tabulate(match_all, ["Group Name", "TTP count"], tablefmt="grid"))    
            logger.info('Total groups %d' % len(match_all))

    def get_all_ttp(self):
        '''
        Enumerate all TTP
        '''
        with self.client.session(self.database, SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:
                q_ttp = 'match $e isa external-reference, has source-name "mitre-attack", has external-id like "T[0-9]+";\
                $e has external-id $eid;$a isa attack-pattern, has name $an;\
                $rel (referencing: $a, referenced: $e) isa external-referencing;\
                get $an,$eid;'
                
                answer_iterator = read_transaction.query().match(q_ttp)

                self._ttp= {}

                for q in answer_iterator:
                    attack_name = q.get('an').get_value()
                    ttp_id = q.get('eid').get_value()

                    self._ttp[ttp_id]=attack_name

    def get_all_subttp(self):
        '''
        Enumerate all sub TTP
        '''
        with self.client.session(self.database, SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:
                q_ttp = 'match $e isa external-reference, has source-name "mitre-attack", has external-id like "T[0-9]+\.[0-9]";\
                $e has external-id $eid;$a isa attack-pattern, has name $an;\
                $rel (referencing: $a, referenced: $e) isa external-referencing;\
                get $an,$eid;'
                
                answer_iterator = read_transaction.query().match(q_ttp)

                self._ttp= {}

                for q in answer_iterator:
                    attack_name = q.get('an').get_value()
                    ttp_id = q.get('eid').get_value()

                    self._subttp[ttp_id]=attack_name

    def get_ttp_info(self,ttp_list:list,labels=['name']):
        with self.client.session(self.database, SessionType.DATA) as session:
            ## get various count stats
            with session.transaction(TransactionType.READ) as read_transaction:
                
                data = []
                for ttp_id in ttp_list:
                    
                    q_ttp = f'match\
                            $exref isa external-reference, has source-name "mitre-attack", has external-id "{ttp_id}";\
                            $ap isa attack-pattern;\
                            $rel (referencing: $ap, referenced: $exref) isa external-referencing;\
                            get $ap;'

                    answer_iterator = read_transaction.query().match(q_ttp)

                    for q in answer_iterator:
                        ap = q.get('ap')
                        attr_dict = {}
                        attrs = ap.as_remote(read_transaction).get_has()
                        for x in attrs:
                            attr_dict[str(x.get_type().get_label())]=str(x.get_value())             
                        data.append(attr_dict)
                logger.info(data[0])
                #logger.info('\n'+tabulate(data, ["TTP ID", "Name", "Description", "Revoked"], tablefmt="grid"))    


    def get_ttp_intrusions(self,sort_by='asc',limit=5,threshold=None):
        with self.client.session(self.database, SessionType.DATA) as session:
            ## get various count stats
            with session.transaction(TransactionType.READ) as read_transaction:

                if self._ignoreRevoked:
                    revoke_flag = '$ap has revoked false;'
                else:
                    revoke_flag = '\n'

                query = f'match\
                        $exref isa external-reference, has source-name "mitre-attack", has external-id like "T[0-9]+";\
                        $exref has external-id $exid;\
                        $ap isa attack-pattern, has name $ap_name;\
                        {revoke_flag}\
                        $in isa intrusion-set, has alias $in_alias;\
                        $in has name $in_name;\
                        $rel (referencing: $ap, referenced: $exref) isa external-referencing;\
                        $use (used: $ap, used-by: $in) isa use;\
                        get $ap_name,$exid,$in_name;\
                        group $exid; count;'

                groups_iter = read_transaction.query().match_group_aggregate(query)
                data = []
                for g in groups_iter:
                    count_int = g.numeric().as_int()
                    attribute_str = g.owner()
                    logger.debug(f'Is a type {attribute_str.is_type()}')
                    logger.debug(f'Is a thing {attribute_str.is_thing()}')
                    logger.debug(f'Is a attribute {attribute_str.is_attribute()}')
                    logger.debug(f'Get Type {attribute_str.get_type()}')
                    logger.debug(f'TTP = {attribute_str.get_value()} Count = {count_int}')
                    data.append([attribute_str.get_value(),count_int])
                # sort the list
                if sort_by == 'asc':
                    data = sorted(data,key=itemgetter(1))
                    if threshold: data = list(filter(lambda x: x[1]<=threshold, data))
                elif sort_by == 'desc':
                    data = sorted(data,key=itemgetter(1),reverse=True)
                    if threshold: data = list(filter(lambda x: x[1]>=threshold, data))

                else: raise Exception('Order is either asc or desc')

                logger.info('\n'+tabulate(data[0:limit], ["TTP", "Intrusion counts"], tablefmt="grid"))  

    def get_stats(self):
        with self.client.session(self.database, SessionType.DATA) as session:
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
                