# connection.py
import sqlite3
import sys
import logging
import strings_log as log
import strings_sql as sql
from reciept_py import RecieptHeader, RecieptBody, sys

# Database Object
class Connection:
    def __init__(self):
        self.conn = sqlite3.connect('food.db',0)
        self.build_tables()
    def build_tables(self):
        self.conn.execute(sql.headcreate)
        self.conn.execute(sql.bodycreate)   
        self.conn.commit()
    def __exit__(self, et, ev, tb):
        self.conn.close()
    def insert(self, head, body):
        code, products = body
        self.conn.execute(sql.headinsert, head)
        [self.conn.execute(sql.bodyinsert, (k, "{0:.2f}".format(products[k]),code)) for k in products.keys()]
        self.conn.commit()
    def load(self):
        head = self.conn.execute(sql.algrocery)
        return head
    def loadByGroup(self, group, value):
        return self.conn.execute(sql.hdgrocery.format(group, value))
