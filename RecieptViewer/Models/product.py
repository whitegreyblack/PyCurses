#!/usr/bin/env python3
"""Data model for a product data"""

__author__ = "Samuel Whang"

class Product:
    __slots__ = ['name',]
    def __init__(self, name):
        self.name = name
