import sys
import json
from typing import Dict, Any, List, Tuple
from stix_model.sdos import (
    attack_pattern_mapping, campaign_mapping, course_of_action_mapping,
    grouping_mapping, identity_mapping, incident_mapping, indicator_mapping,
    infrastructure_mapping, intrusion_set_mapping, location_mapping,
    malware_mapping, malware_analysis_mapping, note_mapping,
    observed_data_mapping, opinion_mapping, report_mapping,
    threat_actor_mapping, tool_mapping, vulnerability_mapping
)
from stix_model.scos import (
    artifact_mapping, autonomous_system_mapping, directory_mapping,
    domain_name_mapping, email_address_mapping, email_message_mapping,
    file_mapping, ipv4_addr_mapping, ipv6_addr_mapping, mac_addr_mapping,
    mutex_mapping, network_traffic_mapping, process_mapping, software_mapping,
    url_mapping, user_account_mapping, windows_registry_key_mapping,
    windows_registry_value_mapping, x509_certificate_mapping
)
from stix_model.relationships import (
    uses_mapping, targets_mapping, resolves_to_mapping, related_to_mapping,
    originates_from_mapping, located_at_mapping, has_mapping, impersonates_mapping,
    hosts_mapping, exfiltrates_to_mapping, duplicate_of_mapping, downloads_mapping,
    derived_from_mapping, controls_mapping, communicates_with_mapping,
    characterizes_mapping, belongs_to_mapping, beacons_to_mapping, based_on_mapping,
    authored_by_mapping, attributed_to_mapping, compromises_mapping, consists_of_mapping,
    delivers_mapping, drops_mapping, exploits_mapping, indicates_mapping,
    investigates_mapping, mitigates_mapping, ownership_mapping, reference_mapping,
    remediates_mapping, variant_of_mapping
)
from stix_model.meta_objects import marking_definition_mapping
from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions

# Map of STIX object types to their corresponding loaders
LOADER_MAP: Dict[str, Any] = {
    # STIX Domain Objects (SDOs)
    "attack-pattern": attack_pattern_mapping,
    "campaign": campaign_mapping,
    "course-of-action": course_of_action_mapping,
    "grouping": grouping_mapping,
    "identity": identity_mapping,
    "incident": incident_mapping,
    "indicator": indicator_mapping,
    "infrastructure": infrastructure_mapping,
    "intrusion-set": intrusion_set_mapping,
    "location": location_mapping,
    "malware": malware_mapping,
    "malware-analysis": malware_analysis_mapping,
    "note": note_mapping,
    "observed-data": observed_data_mapping,
    "opinion": opinion_mapping,
    "report": report_mapping,
    "threat-actor": threat_actor_mapping,
    "tool": tool_mapping,
    "vulnerability": vulnerability_mapping,

    # STIX Cyber-observable Objects (SCOs)
    "artifact": artifact_mapping,
    "autonomous-system": autonomous_system_mapping,
    "directory": directory_mapping,
    "domain-name": domain_name_mapping,
    "email-addr": email_address_mapping,
    "email-message": email_message_mapping,
    "file": file_mapping,
    "ipv4-addr": ipv4_addr_mapping,
    "ipv6-addr": ipv6_addr_mapping,
    "mac-addr": mac_addr_mapping,
    "mutex": mutex_mapping,
    "network-traffic": network_traffic_mapping,
    "process": process_mapping,
    "software": software_mapping,
    "url": url_mapping,
    "user-account": user_account_mapping,
    "windows-registry-key": windows_registry_key_mapping,
    "windows-registry-value": windows_registry_value_mapping,
    "x509-certificate": x509_certificate_mapping,

    # STIX meta objects
    "marking-definition": marking_definition_mapping
}

RELATIONSHIP_mapping_MAP: Dict[str, Any] = {
    "attributed-to": attributed_to_mapping,
    "authored-by": authored_by_mapping,
    "based-on": based_on_mapping,
    "beacons-to": beacons_to_mapping,
    "belongs-to": belongs_to_mapping,
    "characterizes": characterizes_mapping,
    "communicates-with": communicates_with_mapping,
    "compromises": compromises_mapping,
    "consists-of": consists_of_mapping,
    "controls": controls_mapping,
    "delivers": delivers_mapping,
    "derived-from": derived_from_mapping,
    "downloads": downloads_mapping,
    "drops": drops_mapping,
    "duplicate-of": duplicate_of_mapping,
    "exfiltrates-to": exfiltrates_to_mapping,
    "exploits": exploits_mapping,
    "has": has_mapping,
    "hosts": hosts_mapping,
    "impersonates": impersonates_mapping,
    "indicates": indicates_mapping,
    "investigates": investigates_mapping,
    "located-at": located_at_mapping,
    "mitigates": mitigates_mapping,
    "originates-from": originates_from_mapping,
    "ownership": ownership_mapping,
    "reference": reference_mapping,
    "related-to": related_to_mapping,
    "remediates": remediates_mapping,
    "resolves-to": resolves_to_mapping,
    "targets": targets_mapping,
    "uses": uses_mapping,
    "variant-of": variant_of_mapping
}

