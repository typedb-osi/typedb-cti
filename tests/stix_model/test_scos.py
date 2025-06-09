import unittest
from src.stix_model.scos import TypeDBDocumentMapping, artifact_loader, autonomous_system_loader, directory_loader, domain_name_loader, email_address_loader, email_message_loader, file_loader
from typedb.driver import *

DB_NAME = "test_stix"
SERVER_ADDR = "127.0.0.1:1729"
USERNAME = "admin"
PASSWORD = "password"

class TestCyberObservableLoader(unittest.TestCase):
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

    def test_artifact_loader(self):
        doc = {
            "type": "artifact",
            "spec_version": "2.1",
            "id": "artifact--ca17bcf8-9846-5ab4-8662-75c1bf6e63ee",
            "mime_type": "image/jpeg",
            "payload_bin": "VBORw0KGgoAAAANSUhEUgAAADI==",
            "hashes": {
                "MD5": "d41d8cd98f00b204e9800998ecf8427e",
                "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }
        }
        pipeline = artifact_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_autonomous_system_loader(self):
        doc = {
            "type": "autonomous-system",
            "spec_version": "2.1",
            "id": "autonomous-system--f720c34b-98ae-597f-ade5-27dc241e8c74",
            "number": 15139,
            "name": "Slime Industries",
            "rir": "ARIN"
        }
        pipeline = autonomous_system_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_directory_loader(self):
        doc = {
            "type": "directory",
            "spec_version": "2.1",
            "id": "directory--93c0a9b0-520d-545d-9094-1a08ddf46b05",
            "path": "C:\\Windows\\System32",
            "ctime": "2016-01-20T14:11:25.55Z",
            "mtime": "2016-01-20T14:11:25.55Z",
            "atime": "2016-01-20T14:11:25.55Z"
        }
        pipeline = directory_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_domain_name_loader(self):
        doc = {
            "type": "domain-name",
            "spec_version": "2.1",
            "id": "domain-name--3c10e93f-798e-5a26-a0c1-08156efab7f5",
            "value": "example.com"
        }
        pipeline = domain_name_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_email_address_loader(self):
        doc = {
            "type": "email-addr",
            "spec_version": "2.1",
            "id": "email-addr--2d77a846-6264-5d51-b586-e43822ea1ea3",
            "value": "john@example.com",
            "display_name": "John Doe",
            "belongs_to_ref": "user-account--a0c1b8c7-d6e5-4f3g-2h1i-0j9k8l7m6n5o"
        }
        pipeline = email_address_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

    def test_email_message_loader(self):
        # Create a document representing an email message
        doc = {
            "type": "email-message",
            "spec_version": "2.1",
            "id": "email-message--72b7698f-10c2-565a-a2a6-b4996a2f2265",
            "from_ref": "email-addr--89f52ea8-d6ef-51e9-8fce-6a29236436ed",
            "to_refs": ["email-addr--e4ee5301-b52d-59cd-a8fa-8036738c7194"],
            "is_multipart": False,
            "date": "1997-11-21T15:55:06.000Z",
            "subject": "Saying Hello"
        }

        # Apply the email message loader
        pipeline = email_message_loader.apply(doc)
        query = "\n".join(pipeline)

        # Commit the query
        self.commit_query(query)

    def test_file_loader(self):
        """Test the file loader with a basic file example."""
        doc = {
            "type": "file",
            "id": "file--f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "spec_version": "2.1",
            "hashes": {
                "MD5": "44d88612fea8a8f36de82e1278abb02f",
                "SHA-1": "55d88612fea8a8f36de82e1278abb02f",
                "SHA-256": "66d88612fea8a8f36de82e1278abb02f"
            },
            "size": 12345,
            "name": "example.exe",
            "mime_type": "application/x-dosexec",
            "ctime": "2016-01-20T14:11:25.55Z",
            "mtime": "2016-01-20T14:11:25.55Z",
            "atime": "2016-01-20T14:11:25.55Z"
        }

        pipeline = file_loader.apply(doc)
        query = "\n".join(pipeline)
        self.commit_query(query)

if __name__ == '__main__':
    unittest.main() 