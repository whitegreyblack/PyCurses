#!/usr/bin/env python3
"""Data model for a product data"""

__author__ = "Samuel Whang"

class Product:
    def __init__(self, name):
        self.name = name

    @property
    def description(self):
        return f"{self.name} | Quantity: 1"

if __name__ == "__main__":
    product = Product("example")
    print(product.description)
