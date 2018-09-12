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
    def __init__(self):
        # create connection to db
        self.logargs = {'classname': self.__class__.__name__}
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

    def insert_reciepts(self, yaml_objs: dict):
        self.log("inserting reciepts data into database.")

        insert_command = statements.insert_reciepts_command('reciepts', 8) 
        for file_name, yaml_obj in yaml_objs.items():
            file_only, _ = fileonly(file_name)
            self.conn.execute(insert_command, (file_only,
                                               yaml_obj.store,
                                               date(yaml_obj.date),
                                               yaml_obj.category,
                                               real(yaml_obj.subtotal),
                                               real(yaml_obj.tax),
                                               real(yaml_obj.total),
                                               real(yaml_obj.payment)))
        self.log("completed inserting reciepts data.")
            # now do the products
        '''
        code, products = body
        self.conn.execute(stmts['headinsert'], head)
        [self.conn.execute(stmts['bodyinsert'], (k, "{0:.2f}".format(
            products[k]), code)) for k in products.keys()]
        self.conn.commit()
        self.logger.info(f"{self.__class__.__name__}: insert row")
        '''

    def insert_products(self, products):
        # insert product row into products table
        pass
'''
    def stats(self):
        # returns information used in statistics printing
        fc = self.conn.execute(stmts['filecount'])
        tot = self.conn.execute(stmts['total'])
        return fc, tot

    def load(self):
        # return all reciepts
        return self.conn.execute(stmts['algrocery'])

    def load_bodies(self, codes):
        # return list of recieptbodies matching codes
        return [self.load_body(c) for c in codes]

    def load_body(self, code):
        # return recieptbody matching code
        pass

    def loadByGroup(self, group, value):
        # return reciepts matching group name
        return self.conn.execute(stmts['hdgrocery'].format(group, value))

    def getMinDate(self):
        # return latest date in database
        return (self.conn.execute(stmts['mindate'])).replace("-", ",")

    def getMaxDate(self):
        # return earliest date in database
        return (self.conn.execute(stmts['maxdate'])).replace("-", ",")
'''

if __name__ == "__main__":
    db = Connection()
