#!/usr/bin/env python3

'''
User Interface Control Components
'''

__author__ = "Samuel Whang"

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

    def add_item(self, item):
        self.items.append(item)

    def draw(self, screen):
        screen.addch(self.y, self.x, '+')
        screen.addch(self.height, self.x, '+')
        screen.addch(self.y, self.width, '+')
        screen.addch(self.height, self.width, '+')
         
        for index, item in enumerate(self.items):
            item.draw(screen, self.x + 1, self.y + index + 1)

class Card:
    def __init__(self, model, title=None):
        self.model = model
        self.focused = False

    @property
    def description(self):
        return self.model.description[0:10]

    def draw(self, screen, x, y):
        screen.addstr(y, x, self.description)

def test_card():
    from models import Product
    card = ViewCard(Product("example"))
    assert card.description == "example"

def test_window():
    window = Window("Example", 10, 15)
    assert window.title == "Example"
    assert (window.term_width, window.term_height) == (10, 15) 
