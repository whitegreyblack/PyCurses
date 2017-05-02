import sys

# Prepare for database insertion
class RecieptHeader:
    def __init__(self, store, date, type, code, sub, tax, tot):
        self.store = store
        self.date = date # YYYY-MM-DD
        self.type = type
        self.code = code
        self.subtotal = sub
        self.tax = tax
        self.total = tot
    def __repr__(self):
        return "{}({}: {})".format(self.__class__.__name__, self.store, self.type)
    def push(self):
        return self.store, self.date, self.type, self.code, self.subtotal, self.tax, self.total

# Prepare for database insertion
class RecieptBody:
    def __init__(self, code, products):
        self.code = code
        self.products = products
    def __repr__(self):
        return "{}(items:{})".format(self.__class__.__name__, len(self.products))
    def push(self):
        return self.code, self.products