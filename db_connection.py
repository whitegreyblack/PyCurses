# connection.py
import sqlite3
import sys
import logging
import strings_log as log
import strings_sql as sql

# Database Object
class Connection:
    def __init__(self):
        """create connection to db"""
        self.conn = sqlite3.connect('food.db',0)
        self.build_tables()
    def build_tables(self):
        """create tables in sqlite"""
        self.conn.execute(sql.headcreate)
        self.conn.execute(sql.bodycreate)   
        self.conn.commit()
    def __exit__(self, et, ev, tb):
        self.conn.close()
    def insert(self, head, body):
        """insert row into reciept head and body"""
        code, products = body
        self.conn.execute(sql.headinsert, head)
        [self.conn.execute(sql.bodyinsert, (k, "{0:.2f}".format(products[k]),code)) for k in products.keys()]
        self.conn.commit()
    def load(self):
        """return all reciepts"""
        return self.conn.execute(sql.algrocery)
    def load_bodies(self, codes):
        """return list of recieptbodies matching codes"""
        return [self.load_body(c) for c in codes]
    def load_body(self, code):
        """return recieptbody matching code"""
        pass
    def loadByGroup(self, group, value):
        """return reciepts matching group name"""
        return self.conn.execute(sql.hdgrocery.format(group, value))
    def getMinDate(self):
        """return latest date in database"""
        return (self.conn.execute(sql.mindate)).replace("-",",")
    def getMaxDate(self):
        """return earliest date in database"""
        return (self.conn.execute(sql.maxdate)).replace("-",",")
