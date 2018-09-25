#!/usr/bin/env python3

__author__ = "Samuel Whang"

from source.utils import SQLType

def drop_table(table_name):
    return f"DROP TABLE IF EXISTS {table_name};"

def create_table(table_name, columnslist, unique=None):
    columns = ', '.join(f"{n} {t}" for n, t in columnslist)
    uniquery = ""
    if unique:
        uniquery = f", UNIQUE({', '.join(unique)})"
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}{uniquery});"

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

if __name__ == "__main__":
    print(create_statement("A", [['a', 123],]))
