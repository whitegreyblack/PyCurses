"""Schema.py
Holds table info to build sqlite tables much easier
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
    def __init__(self, name, fields, unique=None):
        self.name = name
        self.fields = fields
        self.unique = unique

    def __repr__(self):
        columns = self.join_fields()
        unique = self.join_unique()
        return f"Table: {self.name}({columns}{unique});"

    def join_params(self) -> str:
        return ', '.join(['?' for _ in range(len(self.fields))])

    def join_fields(self) -> str:
        return ', '.join(f"{n} {t}" for n, t in self.fields)

    def join_unique(self) -> str:
        unique = ""
        if self.unique:
            unique = f", UNIQUE({', '.join(self.unique)})"
        return unique

    def join_columns(self, columns) -> str:
        return ', '.join(columns)

    @property
    def drop_command(self) -> str:
        return f"DROP TABLE IF EXISTS {self.name};"

    @property
    def create_command(self) -> str:
        columns = self.join_fields()
        unique = self.join_unique()
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({columns}{unique});"

    @property
    def insert_command(self) -> str:
        params = self.join_params()
        return f"INSERT OR IGNORE INTO {self.name} VALUES ({params});"

    @property
    def select_command(self) -> str:
        return f"SELECT * FROM {self.name}"

    def select_command_on(self, columns) -> str:
        fields = self.join_columns(columns)
        return f"SELECT {fields} FROM {self.name};"

if __name__ == "__main__":
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