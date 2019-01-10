#!/usr/bin/env python3
"""
Data models to hold data from db
"""

__author__ = "Samuel Whang"

import textwrap
from faker import Faker
from faker.providers import job, phone_number
from fakedata.name import Name
from fakedata.phonenumber import PhoneNumber
from typing import Union
from collections import namedtuple

Currency = Union[int, float]

shortnames = {
    'Leevers': 'Leevers',
    'Bek Internet': 'Bek',
}

def shorten(storename):
    store_words = storename.split()
    for word in store_words:
        if word in shortnames.keys():
            return shortnames[word]
    return storename

def day_month(date):
    pass

point = namedtuple('Point', 'x y')
pointgrid = namedtuple('PointGrid', 'x y width height')

fake = Faker()
fake.add_provider(job)
fake.add_provider(phone_number)

class Person:
    def __init__(self, name=None, address=None, job=None, phone_number=None):
        self.name = name if name else Name.random((('female', 'first last'),))
        self.address = address if address else fake.address()
        self.job = job if job else fake.job()
        self.phone_number = phone_number if phone_number else PhoneNumber.random()
        self.description = fake.text()
    
    def display(self, x, y, mx, my, indent=0):
        space = ' ' * indent
        yield (y + 0, x, space + "Name         :")
        yield (y + 1, x, space + "Address      :")
        yield (y + 4, x, space + "Phone Number :")
        yield (y + 5, x, space + "Occupation   :")
        yield (y + 7, x, space + "Description  :")

        dy = 0
        dx = indent + 18
        yield (y, dx, str(self.name))
        dy += 1

        addr = self.address.split('\n')
        for line in addr:
            yield (y + dy, dx, line)
            dy += 1
        dy += 1

        yield (y + dy, dx, self.job)
        dy += 1

        yield (y + dy, dx, self.phone_number)
        dy += 2

        desc = textwrap.wrap(self.description, mx - dx)
        for line in desc:
            yield (y + dy, dx, line)
            dy += 1

class Transaction:
    properties = ["subtotal", "tax", "total", "payment"]
    def __init__(self, 
                 total: Currency, 
                 payment: Currency, 
                 subtotal: Currency, 
                 tax: Currency = 0,
                 change: Currency = 0.00):

        self.subtotal = subtotal
        self.total = total
        self.payment = payment
        self.tax = self.total - self.total
        self.change = payment - total

        if self.change < 0:
            raise ValueError('payment less than total cost')

class Product:
    def __init__(self, name: str, price: Currency):
        self.name = name
        self.name_format = '{}'
        self.price = float(price)
        self.price_format = '{:.2f}'

    @property
    def description(self):
        return self.name, self.price
    
    @property
    def formats(self):
        return self.name_format, self.price_format

    @property
    def format_criteria(self):
        return '{}{}{:.2f}'

class Reciept:
    def __init__(self, 
                 store: str, 
                 store_short: str,
                 date: str,
                 date_short: str,
                 category: str, 
                 products: list, 
                 transaction: Transaction):
        """Initialize fields used in reciept"""
        self.store = store
        self.store_short = store_short
        self.date = date
        self.date_short = date_short
        self.category = category
        self.products = products
        self.transaction = transaction

    @property
    def description(self):
        return self.store, self.date_short

    @property
    def short_description(self):
        return self.store_short, self.date_short

    @property
    def formats(self):
        return '{}', '{}'

    @property
    def format_criteria(self):
        return '{}{}{}'

if __name__ == "__main__":
    product = Product("example", 4)
    print(product.description)
