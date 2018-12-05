"""
Schema.py: 
    Holds table info to build sqlite tables much easier. Very naive 
    implementation but does allow for quick command building and QOL 
    functions.
    Should not interact with any database. Most functions return string 
    results to be used elsewhere as sql commands.
"""

__author__ = "Samuel Whang"

class SQLType:
    """Handles datatype inserting for sql create commands"""
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

class Table:
    """Using a class to place all necessary table info into a single object
    to create sql commands without outside input.
    """
    def __init__(self, name: str, fields: list, unique=None):
        """Applies parameters to corresponding instance properties"""
        self.name = name
        self.fields = fields
        self.unique = unique

    def __repr__(self) -> str:
        """Returns a string representation of the current table"""
        columns = self.join_fields()
        unique = self.join_unique()
        return f"{self.name}({columns}{unique});"

    def join_params(self) -> str:
        """
        Returns a selector string used in insert queries based on the number
        of fields in the current table
        """
        return ', '.join(['?' for _ in range(len(self.fields))])

    def join_fields(self) -> str:
        """Returns all fields and datatypes in the table"""
        return ', '.join(f"{n} {t}" for n, t in self.fields)

    def join_unique(self) -> str:
        """Returns the constraint in a table if it exists"""
        unique = ""
        if self.unique:
            unique = f", UNIQUE({', '.join(self.unique)})"
        return unique

    def join_columns(self, columns: list) -> str:
        return ', '.join(columns)

    @property
    def drop_command(self) -> str:
        """Returns sub string of a drop table command"""
        return f"DROP TABLE IF EXISTS {self.name};"

    @property
    def create_command(self) -> str:
        """Returns a create table command in sql as a string"""
        columns = self.join_fields()
        unique = self.join_unique()
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({columns}{unique});"

    @property
    def insert_command(self) -> str:
        """Returns an insert table command in sql as a string"""
        params = self.join_params()
        return f"INSERT OR IGNORE INTO {self.name} VALUES ({params});"

    @property
    def select_command(self) -> str:
        """
        Returns a select query comand in sql as a string that pulls all known
        fields columns in the current table
        """
        return f"SELECT * FROM {self.name}"

    def select_command_on(self, columns: list) -> str:
        """
        Returns a select query command in sql as a string that pulls only the
        columns specified in the columns paramater
        """
        fields = self.join_columns(columns)
        return f"SELECT {fields} FROM {self.name};"

    def select_join_table(self, colA: list, tableB: object, colB: list) -> str:
        """
        SELECT *
        FROM tableA
        JOIN tableB
            ON tableA.field = tableB.field
        """
        columns = self.join_columns(columns)
        return "Not Yet Implemented"
        

def build_reciepts_table():
    """Pre-specified table information used in creating a table object"""
    return Table("reciepts",
                 [
                    ("filename", SQLType.TEXT),
                    ("store", SQLType.VARCHAR()),
                    ("short", SQLType.TEXT),
                    ("date", SQLType.VARCHAR(10)), 
                    ("category", SQLType.VARCHAR()),
                    ("subtotal", SQLType.REAL),
                    ("tax", SQLType.REAL),
                    ("total", SQLType.REAL),
                    ("payment", SQLType.REAL)
                 ], unique=["filename",])

def build_products_table():
    """Pre-specified table information used in creating a table object"""
    return Table("products", 
                 [
                    ("filename", SQLType.TEXT),
                    ("product", SQLType.VARCHAR()),
                    ("price", SQLType.REAL)
                 ], unique=["filename", "product", "price"])

if __name__ == "__main__":
    # create a simple table with some fields and datatype values
    fields = [
        ("a", SQLType.INT),
        ("b", SQLType.INT),
        ("c", SQLType.VARCHAR(20))
    ]
    t = Table("example", fields, ["b",])
    print(t)
    print(t.drop_command)
    print(t.create_command)
    print(t.insert_command)
    print(t.select_command_on(['a', 'b']))

    print(build_reciepts_table())
    print(build_products_table())
