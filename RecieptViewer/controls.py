#!/usr/bin/env python3

'''
User Interface Control Components
'''

__author__ = "Samuel Whang"

import curses
from utils import border

class Window:
    def __init__(self, title, x, y):
        self.title = title
        self.term_width = x
        self.term_height = y
        self.width = x - 2
        self.height = y - 2
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)

    def draw(self, screen):
        screen.border()
        screen.addstr(0, 1, self.title)
        for window in self.windows:
            window.draw(screen)

class ScrollList:
    def __init__(self, x, y, width, height):
        self.items = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = 0

    def add_item(self, item):
        self.items.append(item)

    def draw(self, screen):
        border(screen, self.x, self.y, self.width, self.height)
        screen.addch(self.y + 1, self.x + self.width, curses.ACS_BLOCK)
        for index, item in enumerate(self.items):
            item.draw(screen,
                      self.x + 1, 
                      self.y + index + 1, 
                      self.index == index)

class Card:
    def __init__(self, model, title=None):
        self.model = model
        self.selected = False

    @property
    def description(self):
        return self.model.description

    def draw(self, screen, x, y, selected):
        if selected:
            screen.addstr(y, x, self.description, curses.color_pair(1))
        else:
            screen.addstr(y, x, self.description)

class Form:
    def __init__(self, x, y, width, height, model, title=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.model = model
        self.title = title
        self.selected = False

class ProductForm(Form):
    def __init__(self, x, y, width, height, model, title=None):
        super().__init__(x, y, width, height, model, title)

    def draw(self, screen):
        border(screen, self.x, self.y, self.width, self.height)
        # title
        if self.title:
            screen.addstr(self.y + 1, self.x + 1, self.title)
        
        # details
        screen.addstr(self.y + 3, self.x + 1, "Store: Example Store")

def test_card():
    from models import Product
    card = ViewCard(Product("example"))
    assert card.description == "example"

def test_window():
    window = Window("Example", 10, 15)
    assert window.title == "Example"
    assert (window.term_width, window.term_height) == (10, 15) 
