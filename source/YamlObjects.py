"""YamlObjects.py

holds all objects used during transporting data from yaml to database
"""

__Author__ = "Sam Whang"

import datetime
import yaml

def validate_reciept_store(filename, storename):
    store_from_filename = filename.split('.')[0].split('-')[1]
    store = storename.replace(" ", "").lower()
    return store_from_filename == store

def validate_reciept_date(filename, date):
    try: 
        filedate = datetime.date(*date)
    except:
        return False
    return filedate < datetime.date.today()

class Reciept(yaml.YAMLObject):
    __doc__ = """Yaml Object Class used to describe a reciept"""
    yaml_tag = u'!Reciept'
    properties = {
        'store': (str, validate_reciept_store),
        'date': (list, validate_reciept_date),
        'category': (str, None),
        'products': (dict, None),
        'subtotal': ((int, float), None),
        'tax': ((int, float), None),
        'total': ((int, float), None)
        }

    def __init__(self, *args, **kwargs):
        self.store = args[0]
        self.date = args[1]
        self.category = args[2]
        self.products = args[3]
        self.subtotal = args[4]
        self.tax = args[5]
        self.total = args[6]
