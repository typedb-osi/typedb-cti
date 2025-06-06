from typing import List, Optional, Dict, Any
from datetime import datetime
import time

JSON = Dict[str, Any]

def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\'")

def isa_statement(var: str, type_: str) -> str:
    return f"${var} isa {type_};"

class KeyMapping:
    def __init__(self, doc_key: str, attribute: str, quoted: bool = False):
        self.doc_key = doc_key
        self.attribute = attribute
        self.quoted = quoted

    def statement(self, var: str, value: any) -> str:
        if self.quoted:
            value = f"'{escape(value)}'"
        if type(value) == bool:
            value = "true" if value else "false"
        return f"${var} has {self.attribute} {value};"


class HasMapping:
    def __init__(self, doc_key: str, attribute: str, quoted: bool = False):
        self.doc_key = doc_key
        self.attribute = attribute
        self.quoted = quoted

    def statement(self, var: str, value: any) -> str:
        if self.quoted:
            value = f"'{escape(value)}'"
        if type(value) == bool:
            value = "true" if value else "false"
        return f"${var} has {self.attribute} {value};"


class RelationMapping:
    def __init__(self, doc_key: str, value_processor: "TypeDBDocumentMapping", relation_type: str, self_role: str, embedded_role: str):
        self.doc_key = doc_key
        self.value_processor = value_processor
        self.relation_type = relation_type
        self.self_role = self_role
        self.embedded_role = embedded_role

    def insert_query(self, doc: JSON, first_player_var: str) -> List[str]:
        pipeline = []
        pipeline.extend(self.value_processor.insert_query(doc, first_player_var))

        embedded_var = self.value_processor.var_with_prefix(first_player_var)
        pipeline.append(f"insert {self.relation_type} ({self.self_role}: ${first_player_var}, {self.embedded_role}: ${embedded_var});")
        return pipeline


class LinksMapping:
    def __init__(self, doc_key: str, player_lookup: str):
        self.doc_key = doc_key
        self.player_lookup = player_lookup


class PropertyMappings:
    def __init__(self):
        self.has_key_mappings = []
        self.has_mappings = []
        self.relation_mappings = []
        self.links_mappings = []
    
    def key(self, doc_key: str, attribute: str, quoted: bool = False):
        self.has_key_mappings.append(KeyMapping(doc_key, attribute, quoted))
        return self

    def has(self, doc_key: str, attribute: str, quoted: bool = False):
        self.has_mappings.append(HasMapping(doc_key, attribute, quoted))
        return self

    def relation(self, doc_key: str, value_processor: "TypeDBDocumentMapping", relation_type: str, self_role: str, embedded_role: str):
        self.relation_mappings.append(RelationMapping(doc_key, value_processor, relation_type, self_role, embedded_role))
        return self
    
    def links(self, doc_key: str, player_lookup: str):
        self.links_mappings.append(LinksMapping(doc_key, player_lookup))
        return self

    def include(self, property_mappings: "PropertyMappings"):
        for mapping in property_mappings.has_key_mappings:
            for existing_mapping in self.has_key_mappings:
                if mapping.doc_key == existing_mapping.doc_key:
                    raise ValueError(f"Duplicate key property mapping for {mapping.doc_key}")
        self.has_key_mappings.extend(property_mappings.has_key_mappings)
        for mapping in property_mappings.has_mappings: 
            for existing_mapping in self.has_mappings:
                if mapping.doc_key == existing_mapping.doc_key:
                    raise ValueError(f"Duplicate has property mapping for {mapping.doc_key}")
        self.has_mappings.extend(property_mappings.has_mappings)
        for mapping in property_mappings.relation_mappings:
            for existing_mapping in self.relation_mappings:
                if mapping.doc_key == existing_mapping.doc_key:
                    raise ValueError(f"Duplicate relation property mapping for {mapping.doc_key}")
        self.relation_mappings.extend(property_mappings.relation_mappings)
        for mapping in property_mappings.links_mappings:
            for existing_mapping in self.links_mappings:
                if mapping.doc_key == existing_mapping.doc_key:
                    raise ValueError(f"Duplicate links property mapping for {mapping.doc_key}")
        self.links_mappings.extend(property_mappings.links_mappings)
        return self


