# base.py

""" Base window class which all other windows derive from """

import curses
from math import ceil, floor

from source.keymap import EventMap
from source.utils import EventHandler
from source.window.base import Window


class ListWindow(Window):
    def __init__(self, window, title=None, dataobj=None, focused=False, showing=True):
        super().__init__(window, title, focused=focused, showing=showing)
        self.dataobject = dataobj
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
        print('called list window')
        if not self.showing:
            return
        self.erase()
        self.draw_border()

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
            self.window.addstr(y, x, s, c)

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

