# connection.py
import sqlite3
from dbreciept import RecieptHeader, RecieptBody, sys

headcreate = """create table if not exists reciepthead (store varchar(25),
    date varchar(10), type varchar(10), code varchar(30) PRIMARY KEY,
    subtotal real, tax real, total real, UNIQUE(store, code))"""
headinsert = """insert into reciepthead values (?,?,?,?,?,?,?);"""

bodycreate = """create table if not exists recieptbody (item varchar(25), price real, code varchar(30), UNIQUE(item, price, code))"""
bodyinsert = """insert into recieptbody values (?,?,?)"""

# Database Object
class Connection:
    def __init__(self):
        self.conn = sqlite3.connect('food.db')
        self.build_tables()
    def build_tables(self):
        self.conn.execute(headcreate)
        self.conn.execute(bodycreate)
        self.conn.commit()
    def __exit__(self, et, ev, tb):
        self.conn.close()
    def insert(self, head, body):
        if isinstance(head, RecieptHeader) and isinstance(body, RecieptBody):
            headparams = (head.push())
            code, products = (body.push())
            self.conn.execute(headinsert, headparams)
            [self.conn.execute(bodyinsert, (key, "{0:.2f}".format(products[key]),code)) for key in products.keys()]
            self.conn.commit()
        else:
            sys.stderr.write("HEAD and BODY are not of same type")
