from typing import List, Dict, Any

JSON = Dict[str, Any]

def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")

def isa_statement(var: str, type_: str) -> str:
    return f"${var} isa {type_};"

def var_with_prefix(var: str, prefix: str) -> str:
    if len(prefix) > 0:
        return prefix + "_" + var
    else:
        return var


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
    def __init__(self, doc_key: str, attribute: str, quoted: bool = False, single: bool = False):
        self.doc_key = doc_key
        self.attribute = attribute
        self.quoted = quoted
        self.single = single

    def statement(self, var: str, value: any) -> str:
        if self.quoted:
            value = f"'{escape(value)}'"
        if type(value) == bool:
            value = "true" if value else "false"
        return f"${var} has {self.attribute} {value};"

    def fetch(self, owner_var: str) -> str:
        if self.single:
            return f'  "{self.doc_key}": ${owner_var}.{self.attribute},\n'
        else:
            return f'  "{self.doc_key}": [ ${owner_var}.{self.attribute} ],\n'


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

    def fetch(self, self_var: str, var_prefix: str) -> str:
        other_var = var_with_prefix("var", var_prefix)
        return f'  "{self.doc_key}": [ ' + \
                f'match ({self.self_role}: ${self_var}, {self.other_player_role}: ${other_var}) isa {self.relation_type}; fetch ' + \
                self.other_player_processor.fetch(other_var, var_prefix) + \
                '; ],\n'


class RelationExistingPlayerMapping:
    def __init__(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False, single: bool = False):
        self.player_attribute_doc_key = player_attribute_doc_key
        self.player_attribute = player_attribute
        self.relation_type = relation_type
        self.self_role = self_role
        self.player_role = player_role
        self.quoted = quoted
        self.single = single

    def insert_query(self, player_attribute_value: any, first_player_var: str, index: int = 0) -> List[str]:
        pipeline = [f"\n### Load player from property '{self.player_attribute_doc_key}' and link via relation '{self.relation_type}' with role '{self.self_role}'"]
        player_var = f"player_{self.player_attribute_doc_key}_{index}"
        player_type = player_attribute_value.split('--')[0]
        if self.quoted:
            player_attribute_value = f"'{escape(player_attribute_value)}'"
        if type(player_attribute_value) == bool:
            player_attribute_value = "true" if player_attribute_value else "false"
        pipeline.append(f"""put ${player_var} isa {player_type}, has {self.player_attribute} {player_attribute_value};""")
        pipeline.append(f"insert {self.relation_type} ({self.self_role}: ${first_player_var}, {self.player_role}: ${player_var});")
        return pipeline

    def fetch(self, self_var: str, var_prefix: str) -> str:
        other_var = var_with_prefix("var", var_prefix)
        other_attr = var_with_prefix("attr", var_prefix)
        query = f'  "{self.player_attribute_doc_key}": '
        if not self.single:
            query += '[ '
        query += f'match ({self.self_role}: ${self_var}, {self.player_role}: ${other_var}) isa {self.relation_type}; '
        query += f'${other_var} has {self.player_attribute} ${other_attr}; '
        if self.single:
            query += f'return first ${other_attr};,\n'
        else:
            query += f'return {{ ${other_attr} }}; ],\n'
        return query


