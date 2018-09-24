"""
database.py: Connection object to access sqlite3 database
"""

__author__ = "Samuel Whang"

import sqlite3
import logging
import datetime
from collections import namedtuple
# from strings import stmts
import source.statements as statements
from source.utils import setup_logger
from source.utils import filename_and_extension as fileonly
from source.utils import format_float as real
from source.utils import format_date as date

spacer = "  "

def unpack(cursor):
    """Returns data in a database cursor object as list"""
    return [data for data in cursor]

class Connection:
    '''
    Database object
    '''
    logger_name = 'database'
    logger_file = 'database.log'
    logger_args = {'currentfile':__file__}
    
    rebuild = False

    def __init__(self, logger=None, rebuild=False):
        """Create connection to db"""
        
        self.logger = logger
        if not self.logger:
            self.logger = setup_logger(Connection.logger_name,
                                       Connection.logger_file, 
                                       extra=Connection.logger_args)

        self.conn = sqlite3.connect('reciepts.db')
        self.rebuild = rebuild
        self.log("created database connection.")

    def __exit__(self):
        self.log("closing database connection.")
        self.conn.close()
        self.log("closed database connection.")

    def log(self, message):
        self.logger.info(f"{self.__class__.__name__}: {message}")

    def send(self, message):
        results = self.conn.execute(message.request)
        if message.requires_commit:
            self.commit() 
        return results

    def rebuild_tables(self):
        if self.rebuild:
            self.drop_tables()
            self.build_tables()

    def drop_tables(self, tables=None):
        # delete tables in sqlite
        if not tables:
            tables = ['reciepts', 'products']
        self.log("dropping tables in database.")
        for table in tables:
            self.conn.execute(statements.drop_table(table))
            self.log(f"{spacer}x Dropped {table}")
        self.conn.commit()
        self.log("dropped tables in database.")

    def build_tables(self, tables=None):
        # create tables in sqlite
        if not tables:
            tables = [
                statements.create_reciepts_table(),
                statements.create_products_table(),
                ]
        self.log("building tables in database.")
        for tablequery in tables:
            self.conn.execute(tablequery)
        self.conn.commit()
        self.log("built tables in database.")

    def inserted_files(self, fields=None):
        self.log("retrieving inserted files from database")
        cursor = self.conn.execute("SELECT FILENAME FROM reciepts")
        for data in unpack(cursor):
            yield data

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
                self.log(f"inserting {file_name}:")

                file_only, _ = fileonly(file_name)
                self.conn.execute(insert_command, (file_only,
                                                   yaml_obj.store,
                                                   date(yaml_obj.date),
                                                   yaml_obj.category,
                                                   real(yaml_obj.subtotal),
                                                   real(yaml_obj.tax),
                                                   real(yaml_obj.total),
                                                   real(yaml_obj.payment)))
                self.log(f"{spacer}+ 'filename': '{file_only}'")
                self.log(f"{spacer}+ 'storename': '{yaml_obj.store}'")
                self.log(f"{spacer}+ 'category': '{yaml_obj.category}'")
                self.log(f"{spacer}inserted into reciept table")

                for product, price in yaml_obj.products.items():
                    self.log(f"{spacer}+ '{product}': '{price:.2f}'")
                    self.conn.execute(product_command, (file_only,
                                                        product, 
                                                        real(price)))

                self.log(f"{spacer}inserted into products table")
            else:
                self.log(f"data from {file_name} already inserted")

        self.conn.commit()
        self.committed = list(yaml_objs.keys())
        self.log("completed inserting reciepts data.")

    def select_reciepts(self):
        fields = "filename store date category subtotal tax total payment"
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
            self.log(product)
            yield productinfo(*product)

if __name__ == "__main__":
    logger = setup_logger('dblog', 'db.log', extra={'currentfile': __file__})
    db = Connection(logger=logger)
