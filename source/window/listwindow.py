# base.py

""" Base window class which all other windows derive from """

import textwrap
from source.window.base import Window


class ListWindow(Window):
    def __init__(self, window, title=None, data=None, properties=None, keymap=None):
        super().__init__(window, title, properties, keymap=keymap)
        self.data = data
        self.index = -1

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
        
        if self.data:
            for y, d in enumerate(self.data):
                for text in textwrap.wrap(d, self.width):
                    self.term.addstr(y+1, 1, text)
                    break
