import json
from typing import Dict, Any, List
from stix_model.sdos import (
    attack_pattern_loader, campaign_loader, course_of_action_loader,
    grouping_loader, identity_loader, incident_loader, indicator_loader,
    infrastructure_loader, intrusion_set_loader, location_loader,
    malware_loader, malware_analysis_loader, note_loader,
    observed_data_loader, opinion_loader, report_loader,
    threat_actor_loader, tool_loader, vulnerability_loader
)
from stix_model.scos import (
    artifact_loader, autonomous_system_loader, directory_loader,
    domain_name_loader, email_address_loader, email_message_loader,
    file_loader, ipv4_addr_loader, ipv6_addr_loader, mac_addr_loader,
    mutex_loader, network_traffic_loader, process_loader, software_loader,
    url_loader, user_account_loader, windows_registry_key_loader,
    windows_registry_value_loader, x509_certificate_loader
)
from stix_model.relationships import uses_loader

# Map of STIX object types to their corresponding loaders
LOADER_MAP: Dict[str, Any] = {
    # STIX Domain Objects (SDOs)
    "attack-pattern": attack_pattern_loader,
    "campaign": campaign_loader,
    "course-of-action": course_of_action_loader,
    "grouping": grouping_loader,
    "identity": identity_loader,
    "incident": incident_loader,
    "indicator": indicator_loader,
    "infrastructure": infrastructure_loader,
    "intrusion-set": intrusion_set_loader,
    "location": location_loader,
    "malware": malware_loader,
    "malware-analysis": malware_analysis_loader,
    "note": note_loader,
    "observed-data": observed_data_loader,
    "opinion": opinion_loader,
    "report": report_loader,
    "threat-actor": threat_actor_loader,
    "tool": tool_loader,
    "vulnerability": vulnerability_loader,
    
    # STIX Cyber-observable Objects (SCOs)
    "artifact": artifact_loader,
    "autonomous-system": autonomous_system_loader,
    "directory": directory_loader,
    "domain-name": domain_name_loader,
    "email-addr": email_address_loader,
    "email-message": email_message_loader,
    "file": file_loader,
    "ipv4-addr": ipv4_addr_loader,
    "ipv6-addr": ipv6_addr_loader,
    "mac-addr": mac_addr_loader,
    "mutex": mutex_loader,
    "network-traffic": network_traffic_loader,
    "process": process_loader,
    "software": software_loader,
    "url": url_loader,
    "user-account": user_account_loader,
    "windows-registry-key": windows_registry_key_loader,
    "windows-registry-value": windows_registry_value_loader,
    "x509-certificate": x509_certificate_loader
}

RELATIONSHIP_LOADER_MAP: Dict[str, Any] = {
    "uses": uses_loader
}

def load_stix_bundle(file_path: str) -> List[str]:
    """
    Load a STIX bundle from a file and process each object using the appropriate loader.
    Returns a list of TypeQL statements to be executed.
    """
    with open(file_path, 'r') as f:
        bundle = json.load(f)
    
    if not isinstance(bundle, dict) or 'objects' not in bundle:
        raise ValueError("Invalid STIX bundle format: missing 'objects' array")
    
    insert_queries = []
    for stix_object in bundle['objects']:
        if not isinstance(stix_object, dict) or 'type' not in stix_object:
            print(f"Warning: Skipping invalid STIX object: {stix_object}")
            continue
            
        object_type = stix_object['type']
        if object_type == "relationship":
            relationship_type = stix_object['relationship_type']
            loader = RELATIONSHIP_LOADER_MAP.get(relationship_type)
        else:
            relationship_type = None 
            loader = LOADER_MAP.get(object_type)
        
        if loader is None:
            print(f"Warning: No loader found for STIX document: {object_type} (relationship: {relationship_type})")
            continue
            
        insert_query = loader.insert_query(stix_object)
        insert_queries.append("\n".join(insert_query))

    
    return insert_queries

if __name__ == "__main__":
    # Example usage
    insert_queries = load_stix_bundle("sample-stix-ics-attack.json")
    for insert_query in insert_queries:
        print(insert_query)
        print("---") 