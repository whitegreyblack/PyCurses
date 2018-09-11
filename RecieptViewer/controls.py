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
        self.index = 0

    @property
    def current_window(self):
        for window in self.windows:
            if hasattr(window, 'selected') and window.selected:
                return window

    def add_window(self, window):
        self.windows.append(window)

    def add_windows(self, windows):
        for window in windows:
            self.windows.append(window)

    def add_keymap(self, keymap):
        self.keymap = keymap

    def change_window(self):
        current = self.current_window()
        current.selected = False

    def get_window(self, window_id):
        for window in self.windows:
            if window.wid == window_id:
                return window

    def send_signal(self, command, debug=False):
        if (command, self.current_window.wid) in self.keymap:
            print(f"{self.current_window.wid}")
            self.current_window.get_signal(command)
            next_window_id = self.keymap[(command, self.current_window.wid)]

            if next_window_id is None:
                return False
            
            if next_window_id is not self.current_window.wid:
                next_window = self.get_window(next_window_id)
                self.current_window.selected = False
                next_window.selected = True
        return True

    def draw(self, screen):
        screen.border()
        screen.addstr(0, 1, self.title)
        dimensions = f"{self.term_width}, {self.term_height}"
        screen.addstr(0, self.term_width - len(dimensions) - 1, dimensions)
        for window in self.windows:
            window.draw(screen)

class ScrollList:
    def __init__(self, x, y, width, height, title=None, wid='ScrollList', selected=False):
        self.wid = wid
        self.items = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.index = 0
        self.selected = selected

    def add_item(self, item):
        self.items.append(item)

    def add_items(self, items):
        for item in items:
            self.items.append(item)

    def get_signal(self, command, debug=False):
        if command == curses.KEY_DOWN:
            self.index = min(self.index + 1, len(self.items) - 1)
        elif command == curses.KEY_UP:
            self.index = max(self.index - 1, 0)

    def draw(self, screen):
        dx = self.width - self.x
        dy = self.height - self.y
        border(screen, self.x, self.y, dx, dy)
        
        if self.title:
            screen.addstr(self.y, self.x + 1, self.title) 

        screen.addstr(self.y, self.x - 1, str(self.index))
        # screen.addch(self.y + 1, self.width, curses.ACS_BLOCK)
        for index, item in enumerate(self.items):
            item.draw(screen,
                      self.x + 1, 
                      self.y + index + 1, 
                      self.selected and self.index == index)
        
        if not self.selected:
            screen.addstr(self.y + index + 2, self.x + 1, 'UNSELECTED')
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
    def __init__(self, x, y, width, height, model, wid='Form', title=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.model = model
        self.wid = 'Form'
        self.title = title
        self.selected = False

class ProductForm(Form):
    #def __init__(self, x, y, width, height, model, title=None):
    #    super().__init__(wid, x, y, width, height, model, title)

    def draw(self, screen):
        border(screen, self.x, self.y, self.width, self.height - self.y)
        screen.addstr(self.y, 
                      self.x + 1, 
                      f"{self.x}, {self.y}, {self.width}, {self.height}")
        if self.title:
            screen.addstr(self.y + 1, self.x + 1, self.title)
       
        if self.selected:
            screen.addstr(self.y + 2, self.x + 1, 'Selected')

        screen.addstr(self.y + 3, self.x + 1, "Store: Example Store")

    def get_signal(self, command):
        return

def test_card():
    from models import Product
    card = ViewCard(Product("example"))
    assert card.description == "example"

def test_window():
    window = Window("Example", 10, 15)
    assert window.title == "Example"
    assert (window.term_width, window.term_height) == (10, 15) 
