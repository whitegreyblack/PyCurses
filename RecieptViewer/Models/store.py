#!/usr/bin/env python3
"""Data model for store data from db"""

__author__ = "Samuel Whang"

class Store:
    __slots__ = ['name',]
    def __init__(self, store_name):
        self.name = store_name

if __name__ == "__main__":
    print(f"{Store.__name__}: {Store.__slots__}")
