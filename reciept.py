# -----------------------------------------------------------------------------
# Author  : Sam Whang | whitegreyblack
# FileName: Reciept
# FileInfo: Python Object used in parsing YAML files during runtime
# -----------------------------------------------------------------------------
import datetime as dt
import yaml
import sys


class Reciept(yaml.YAMLObject):
    __doc__ = """Python Reciept using Yaml Object Parent for DB insertions"""
    yaml_tag = u'!Reciept'

    def __init__(self, *args):
        self.store = args[0]
        self.date = dt.date(args[1][0], args[1][1], args[1][2]).isoformat()
        self.type = args[2]
        self.prod = args[3]
        self.sub = args[4]
        self.tax = args[5]
        self.tot = args[6]
        print(self.store, type(self.store))
        print(self.date, type(self.date))
        self.code = self.store.replace(".", "") + self.date

    def frmt(self, n):
        return "{:.2f}".format(n)

    def __repr__(self):
        return "{}({}: {})".format(self.__class__.__name__,
                                   self.store, self.frmt(self.tot))

    def head(self):
        return self.store, self.date, self.type, self.code, \
            self.frmt(self.sub), self.frmt(self.tax), self.frmt(self.tot)

    def body(self):
        return self.code, self.products
