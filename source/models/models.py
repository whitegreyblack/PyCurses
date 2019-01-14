#!/usr/bin/env python3
"""
Data models to hold data from db
"""

__author__ = "Samuel Whang"

import textwrap
from faker import Faker
from faker.providers import job, phone_number
from fakedata.name import (
    Name,
    SHORT_NAME_SCHEMA
)
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

class Task:
    tid = 0
    statuses = {
        0: "No Status",
        1: "Todo",
        2: "In progress",
        3: "Done",
    }
    def __init__(self, title, status, created, description=None, tid=None):
        self.title = title
        self.status_id = status
        self.status = Task.statuses[status]
        self.created = created
        self.description = description if description else fake.text() + fake.text()

        if tid:
            self.tid = nid
            Task.tid = max(Task.tid, tid) + 1
        else:
            self.nid = Task.tid
            Task.tid += 1
    def display(self, x, y, mx, my, indent):
        text = textwrap.wrap(self.description, mx)
        for i, line in enumerate(text):
            yield (y + i, 1, line)

class Note:
    nid = 0
    def __init__(self, title, nid=None, created=None, modified=None, note=None):
        self.title = title
        self.created = created
        self.modified = modified
        self.note = note

        if nid:
            self.nid = nid
            Note.nid = max(Note.nid, nid) + 1
        else:
            self.nid = Note.nid
            Note.nid += 1

    def __repr__(self):
        return f"Note({self.nid}, '{self.title}')"

    def display(self, x, y, mx, my, indent):
        text = textwrap.wrap(self.note, mx)
        for i, line in enumerate(text):
            yield (y + i, 1, line)

    @classmethod
    def from_database(self, nid, title, created, modified, note):
        return Note(title, nid, created, modified, note)

class Person:
    def __init__(self, name=None, address=None, job=None, phone_number=None):
        self.name = name if name else Name.random(SHORT_NAME_SCHEMA)
        self.address = address if address else fake.address()
        self.job = job if job else fake.job()
        self.phone_number = phone_number if phone_number else PhoneNumber.random()
        self.description = fake.text()
    
    def display(self, x, y, mx, my, indent=None):
        space = ''
        yield (y + 0, x, space + "Name        :")
        yield (y + 1, x, space + "Address     :")
        yield (y + 4, x, space + "Phone Number:")
        yield (y + 5, x, space + "Occupation  :")
        yield (y + 7, x, space + "Description :")

        dy = 0
        dx = indent + 13
        yield (y, dx, str(self.name))
        dy += 1

        addr = self.address.split('\n')
        for line in addr:
            yield (y + dy, dx, line)
            dy += 1
        dy += 1

        yield (y + dy, dx, self.phone_number)
        dy += 1

        occu = textwrap.wrap(self.job, mx - dx)
        for i, line in enumerate(occu):
            yield (y + dy + i, dx, line)
        dy += 2

        desc = textwrap.wrap(self.description, mx - dx)
        for line in desc[:my-dy]:
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
    test_names = [
        'Apples', 'Oranges', 'Pears', 'Watermelons', 'Peaches'
    ]
    test_prices = [3, 5, 888, 24, 55]
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

    @staticmethod
    def test_products():
        for n, p in zip(Product.test_names, Product.test_prices):
            yield Product(n, p) 

class Reciept:
    def __init__(
            self, 
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