"""
Load a JSON document, that represents a central concept, plus some attribute ownerships, some of which may be keys.
"""
class TypeDBDocumentMapping:
    def __init__(self, type_: str):
        self.var = f"var_{type_}_{int(time.time() * 1000)}"
        self.type_ = type_
        self.property_mappings = PropertyMappings()

    def key(self, doc_key: str, attribute: str, quoted: bool = False):
        self.property_mappings.key(doc_key, attribute, quoted)
        return self

    def has(self, doc_key: str, attribute: str, quoted: bool = False):
        self.property_mappings.has(doc_key, attribute, quoted)
        return self

    def embedded_relation(self, doc_key: str, embedded_loader: "TypeDBDocumentMapping", relation_type: str, self_role: str, embedded_role: str):
        self.property_mappings.relation(doc_key, embedded_loader, relation_type, self_role, embedded_role)
        return self
    
    def links(self, doc_key: str, player_lookup: str):
        self.property_mappings.links(doc_key, player_lookup)
        return self
    
    def include(self, property_mappings: "PropertyMappings"):
        self.property_mappings.include(property_mappings)
        return self

    def insert_query(self, doc: JSON, var_prefix: str = "") -> List[str]:
        print(doc)
        pipeline = []
        var = self.var_with_prefix(var_prefix)

        put_statements = [isa_statement(var, self.type_)]

        # # TODO: keys might be inserted with 'put' instead of 'insert' clauses
        for has_key in self.property_mappings.has_key_mappings:
            value = doc.get(has_key.doc_key)
            if type(value) == list:
                for v in value:
                    put_statements.append(has_key.statement(var, v))
            elif value is not None:
                put_statements.append(has_key.statement(var, value))
        
        put_stage = "put\n" + "\n".join(put_statements)
        pipeline.append(put_stage)

        insert_statements = []
        for has in self.property_mappings.has_mappings:
            value = doc.get(has.doc_key)
            if type(value) == list:
                for v in value:
                    insert_statements.append(has.statement(var, v))
            elif value is not None:
                insert_statements.append(has.statement(var, value))

        if len(insert_statements) > 0:
            insert_stage = "insert\n" + "\n".join(insert_statements)
            pipeline.append(insert_stage)

        for relation in self.property_mappings.relation_mappings:
            value = doc.get(relation.doc_key)
            if type(value) == list:
                for v in value:
                    pipeline.extend(relation.insert_query(v, var))
            elif value is not None:
                pipeline.extend(relation.insert_query(value, var))
        
        return pipeline

    def var_with_prefix(self, prefix: str):
        if len(prefix) > 0:
            return prefix + "_" + self.var
        else:
            return self.var


class ConstantStatement:
    def __init__(self, statement_format_string: str):
        self.statement_format_string = statement_format_string
    
    def apply(self, var: str, builder: str = "") -> List[str]:
        return [self.statement_format_string.format(var=var)]


class DirectValueStatement:
    def __init__(self, doc_key: str, statement_format_string: str, quoted: bool):
        self.statement_format_string = statement_format_string
        self.doc_key = doc_key
        self.quoted = quoted
    
    # TODO: if we have had query builders, we can make this injection-safe?
    def apply(self, doc: JSON, var: str) -> List[str]:
        values = doc.get(self.doc_key)
        statements = []
        if values is not None:
            if isinstance(values, list):
                for value in values:
                    statements.append(self._format_statement(var=var, value=value))
            else:
                statements.append(self._format_statement(var=var, value=values))
        return statements
    
    def _format_statement(self, var: str, value: Optional[str]):
        if self.quoted:
            value = f"'{escape(value)}'"
        return self.statement_format_string.format(var=var, value=value)


class ProcessedValueStages:
    def __init__(self, doc_key: str, value_processor: TypeDBDocumentMapping, statement_format_string: str):
        self.statement_format_string = statement_format_string
        self.doc_key = doc_key
        self.value_processor = value_processor
    
    # TODO: if we have had query builders, we can make this injection-safe?
    def apply(self, doc: JSON, var: str) -> List[str]:
        values = doc.get(self.doc_key)
        player_stages = []
        relation_statements = []
        if values is not None:
            if isinstance(values, list):
                for (i, value) in enumerate(values):
                    other_var = self.value_processor.var_with_prefix(f"{var}_{i}")
                    processed = self.value_processor.apply(value, var_prefix=f"{var}_{i}")
                    player_stages = processed + player_stages
                    relation_statements.append(self._format_statement(var=var, other_var=other_var))
            else:
                value = values
                other_var = self.value_processor.var_with_prefix(var)
                processed = self.value_processor.apply(value, var_prefix=var)
                player_stages = processed + player_stages
                relation_statements.append(self._format_statement(var=var, other_var=other_var)) 

        stages = player_stages
        if len(player_stages) > 0:
            stages.append("put\n" + ";\n".join(relation_statements) + ";")

        return stages
    
    def _format_statement(self, var: str, other_var: [str]):
        return self.statement_format_string.format(var=var, other_var=other_var)

