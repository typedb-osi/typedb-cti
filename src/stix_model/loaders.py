from typing import List, Optional, Dict, Any
from datetime import datetime
import time

JSON = Dict[str, Any]

def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")

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


class RelationNewPlayerMapping:
    def __init__(self, doc_key: str, other_player_processor: "TypeDBDocumentMapping", relation_type: str, self_role: str, other_player_role: str):
        self.doc_key = doc_key
        self.other_player_processor = other_player_processor
        self.relation_type = relation_type
        self.self_role = self_role
        self.other_player_role = other_player_role

    def insert_query(self, doc: JSON, first_player_var: str, index: int = 0) -> List[str]:
        pipeline = [f"\n### Load complete player from property '{self.doc_key}' and link via relation '{self.relation_type}' with role '{self.self_role}'"]
        pipeline.extend(self.other_player_processor.insert_query(doc, first_player_var + f"_{index}"))

        other_player_var = self.other_player_processor.var_with_prefix(first_player_var + f"_{index}")
        pipeline.append(f"\ninsert {self.relation_type} ({self.self_role}: ${first_player_var}, {self.other_player_role}: ${other_player_var});")
        return pipeline


class RelationExistingPlayerMapping:
    def __init__(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False):
        self.player_attribute_doc_key = player_attribute_doc_key
        self.player_attribute = player_attribute
        self.relation_type = relation_type
        self.self_role = self_role
        self.player_role = player_role
        self.quoted = quoted

    def insert_query(self, player_attribute_value: any, first_player_var: str, index: int = 0) -> List[str]:
        pipeline = [f"\n### Load player from property '{self.player_attribute_doc_key}' and link via relation '{self.relation_type}' with role '{self.self_role}'"]
        player_var = f"player_{self.player_attribute_doc_key}_{index}"
        player_type_var = f"{player_var}_type"
        if self.quoted:
            player_attribute_value = f"'{escape(player_attribute_value)}'"
        if type(player_attribute_value) == bool:
            player_attribute_value = "true" if player_attribute_value else "false"
        pipeline.append(f"""match 
${player_var} has {self.player_attribute} {player_attribute_value};
${player_var} isa! ${player_type_var};
${player_type_var} plays {self.relation_type}:{self.player_role};""")
        pipeline.append(f"insert {self.relation_type} ({self.self_role}: ${first_player_var}, {self.player_role}: ${player_var});")
        return pipeline


class LinksMapping:
    def __init__(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False):
        self.player_attribute_doc_key = player_attribute_doc_key
        self.player_attribute = player_attribute
        self.role = role
        self.quoted = quoted

    def insert_query(self, player_attribute_value: any, relation_var: str, relation_type: str, index: int = 0) -> List[str]:
        pipeline = [f"\n### Relation '{relation_type}' links player using property {self.player_attribute_doc_key} with role {self.role}"]
        player_var = f"player_{self.player_attribute_doc_key}_{index}"
        player_type_var = f"{player_var}_type"
        if self.quoted:
            player_attribute_value = f"'{escape(player_attribute_value)}'"
        if type(player_attribute_value) == bool:
            player_attribute_value = "true" if player_attribute_value else "false"
        pipeline.append(f"""match 
${player_var} has {self.player_attribute} {player_attribute_value};
${player_var} isa! ${player_type_var};
${player_type_var} plays {relation_type}:{self.role};""")
        pipeline.append(f"insert ${relation_var} links ({self.role}: ${player_var});")
        return pipeline


