#!/usr/bin/env python3

__author__ = "Samuel Whang"

class SQLType:
    NULL = 'NULL'
    INT = 'INTEGER'
    REAL = 'REAL'
    TEXT = 'TEXT'
    BLOB = 'BLOB'
    
    @staticmethod
    def VARCHAR(length: int = 0) -> str:
        if length == 0:
            return "VARCHAR"
        return f"VARCHAR({length})"


def create_table(table_name, columnslist):
    columns = ', '.join(f"{n} {t}" for n, t in columnslist)
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"

def drop_table(table_name):
    return f"DROP TABLE IF EXISTS {table_name};"

def create_reciepts_table():
    return create_table('reciepts', [('filename', SQLType.TEXT),
                                     ('store', SQLType.VARCHAR()),
                                     ('date', SQLType.VARCHAR(10)), 
                                     ('category', SQLType.VARCHAR()),
                                     ('subtotal', SQLType.REAL),
                                     ('tax', SQLType.REAL),
                                     ('total', SQLType.REAL),
                                     ('payment', SQLType.REAL)])

def create_products_table():
    return create_table('products', [('filename', SQLType.TEXT),
                                     ('name', SQLType.VARCHAR()),
                                     ('price', SQLType.REAL),
                                     ('quantity', SQLType.INT)])

def insert_reciepts_command(table, num_fields):
    fields = ', '.join(['?' for i in range(num_fields)])
    return f"INSERT INTO {table} VALUES ({fields});"
'''
def create_payments_table():
    return create_table('payments', [('name', SQLType.VARCHAR()), 
                                     ('payment', SQLType.REAL),
                                     ('pay_type', SQLType.VARCHAR())])
def create_store_table():
    return create_table('stores', [('name', SQLType.VARCHAR()),
                                   ('category', SQLType.VARCHAR()),
                                   ('tax', SQLType.REAL)])
'''
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
