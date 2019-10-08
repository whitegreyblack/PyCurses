# base.py

""" Base window class which all other windows derive from """

import curses
from math import ceil, floor

from source.keymap import EventMap
from source.utils import EventHandler
from source.window.property import WindowProperty


class Window:
    window_id = 0
            
    def __repr__(self):
        clsname = self.__class__.__name__
        description = f"{self.window_id}{(f'-{self.title}') if self.title else ''}"
        return f"{clsname}({description})"

    def __init__(
            self, 
            term, 
            title=None, 
            properties=None,
            keymap=None,
            windows=None
    ):
        # keep track of current window id based on number of initialized 
        # windows
        self.window_id = Window.window_id
        Window.window_id += 1

        # curses screen reference
        self.term = term
        self.title = title
        self.title_centered = False
        self.term_height, self.term_width = term.getmaxyx()
        self.parent = None
        self.width = self.term_width - 2
        self.height = self.term_height - 2
        self.keymap = keymap

        if not properties:
             # default window settings if none provided
            properties = WindowProperty()
        for prop, value in properties.__dict__.items():
            setattr(self, prop, value)
        
        self.children = dict()
        if windows:
            for window in windows:
                window.parent = self
                self.children[window.window_id] = window
        if self.focusable:
            self.focused = self.window_id
        for child_window in self.children.values():
            if child_window.focusable:
                child_window.focused = True
                break
        self.closed = False

    @property
    def active(self):
        if self.focusable and self.focused:
            return self.window_id
        if self.children:
            for window_id, child_window in self.children.items():
                if child_window.focused:
                    print(child_window)
                    return window_id
        raise Exception("No active window found")

    def change_focus(self):
        ...

    def draw_title(self):
        if self.title:
            c = curses.color_pair(2)
            x, y, s = 0, 0, self.title[:self.term_width//2]
            # children titles are -1 from the right
            if self.title_centered:
                c = curses.color_pair(1)
                if self.focused:
                    c = curses.color_pair(2)
                x = self.width // 2 - len(self.title) // 2
            else:
                if self.parent:
                    x = self.width - len(s) - 2
                    c = curses.color_pair(1)
                    if self.focused:
                        c = curses.color_pair(2)
                else:
                    s = s.rjust(len(s)+2).ljust(self.width+2)
            self.term.addstr(y, x, s, c)

    def draw(self):
        """
        Handles erasing of window, border drawing and title placement.
        Then calls children object draw functions
        """
        if not self.showing:
            return
        self.term.erase()
        if self.border:
            self.term.border()
        self.draw_title()
        dimensions = f"{self.term_width}, {self.term_height}"
        self.term.addstr(
            self.term_height - 1, 
            self.term_width - len(dimensions) - 1, 
            dimensions
        )

        for child in self.children.values():
            child.draw()

    def close(self):
        self.closed = True
 
    def handle_key(self, key):
        if key in self.keymap:
            getattr(self, self.keymap[key])()
            return True
        return False