class PropertyMappings:
    def __init__(self):
        self.has_key_mappings = []
        self.has_mappings = []
        self.relation_new_player_mappings = []
        self.relation_existing_player_mappings = []
        self.links_mappings = []
    
    def key(self, doc_key: str, attribute: str, quoted: bool = False):
        self.has_key_mappings.append(KeyMapping(doc_key, attribute, quoted))
        return self

    def has(self, doc_key: str, attribute: str, quoted: bool = False):
        self.has_mappings.append(HasMapping(doc_key, attribute, quoted))
        return self

    def relation_and_new_player(self, doc_key: str, other_player_processor: "TypeDBDocumentMapping", relation_type: str, self_role: str, other_player_role: str):
        self.relation_new_player_mappings.append(RelationNewPlayerMapping(doc_key, other_player_processor, relation_type, self_role, other_player_role))
        return self

    def relation_existing_player(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False):
        self.relation_existing_player_mappings.append(RelationExistingPlayerMapping(player_attribute_doc_key, player_attribute, relation_type, self_role, player_role, quoted))
        return self
    
    def links(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False):
        self.links_mappings.append(LinksMapping(player_attribute_doc_key, player_attribute, role, quoted))
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
        for mapping in property_mappings.relation_new_player_mappings:
            for existing_mapping in self.relation_new_player_mappings:
                if mapping.doc_key == existing_mapping.doc_key:
                    raise ValueError(f"Duplicate relation property mapping for {mapping.doc_key}")
        self.relation_new_player_mappings.extend(property_mappings.relation_new_player_mappings)
        for mapping in property_mappings.relation_existing_player_mappings:
            for existing_mapping in self.relation_existing_player_mappings:
                if mapping.player_attribute_doc_key == existing_mapping.player_attribute_doc_key:
                    raise ValueError(f"Duplicate relation property mapping for {mapping.player_attribute_doc_key}")
        self.relation_existing_player_mappings.extend(property_mappings.relation_existing_player_mappings)
        for mapping in property_mappings.links_mappings:
            for existing_mapping in self.links_mappings:
                if mapping.player_attribute_doc_key == existing_mapping.player_attribute_doc_key:
                    raise ValueError(f"Duplicate links property mapping for {mapping.player_attribute_doc_key}")
        self.links_mappings.extend(property_mappings.links_mappings)
        return self


"""
Load a JSON document, that represents a central concept, plus some attribute ownerships, some of which may be keys.
"""
class TypeDBDocumentMapping:
    def __init__(self, type_: str):
        self.var = f"{type_}"
        self.type_ = type_
        self.property_mappings = PropertyMappings()

    def key(self, doc_key: str, attribute: str, quoted: bool = False):
        self.property_mappings.key(doc_key, attribute, quoted)
        return self

    def has(self, doc_key: str, attribute: str, quoted: bool = False):
        self.property_mappings.has(doc_key, attribute, quoted)
        return self

    def relation_and_new_player(self, doc_key: str, other_player_mapping: "TypeDBDocumentMapping", relation_type: str, self_role: str, other_player_role: str):
        self.property_mappings.relation_and_new_player(doc_key, other_player_mapping, relation_type, self_role, other_player_role)
        return self
    
    def relation_existing_player(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False):
        self.property_mappings.relation_existing_player(player_attribute_doc_key, player_attribute, relation_type, self_role, player_role, quoted)
        return self

    def links(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False):
        self.property_mappings.links(player_attribute_doc_key, player_attribute, role, quoted)
        return self

    def include(self, property_mappings: "PropertyMappings"):
        self.property_mappings.include(property_mappings)
        return self

    def insert_query(self, doc: JSON, var_prefix: str = "") -> List[str]:
        pipeline = [f"\n### Put object of type '{self.type_}'"]
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
                for i, v in enumerate(value):
                    insert_statements.append(has.statement(var + f"_{i}", v))
            elif value is not None:
                insert_statements.append(has.statement(var, value))

        if len(insert_statements) > 0:
            insert_stage = "insert\n" + "\n".join(insert_statements)
            pipeline.append(insert_stage)

        for new_relation in self.property_mappings.relation_new_player_mappings:
            value = doc.get(new_relation.doc_key)
            if type(value) == list:
                for i, v in enumerate(value):
                    pipeline.extend(new_relation.insert_query(v, var, i))
            elif value is not None:
                pipeline.extend(new_relation.insert_query(value, var))
        
        for existing_relation in self.property_mappings.relation_existing_player_mappings:
            value = doc.get(existing_relation.player_attribute_doc_key)
            if type(value) == list:
                for i, v in enumerate(value):
                    pipeline.extend(existing_relation.insert_query(v, var, i))
            elif value is not None:
                pipeline.extend(existing_relation.insert_query(value, var))
        
        for links in self.property_mappings.links_mappings:
            value = doc.get(links.player_attribute_doc_key)
            if type(value) == list:
                for i, v in enumerate(value):
                    pipeline.extend(links.insert_query(v, var, self.type_, i))
            elif value is not None:
                pipeline.extend(links.insert_query(value, var, self.type_))
        
        return pipeline

    def var_with_prefix(self, prefix: str):
        if len(prefix) > 0:
            return prefix + "_" + self.var
        else:
            return self.var
