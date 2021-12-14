
# TypeDB - Data CTI

**[Overview](#overview)** | **[STIX](#stix)** | **[ATT&CK STIX Data](#att%26ck%20stix%20data)** | **[Installation](#installation)** | **[Examples](#examples)**

[![Discord](https://img.shields.io/discord/665254494820368395?color=7389D8&label=chat&logo=discord&logoColor=ffffff)](https://vaticle.com/discord)
[![Discussion Forum](https://img.shields.io/discourse/https/forum.vaticle.com/topics.svg)](https://forum.vaticle.com)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typedb-796de3.svg)](https://stackoverflow.com/questions/tagged/typedb)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typeql-3dce8c.svg)](https://stackoverflow.com/questions/tagged/typeql)

## Overview
TypeDB - Data CTI is an open source knowledge graph for organisations to organise and manage their cyber threat intelligence knowledge. It's been created to enable CTI professionals to represent their disparate CTI information into one knowledge graph and find new insights about cyber threats. 

This repository provides a schema that is based on [STIX2](https://oasis-open.github.io/cti-documentation/), and contains the [MITRE ATT&CK](https://github.com/mitre-attack/attack-stix-data) dataset to make it easy to start working with TypeDB - Data CTI. In the future, we plan to incorporate other CTI data standards, in order to create an industry-wide knowledge graph that can be used to ingest CTI information in any type of standard. 

[insert screenshot]


## STIX

[Structured Threat Information Expression (STIX™)](https://oasis-open.github.io/cti-documentation/) is a language and serialization format used to exchange cyber threat intelligence (CTI).

STIX enables organizations to share CTI with one another in a consistent and machine readable manner, allowing security communities to better understand what computer-based attacks they are most likely to see and to anticipate and/or respond to those attacks faster and more effectively.

STIX is designed to improve many different capabilities, such as collaborative threat analysis, automated threat exchange, automated detection and response, and more.

The data model in TypeDB - Data CTI is based on the STIX standard (specifically STIX 2.1), which makes it possible to ingest heterogeneous CTI data into one unified standard. This makes it easy for different CTI analysts to describe their knowledge and share it with each other. 

To learn more, this [introduction](https://oasis-open.github.io/cti-documentation/stix/walkthrough) and [explanation of relationships](https://oasis-open.github.io/cti-documentation/examples/visualized-sdo-relationships) is a good place to start how STIX works and why TypeDB - Data CTI uses it. 

An in-depth overview of the how the STIX2 model has been implemented in TypeDB will follow. 

## ATT&CK STIX Data

[MITRE ATT&CK](https://github.com/mitre-attack/attack-stix-data) is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and in the cybersecurity product and service community.

The dataset includes a few custom types, which are prefixed with "x_type". For those types, we refrained from changing the "pure STIX2" model, and created a custom type and ingested the type as a separate attribute. 

## Installation 

**Prerequesites**: Python >3.6,  [TypeDB Core 2.5.0](https://vaticle.com/download#core),  [TypeDB Python Client API 2.5.0](https://docs.vaticle.com/docs/client-api/python),  [TypeDB Studio 2.4.0-alpha-4](https://vaticle.com/download#typedb-studio).

Clone this repo:

```bash 
    git clone https://github.com/typedb-osi/typedb-data-cti
```

Set up a virtual environment and install the dependencies:

```bash
    cd <path/to/typedb-data-cti>/
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```
Start TypeDB
```bash 
    typedb server
```
Start the migrator script

```bash
    python migrator.py
```
This will create a new database called `cti`, insert the schema file and ingest the MITRE ATTCK datasets; it will take one or two minutes to complete. 

## Examples 

Once the data is loaded, you can try these queries to start to explore the data. 

*Find me all the attack patterns that are being used by the Malware "Tiktok Pro*
```
match 
$malware isa malware, has name "FakeSpy";
$attack-pattern isa attack-pattern, has name $apn;
$use (used-by: $malware, used: $attack-pattern) isa use; 
```

This will return 15 different `attack-patterns`, all of which have a relation of type `use` to the FakeSpy `malware`. This is how the query result looks like in TypeDB Studio: 

![query_1](Images/query_1.png)

*Traversal example for mitre*
```
match 
$intrusion isa intrusion-set; $malware isa malware; $3 isa attack-pattern; 
$x (used-by: $intrusion, used: $malware) isa use; 
$y (used-by: $malware, used: $attack-pattern) isa use; 
$z (used-by: $intrusion, used: $$attack-pattern) isa use; 
```

*Inference example*
```
match  
$course isa course-of-action, has name "Restrict File and Directory Permissions";
$in isa intrusion-set, has name "BlackTech";  
$im (mitigated: $in, mitigating: $course) isa inferred-mitigation;
```

## Community
If you need any technical support or want to engage with this community, you can join the *#cti* channel in the [TypeDB Discord server](https://vaticle.com/typedb). 