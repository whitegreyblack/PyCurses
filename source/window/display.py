"""display.py"""
from source.window.base import Window

class DisplayWindow(Window):
    def __init__(self, window, title=None, dataobj=None, focused=False, showing=True):
        super().__init__(window, title, focused=focused, showing=showing)
        self.dataobject = dataobj
        self.selected = -1

    def on_data_changed(self, sender, arg):
        """This is a base event handler. Can remove or add more"""
        self.dataobject = arg
    
    def draw(self):
        if not self.showing:
            return

        super().draw()
        if self.dataobject:
            mx, my = self.width, self.height
            strings = list(self.dataobject.display(1, 1, mx, my, 2))
            print(strings)
            if strings:
                for y, x, s in strings:
                    if len(s) > mx:
                        raise Exception("Length of string is greater than width of window", s)
                    self.window.addstr(y, x, s)
        else:
            self.window.addstr(1, 1, "No data present")