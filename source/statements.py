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


def create_table(table_name, columnslist, unique=None):
    columns = ', '.join(f"{n} {t}" for n, t in columnslist)
    uniquery = ""
    if unique:
        uniquery = f", UNIQUE({', '.join(unique)})"
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}{uniquery});"

def drop_table(table_name):
    return f"DROP TABLE IF EXISTS {table_name};"

def create_reciepts_table():
    return create_table('reciepts', 
                        [
                            ('filename', SQLType.TEXT),
                            ('store', SQLType.VARCHAR()),
                            ('short', SQLType.TEXT),
                            ('date', SQLType.VARCHAR(10)), 
                            ('category', SQLType.VARCHAR()),
                            ('subtotal', SQLType.REAL),
                            ('tax', SQLType.REAL),
                            ('total', SQLType.REAL),
                            ('payment', SQLType.REAL)
                        ],
                        unique=["filename",])

def create_products_table():
    return create_table('products', 
                        [
                            ('filename', SQLType.TEXT),
                            ('product', SQLType.VARCHAR()),
                            ('price', SQLType.REAL)
                        ],
                        unique=[
                            'filename', 
                            'product', 
                            'price'
                        ])


def insert_command(table, num_fields):
    fields = ', '.join(['?' for i in range(num_fields)])
    return f"INSERT OR IGNORE INTO {table} VALUES ({fields});"

def insert_command_reciept_table():
    return insert_command('reciepts', 9)

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
