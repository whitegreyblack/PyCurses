"""YamlObjects.py
holds all objects used during transporting data from yaml to database
"""

import datetime

import yaml

import source.config as config


def validate_receipt_store(filename, storename):
    store_from_filename = filename.split('.')[0].split('-')[1]
    store = storename.replace(" ", "").lower()
    return store_from_filename == store

def validate_receipt_date(filename, date):
    try: 
        filedate = datetime.date(*date)
    except:
        return False
    return filedate < datetime.date.today()

def format_receipt_date(filename, date):
    try:
        filedate = datetime.date(*date)
    except:
        return date
    return filedate.strftime(config.DATE_FORMAT['L'])


class Receipt(yaml.YAMLObject):
    __doc__ = """Yaml Object Class used to describe a receipt"""
    yaml_tag = u'!Receipt'
    properties = {
        # [key]: (object type(s), validation_handler, format_handler)
        'store': (str, validate_receipt_store, None),
        'short': (str, None, None),
        'date': (list, validate_receipt_date, None),
        'category': (str, None, None),
        'products': (dict, None, None),
        'subtotal': ((int, float), None, None),
        'tax': ((int, float), None, None),
        'total': ((int, float), None, None),
        'payment': ((int, float), None, None)
        }

    def __init__(self, *args, **kwargs):
        self.store = args[0]
        self.short = args[1]
        self.date = args[2]
        self.category = args[3]
        self.products = args[4]
        self.subtotal = args[5]
        self.tax = args[6]
        self.total = args[7]
        self.payment = args[8]
    
    def serialized(self):
        return {
            k: getattr(self, k)
                for k in self.properties.keys()
        }
