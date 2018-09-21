"""Handles routing to different windows"""

__author__ = "Samuel Whang"

class Router:
    def __init__(self, name):
        self.name = name
        self.views = dict()
        self.path = None

    def add_window(self, name, window):
        if name in self.views:
            errmsg = f"Name: {Name} is already being used in views"
            raise ValueError(errmsg)

        self.views[name] = window
        if len(self.views.keys()) == 1:
            self.path = name

    @property
    def view(self):
        return self.views[self.path]

    @view.setter
    def view(self, name):
        if name not in self.views:
            errmsg = f"Name: {name} does not exit in views"
            raise ValueError(errmsg)

        self.path = name

if __name__ == "__main__":
    r = Router('views')
    r.add_window('viewer', 3)
    r.add_window('other', 5)
    print(r.view)
    r.view = 'other'
    print(r.view)
