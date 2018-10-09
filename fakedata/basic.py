"""Basic generators"""
import random

class Age(int):
    def __init__(self, age):
        self = age

    @classmethod
    def random(cls, low=1, high=100):
        return cls(random.randint(low, high))

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
        phone= f"{openparen}{n[0:3]}{closeparen}{delim}{n[3:6]}{delim}{n[6:]}"
        return cls(phone)

class Person:
    def __init__(self, name, age, phone, address):
        self.name = name
        self.age = age
        self.phonenumber = phone
        self.address = address

    @classmethod
    def random(cls):
        # TODO: Name.Random(), Age.Random(), Phone.Random(), address.Random()
        #       A random person is still faraway from where the generator is
        #       currently at. We would need at least random name, age and 
        #       phone number to create a basic person object.
        return cls(None, None, None, None)
