"""Class to build sql queries"""

# TODO: build from small cases and keep adding on until advanced
# sort of like linq queries
# Chaining methods

class SqlString(str):
    def __init__(self, string=""):
        self = string

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

    @staticmethod
    def check_syntax(string):
        return false

if __name__ == "__main__":
    string = SqlString()          \
                .Select("*")      \
                .From("Reciepts") \
                .OrderBy([""])
    print(string)
