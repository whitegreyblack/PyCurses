"""Fake data generator"""
__author__ = "Samuel Whang"

from source.logger import Loggable
from source.database import Connection
# This can either go two ways. Building data directly from sql queries with a
# join on the tables being used. Very similar to a view table. Or load all
# tables being used into python and have the dataprocessing done within a
# python program.

# Let's try both ways
class DataGenerator:
    def __init__(self):
        self.logger = Loggable(self)
        self.database = Connection(logger=self.logger.logger)
    
    # Option 1: Sql Join Query to generate data
    def generate_data(self, query):
        """
        Step 1:
        query should build two new tables => generated_reciepts, generate_products
        table values should be the same as old reciepts, products tables
        Step 2:
        select data from the old tables and insert them into the new tables
        should act more like a stored proc than a query
        """
        self.database.conn.execute(query)
    
    # Option 2: Generate data using python
    def import_data(self, query):
        self.database.conn.execute(query)

if __name__ == "__main__":
    dg = DataGenerator()