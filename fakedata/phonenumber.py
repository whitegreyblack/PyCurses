import random

class PhoneNumber(str):
    def __init__(self, number):
        self = number

    @classmethod
    def random(cls, delimiter="-", parenthesis=False):
        delim = delimiter
        openparen = ""
        closeparen = ""
        if parenthesis:
            openparen = "("
            closeparen = ")"
        n = str(random.randint(1000000000, 9999999999))
        phone = f"{openparen}{n[0:3]}{closeparen}{delim}{n[3:6]}{delim}{n[6:]}"
        return cls(phone)