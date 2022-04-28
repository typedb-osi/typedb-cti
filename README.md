[![Discord](https://img.shields.io/discord/665254494820368395?color=7389D8&label=chat&logo=discord&logoColor=ffffff)](https://vaticle.com/discord)
[![Discussion Forum](https://img.shields.io/discourse/https/forum.vaticle.com/topics.svg)](https://forum.vaticle.com)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typedb-796de3.svg)](https://stackoverflow.com/questions/tagged/typedb)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-typeql-3dce8c.svg)](https://stackoverflow.com/questions/tagged/typeql)

# TypeDB CTI: Open Source Threat Intelligence Platform

- [Overview](#overview)
- [STIX](#stix)
- [MITRE ATT&CK Data](#mitre-attck-stix-data)
- [Installation](#installation)
- [Examples](#examples)

## Overview

*Watch our first community webinar [here](https://www.youtube.com/watch?v=xuiYorG8-1Q) or read [this blog](https://blog.vaticle.com/introducing-a-knowledge-graph-for-cyber-threat-intelligence-with-typedb-bdb559a92d2a) post for an introduction.*

TypeDB Data - CTI is an open source threat intelligence platform for organisations to store and manage their cyber threat intelligence (CTI) knowledge. It enables threat intel professionals to bring together their disparate CTI information into one database and find new insights about cyber threats.

The benefits of using TypeDB for CTI: 
1. TypeDB enables data to be modelled based on [logical and object-oriented principles](https://docs.vaticle.com/docs/schema/overview). This makes it easy to create complex schemas and ingest disparate and heterogeneous networks of CTI data, through concepts such as type hierarchies, nested relations and n-ary relations.
2. TypeDB's ability to perform [logical inference](https://docs.vaticle.com/docs/schema/rules) during query runtime enables the discovery of new insights from existing CTI data — for example, inferred transitive relations that indicate the attribution of a particular attack pattern to a state-owned entity. 
3. TypeDB enables links between hash values, IP addresses, or indeed any data value that is shared to be made by default, as uniqueness of attribute values is a database guarantee. When attributes are inserted, unique values for any data type are only stored once, and all other uses of that value are connected by relations.

![TypeDB Studio](images/query_0.png)

This repository provides a schema that is based on [STIX2](https://oasis-open.github.io/cti-documentation/), and contains [MITRE ATT&CK](https://github.com/mitre-attack/attack-stix-data) as an example dataset to start exploring this threat intelligence platform. In the future, we plan to incorporate other cyber threat intelligence standards and data sources, in order to create an industry-wide data specification in TypeQL that can be used to ingest any type of threat intel data. 

## STIX

[Structured Threat Information Expression (STIX™)](https://oasis-open.github.io/cti-documentation/) is a language and serialization format used to exchange cyber threat intelligence (CTI).

STIX enables organizations to share CTI with one another in a consistent and machine readable manner, allowing security communities to better understand what computer-based attacks they are most likely to see and to anticipate and/or respond to those attacks faster and more effectively.

STIX is designed to improve many different capabilities, such as collaborative threat analysis, automated threat exchange, automated detection and response, and more.

The data model in TypeDB Data - CTI is currently based on STIX (specifically STIX 2.1), offering a unified and consistent data model for CTI information from an operational to strategic level. This enables the ingestion of heterogeneous CTI data to provide analysts with a single common language to describe the data they work with.  

To learn more about STIX, this [introduction](https://oasis-open.github.io/cti-documentation/stix/walkthrough) and [explanation](https://oasis-open.github.io/cti-documentation/examples/visualized-sdo-relationships) is a good place to start learning how STIX works and why TypeDB Data - CTI uses it. 

An in-depth overview of the how the STIX2 model has been implemented in TypeDB will follow. 

## MITRE ATT&CK STIX Data

[MITRE ATT&CK](https://github.com/mitre-attack/attack-stix-data) is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and in the cybersecurity product and service community.

TypeDB Data - CTI includes a migrator to load MITRE ATT&CK STIX and serves as an example datasets to quickly start exploring this threat intelligence database. 

## Installation 

**Prerequesites**: 
- Python >3.6
- [TypeDB Core 2.6.4](https://vaticle.com/download#core)
- [TypeDB Python Client API 2.6.3](https://docs.vaticle.com/docs/client-api/python)
- [TypeDB Studio 2.4.0-alpha-4](https://vaticle.com/download#typedb-studio)

Clone this repo:

```bash 
git clone https://github.com/typedb-osi/typedb-data-cti
```

Set up a virtual environment and install the dependencies:

```bash
cd <path/to/typedb-data-cti>/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Start TypeDB
```bash 
typedb server
```
Start the migrator script

```bash
python migrate.py
```
This will create a new database called `cti`, insert the schema file and ingest the MITRE ATT&CK datasets; it will take under one minutes to complete. 

## Examples

Once the data is loaded, these queries can be used to explore the data. 

1. Does the "Restrict File and Directory Permissions" course of action mitigate the "BlackTech" intrusion set, and if so, how?
```
match
$course isa course-of-action, has name "Restrict File and Directory Permissions";
$in isa intrusion-set, has name "BlackTech";  
$mit (mitigating: $course, mitigated: $in) isa mitigation;
```
This query returns a relation of type `inferred-mitigation` between the two entities: 
 
![TypeDB Studio](images/query_3.png)

But the `inferred-mitigation` relation does not actually exist in the database, it was inferred at query runtime by TypeDB's reasoner. By double clicking on the inferred relation, the explanation shows that the `course-of-action` actually mitigates an `attack-pattern` with the name `Indicator Blocking`, which has a `use` relation with the `intrusion-set`.

![TypeDB Studio](images/query_4.png)

However, that `use` relation (between the `intrusion-set` and the `attack-pattern`) is also inferred. Double clicking on it shows that the `attack-pattern` is not directly used by the `intrusion-set`. Instead, it is used by a `malware` called `Waterbear`, which is used by the `intrusion-set`.

![TypeDB Studio](images/query_5.png)


2. What attack patterns are used by the malwares that were used by the intrusion set APT28?
```
match 
$intrusion isa intrusion-set, has name "APT28"; 
$malware isa malware, has name $n1; 
$attack-pattern isa attack-pattern, has name $n2;
$rel1 (used-by: $intrusion, used: $malware) isa use; 
$rel2 (used-by: $malware, used: $attack-pattern) isa use; 
```
This query asks for the entity type `intrusion-set` with name `APT28`. It then looks for all the `malwares` that are connected to this `intrusion-set` through the relation `use`. The query also fetches all the `attack-patterns` that are connected through the relation `use` to these `malwares`.

The full answer returns 207 results. Two of those results can be visualised in TypeDB Studio like this: 

![TypeDB Studio](images/query_2.png)

3. What are the attack patterns used by the malware "FakeSpy"?
```
match 
$malware isa malware, has name "FakeSpy";
$attack-pattern isa attack-pattern, has name $apn;
$use (used-by: $malware, used: $attack-pattern) isa use; 
```

Running this query will return 15 different `attack-patterns`, all of which have a relation of type `use` to the `malware`. This is how it is visualised in TypeDB Studio: 

![TypeDB Studio](images/query_1.png)

## Community
If you need any technical support or want to engage with this community, you can join the **#typedb-cti** channel in the [TypeDB Discord server](https://vaticle.com/discord) or join our [Discussion Forum](https://forum.vaticle.com/).
