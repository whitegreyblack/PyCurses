#!/usr/bin/env python3

__author__ = "Samuel Whang"

class ViewCard:
    '''
    UI Component
    '''
    def __init__(self, model):
        self.model = model
        self.focused = False

    def description(self, length):
        return self.model.description[0:length]

if __name__ == "__main__":
    from ..Models.product import Product
    card = ViewCard(Product("example"))
    print(card.description)
