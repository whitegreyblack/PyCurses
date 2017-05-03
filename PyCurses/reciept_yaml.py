import yaml
import datetime as dt

# Yaml Object Extraction
class Reciept(yaml.YAMLObject):
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
        return "{}({}, {}, {})".format(self.__class__.__name__, self.store, self.date, self.tot)

    def build(self):
        date = dt.date(self.date[0], self.date[1], self.date[2]).isoformat()
        code = self.store.replace(" ","") + date
        head = (self.store, date, self.type, code, self.sub, self.tax, self.tot)
        body = (code, self.prod)
        return head, body
