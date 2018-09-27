"""Fake data generator"""
__author__ = "Samuel Whang"

import click
import datetime
import source.utils as utils
from source.logger import Loggable
from source.database import Connection
# This can either go two ways. Building data directly from sql queries with a
# join on the tables being used. Very similar to a view table. Or load all
# tables being used into python and have the dataprocessing done within a
# python program.

# Let's try both ways
internet_build_query = """SELECT * FROM reciepts WHERE short='BEK'"""

class DataGenerator:
    def __init__(self, folder):
        self.folder = folder
        self.export_folder = utils.check_or_create_folder(folder)
        self.logger = Loggable(self)
        self.database = Connection(logger=self.logger.logger)

        # print(f"PATH: {self.formatted_export_folder}")

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
    dg.generate_data()

if __name__ == "__main__":
    main()