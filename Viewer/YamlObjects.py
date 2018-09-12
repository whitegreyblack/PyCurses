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

    '''
    def hash(self):
        self.date = date(self.date[0], self.date[1], self.date[2]).isoformat()
        self.code = self.store.replace(".", "")
        self.code += self.date

    def __repr__(self):
        return f"{self.__class__.__name__}({self.store}: {frmt_flt(self.tot)})"

    def build(self):
        return self.head(), self.body()

    def head(self):
        return(self.store,
               self.date,
               self.type,
               self.code,
               frmt_flt(self.sub),
               frmt_flt(self.tax),
               frmt_flt(self.tot))

    def body(self):
        return self.code, self.prod
    '''
