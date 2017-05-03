import sys

# Prepare for database insertion
def frmt(n):
    return "{:.2f}".format(n)

class Reciept:
    def __init__(self, head, body):
        self.head = head
        self.body = body

class RecieptHeader:
    def __init__(self, *args):
        self.store = args[0]
        self.date = args[1]
        self.type = args[2]
        self.code = args[3]
        self.sub = args[4]
        self.tax = args[5]
        self.tot = args[6]
    def __repr__(self):
        return "{}({}: {:.2f})".format(self.__class__.__name__, self.store, self.tot)
    def push(self):
        return self.store, self.date, self.type, self.code, \
            frmt(self.sub), frmt(self.tax), frmt(self.tot)

# Prepare for database insertion
class RecieptBody:
    def __init__(self, *args):
        self.code = args[0]
        self.products = args[1]
    def __repr__(self):
        return "{}(items:{})".format(self.__class__.__name__, len(self.products))
    def push(self):
        return self.code, self.products