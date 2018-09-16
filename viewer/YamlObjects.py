"""
YamlObjects.py : holds all objects used during transporting data from yaml
                 to database
"""

__Author__ = "Sam Whang"

from datetime import date
from utils import format_float as frmt_flt
import yaml
import sys

class Reciept(yaml.YAMLObject):
    __doc__ = """Python Reciept using Yaml Object Parent for DB insertions"""
    yaml_tag = u'!Reciept'

    def __init__(self, *args):
        self.store = args[0]
        self.date = args[1]
        self.category = args[2]
        self.products = args[3]
        self.subtotal = args[4]
        self.tax = args[5]
        self.total = args[6]
