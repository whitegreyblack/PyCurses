#!/usr/bin/env python3

__author__ = "Samuel Whang"

def create_statement(table_name, columnslist):
    columns = ''.join(n + str(t) + ',' for n, t in columnslist)
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"

def create_card_statment():
    return 

def create_store_statement():
    return """create table if not exists cards (name varchar(20));"""

def create_products_statement():
    return """"create table if not exists products ({})"""
stmts = {
    'headcreate': """create table if not exists reciepthead (store varchar(25),
        date varchar(10), type varchar(10), code varchar(30) PRIMARY KEY,
        subtotal real, tax real, total real, UNIQUE(store, date, total))""",
    'headinsert': """insert or ignore into reciepthead \
            values (?,?,?,?,?,?,?);""",

    'bodycreate': """create table if not exists recieptbody (item varchar(25),
        price real, code varchar(30), UNIQUE(item, price, code))""",
    'bodyinsert': """insert or ignore into recieptbody values (?,?,?)""",

    'filecount': """select count(*) from reciepthead""",
    'total': """select sum(total) from reciepthead""",

    'algrocery': """select * from reciepthead""",
    'hdgrocery': """select * from reciepthead where {}='{}'""",
    'bdgrocery': """select * from reciepthead where code={}""",

    'mindate': """select min(date) from reciepthead""",
    'maxdate': """select max(date) from reciepthead""",
}

if __name__ == "__main__":
    print(create_statement("A", [['a', 123],]))
