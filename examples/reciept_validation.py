import yaml
from cerberus import Validator
from source.YamlObjects import receipt

v = Validator()
schema_text = """
date: 
  type: list
  items: [
    type: integer,
    type: integer,
    type: integer
  ]
"""

schema = yaml.load(schema_text)
print(schema)
document = {'date': [1,2,3]}
print(v.validate(document, schema))

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
"""
schema = yaml.load(schema_text)
print(schema)
document = {'store': 'a', 'short': 'a', 'date': [1,2,3]}
print(v.validate(document, schema))

with open('./data/schema.yaml', 'r') as f:
    schema = yaml.load(f.read())
with open('./data/store.yaml', 'r') as f:
    document = yaml.load(f.read()).serialized()
print(document)
print(v.validate(document, schema))