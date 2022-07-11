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
import sys
import requests

import requests
import shutil

import os

logging.basicConfig(level=logging.INFO) 

def download_file(url,folder):
    local_filename = os.path.join(folder,url.split('/')[-1])

    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Remote file does not exist')
    return local_filename

URL_GIT = 'https://github.com/mitre-attack/attack-stix-data/blob/master/'
URL_ENTERPRISE = f'{URL_GIT}enterprise-attack/enterprise-attack.json'
URL_MOBILE = f'{URL_GIT}enterprise-attack/mobile-attack.json'
URL_ICS = f'{URL_GIT}enterprise-attack/ics-attack.json'

parser = argparse.ArgumentParser(description='Download specific versions of the attack dataset from MITRE')
parser.add_argument('--type', dest='type', default='enterprise', help='Download either enterprise,mobile or ics attack data')
parser.add_argument('--version', dest='version', default='latest', help='Download a specific version')
parser.add_argument('--folder', dest='folder', default='./data/mitre', help='Download into specific folder')

try:
    args = parser.parse_args()

    if args.type == 'enterprise':
        logging.info('Downloading enterprise file...')
        if args.version == 'latest':
            file = download_file(URL_ENTERPRISE,args.folder)
        else:
            url_version =f'{URL_GIT}enterprise-attack/ics-enterprise-{args.version}.json'
            file = download_file(url_version,args.folder)
        logging.info(f'Ready in {file}')

    elif args.type == 'mobile':
        logging.info('Downloading enterprise file...')
        if args.version == 'latest':
            file = download_file(URL_MOBILE,args.folder)
        else:
            url_version =f'{URL_GIT}enterprise-attack/ics-mobile-{args.version}.json'
            file = download_file(url_version,args.folder)
        logging.info(f'Ready in {file}')

    elif args.type == 'ics':
        logging.info('Downloading enterprise file...')
        if args.version == 'latest':
            file = download_file(URL_ICS,args.folder)
        else:
            url_version =f'{URL_GIT}enterprise-attack/ics-attack-{args.version}.json'
            file = download_file(url_version,args.folder)

        logging.info(f'Ready in {file}')

except argparse.ArgumentError:
    parser.print_help()
    sys.exit(0)
except Exception as e:
    logging.error(e)
    sys.exit(0)
