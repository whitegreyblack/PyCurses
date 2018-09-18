#!/usr/bin/env python3

'''
User Interface Control Components
'''

__author__ = "Samuel Whang"

import sys
sys.path.append('..')

import curses
from viewer.utils import border

class UIControl:
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title

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
    def window(self):
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
        self.window.selected = False

    def get_window(self, window_id):
        for window in self.windows:
            if window.wid == window_id:
                return window

    def send_signal(self, command, debug=False):
        if (command, self.window.wid) in self.keymap:
            self.window.get_signal(command)

            if self.window.wid == 'ScrollList':
                self.get_window('Form').model = self.window.model

            next_window_id = self.keymap[(command, self.window.wid)]

            if next_window_id is None:
                return False
           
            if next_window_id is not self.window.wid:
                next_window = self.get_window(next_window_id)
                
                self.window.selected = False
                next_window.selected = True
                if next_window.wid == 'Prompt':
                    next_window.visible = True
        return True

    def draw(self, screen):
        screen.border()
        screen.addstr(0, 1, self.title)
        dimensions = f"{self.term_width}, {self.term_height}"
        screen.addstr(0, self.term_width - len(dimensions) - 1, dimensions)
        for window in self.windows:
            window.draw(screen)

# TODO Create a button class to pass into Prompt confirm/cancel parameters
class Button(UIControl):
    def __init__(self, x, y, width, height, label):
        super().__init__(x, y, width, height, None)
        self.label = label

class Prompt(UIControl):
    def __init__(self, window, title=None, confirm=None, cancel=None, wid='Prompt'):
        self.window = window
        y, x = window.getbegyx()
        my, mx = window.getmaxyx()
        super().__init__(x, y, mx - x, my - y, title)
        self.wid = wid
        self.confirm = confirm
        self.cancel = cancel
        self.selected = False
        self.visible = False

        # TODO should be changeable through constructor
        # class button: property isSelected/Selected

    @property
    def button(self):
        # TODO: a better way to access buttons. What if we have multiple? Or a single one?
        for button in [self.confirm, self.cancel]:
            if button.selected:
                return button

    def get_signal(self, command, debug=False):
        if command == curses.KEY_LEFT and self.button == self.cancel:
            self.cancel.select = False
            self.confirm.select = True
        if command == curses.KEY_RIGHT and self.button == self.confirm:
            self.confirm.select = False
            self.cancel.select = True

    def draw(self, screen):
        if self.visible:
            dx = self.width - self.x
            dy = self.height - self.y
            # screen.erase()
            self.window.erase()
            self.window.bkgdset(' ', curses.color_pair(3))
            self.window.border()
            self.window.addstr(1, 1, 'Are you sure you want to quit?');

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

    @property
    def model(self):
        if self.items:
            return self.items[self.index]
        return None

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
        for index, item in enumerate(self.items):
            if self.index == index:
                screen.addch(self.y + index + 1, 
                             self.width, 
                             curses.ACS_BLOCK)
            item.draw(screen,
                      self.x + 1, 
                      self.y + index + 1, 
                      self.width,
                      self.height,
                      self.selected,
                      self.index == index)
        
class Card:
    def __init__(self, model, title=None):
        self.model = model
        self.title = title
        self.selected = False

    def format_description(self, length):
        fields = self.model.description
        formats = self.model.formats
        space = max(0, length - sum(len(fo.format(fi)) 
                        for fi, fo in zip(fields, formats)))

        # minimum width should be 80? 
        if space == 0:
            fields = self.model.short_description
            space = max(0, length - sum(len(fo.format(fi))
                        for fi, fo in zip(fields, formats)))

        return self.model.format_criteria.format(fields[0],
                                                 ' ' * space,
                                                 fields[1])

    def draw(self, screen, x, y, dx, dy, focused, selected):
        description = self.format_description(dx - x)
        if focused and selected:
            screen.addstr(y, x, 
                          description, 
                          curses.color_pair(1))
        elif selected:
            screen.addstr(y, x,
                          description,
                          curses.color_pair(2))
        else:
            screen.addstr(y, x, description)

class Form:
    def __init__(self, x, y, width, height, model=None, wid='Form', title=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.model = model
        self.wid = 'Form'
        self.title = title
        self.selected = False

class RecieptForm(Form):
    #def __init__(self, x, y, width, height, model, title=None):
    #    super().__init__(wid, x, y, width, height, model, title)

    def draw(self, screen):
        border(screen, self.x, self.y, self.width, self.height - self.y)
        screen.addstr(self.y, 
                self.width + self.x - len(f"x:{self.x}, y:{self.y}, w:{self.width}, z:{self.height}"), 
                f"x:{self.x}, y:{self.y}, w:{self.width}, z:{self.height}")

        if self.model:
            title = self.title if self.title else "Reciept"
            screen.addstr(self.y + 1, self.x + 1, title)
           
            screen.addstr(self.y + 3, self.x + 1, f"Store:    {self.model.model.store}" )
            screen.addstr(self.y + 4, self.x + 1, f"Date :    {self.model.model.date}")
            screen.addstr(self.y + 5, self.x + 1, f"Category: {self.model.model.category}")

            screen.addstr(self.y + 7, self.x + 1, f"Products:")
            product_index = 8
            for product in self.model.model.products:
                screen.addstr(self.y + product_index, 
                              self.x + 1,
                              f"\t{product}")
                product_index += 1

            screen.addstr(self.y + 10, self.x + 1, f"Subtotal: {self.model.model.transaction.subtotal}")
            screen.addstr(self.y + 11, self.x + 1, f"Tax     : {self.model.model.transaction.tax}")
            screen.addstr(self.y + 12, self.x + 1, f"Total   : {self.model.model.transaction.total}")
            screen.addstr(self.y + 13, self.x + 1, f"Payment : {self.model.model.transaction.payment}")
        else:
            screen.addstr((self.y + self.height) // 2, 
                          ((self.x + self.width) // 2) - (len("No file selected") // 2), 
                          "No file selected")

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
