import yaml
import pytest
from cerberus import Validator
from source.YamlObjects import Receipt

def test_simple_schema():
    v = Validator()
    document = {'data': [1,2,3]}
    schema_text = """
data: 
  type: list
  items: [
    type: integer,
    type: integer,
    type: integer
  ]
"""[1:]

    schema = yaml.load(schema_text)
    assert v.validate(document, schema) == True

def test_multi_schema():
    v = Validator()
    document = {'store': 'a', 'short': 'a', 'date': [1,2,3]}
    schema_text = """
store:
  type: string
short:
  type: string
date: 
  type: list
  items: [
    type: integer,
    type: integer,
    type: integer
  ]
"""[1:]
    schema = yaml.load(schema_text)
    assert v.validate(document, schema) == True

def test_validation_from_files():
    v = Validator()
    with open("./data/schema.yaml", 'r') as f:
        schema = yaml.load(f.read())
    with open("./data/store.yaml", 'r') as f:
        document = yaml.load(f.read()).serialized()
    assert v.validate(document, schema) == True