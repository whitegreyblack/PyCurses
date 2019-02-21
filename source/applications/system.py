# system.py (tree/fileexplorer)
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

class SystemObject(object):
    def __init__(self, name:str):
        self.name = name

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
        
        return x, y, f"{indentation}{self.name}{space_empty}"


class File(SystemObject):
    def __repr__(self):
        return f"File({self.name})"


class Folder(SystemObject):
    def __init__(self, name:str, children:list=None):
        super().__init__(name)
        if children:
            self.children = children
        else:
            self.children = []
    def __repr__(self):
        return f"Folder({self.name})"


# TODO: fake data for use in testing -- move or delete later
data = [
    Folder("Documents", [
        File("Projects"),
        File("Games"),
        File("History 101"),
    ]),
    Folder("Music"),
    Folder("Pictures", [
        Folder("Family Pictures", [
            "Photo_1.png",
            "Photo_2.png"
        ]),
        File("Random_Photo.png")
    ]),
    File("Out_Of_Place_File.txt"),
]


class SystemApplication(Application):
    CLI_NAMES = ('tree', 'system', 'file', 'files', 'filesystem')
    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.data = data
        
        # main window
        self.window.title = 'File System Example'

        # scroll window
        scroller = ScrollableWindow(
            screen.subwin(height - 2, width, 1, 0),
            title="File Explorer",
            data=[str(n) for n in self.data],
            focused=True,
            # data_changed_handlers=(self.on_data_changed,)
        )

        scroller.keypresses.on(
            (27, self.keypress_escape),
            (curses.KEY_DOWN, keypress_up),
            (curses.KEY_UP, keypress_down)
        )

        self.window.add_windows(
            scroller,
        )

        self.window.keypresses.on(
            (27, self.keypress_escape),
        )

if __name__ == "__main__":
    pass
