import sys
import yaml
import datetime as dt


# -----------------------------------------------------------------------------
# Yaml Object Extraction
# -----------------------------------------------------------------------------
"""
class YamlReciept(yaml.YAMLObject):
    yaml_tag=u'!Reciept'
    def __init__(self, *args):
        self.store = args[0]
        self.date = args[1]
        self.type = args[2]
        self.prod = args[3]
        self.sub = args[4]
        self.tax = args[5]
        self.tot = args[6]

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,
                                        self.store, self.date, self.tot)

    def build(self):
        date = dt.date(self.date[0], self.date[1], self.date[2]).isoformat()
        code = self.store.replace(" ","") + date
        head = (self.store, date, self.type, code, self.sub, self.tax, self.tot)
        body = (code, self.prod)
        return head, body  
"""
# -----------------------------------------------------------------------------
# Python Object For DB Insertion
# -----------------------------------------------------------------------------
def frmt(n):
    return "{:.2f}".format(n)
# -----------------------------------------------------------------------------
# Reciept Object
# -----------------------------------------------------------------------------
class Reciept:
    def __init__(self, *args):
        self.store = args[0]
        self.date = date(args[1][0], args[1][1], args[1][0])
        self.type = args[2]
        self.prod = args[3]
        self.sub = args[4]
        self.tax = args[5]
        self.tot = args[6]
        self.code = self.store.replace(".","") + self.date
        
    def __repr__(self):
        return "{}({}: {:.2f})".format(self.__class__.__name__,
                                        self.store, self.tot)

    def head(self):
        return self.store, self.date, self.type, self.code, \
            frmt(self.sub), frmt(self.tax), frmt(self.tot)

    def body(self):
        return self.code, self.products

# Header Object for Reciept
# Holds everything apart from product list
"""
class RecieptHeader:
    def __init__(self, *args):
        self.store = args[0]
        self.date = args[1]
        self.type = args[2]
        self.code = args[3]
        self.sub = args[4]
        self.tax = args[5]
        self.tot = args[6]
        
    def __repr__(self):
        return "{}({}: {:.2f})".format(self.__class__.__name__,
                                        self.store, self.tot)
    def build(self):
        date = dt.date(self.date[0], self.date[1], self.date[2]).isoformat()
        code = self.store.replace(" ","") + date
        head = (self.store, date, self.type, code, self.sub, self.tax, self.tot)
        body = (code, self.prod)
        return head, body

    def push(self):
        return self.store, self.date, self.type, self.code, \
            frmt(self.sub), frmt(self.tax), frmt(self.tot)

# Body Object for Reciept
# Holds the items listed in reciept objects
class RecieptBody:
    def __init__(self, *args):
        self.code = args[0]
        self.products = args[1]

    def __repr__(self):
        return "{}(items:{})".format(self.__class__.__name__,
                len(self.products))

    def push(self):
        return self.code, self.products
"""
