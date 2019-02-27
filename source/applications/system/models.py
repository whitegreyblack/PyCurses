import curses
import random

import source.utils as utils
from source.applications.application import Application
from source.window import (DisplayWindow, PromptWindow, ScrollableWindow,
                           Window, WindowProperty)
from source.window.scrollable import (keypress_up, keypress_down)

"""
Currently we manually build the file system during runtime.

Ex.:
    data = {
        Folder(x): ...,
        ...,
    }

Eventually we would like to move to a data reader/parser of
a file to keep it simple and easier to modify

Ex.: 
    Folder 1:
        Folder 1.1:
            File A
            File B
        File C
    Folder 2:
        -- empty --
    File D
"""

def parse_system_structure(data):
    pass


# At its most basic representation, it's just a basic tree structure with
# unlimited number (not really) of children elements
# Ex. Tree(n1(n4, n5), n2(), n3(n6))

class SystemWindow(ScrollableWindow):
    def keypress_enter(self, *arg, **kwargs):
        if hasattr(self.data[self.index], 'children'):
            data = self.data[self.index].children
            if data:
                self.data = data
                self.index = 0
            else:
                self.data = None

    def keypress_escape(self, *arg, **kwargs):
        data = self.data[self.index].parent
        if data:
            self.data = data
        else:
            exit()

    def draw(self):
        if not self.showing:
            return

        Window.draw(self)

        if not self.data:
            self.window.addstr(1, 1, "No data")
            return

        rows_in_view = None
        s, e = 0, self.height
        halfscreen = self.height // 2

        if len(self.data) > self.height:
            if self.index < halfscreen:
                pass
            elif self.index > len(self.data) - halfscreen - 1:
                s = len(self.data) - self.height
                e = s + self.height + 1
            else:
                s = self.index - halfscreen
                e = s + self.height
            rows_in_view = self.data[s:e]
        else:
            s = 0
            rows_in_view = self.data

        for i, r in enumerate(rows_in_view):
            if not isinstance(r, str):
                _, _, r = r.display(1, 1, self.width, self.height, 0)

            print(r)

            l = r[:self.width]
            available = self.width - len(l)
            l = f"{l}{' ' * (self.width - len(l))}"
            c = curses.color_pair(1)
            if s + i == self.index:
                if self.focused:
                    c = curses.color_pair(2)
                else:
                    c = curses.color_pair(3)
            # c = curses.color_pair((s + i == self.index) * 2)
            self.window.addstr(i + 1, 1, l, c)

class Directory(object):
    def __init__(self, sysobjs=None):
        self.sysobjs = sysobjs if sysobjs else []
    
    def items(self):
        return len(self.sysobjs)


class SystemObject(object):
    def __init__(self, name:str):
        self.name = name
        self.parent = None

    def __str__(self):
        return self.name

    def display(self, x, y, mx, my, indent):
        indentation = " " * indent
        space_remaining = mx - indent
        
        space_empty = None
        # fills entirely
        if len(self.name) > space_remaining:
            space_empty = ""
            display_name = self.name[:space_remaining-2] + "~/"
        else:
            display_name = self.name + "/"
            space_remaining -= len(display_name) - 1
            space_empty = " " * space_remaining
        
        print(display_name)
        return x, y, f"{indentation}{display_name}{space_empty}"


class File(SystemObject):
    def __repr__(self):
        return f"File({self.name})"


class Folder(SystemObject):
    def __init__(self, name:str, children:list=None):
        super().__init__(name)
        if children:
            for child in children:
                child.parent = self
            self.children = children
        else:
            self.children = []
    def __repr__(self):
        return f"Folder({self.name})"