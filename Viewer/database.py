"""
database.py: Connection object to access sqlite3 database
"""

__author__ = "Samuel Whang"

import sqlite3
import logging
# from strings import stmts
import statements

class Connection:
    '''
    Database object
    '''
    def __init__(self):
        # create connection to db
        logging.basicConfig(filename="dbconnection.log", level=logging.DEBUG)
        logging.debug(f"{self.__class__.__name__}: creating database connection.")  
        self.conn = sqlite3.connect('reciepts.db')
        logging.debug(f"{self.__class__.__name__}: created database connection.")

    def __exit__(self):
        logging.debug(f"{self.__class__.__name__}: closing database connection.")
        self.conn.close()
        logging.debug(f"{self.__class__.__name__}: closed database connection.")

    def drop_tables(self):
        # delete tables in sqlite
        logging.debug(f"{self.__class__.__name__}: dropping tables in database.")
        self.conn.execute(statements.drop_table('reciepts'))
        self.conn.execute(statements.drop_table('products'))
        self.conn.commit()
        logging.debug(f"{self.__class__.__name__}: dropped tables in database.")

    def build_tables(self):
        # create tables in sqlite
        logging.debug(f"{self.__class__.__name__}: building tables in database.")
        self.conn.execute(statements.create_reciepts_table())
        self.conn.execute(statements.create_products_table())
        self.conn.commit()
        logging.debug(f"{self.__class__.__name__}: built tables in database.")
'''
    def insert(self, head, body):
        # insert row into reciept head and body
        code, products = body
        self.conn.execute(stmts['headinsert'], head)
        [self.conn.execute(stmts['bodyinsert'], (k, "{0:.2f}".format(
            products[k]), code)) for k in products.keys()]
        self.conn.commit()
        logging.debug(f"{self.__class__.__name__}: insert row")

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
