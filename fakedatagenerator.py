"""Fake data generator"""
__author__ = "Samuel Whang"

import yaml
import click
import datetime
import calendar
import source.utils as utils
from source.logger import Loggable
from source.YamlObjects import Reciept
from source.database import Connection
from examples.calendar_widget import date, iter_months_years
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

internet_build_query = """SELECT * FROM reciepts WHERE short='BEK'"""

class DataGenerator:
    def __init__(self, folder):
        self.folder = folder
        self.export_folder = utils.check_or_create_folder(folder)
        self.logger = Loggable(self)
        self.database = Connection(logger=self.logger.logger)

        print(f"PATH: {self.export_folder}")

    def generate_internet_data(self):
        filenames = {
            (y, m, 1): str(y)[2:] + f"{m:02}" + '01' + '-internet.yaml'
                for y, m in iter_months_years(date(2017, 3, 1), 
                                              date(2018, 9, 1))
        }
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
        filenames = {
            (y, m, d): str(y)[2:] + f"{m:02}" + f"{d:02}" + '-grocery.yaml'
                for y, m in iter_months_years(date(2017, 3, 1),
                                              date(2018, 9, 1))
                    for d in (15, 30)
        }
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