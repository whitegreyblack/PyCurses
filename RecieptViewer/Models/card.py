#!/usr/bin/env python3
"""Data model for card data from the database"""

__author__ = "Samuel Whang"

class Card:
    __slots__ = ['number',]
    def __init__(self, card_number: str):
       self.number = card_number

if __name__ == "__main__":
    print(f"{Card.__name__}: {Card.__slots__}")
