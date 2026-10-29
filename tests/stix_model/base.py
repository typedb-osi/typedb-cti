import os
import re
import unittest
from main import setup, LOADER_MAP
from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions, DriverTlsConfig

DB_NAME = "test_stix"
SERVER_ADDR = os.environ.get("TYPEDB_ADDRESS", "127.0.0.1:1729")
USERNAME = os.environ.get("TYPEDB_USERNAME", "admin")
PASSWORD = os.environ.get("TYPEDB_PASSWORD", "password")

TIMESTAMP = "2016-01-01T00:00:00.000Z"

# Required properties (beyond type/id) of the object types that test documents reference
REQUIRED_PROPERTIES = {
    "identity": {"name": "Referenced Identity"},
    "campaign": {"name": "Referenced Campaign"},
    "indicator": {"pattern": "[file:name = 'x']", "pattern_type": "stix", "valid_from": TIMESTAMP},
    "email-addr": {"value": "referenced@example.com"},
    "ipv4-addr": {"value": "198.51.100.1"},
    "domain-name": {"value": "example.com"},
    "file": {"name": "referenced.exe"},
    "user-account": {"user_id": "referenced"},
}


def referenced_ids(doc):
    for key, value in doc.items():
        if key.endswith("_ref"):
            yield value
        elif key.endswith("_refs"):
            yield from value


def minimal_object(stix_id):
    """A minimal valid STIX object with the given ID, standing in for an object a test document references."""
    type_ = stix_id.split("--")[0]
    doc = {"type": type_, "id": stix_id, "spec_version": "2.1", "created": TIMESTAMP, "modified": TIMESTAMP}
    doc.update(REQUIRED_PROPERTIES.get(type_, {}))
    return doc


class TypeDBTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = TypeDB.driver(SERVER_ADDR, Credentials(USERNAME, PASSWORD), DriverOptions(DriverTlsConfig.disabled()))
        # Create a fresh test database with the full schema
        setup(cls.driver, DB_NAME)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def setUp(self):
        self.assert_empty_database()

    def tearDown(self):
        self.delete_all_data()
        self.assert_empty_database()

    def delete_all_data(self):
        with self.driver.transaction(DB_NAME, TransactionType.WRITE) as transaction:
            transaction.query("match $x isa! $t; relation $t; delete $x;").resolve()
            transaction.query("match $x isa! $t; entity $t; delete $x;").resolve()
            transaction.query("match $x isa! $t; attribute $t; delete $x;").resolve()
            transaction.commit()

    def assert_empty_database(self):
        with self.driver.transaction(DB_NAME, TransactionType.READ) as transaction:
            result = next(transaction.query("match $x isa! $t; reduce $count = count;").resolve())
            self.assertEqual(result.get("count").get_integer(), 0)

    def commit_query(self, query):
        with self.driver.transaction(DB_NAME, TransactionType.WRITE) as transaction:
            transaction.query(query).resolve()
            transaction.commit()

    def assert_round_trip(self, mapping, doc):
        """
        Insert the document, alongside minimal versions of the objects it references (as a self-contained bundle
        would provide them), then fetch it back and check its non-timestamp scalar properties survived.
        """
        with self.driver.transaction(DB_NAME, TransactionType.WRITE) as transaction:
            for ref in referenced_ids(doc):
                referenced = minimal_object(ref)
                transaction.query("\n".join(LOADER_MAP[referenced["type"]].insert_query(referenced))).resolve()
            transaction.query("\n".join(mapping.insert_query(doc))).resolve()
            transaction.commit()

        with self.driver.transaction(DB_NAME, TransactionType.READ) as transaction:
            query = mapping.match("x", doc["id"]) + " fetch " + mapping.fetch("x") + ";"
            fetched = list(transaction.query(query).resolve())
        self.assertEqual(len(fetched), 1)
        for key, value in doc.items():
            # TypeDB returns timestamps in its own canonical format, so only compare the other scalars
            if isinstance(value, (str, int, bool)) and not re.match(r"\d{4}-\d\d-\d\dT", str(value)):
                self.assertEqual(fetched[0][key], value, f"property '{key}'")
