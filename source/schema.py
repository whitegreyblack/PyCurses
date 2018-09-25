"""Schema.py
Holds table info to build sqlite tables much easier
"""

__author__ = "Samuel Whang"
from source.utils import SQLType
from source.sqlbuilder import SqlString as sql

class Table:
    def __init__(self, name, fields, unique=None):
        self.name = name
        self.fields = fields
        self.unique = unique

    def __repr__(self):
        columns = self.join_fields()
        unique = self.join_unique()
        return f"Table: {self.name}({columns}{unique});"

    def join_fields(self) -> str:
        return ', '.join(f"{n} {t}" for n, t in self.fields)

    def join_unique(self) -> str:
        unique = ""
        if self.unique:
            unique = f", UNIQUE({', '.join(self.unique)})"
        return unique

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
        pass

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