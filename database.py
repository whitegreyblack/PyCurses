# -----------------------------------------------------------------------------
# Author  : Sam Whang | whitegreyblack
# FileName: database.py
# FileInfo: Connection object to access sqlite3 database
# -----------------------------------------------------------------------------
import sqlite3
import logging
from strings import stmts

# Database Object


class Connection:
    def __init__(self):
        # create connection to db
        self.conn = sqlite3.connect('food.db', 0)
        logging.debug("\tDB: Created Connection")
        self.build_tables()

    def build_tables(self):
        # create tables in sqlite
        self.conn.execute(stmts['headcreate'])
        self.conn.execute(stmts['bodycreate'])
        self.conn.commit()
        logging.debug("\tDB: Created Tables")

    def __exit__(self, et, ev, tb):
        self.conn.close()

    def insert(self, head, body):
        # insert row into reciept head and body
        code, products = body
        self.conn.execute(stmts['headinsert'], head)
        [self.conn.execute(stmts['bodyinsert'], (k, "{0:.2f}".format(
            products[k]), code)) for k in products.keys()]
        self.conn.commit()
        logging.debug("\tDB: Insertions Completed")

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
