#!/usr/bin/env python3
"""
Data models to hold data from db
"""

__author__ = "Samuel Whang"

from typing import Union

Currency = Union[int, float]

class Transaction:
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
                 date: str, 
                 category: str, 
                 products: list, 
                 transaction: Transaction):
        """Initialize fields used in reciept"""
        self.store = store
        self.date = date
        self.category = category
        self.products = products
        self.transaction = transaction

    @property
    def description(self):
        return self.store, self.date

    @property
    def formats(self):
        return '{}', '{}'

    @property
    def format_criteria(self):
        return '{}{}{}'

if __name__ == "__main__":
    product = Product("example", 4)
    print(product.description)
