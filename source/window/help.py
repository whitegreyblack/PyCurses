"""help.py"""
from source.window.base import Window

class HelpWindow(Window):
    def __init__(self, window, title=None, dataobj=None, focused=False, showing=False, opener=None):
        super().__init__(window, title, focused=focused, showing=showing)
        self.dataobject = dataobj
        self.selected = -1
        self.opener = None

    def set_opener(self, sender):
        self.opener = sender

    def refocus_opener(self, sender):
        self.opener.focus(sender)
        self.opener = None

    def draw(self):
        if not self.showing:
            return

        super().draw()
        if self.dataobject:
            mx, my = self.width, self.height
            for y, x, s in self.dataobject.display(1, 1, mx, my, 2):
                if len(s) > mx:
                    raise BaseException(s)
                self.window.addstr(y, x, s)
        else:
            self.window.addstr(1, 1, "No data present")