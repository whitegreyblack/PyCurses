"""database.py: Connection object to access sqlite3 database"""

__author__ = "Samuel Whang"

import datetime
import logging
import sqlite3
from collections import namedtuple

import source.config as config
from source.logger import Loggable
from source.schema import (SQLType, Table, build_products_table,
                           build_receipts_table)
from source.utils import filename_and_extension as fileonly
from source.utils import format_date as date
from source.utils import format_float as real
from source.utils import logargs, setup_logger, setup_logger_from_logargs
from source.YamlObjects import receipt
from source.models.models import Note

spacer = "  "

def unpack(cursor):
    """Returns data in a database cursor object as list"""
    return [data for data in cursor]

# class Connection(Loggable):
class Connection:
    """
    Database Connection Object
    TODO: make this more abstract for different connections
    """
    schema = None
    rebuild = False
    database_path = None
    clean_script_path = None
    rebuild_script_path = None

    def __init__(self, database, schema=None, rebuild=False):
        if database:
            self.database = database
        if schema:
            self.schema = schema
        if rebuild:
            self.rebuild = rebuild

        self._connection = sqlite3.connect(
            self.database,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.schema = schema
        self.rebuild_database(rebuild)
    
    def __del__(self):
        print(self.database_path)
        self._connection.close()

    def rebuild_database(self, rebuild):
        """
        If table needs rebuilding, the rebuild script path linked to the
        rebuild script will be opened and each statement in the script 
        executed.
        """
        if not rebuild or not self.rebuild_script_path:
            return

        with open(self.rebuild_script_path, 'r') as sql:
            for stmt in ''.join(sql.readlines()).split(';'):
                self._connection.execute(f"{stmt};")
        self._connection.commit()

    def insert(self, obj):
        if not self.model_name:
            raise NotImplementedError
        fn_name = 'insert_' + self.model_name
        if hasattr(self, 'insert_' + self.model_name):
            getattr(self, fn_name)(obj)
        else:
            raise Exception(f"function name not found {fn_name}")

class PersonConnection(Connection):
    database = config.DATABASE_POINTER_CONTACTS

    def __init__(self, database=None, schema=None, rebuild=False):
        """Wrapper to pass in contact connection specific attributes"""
        super().__init__(database, schema, rebuild)

class QuizConnection(Connection):
    database = config.DATABASE_POINTER_QUIZ
    clean_script = config.CONNECTION_CLEAN_SCRIPT_QUIZ
    rebuild_script = config.CONNECTION_REBUILD_SCRIPT_QUIZ

    def __init__(self, database=None, schema=None, rebuild=False):
        """Wrapper to pass in quiz connection specific attributes"""
        super().__init__(database, schema, rebuild)

    def select_questions(self):
        return []

    def insert_question(self):
        pass

class ReceiptConnection(Connection):
    
    database = config.DATABASE_POINTER_RECEIPTS
    clean_script = config.CONNECTION_CLEAN_SCRIPT_RECEIPTS
    rebuild_script = config.CONNECTION_REBUILD_SCRIPT_RECEIPTS

    def __init__(self, database=None, schema=None, rebuild=False):
        if database:
            self.database = database
        if schema:
            self.schema = schema
        if rebuild:
            self.rebuild = rebuild

        super().__init__(database, rebuild=rebuild)
        self.tables = [
            build_receipts_table(),
            build_products_table()
        ]
        self.committed = []

    #     self.log("closing database connection.")
    #     self.conn.close()
    #     self.log("closed database connection.")

    def table(self, name):
        for table in self.tables:
            if table.name == name:
                return table
        self.log(f"{name} table not found in database tables list",
                 level=logging.WARNING)

    def send(self, message):
        results = self.conn.execute(message.request)
        if message.requires_commit:
            self.commit() 
        return results

    def rebuild_tables(self):
        if self.rebuild:
            self.drop_tables()
            self.build_tables()

    def drop_tables(self):
        # delete tables in sqlite
        self.log("dropping tables in database.")
        tablenames = []
        for table in self.tables:
            self.conn.execute(table.drop_command)
            self.log(f"{spacer}x Dropped {table.name}")
            tablenames.append(table.name)
        self.conn.commit()
        self.log("dropped tables {', '.join(tablenames)} in database.")

    def build_tables(self, tables=None):
        # create tables in sqlite
        self.log("building tables in database.")
        tablenames = []
        for table in self.tables:
            self.conn.execute(table.create_command)
            self.log(f"{spacer}+ Created {table.name}")
            tablenames.append(table.name)
        self.conn.commit()
        self.log("created tables {', '.join(tablenames)} in database.")

    def previously_inserted_files(self, fields=None):
        self.log("retrieving inserted files from database")
        cursor = self.conn.execute("SELECT FILENAME FROM receipts;")
        for data in unpack(cursor):
            yield data

    def insert_files(self, yaml_objs: dict):
        if not yaml_objs:
            self.log("no yaml receipts to insert. returning early")
            return

        self.log("inserting receipts data into database.")
        inserted_files = self.previously_inserted_files()
        
        receipt_table = self.table("receipts")
        product_table = self.table("products")

        # iterate through the files verified by yamlchecker
        for file_name, yaml_obj in yaml_objs.items():
            if file_name not in inserted_files:
                self.log(f"inserting {file_name}")

                file_only, _ = fileonly(file_name)
                self.conn.execute(
                    receipt_table.insert_command, 
                    (
                        file_only,
                        yaml_obj.store,
                        yaml_obj.short,
                        date(yaml_obj.date),
                        yaml_obj.category,
                        real(yaml_obj.subtotal),
                        real(yaml_obj.tax),
                        real(yaml_obj.total),
                        real(yaml_obj.payment)
                    )
                )
                                    
                self.log(f"{spacer}+ 'filename': '{file_only}'")
                self.log(f"{spacer}+ 'storename': '{yaml_obj.store}'")
                self.log(f"{spacer}+ 'category': '{yaml_obj.category}'")
                self.log(f"{spacer}inserted into receipt table")

                for product, price in yaml_obj.products.items():
                    self.log(f"{spacer}+ '{product}': '{price:.2f}'")
                    self.conn.execute(
                        product_table.insert_command, 
                        (
                            file_only,
                            product, 
                            real(price)
                        )
                    )
                self.log(f"{spacer}inserted into products table")
            else:
                self.log(f"data from {file_name} already inserted")

        self.conn.commit()
        self.committed = list(yaml_objs.keys())
        self.log("completed inserting receipts data.")

    def select_receipts(self):
        fields = "rid sid created purchased_on subtotal tax total payment rfile"
        receipttuple = namedtuple('receipt', fields)
        cursor = self._connection.execute("SELECT * FROM receipts;")
        for receiptobj in list(cursor):
            print(receiptobj)
            yield receipttuple(*receiptobj)

    def select_store(self, store_id):
        store = namedtuple("StoreName", "store cid")

        c = f"""
        select store, id_category
        from stores
        where id_store = {store_id};
        """[1:]
        cursor = self._connection.execute(c)
        for info in unpack(cursor):
            return store(*info)

    def select_category(self, category_id):
        c = f"select category from storecategory where id_category={category_id};"
        cursor = self._connection.execute(c)
        for info in unpack(cursor):
            return info

    def select_from_table(self, table, fields, condition=None):
        if condition:
            select_from_table_with_condition(table, fields, condition)
        return self.conn.execute(f"SELECT {fields} from {table}")

    def select_from_table_with_condition(self, table, fields, condition):
        return self.conn.execute(f"SELECT {fields} FROM {table} {condition}");

    def select_receipt_products(self, receipt_id):
        product = namedtuple("ProductInfo", "product price")
        c = f"""
        SELECT product, price 
        from receiptproducts rp 
        join products p 
        on rp.id_product = p.id_product
        where rp.id_receiptproduct = {receipt_id};
        """[1:]
        cursor = self._connection.execute(c)
        for info in unpack(cursor):
            yield product(*info)

class NoteConnection(Connection):
    model_name = "note"
    schema = None
    database_path = config.DATABASE_POINTER_NOTES
    clean_script_path = config.CONNECTION_CLEAN_SCRIPT_NOTES
    rebuild_script_path = config.CONNECTION_REBUILD_SCRIPT_NOTES

    def __init__(self, database=None, schema=None, rebuild=False):
        if database:
            self.database_path = database
        if schema:
            self.schema = schema
        if rebuild:
            self.rebuild = rebuild
        
        super().__init__(self.database_path, self.schema, self.rebuild)

        self.fields = list(self.tables_info())
        if not self.fields:
            raise Exception("Table not initialized for notes app")

    def tables_info(self):
        table_info = []
        cursor = self._connection.execute('pragma table_info(notes)')
        for colnum, colname, coltype, _, _, autoincrement in cursor:
            yield (colname, coltype)
    
    def select_max_note_id(self):
        statement = "SELECT MAX(id_note) FROM NOTES;"
        cursor = self._connection.execute(statement)
        for max_id in cursor.fetchone():
            return max_id

    def select_from_table(self):
        table = "notes"
        fields = ", ".join(n for (n, t) in self.fields)
        statement = f"select {fields} from {table}"
        for note in self._connection.execute(statement).fetchall():
            yield note
    
    def insert_note(self, obj):
        print(obj)
        if isinstance(obj, Note):
            attr = f"""
'{obj.title}', '{obj.created}', '{obj.modified}', {repr(obj.note)}
"""[1:]
        else:
            attr = f"""
'{obj['title']}', 
'{datetime.datetime(*obj['created'])}', 
'{datetime.datetime(*obj['modified'])}', 
{repr(obj['note'])}
"""[1:]
        print('Attr:', attr)
        s = f"INSERT INTO NOTES (title, created, modified, note) VALUES ({attr});"
        self._connection.execute(s)
        self._connection.commit()
        print(obj, "written to db")

class NoteConnection:
    """TODO: make this more abstract for different connections"""
    def __init__(self):
        # leave the logging initialization to the loggable class
        self.__connection = sqlite3.connect(
            'data/notes.db', 
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.fields = list(self.tables_info())
        if not self.fields:
            self.__connection.execute()

    def tables_info(self):
        table_info = []
        cursor = self.__connection.execute('pragma table_info(notes)')
        for colnum, colname, coltype, _, _, autoincrement in cursor:
            yield (colname, coltype)
    
    def select_from_table(self):
        table = "notes"
        print(self.fields)
        fields = ", ".join(n for (n, t) in self.fields)
        print(fields)
        statement = f"select {fields} from {table}"
        print(statement)
        for note in self.__connection.execute(statement).fetchall():
            yield note
    
if __name__ == "__main__":
    # args = logargs(type("db_main", (), dict()))
    # logger = setup_logger_from_logargs(args)
    # db = Connection(None, logger=logger)
    n = NoteConnection()
    print(datetime.datetime.strftime(
        datetime.datetime.today(), 
        '%Y-%m-%d %I:%M:%S')
    )
    for (rowid, title, created, modified, note) in n.select_from_table():
        print(created, type(created))
