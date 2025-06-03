from typing import List, Optional, Dict, Any
from datetime import datetime

JSON = Dict[str, Any]

def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\'")

class PropertyLoaders:
    def __init__(self):
        self.has_key_loaders = []
        self.has_loaders = []
        self.relation_loaders = []
    
    def key(self, doc_key: str, statement: str, quoted: bool = False):
        self.has_key_loaders.append(DirectValueStatement(doc_key, "${var} " + statement, quoted))
        return self

    def has(self, doc_key: str, statement: str, quoted: bool = False):
        self.has_loaders.append(DirectValueStatement(doc_key, "${var} " + statement, quoted))
        return self

    def relation(self, doc_key: str, value_processor: "TypeDBDocumentLoader", statement: str):
        self.relation_loaders.append(ProcessedValueStages(doc_key, value_processor, statement))
        return self

    def include(self, property_loaders: "PropertyLoaders"):
        for loader in property_loaders.has_key_loaders:
            for existing_loader in self.has_key_loaders:
                if loader.doc_key == existing_loader.doc_key:
                    raise ValueError(f"Duplicate key property loader for {loader.doc_key}")
        self.has_key_loaders.extend(property_loaders.has_key_loaders)
        for loader in property_loaders.has_loaders: 
            for existing_loader in self.has_loaders:
                if loader.doc_key == existing_loader.doc_key:
                    raise ValueError(f"Duplicate has property loader for {loader.doc_key}")
        self.has_loaders.extend(property_loaders.has_loaders)
        for loader in property_loaders.relation_loaders:
            for existing_loader in self.relation_loaders:
                if loader.doc_key == existing_loader.doc_key:
                    raise ValueError(f"Duplicate relation property loader for {loader.doc_key}")
        self.relation_loaders.extend(property_loaders.relation_loaders)
        return self


"""
Load a JSON document, that represents a central concept, plus some attribute ownerships, some of which may be keys.
"""
class TypeDBDocumentLoader:
    def __init__(self, var: str, isa: str):
        self.var = var
        self.isa_loader = ConstantStatement("${var} " + isa)
        self.property_loaders = PropertyLoaders()
    

    def key(self, doc_key: str, statement: str, quoted: bool = False):
        self.property_loaders.key(doc_key, statement, quoted)
        return self

    def has(self, doc_key: str, statement: str, quoted: bool = False):
        self.property_loaders.has(doc_key, statement, quoted)
        return self

    def relation(self, doc_key: str, value_processor: "TypeDBDocumentLoader", statement: str):
        self.property_loaders.relation(doc_key, value_processor, statement)
        return self
    
    def include(self, property_loaders: "PropertyLoaders"):
        self.property_loaders.include(property_loaders)
        return self

    def apply(self, doc: JSON, var_prefix: str = "") -> List[str]:
        pipeline = []

        statements = self.isa_loader.apply(self.var_with_prefix(var_prefix))
        # TODO: keys might be inserted with 'put' instead of 'insert' clauses
        for has_key in self.property_loaders.has_key_loaders:
            statements.extend(has_key.apply(doc, self.var_with_prefix(var_prefix)))
        if len(statements) > 0:
            put_stage = "put\n" + ";\n".join(statements) + ";"
            pipeline.append(put_stage)

        statements = []
        for has in self.property_loaders.has_loaders:
            statements.extend(has.apply(doc, self.var_with_prefix(var_prefix)))
        if len(statements) > 0:
            insert_stage = "insert\n" + ";\n".join(statements) + ";"
            pipeline.append(insert_stage)

        for relation in self.property_loaders.relation_loaders:
            pipeline.extend(relation.apply(doc, self.var_with_prefix(var_prefix)))
        
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
    def __init__(self, doc_key: str, value_processor: TypeDBDocumentLoader, statement_format_string: str):
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

