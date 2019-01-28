"""prompt.py"""
from source.window.base import Window

class PromptWindow(Window):
    def __init__(self, window, title=None, focused=False, showing=True):
        super().__init__(window, title, focused=focused, showing=showing)
        self.showing = showing

    def draw(self):
        super().draw()
        y, x = self.window.getbegyx()
        self.window.addch(1, 1, ' ')
        self.window.refresh()
    
    def erase(self):
        super().erase()
        curses.curs_set(0)