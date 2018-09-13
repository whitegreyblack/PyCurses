"""
database.py: Connection object to access sqlite3 database
"""

__author__ = "Samuel Whang"

import sqlite3
import logging
# from strings import stmts
import statements
import datetime
from utils import setup_logger
from utils import filename_and_extension as fileonly
from utils import format_float as real
from utils import format_date as date
class Connection:
    '''
    Database object
    '''
    def __init__(self, logger=None):
        # create connection to db
        self.logargs = {'classname': self.__class__.__name__}

        self.logger = logger
        if not self.logger:
            self.logger = setup_logger('dblog', 'db.log')

        self.log("creating database connection.")  

        self.conn = sqlite3.connect('reciepts.db')

        self.log("created database connection.")

    def __exit__(self):
        self.log("closing database connection.")

        self.conn.close()

        self.log("closed database connection.")

    def log(self, message):
        self.logger.info(message, extra=self.logargs)

    def drop_tables(self):
        # delete tables in sqlite
        self.log("dropping tables in database.")

        self.conn.execute(statements.drop_table('reciepts'))
        self.conn.execute(statements.drop_table('products'))
        self.conn.commit()

        self.log("dropped tables in database.")

    def build_tables(self):
        # create tables in sqlite
        self.log("building tables in database.")

        self.conn.execute(statements.create_reciepts_table())
        self.conn.execute(statements.create_products_table())
        self.conn.commit()

        self.log("built tables in database.")

    def inserted_files(self, fields=None):
        return self.conn.execute("SELECT FILENAME FROM reciepts")

    def insert_files(self, yaml_objs: dict):
        if not yaml_objs:
            self.log("no yaml reciepts to insert. returning early")
            return

        self.log("inserting reciepts data into database.")
        
        inserted_files = self.inserted_files()
        insert_command = statements.insert_command('reciepts', 8) 
        product_command = statements.insert_command('products', 3)
        for file_name, yaml_obj in yaml_objs.items():
            if file_name not in inserted_files:
                self.log(f"inserting data from {file_name}")

                file_only, _ = fileonly(file_name)
                self.conn.execute(insert_command, (file_only,
                                                   yaml_obj.store,
                                                   date(yaml_obj.date),
                                                   yaml_obj.category,
                                                   real(yaml_obj.subtotal),
                                                   real(yaml_obj.tax),
                                                   real(yaml_obj.total),
                                                   real(yaml_obj.payment)))

                self.log(f"inserted data from {file_name} into reciepts table")
                    
                for product, price in yaml_obj.products.items():
                    self.log(f"inserting '{product}': '{real(price)}'")
                    self.conn.execute(product_command, (file_only,
                                                        product, 
                                                        real(price)))

                self.log(f"inserted data from {file_name} into products table")
            else:
                self.log(f"data from {file_name} already inserted")

        self.conn.commit()
        self.log("completed inserting reciepts data.")
    
    def select_reciepts(self):
        return self.conn.execute("SELECT * FROM reciepts;")

    def select_reciept_products(self, reciept):
        cmd = f"SELECT product, price FROM products WHERE filename = '{reciept}'"
        return self.conn.execute(cmd)

if __name__ == "__main__":
    logger = setup_logger('dblog', 'db.log')
    db = Connection(logger=logger)
