# base.py

""" Base window class which all other windows derive from """

import textwrap
from source.window.base import Window


class ListWindow(Window):
    def __init__(self, window, title=None, data=None, properties=None):
        super().__init__(window, title, properties)
        self.data = data
        self.index = -1

    def __repr__(self):
        clsname = self.__class__.__name__
        identifier = f"{self.wid}{'-' + self.title if self.title else ''}"
        return f"{clsname}({identifier})"

    def draw(self):
        """
            Handles erasing of window, border drawing and title placement.
            Then calls children object draw functions
        """
        print('called list window draw')
        if not self.showing:
            print('not showing returns')
            return

        self.erase()
        self.draw_border()
        self.draw_title()
        
        if self.data:
            for y, d in enumerate(self.data):
                print(self.width)
                for text in textwrap.wrap(d, self.width):
                    self.window.addstr(y+1, 1, text)
                    break
        """
        if not self.parent:
            dimensions = f"{self.term_width}, {self.term_height}"
            self.window.addstr(
                self.term_height - 1, 
                self.term_width - len(dimensions) - 1, 
                dimensions
            )

        for window in self.windows:
            if window.showing:
                window.draw()
        """

