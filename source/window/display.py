# display.py
from source.window.base import Window
from source.window.property import WindowProperty


class DisplayWindow(Window):
    def __init__(self, window, title=None, dataobj=None, properties=None, keymap=None):
        if not properties:
            properties = WindowProperty()
        super().__init__(window, title, properties, keymap=None)
        self.dataobject = dataobj
        self.selected = -1

    def on_data_changed(self, sender, arg):
        """This is a base event handler. Can remove or add more"""
        self.dataobject = arg
    
    def draw(self):
        if not self.showing:
            return
        self.term.erase()
        if self.border:
            self.term.border()        
        self.draw_title()
        if not self.dataobject:
            return
        mx, my = self.width, self.height
        for y, x, s in self.dataobject.display(1, 1, mx, my, 2):
            self.term.addstr(y, x, s)
