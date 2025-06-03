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
    file_loader
)

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
    "file": file_loader
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
    
    all_statements = []
    for stix_object in bundle['objects']:
        if not isinstance(stix_object, dict) or 'type' not in stix_object:
            print(f"Warning: Skipping invalid STIX object: {stix_object}")
            continue
            
        object_type = stix_object['type']
        loader = LOADER_MAP.get(object_type)
        
        if loader is None:
            print(f"Warning: No loader found for STIX object type: {object_type}")
            continue
            
        try:
            statements = loader.apply(stix_object)
            all_statements.extend(statements)
        except Exception as e:
            print(f"Error processing STIX object of type {object_type}: {str(e)}")
            continue
    
    return all_statements

if __name__ == "__main__":
    # Example usage
    statements = load_stix_bundle("sample-stix-ics-attack.json")
    for statement in statements:
        print(statement)
        print("---") 