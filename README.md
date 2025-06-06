# TypeDB STIX Schema

This repository contains a TypeDB schema designed to represent the [STIX™ Version 2.1](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html) standard for cyber threat intelligence. The schema is defined across several TypeQL (`.tql`) files.

This repository is compatible with TypeDB 3.x

## Setup

Set up and run a TypeDB Server instance.

**Initialise Schema**

The easiest way to initialise the schema is through TypeDB Console. Run the setup script:
```
typedb console --address=<address> --username=<username> --password=<password> --script=<path to schema/setup_script.tqls
```

The schema files are interdependent (e.g., objects use properties, relationships connect objects). They should typically be loaded into TypeDB in a specific order, often starting with properties, then objects, and finally relationships. The `setup_script.tqls` contains the necessary commands for the loading sequence for the TypeDB console or client.

**Load Sample Data**

TODO properly load the data via python

Temporary micro data: load the a single stix object in the root of this project to play with. This is handwritten and not meant to be a scalable solution

You can do it like this:
```
typedb console --address=<address> --username=<username> --password=<password> --script=<path to sample_data_script.tqls
```

## Sample queries

Here's how to write some basic TypeQL queries to answer some questions:

1) Is this file hash [specific_hash_value] associated with any files that are downloaded by malware?
    Query:
    ```typeql
    match
      $file isa file, has hash "<hash>";
      $malware isa malware, has name $malware-name;
      downloads (downloading-source: $malware, downloaded-target: $file);
    fetch {
      "malware": $malware-name
    };
    ```

2) Is there an infrastructure with a "<infra>", which hosts a tool that delivers a malware, that communicates with an IPV4 address "<ip>"?
    Query:
    ```typeql
    match
      $infra isa infrastructure, has name $infra-name; 
      $infra-name == "<infra>";
      $tool isa tool, has name $tool-name;
      hosts (hosting-source: $infra, hosted-target: $tool);
      $malware isa malware, has name $malware-name;
      delivers (delivering-source: $tool, delivered-target: $malware);
      $ip isa  ipv4-addr, has ipv4_value "<ip>";
      communicates-with (communicating-source: $malware, communicated-target: $ip);
    fetch {
      "infrastructure": $infra-name,
      "tool": $tool-name,
      "malware": $malware-name
    };
    ```



## Schema Structure

The STIX standard defines various objects and their relationships. This schema maps these concepts into TypeDB's type system using entities, attributes, and relations. The schema is organized into the following files:

1.  **`properties.tql`**:
    *   Defines common low-level attributes (properties in STIX terminology) that are reused across different STIX objects. This includes basic types like strings, timestamps, lists, and controlled vocabularies (enums) specified by the STIX standard.

2.  **`domain_objects.tql`**:
    *   Defines the STIX Domain Objects (SDOs). These represent the high-level concepts in threat intelligence.
    *   Examples: `attack-pattern`, `campaign`, `course-of-action`, `identity`, `indicator`, `intrusion-set`, `malware`, `observed-data`, `threat-actor`, `tool`, `vulnerability`.
    *   Each SDO entity inherits from a base `stix-domain-object` and owns the relevant properties defined in `properties.tql` or specific attributes defined within this file.

3.  **`cyber_observable_objects.tql`**:
    *   Defines the STIX Cyber-observable Objects (SCOs). These represent the technical details and artifacts observed in the cyber domain.
    *   Examples: `artifact`, `autonomous-system`, `directory`, `domain-name`, `email-addr`, `email-message`, `file`, `ipv4-addr`, `ipv6-addr`, `mac-addr`, `mutex`, `network-traffic`, `process`, `software`, `url`, `user-account`, `windows-registry-key`, `x509-certificate`.
    *   Each SCO entity inherits from a base `stix-cyber-observable-object` and owns relevant properties.

4. ** `meta_objects.tql`
  * Defines the STIX meta objects

5.  **`relationships.tql`**:
    *   Defines the STIX Relationship Objects (SROs), which represent connections between other STIX objects.
    *   Includes the generic `relationship` type and specific relationship types derived from it (e.g., `related-to`, `duplicate-of`).
    *   Also defines TypeDB relations that model the *linking properties* often found on SDOs and SCOs (like `created_by_ref`, `resolves_to_ref`, `belongs_to_ref`). These TypeDB relations provide a more direct and queryable link between entities compared to just storing the target object's ID in an attribute. For instance, the `resolves_to_ref` attribute on `domain-name` is modeled using a `resolves-to` relation connecting a `domain-name` entity to an `ipv4-addr` or `ipv6-addr` entity.

### TODOs

* Object markings (NOT granular)
  * This one just needs to be done, and isn't dependent on ordering

* Process refs
    owns opened-connection-refs @card(0..),
    owns creator-user-ref,
    owns image-ref,
    owns parent-ref,
    owns child-refs @card(0..)
  * And dicts: environment-variables

* Windows Registry Key
  * creator_user_ref,

  
### Missing components

There are several missing components, mostly in things that require ordered lists in TypeDB, which are not yet implemented.

* Granular markings
  * Ordering matters for granular markings, no matter how they are implemented.
  * There are two major options for implementation: 'natively' in TypeDB, or as as simple strings interpreted by the application.

* All components that semantically conceptually require list orderings:
  * email.received-line[] 


### TypeDB-specific interpretations

- Kill chain phase 

Consultation with experts has suggested that there be globally unique kill_chain_phase entities, instead of attributes/structs.

- External references

These are modeled as entities.

- Extensions

Predefined extensions are modeled using native TypeDB subtypes!

- Dictionaries

TypeDB doesn't have first-class support for dictionaries. As a result, we use an approximation like this, using for example 'hashes':
```
define
  entity STIX-type, # some STIX object that contains some dictionary
    plays hashes-dictionary-entry:owner;
  
  relation hashes-dictionary-entry,
    relates owner @card(1),
    owns hash_algorithm @card(1),   # key
    owns hash_value @card(1);       # value
```

Essentially, the central STIX instance that is meant to _contain_ a dictionary will instead be connected to a set of dictionary entries. This mostly works since we exactly 1 dictionary per object in STIX. A more general would introduce a dictionary entity to hold these entries, so we could connect multiple dictionaries to the same owner.

This implementation of dictionaries does not enforce uniquess of dictionary entry keys (TypeDB's uniqueness contraint is global _per type_, not conditional on any instance, for the time being.)


## Relation to STIX Standard

This schema aims to faithfully represent the structure, properties, and relationships defined in the STIX 2.1 specification. The names of entities, relations, and attributes generally follow the STIX object and property names. Relation role names have been created to try to contextualise relations "source" and "target" specifications. Refer to the official [STIX 2.1 documentation](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html) for detailed definitions of each object and property. 