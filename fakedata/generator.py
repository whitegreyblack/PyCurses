"""Fake data generator"""
__author__ = "Samuel Whang"

import yaml
import click
import random
import datetime
import calendar
import source.utils as utils
from source.logger import Loggable
from source.YamlObjects import Reciept
from source.database import Connection
from examples.calendar_widget import date, parse_date, iter_months_years
# This can either go two ways. Building data directly from sql queries with a
# join on the tables being used. Very similar to a view table. Or load all
# tables being used into python and have the dataprocessing done within a
# python program.

# monthsinyear = iter_months_years(date(2017, 3, 1), 
#                                  date(2018, 9, 1))
# filenames = [
#     str(y)[2:] + f"{m:02}" + '01' + 'internet.yaml'
#         for y, m in monthsinyear
# ]
# print(filenames)

# fake data stuff -- probably create a fake table to hold these
class RandomProductData:
    def __init__(self, table, product, price, deviation):
        self.table = table
        self.product = product
        self.price = int((price + random.uniform(-1, 1) * deviation) * 100) / 100

    def __repr__(self):
        return f"{self.table}-{self.product}: {self.price}"

# products[storecategory][product](price, deviation)
products = {
    'general': {
        'toothbrush': (2.99, 1.0),
        'toilet paper': (7.99, 1.0),
        'miscellanious': (8.97, 2.0),
    },
    'utility': {
        'electricity': (110.0, 30.0),
        'sewage': (37.0, 12.0),
        'internet': (78.0, 7.0),
        'gas': (112.0, 13)
    },
    'grocery': {
        'meat': (8.99, 4.0),
        'veggies': (1.50, 2.0),
        'pastry': (4.0, 1.0),
        'chips': (3.99, 1.25),
    },
    'resturant': {
        'dine-in': (9.99, 1.25),
        'take-out': (9.00, 0.84),
        'fast-food': (7.99, 1.25),
    }
}

def random_product_data(catalog):
    return [
        RandomProductData(category, product, price, deviation)
            for category, products in catalog.items()
                for product, (price, deviation) in products.items()
    ]

# TODO: single file option
internet_build_query = """SELECT * FROM reciepts WHERE short='BEK'"""

class DataGenerator:
    phone_number_regex = r"[1]?[\-\.\ ]??\d{3}?[\-\.\ ]?\d{3}[\-\.\ ]?\d{4}|(?>\(\d{3}\)|\d{3})[\-\.\ ]?\d{3}[\-\.\ ]\d{4}"
    phone_number_formats = (
            "###-###-####",
            "###.###.####",
            "(###)###-####",
            "(###) ###-####",
            "(###)###.####",
            "(###) ###.####"
    )
    def __init__(self, folder):
        self.folder = folder
        self.export_folder = utils.check_or_create_folder(folder)
        self.logger = Loggable(self)
        self.database = Connection(logger=self.logger.logger)

        print(f"PATH: {self.export_folder}")

    def generate_phonenumber(self):
        return 

    def generate_filenames(self, start, end, days, category):
        startDate = parse_date(start)
        endDate = parse_date(end)
        return {
            (y, m, d): f"{str(y)[2:]}{m:02}{d:02}-{cat}.yaml"
                for y, m in iter_months_years(startDate, endDate)
                    for cat in category
                        for d in days
        }

    def generate_internet_data(self):
        filenames = self.generate_filenames("2017-3-1", 
                                            "2018-3-1", 
                                            (1,), 
                                            ("utility",))

        for datetup, filename in filenames.items():
            reciept = Reciept('Internet', 
                              'Net', 
                              list(datetup),
                              'utility',
                              {'internet': 73.59},
                              73.59,
                              0.0,
                              73.59,
                              73.59)
            with open(self.export_folder + filename, 'w') as yamlfile:
                yamlfile.write(yaml.dump(reciept))

    def generate_grocery_data(self):
        filenames = self.generate_filenames("2017-3-1", 
                                            "2018-3-1", 
                                            (8, 22), 
                                            ("groceries",))

        for datetup, filename in filenames.items():
            reciept = Reciept('Grocery',
                              'Food',
                              list(datetup),
                              'groceries',
                              {'food': 24.99},
                              24.99,
                              0.0,
                              24.99,
                              24.99)
            with open(self.export_folder + filename, 'w') as yamlfile:
                yamlfile.write(yaml.dump(reciept))

    def generate_fast_food_data(self):
        pass

    def generate_general_store_data(self):
        pass

    # Let's try both ways
    # Option 1: Sql Join Query to generate data
    def generate_data(self):
        """
        Step 1:
        query should build two new tables => generated_reciepts, generate_products
        table values should be the same as old reciepts, products tables
        Step 2:
        select data from the old tables and insert them into the new tables
        should act more like a stored proc than a query
        """
        cursor = self.database.conn.execute(internet_build_query)
        for i in cursor:
            print(i)
    
    # Option 2: Generate data using python
    def import_data(self, query):
        self.database.conn.execute(query)

@click.command()
@click.option("-o", "folder", default="generated/", required=False,
              help="Folder to hold all generated files from script.")
def main(folder):
    dg = DataGenerator(folder)
    # dg.generate_internet_data()
    dg.generate_grocery_data()

if __name__ == "__main__":
    main()
