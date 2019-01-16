"""Class to build sql queries"""

# TODO: build from small cases and keep adding on until advanced
# sort of like linq queries
# Chaining methods

class SqlString(str):
    def __init__(self, string=""):
        self = string

    def Drop(self, table):
        return SqlString(f"DROP TABLE IF EXISTS {table}")

    def Create(self, table, fields, unique):
        return SqlString

    def Select(self, fields):
        def join(fields):
            return fields if fields is "*" else ", ".join(fields)
        return SqlString(f"SELECT {join(fields)}")
    
    def From(self, table):
        return SqlString(self + f" FROM {table}")

    def Where(self, conditions):
        return SqlString(self + f" WHERE {' and '.join(conditions)}")

    def OrderBy(self, orders):
        return SqlString(self + f" ORDER BY {' and '.join(orders)}")

    def End(self):
        return SqlString(self + ";")

    @staticmethod
    def check_syntax(string):
        return false

if __name__ == "__main__":
    string = SqlString()          \
                .Select("*")      \
                .From("receipts") \
                .OrderBy(["Name", "Product"])
    print(string)