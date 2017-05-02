import datetime
import yaml
from dbreciept import RecieptHeader, RecieptBody

# Yaml Object Extraction
class YamlReciept(yaml.YAMLObject):
    yaml_tag=u'!Reciept'
    def __init__(self, store, date, type, products, subtotal, tax, total):
        self.store = store
        self.date = date
        self.type = type
        self.products = products
        self.subtotal = subtotal
        self.tax = tax
        self.total = total
    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.store, self.date, self.total)
    def build(self):
        date = datetime.date(self.date[0], self.date[1], self.date[2])
        code= self.store + date.isoformat()
        return RecieptHeader(self.store, date, self.type, code, self.subtotal, self.tax, self.total), RecieptBody(code, self.products)