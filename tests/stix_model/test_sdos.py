import unittest
from src.stix_model.sdos import TypeDBDocumentMapping, attack_pattern_loader, campaign_loader, course_of_action_loader, grouping_loader, identity_loader, incident_loader, indicator_loader, infrastructure_loader, intrusion_set_loader, location_loader, malware_loader, malware_analysis_loader, note_loader, observed_data_loader, opinion_loader, report_loader, threat_actor_loader, tool_loader, vulnerability_loader
from typedb.driver import *

DB_NAME = "test_stix"
SERVER_ADDR = "127.0.0.1:1729"
USERNAME = "admin"
PASSWORD = "password"

class TestAttackLoader(unittest.TestCase):
    def setUp(self):
        self.driver = TypeDB.driver(SERVER_ADDR, Credentials(USERNAME, PASSWORD), DriverOptions(False, None))
        # Clean up any existing test database
        if not self.driver.databases.contains(DB_NAME):
            self.driver.databases.create(DB_NAME)
        
        # Create fresh test database
        with self.driver.transaction(DB_NAME, TransactionType.SCHEMA) as transaction:
            if len(list(transaction.query("match entity $t;").resolve())) == 0:
                # load all the schema files
                with open("schema/properties.tql", "r") as f:
                    query = f.read()
                    transaction.query(query)
                with open("schema/relationships.tql", "r") as f:
                    query = f.read()
                    transaction.query(query)
                with open("schema/additional_components.tql", "r") as f:
                    query = f.read()
                    transaction.query(query)
                with open("schema/domain_objects.tql", "r") as f:
                    query = f.read()
                    transaction.query(query)
                with open("schema/cyber_observable_objects.tql", "r") as f:
                    query = f.read()
                    transaction.query(query)
                transaction.commit()
        self.assert_empty_database()

    def tearDown(self):
        self.delete_all_data()
        self.assert_empty_database()

    def delete_all_data(self):
        with self.driver.transaction(DB_NAME, TransactionType.WRITE) as transaction:
            transaction.query("match $x isa! $t; relation $t; delete $x;")
            transaction.query("match $x isa! $t; entity $t; delete $x;")
            transaction.query("match $x isa! $t; attribute $t; delete $x;")
            transaction.commit()

    def assert_empty_database(self):
        with self.driver.transaction(DB_NAME, TransactionType.READ) as transaction:
            result = next(transaction.query("match $x isa! $t; reduce $count = count;").resolve())
            self.assertEqual(result.get("count").get_integer(), 0)

    def commit_query(self, query):
        with self.driver.transaction(DB_NAME, TransactionType.WRITE) as transaction:
            transaction.query(query)
            transaction.commit()

    def test_attack_pattern_loader(self):
        doc = {
            "type": "attack-pattern",
            "spec_version": "2.1",
            "id": "attack-pattern--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
            "created": "2016-05-12T08:17:27.000Z",
            "modified": "2016-05-12T08:17:27.000Z",
            "name": "Spear Phishing",
            "description": "...",
            "external_references": [
                {
                    "source_name": "capec",
                    "external_id": "CAPEC-163"
                }
            ]
        }
        pipeline = attack_pattern_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_campaign_loader(self):
        doc = {
            "type": "campaign",
            "spec_version": "2.1",
            "id": "campaign--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:00.000Z",
            "modified": "2016-04-06T20:03:00.000Z",
            "name": "Green Group Attacks Against Finance",
            "description": "Campaign by Green Group against a series of targets in the financial services sector."
        }
        pipeline = campaign_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_course_of_action_loader(self):
        doc = {
            "type": "course-of-action",
            "spec_version": "2.1",
            "id": "course-of-action--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "name": "Add TCP port 80 Filter Rule to the existing Block UDP 1434 Filter",
            "description": "This is how to add a filter rule to block inbound access to TCP port 80 to the existing UDP 1434 filter ..."
        }
        pipeline = course_of_action_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_grouping_loader(self):
        doc = {
            "type": "grouping",
            "spec_version": "2.1",
            "id": "grouping--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
            "created_by_ref": "identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
            "created": "2015-12-21T19:59:11.000Z",
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "The Black Vine Cyberespionage Group",
            "description": "A simple collection of Black Vine Cyberespionage Group attributed intel",
            "context": "suspicious-activity",
            "object_refs": [
                "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
                "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
                "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
                "file--0203b5c8-f8b6-4ddb-9ad0-527d727f968b"
            ]
        }
        pipeline = grouping_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_identity_loader(self):
        doc = {
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--e5f1b90a-d9b6-40ab-81a9-8a29df4b6b65",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:00.000Z",
            "modified": "2016-04-06T20:03:00.000Z",
            "name": "ACME Widget, Inc.",
            "identity_class": "organization"
        }
        pipeline = identity_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_incident_loader(self):
        doc = {
            "type": "incident",
            "spec_version": "2.1",
            "id": "incident--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "name": "Incident 43",
            "description": "This incident addresses APT 28 ..."
        }
        pipeline = incident_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_indicator_loader(self):
        doc = {
            "type": "indicator",
            "spec_version": "2.1",
            "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "indicator_types": ["malicious-activity"],
            "name": "Poison Ivy Malware",
            "description": "This file is part of Poison Ivy",
            "pattern": "[ file:hashes.'SHA-256' = '4bac27393bdd9777ce02453256c5577cd02275510b2227f473d03f533924f877' ]",
            "pattern_type": "stix",
            "valid_from": "2016-01-01T00:00:00Z"
        }
        pipeline = indicator_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_infrastructure_loader(self):
        doc = {
            "type": "infrastructure",
            "spec_version": "2.1",
            "id": "infrastructure--38c47d93-d984-4fd9-b87b-d69d0841628d",
            "created": "2016-05-07T11:22:30.000Z",
            "modified": "2016-05-07T11:22:30.000Z",
            "name": "Poison Ivy C2",
            "infrastructure_types": ["command-and-control"]
        }
        pipeline = infrastructure_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_intrusion_set_loader(self):
        doc = {
            "type": "intrusion-set",
            "spec_version": "2.1",
            "id": "intrusion-set--4e78f46f-a023-4e5f-bc24-71b3ca22ec29",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "name": "Bobcat Breakin",
            "description": "Incidents usually feature a shared TTP of a bobcat being released within the building containing network access, scaring users to leave their computers without locking them first. Still determining where the threat actors are getting the bobcats.",
            "aliases": ["Zookeeper"],
            "goals": ["acquisition-theft", "harassment", "damage"]
        }
        pipeline = intrusion_set_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_location_loader(self):
        doc = {
            "type": "location",
            "spec_version": "2.1",
            "id": "location--a6e9345f-5a15-4c29-8bb3-7dcc5d168d64",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:00.000Z",
            "modified": "2016-04-06T20:03:00.000Z",
            "region": "south-eastern-asia",
            "country": "th",
            "administrative_area": "Tak",
            "postal_code": "63170"
        }
        pipeline = location_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_malware_loader(self):
        doc = {
            "type": "malware",
            "spec_version": "2.1",
            "id": "malware--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
            "created": "2016-05-12T08:17:27.000Z",
            "modified": "2016-05-12T08:17:27.000Z",
            "name": "Cryptolocker",
            "description": "A variant of the cryptolocker family",
            "malware_types": ["ransomware"],
            "is_family": False,
            "capabilities": ["encrypts-files", "exfiltrates-data"],
            "implementation_languages": ["c++"],
            "architecture_execution_envs": ["x86-64"]
        }
        pipeline = malware_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_malware_analysis_loader(self):
        doc = {
            "type": "malware-analysis",
            "spec_version": "2.1",
            "id": "malware-analysis--d25167b7-fed0-4068-9ccd-a73dd2c5b07c",
            "created": "2020-01-16T18:52:24.277Z",
            "modified": "2020-01-16T18:52:24.277Z",
            "product": "microsoft",
            "analysis_engine_version": "5.1.0",
            "analysis_definition_version": "053514-0062",
            "analysis_started": "2012-02-11T08:36:14Z",
            "analysis_ended": "2012-02-11T08:36:14Z",
            "result": "malicious"
        }
        pipeline = malware_analysis_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_note_loader(self):
        doc = {
            "type": "note",
            "spec_version": "2.1",
            "id": "note--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
            "created": "2016-05-12T08:17:27.000Z",
            "modified": "2016-05-12T08:17:27.000Z",
            "abstract": "Tracking Team Note#1",
            "content": "This note indicates the various steps taken by the threat analyst team to investigate this specific campaign. Step 1) Do a scan 2) Review scanned results for identified hosts not known by external intel etc.",
            "authors": ["John Doe"],
            "object_refs": ["campaign--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f"]
        }
        pipeline = note_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_observed_data_loader(self):
        doc = {
            "type": "observed-data",
            "spec_version": "2.1",
            "id": "observed-data--b67d30ff-02ac-498a-92f9-32f845f448cf",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T19:58:16.000Z",
            "modified": "2016-04-06T19:58:16.000Z",
            "first_observed": "2015-12-21T19:00:00Z",
            "last_observed": "2015-12-21T19:00:00Z",
            "number_observed": 50,
            "object_refs": [
                "ipv4-addr--efcd5e80-570d-4131-b213-62cb18eaa6a8",
                "domain-name--ecb120bf-2694-4902-a737-62b74539a41b"
            ]
        }
        pipeline = observed_data_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_opinion_loader(self):
        doc = {
            "type": "opinion",
            "spec_version": "2.1",
            "id": "opinion--b01efc25-77b4-4003-b18b-f6e24b5cd9f7",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-05-12T08:17:27.000Z",
            "modified": "2016-05-12T08:17:27.000Z",
            "object_refs": ["relationship--16d2358f-3b0d-4c88-b047-0da2f7ed4471"],
            "opinion": "strongly-disagree",
            "explanation": "This doesn't seem like it is feasible. We've seen how PandaCat has attacked Spanish infrastructure over the last 3 years, so this change in targeting seems too great to be viable. The methods used are more commonly associated with the FlameDragonCrew."
        }
        pipeline = opinion_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_report_loader(self):
        doc = {
            "type": "report",
            "spec_version": "2.1",
            "id": "report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
            "created_by_ref": "identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
            "created": "2015-12-21T19:59:11.000Z",
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "The Black Vine Cyberespionage Group",
            "description": "A simple report with an indicator and campaign",
            "published": "2016-01-20T17:00:00.000Z",
            "report_types": ["campaign"],
            "object_refs": [
                "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
                "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
                "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a"
            ]
        }
        pipeline = report_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_threat_actor_loader(self):
        doc = {
            "type": "threat-actor",
            "spec_version": "2.1",
            "id": "threat-actor--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "threat_actor_types": ["crime-syndicate"],
            "name": "Evil Org",
            "description": "The Evil Org threat actor group",
            "aliases": ["Syndicate 1", "Evil Syndicate 99"],
            "roles": ["director"],
            "goals": ["Steal bank money", "Steal credit cards"],
            "sophistication": "advanced",
            "resource_level": "team",
            "primary_motivation": "organizational-gain"
        }
        pipeline = threat_actor_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_tool_loader(self):
        doc = {
            "type": "tool",
            "spec_version": "2.1",
            "id": "tool--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2016-04-06T20:03:48.000Z",
            "modified": "2016-04-06T20:03:48.000Z",
            "tool_types": ["remote-access"],
            "name": "VNC"
        }
        pipeline = tool_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_vulnerability_loader(self):
        doc = {
            "type": "vulnerability",
            "spec_version": "2.1",
            "id": "vulnerability--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061",
            "created": "2016-05-12T08:17:27.000Z",
            "modified": "2016-05-12T08:17:27.000Z",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "CVE-2016-1234",
            "external_references": [
                {
                    "source_name": "cve",
                    "external_id": "CVE-2016-1234"
                }
            ]
        }
        pipeline = vulnerability_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

if __name__ == '__main__':
    unittest.main() 