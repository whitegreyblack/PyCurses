"""
database.py: Connection object to access sqlite3 database
"""

__author__ = "Samuel Whang"

import sqlite3
import logging
import datetime
from collections import namedtuple
# from strings import stmts
from source.logger import Loggable
from source.utils import logargs
from source.utils import setup_logger
from source.YamlObjects import Reciept
from source.utils import format_date as date
from source.utils import format_float as real
from source.utils import filename_and_extension as fileonly

spacer = "  "

def unpack(cursor):
    """Returns data in a database cursor object as list"""
    return [data for data in cursor]

class Connection(Loggable):
    """Database Connection Object"""
    rebuild = False

    def __init__(self, tables, logger=None, rebuild=False):
        # leave the logging initialization to the loggable class
        super().__init__(self, logger=logger)

        self.conn = sqlite3.connect('reciepts.db')
        self.tables = tables
        self.rebuild = rebuild
        self.committed = []
        self.log("created database connection.")

    def __exit__(self):
        self.log("closing database connection.")
        self.conn.close()
        self.log("closed database connection.")

    def table(self, name):
        for table in self.tables:
            if table.name == name:
                return table
        self.log(f"{name} table not found in database tables list",
                 level=logging.WARNING)

    def send(self, message):
        results = self.conn.execute(message.request)
        if message.requires_commit:
            self.commit() 
        return results

    def rebuild_tables(self):
        if self.rebuild:
            self.drop_tables()
            self.build_tables()

    def drop_tables(self):
        # delete tables in sqlite
        self.log("dropping tables in database.")
        tablenames = []
        for table in self.tables:
            self.conn.execute(table.drop_command)
            self.log(f"{spacer}x Dropped {table.name}")
            tablenames.append(table.name)
        self.conn.commit()
        self.log("dropped tables {', '.join(tablenames)} in database.")

    def build_tables(self, tables=None):
        # create tables in sqlite
        self.log("building tables in database.")
        tablenames = []
        for table in self.tables:
            self.conn.execute(table.create_command)
            self.log(f"{spacer}+ Created {table.name}")
            tablenames.append(table.name)
        self.conn.commit()
        self.log("created tables {', '.join(tablenames)} in database.")

    def inserted_files(self, fields=None):
        self.log("retrieving inserted files from database")
        cursor = self.conn.execute("SELECT FILENAME FROM reciepts;")
        for data in unpack(cursor):
            yield data

    def insert_files(self, yaml_objs: dict):
        if not yaml_objs:
            self.log("no yaml reciepts to insert. returning early")
            return

        self.log("inserting reciepts data into database.")
        inserted_files = self.inserted_files()
        
        reciept_table = self.table("reciepts")
        product_table = self.table("products")

        # iterate through the files verified by yamlchecker
        for file_name, yaml_obj in yaml_objs.items():
            if file_name not in inserted_files:
                self.log(f"inserting {file_name}")

                file_only, _ = fileonly(file_name)
                self.conn.execute(reciept_table.insert_command, 
                                  (
                                    file_only,
                                    yaml_obj.store,
                                    yaml_obj.short,
                                    date(yaml_obj.date),
                                    yaml_obj.category,
                                    real(yaml_obj.subtotal),
                                    real(yaml_obj.tax),
                                    real(yaml_obj.total),
                                    real(yaml_obj.payment)
                                  )
                )
                                    
                self.log(f"{spacer}+ 'filename': '{file_only}'")
                self.log(f"{spacer}+ 'storename': '{yaml_obj.store}'")
                self.log(f"{spacer}+ 'category': '{yaml_obj.category}'")
                self.log(f"{spacer}inserted into reciept table")

                for product, price in yaml_obj.products.items():
                    self.log(f"{spacer}+ '{product}': '{price:.2f}'")
                    self.conn.execute(product_table.insert_command, 
                                      (
                                        file_only,
                                        product, 
                                        real(price)
                                      )
                    )
                self.log(f"{spacer}inserted into products table")
            else:
                self.log(f"data from {file_name} already inserted")

        self.conn.commit()
        self.committed = list(yaml_objs.keys())
        self.log("completed inserting reciepts data.")

    def select_reciepts(self):
        fields = "filename store short date category subtotal tax total payment"
        reciepttuple = namedtuple('Reciept', fields)
        cursor = self.conn.execute("SELECT * FROM reciepts;")
        for recieptobj in list(cursor):
            yield reciepttuple(*recieptobj)

    def select_from_table(self, table, fields, condition=None):
        if condition:
            select_from_table_with_condition(table, fields, condition)
        return self.conn.execute(f"SELECT {fields} from {table}")

    def select_from_table_with_condition(self, table, fields, condition):
        return self.conn.execute(f"SELECT {fields} FROM {table} {condition}");

    def select_reciept_products(self, reciept):
        productinfo = namedtuple("ProductInfo", "product price")
        fields = "product, price"
        table = "products"
        condition = f"WHERE filename = '{reciept}'"
        cmd = f"SELECT {fields} FROM {table} {condition};"
        cursor = self.conn.execute(cmd)
        for product in unpack(cursor):
            yield productinfo(*product)

if __name__ == "__main__":
    logger = setup_logger('dblog', 'db.log', extra={'currentfile': __file__})
    db = Connection(logger=logger)
