from typing import Dict, Any, List
from .loaders import TypeDBDocumentMapping
from .scos import (
    artifact_loader,
    autonomous_system_loader,
    directory_loader,
    domain_name_loader,
    email_address_loader,
    email_message_loader,
    file_loader,
    ipv4_addr_loader,
    ipv6_addr_loader,
    mac_addr_loader,
    mutex_loader,
    network_traffic_loader,
    process_loader,
    software_loader,
    url_loader,
    user_account_loader,
    windows_registry_key_loader,
    windows_registry_value_loader,
    x509_certificate_loader
)

# Map of STIX object types to their corresponding loaders
SCO_LOADERS: Dict[str, TypeDBDocumentMapping] = {
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

def get_loader_for_type(type_name: str) -> TypeDBDocumentMapping:
    """
    Get the appropriate loader for a given STIX object type.
    
    Args:
        type_name: The STIX object type name (e.g., "artifact", "file", etc.)
        
    Returns:
        The corresponding TypeDBDocumentLoader for the given type
        
    Raises:
        KeyError: If no loader exists for the given type
    """
    if type_name not in SCO_LOADERS:
        raise KeyError(f"No loader found for STIX object type: {type_name}")
    return SCO_LOADERS[type_name]

def load_stix_object(obj: Dict[str, Any]) -> List[str]:
    """
    Load a STIX object into TypeDB using the appropriate loader.
    
    Args:
        obj: A dictionary representing a STIX object
        
    Returns:
        A list of TypeQL statements to insert the object into TypeDB
        
    Raises:
        KeyError: If the object's type is not recognized
        ValueError: If the object is missing required fields
    """
    if "type" not in obj:
        raise ValueError("STIX object must have a 'type' field")
    
    loader = get_loader_for_type(obj["type"])
    return loader.apply(obj)

__all__ = [
    "SCO_LOADERS",
    "get_loader_for_type",
    "load_stix_object",
    # Export all loaders for direct use if needed
    "artifact_loader",
    "autonomous_system_loader",
    "directory_loader",
    "domain_name_loader",
    "email_address_loader",
    "email_message_loader",
    "file_loader",
    "ipv4_addr_loader",
    "ipv6_addr_loader",
    "mac_addr_loader",
    "mutex_loader",
    "network_traffic_loader",
    "process_loader",
    "software_loader",
    "url_loader",
    "user_account_loader",
    "windows_registry_key_loader",
    "windows_registry_value_loader",
    "x509_certificate_loader"
] 