class LinksMapping:
    def __init__(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False, single: bool = False):
        self.player_attribute_doc_key = player_attribute_doc_key
        self.player_attribute = player_attribute
        self.role = role
        self.quoted = quoted
        self.single = single

    def insert_query(self, player_attribute_value: any, relation_var: str, relation_type: str, index: int = 0) -> List[str]:
        pipeline = [f"\n### Relation '{relation_type}' links player using property {self.player_attribute_doc_key} with role {self.role}"]
        player_var = f"player_{self.player_attribute_doc_key}_{index}"
        player_type = player_attribute_value.split('--')[0]
        if self.quoted:
            player_attribute_value = f"'{escape(player_attribute_value)}'"
        if type(player_attribute_value) == bool:
            player_attribute_value = "true" if player_attribute_value else "false"
        pipeline.append(f"""put ${player_var} isa {player_type}, has {self.player_attribute} {player_attribute_value};""")
        pipeline.append(f"insert ${relation_var} links ({self.role}: ${player_var});")
        return pipeline

    def fetch(self, self_var: str, var_prefix: str) -> str:
        player_var = var_with_prefix("var", var_prefix)
        player_attr = var_with_prefix("attr", var_prefix)
        query = f'  "{self.player_attribute_doc_key}": ';
        if not self.single:
            query += '[ '
        query += f'match ${self_var} self ({self.role}: ${player_var}); ${player_var} has {self.player_attribute} ${player_attr}; '
        if self.single:
            query += f'return first ${player_attr};,\n'
        else:
            query += f'return {{ ${player_attr} }}; ],\n'
        return query


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

    def has(self, doc_key: str, attribute: str, quoted: bool = False, single: bool = False):
        self.has_mappings.append(HasMapping(doc_key, attribute, quoted, single))
        return self

    def relation_and_new_player(self, doc_key: str, other_player_mapping: "TypeDBDocumentMapping", relation_type: str, self_role: str, other_player_role: str):
        self.relation_new_player_mappings.append(RelationNewPlayerMapping(doc_key, other_player_mapping, relation_type, self_role, other_player_role))
        return self

    def relation_existing_player(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False, single: bool = False):
        self.relation_existing_player_mappings.append(RelationExistingPlayerMapping(player_attribute_doc_key, player_attribute, relation_type, self_role, player_role, quoted, single))
        return self

    def links(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False, single: bool = False):
        self.links_mappings.append(LinksMapping(player_attribute_doc_key, player_attribute, role, quoted, single))
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
        self.stubs = []

    def var_with_prefix(self, prefix: str) -> str:
        return var_with_prefix(self.var, prefix)

    def key(self, doc_key: str, attribute: str, quoted: bool = False):
        self.property_mappings.key(doc_key, attribute, quoted)
        return self

    def has(self, doc_key: str, attribute: str, quoted: bool = False, single: bool = False):
        self.property_mappings.has(doc_key, attribute, quoted, single)
        return self

    def relation_and_new_player(self, doc_key: str, other_player_mapping: "TypeDBDocumentMapping", relation_type: str, self_role: str, other_player_role: str):
        self.property_mappings.relation_and_new_player(doc_key, other_player_mapping, relation_type, self_role, other_player_role)
        return self

    def relation_existing_player(self, player_attribute_doc_key: str, player_attribute: str, relation_type: str, self_role: str, player_role: str, quoted: bool = False, single: bool = False):
        self.property_mappings.relation_existing_player(player_attribute_doc_key, player_attribute, relation_type, self_role, player_role, quoted, single)
        return self

    def links(self, player_attribute_doc_key: str, player_attribute: str, role: str, quoted: bool = False, single: bool = False):
        self.property_mappings.links(player_attribute_doc_key, player_attribute, role, quoted, single)
        return self

    def stub(self, doc_key: str):
        self.stubs.append(doc_key)
        return self

    def include(self, property_mappings: "PropertyMappings"):
        self.property_mappings.include(property_mappings)
        return self

    def insert_query(self, doc: JSON, var_prefix: str = "") -> List[str]:
        pipeline = [f"\n### Put object of type '{self.type_}'"]
        var = self.var_with_prefix(var_prefix)

        write_statements = [isa_statement(var, self.type_)]

        # # TODO: keys might be inserted with 'put' instead of 'insert' clauses
        for has_key in self.property_mappings.has_key_mappings:
            value = doc.get(has_key.doc_key)
            if type(value) == list:
                for v in value:
                    write_statements.append(has_key.statement(var, v))
            elif value is not None:
                write_statements.append(has_key.statement(var, value))
        
        if len(self.property_mappings.has_key_mappings) == 0:
            # keyless, always insert
            pipeline.append("insert\n" + "\n".join(write_statements))
        else:
            # has a key, put
            pipeline.append("put\n" + "\n".join(write_statements))

        insert_statements = []
        for has in self.property_mappings.has_mappings:
            value = doc.get(has.doc_key)
            if type(value) == list:
                for i, v in enumerate(value):
                    insert_statements.append(has.statement(var, v))
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

    def match(self, var: str, key: str) -> str:
        return f'match ${var} isa {self.type_}, has id "{key}";\n'

    def fetch(self, var: str, var_prefix: str = "") -> str:
        query = '{\n'

        # # TODO: keys might be inserted with 'put' instead of 'insert' clauses
        for has_key in self.property_mappings.has_key_mappings:
            query += f'  "{has_key.doc_key}": ${var}.{has_key.attribute},\n'
        
        for has in self.property_mappings.has_mappings:
            query += has.fetch(var)

        for i, rel in enumerate(self.property_mappings.relation_new_player_mappings):
            query += rel.fetch(var, f"full_{i}_{var_prefix}")

        for i, rel in enumerate(self.property_mappings.relation_existing_player_mappings):
            query += rel.fetch(var, f"ref_{i}_{var_prefix}")

        for i, links in enumerate(self.property_mappings.links_mappings):
            query += f'  "{links.player_attribute_doc_key}": ';
            if not links.single:
                query += '[ '
            query += f'match ${var} links ({links.role}: $player); $player has {links.player_attribute} $player_attr; '
            if links.single:
                query += 'return first $player_attr;,\n'
            else:
                query += 'return { $player_attr }; ],\n'

        return query + '}'