def load_stix_bundle(file_path: str) -> (List[str], List[Tuple[str, Any]]):
    """
    Load a STIX bundle from a file and process each object using the appropriate loader.
    Returns a list of TypeQL statements to be executed.
    """
    with open(file_path, 'r') as f:
        bundle = json.load(f)

    if not isinstance(bundle, dict) or 'objects' not in bundle:
        raise ValueError("Invalid STIX bundle format: missing 'objects' array")

    insert_queries = []
    inserted = []
    for stix_object in bundle['objects']:
        if not isinstance(stix_object, dict) or 'type' not in stix_object:
            sys.stderr.write(f"Warning: Skipping invalid STIX object: {stix_object}\n")
            continue

        object_type = stix_object['type']
        if object_type == "relationship":
            relationship_type = stix_object['relationship_type']
            loader = RELATIONSHIP_mapping_MAP.get(relationship_type)
        else:
            relationship_type = None
            loader = LOADER_MAP.get(object_type)

        if loader is None:
            sys.stderr.write(f"Warning: No loader found for STIX document: {object_type} (relationship: {relationship_type})\n")
            continue

        inserted.append((stix_object['id'], loader))

        insert_query = loader.insert_query(stix_object)
        insert_queries.append("\n".join(insert_query))


    return (insert_queries, inserted)


def setup(driver, db_name):
    # Clean up any existing test database
    if driver.databases.contains(db_name):
        driver.databases.get(db_name).delete()
    driver.databases.create(db_name)

    # Create fresh test database
    with driver.transaction(db_name, TransactionType.SCHEMA) as transaction:
        # load all the schema files
        with open("sample/schema.tql", "r") as f:
            query = f.read()
            transaction.query(query).resolve()
        transaction.commit()

    return driver


DB_NAME = "stix"
SERVER_ADDR = "127.0.0.1:1729"
USERNAME = "admin"
PASSWORD = "password"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TypeDB STIX demo tool")
    parser.add_argument("--address", type=str, help="TypeDB address", default=SERVER_ADDR)
    parser.add_argument("--username", type=str, help="TypeDB username", default=USERNAME)
    parser.add_argument("--password", type=str, help="TypeDB password", default=PASSWORD)
    parser.add_argument("--tls-disabled", action="store_true", help="Connect to TypeDB without TLS encryption")
    parser.add_argument("--db-name", type=str, help="STIX database name", default=DB_NAME)

    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        required=True
    )

    parser_setup = subparsers.add_parser("setup", help="Create or reset the state of the TypeDB STIX database")

    parser_ingest = subparsers.add_parser("ingest", help="Ingest a STIX bundle into TypeDB")
    parser_ingest.add_argument("bundle", help="A STIX bundle JSON file")

    parser_fetch = subparsers.add_parser("fetch", help="Fetch a STIX object")
    parser_fetch.add_argument("--id", help="STIX object ID")

    args = parser.parse_args()

    driver = TypeDB.driver(args.address, Credentials(args.username, args.password), DriverOptions(not args.tls_disabled, None))

    if args.command == "setup":
        setup(driver, args.db_name)
    elif args.command == "ingest":
        (insert_queries, inserted) = load_stix_bundle(args.bundle)
        with driver.transaction(args.db_name, TransactionType.WRITE) as transaction:
            for insert_query in insert_queries:
                transaction.query(insert_query)
            transaction.commit()
    elif args.command == "fetch":
        type = args.id.split('--')[0]
        if type in LOADER_MAP:
            loader = LOADER_MAP[type]
        elif type in RELATIONSHIP_mapping_MAP:
            loader = RELATIONSHIP_mapping_MAP[type]
        else:
            sys.stderr.write(f"Warning: No loader found for STIX object of type `{type}`\n")
            sys.exit(1)
        fetch_query = loader.match('x', args.id) + " fetch " + loader.fetch('x') + ";"
        with driver.transaction(args.db_name, TransactionType.READ) as transaction:
            stream = transaction.query(fetch_query).resolve()
            try:
                print(json.dumps(next(stream), indent=True, sort_keys=True))
            except StopIteration:
                sys.stderr.write(f"STIX object id {args.id} not found\n")
