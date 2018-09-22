import background as bg

class BaseManager:
    def __init__(self, parent):
        self.widgets = []
        self.parent = parent

        if self.parent:
            self.y, self.x = parent.window.getmaxyx()
        self.window = None

    def toggle_border_on(self):
        if self.window:
            self.window.border()

    def toggle_border_off(self):
        if self.window:
            self.window.clear()
