import curses
from collections import namedtuple
# from source.viewrouter import Router
from source.utils import border
from source.utils import format_float as Money

# -- Curses specific classes --
class UIComponent:
    def __init__(self, screen, title=None):
        self.screen = screen
        self.y1, self.x1 = screen.getbegyx()
        self.y2, self.x2 = screen.getmaxyx()
        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

    def __getattr__(self, fnname):
        if hasattr(self.screen, fnname):
            return object.__getattribute__(self.screen, fnname)
    # def border(self):
    #     self.screen.border()

    # def erase(self):
    #     self.screen.erase()

    # def refresh(self):
    #     self.screen.refresh()

class App:
    def __init__(self, screen):
        self.label = None
        # main parent ui component -- handles routing and drawing
        self.window = Window(screen)

        v1 = View('view1', 
                  self.window.subwin(self.window.x1 + 1,
                                     self.window.y1 + 1,
                                     self.window.x2 - 2,
                                     self.window.y2 - 2))
        v2 = View('view2',
                  self.window.subwin(self.window.x1 + 1,
                                     self.window.y1 + 1,
                                     self.window.x2 - 2,
                                     self.window.y2 - 2))
        self.window.add_view(v1)
        self.window.add_view(v2)
        v1.draw("asdf")
        v2.draw("__")
        # self.database, self.checker, ...etc.

class Window(UIComponent):
    def __init__(self, screen, views=None):
        super().__init__(screen)
        self.views = dict()
        if views:
            self.views.update(views)
        self.current = None

    def border(self):
        super().border()
        for view in self.views.values():
            view.border()

    def add_view(self, view):
        self.views[view.name] = view

    def get_view(self, name):
        if name in self.views.keys():
            return self.views[name]
        return None

    def subwin(self, x, y, w, h):
        # window.subwin(nlines, ncols, begin_y, begin_x)
        return self.screen.subwin(h, w, y, x)

class View(UIComponent):
    """Implements a view using curses subwin class"""
    def __init__(self, name, subwin):
        self.name = name
        super().__init__(subwin)

    def draw(self, message):
        self.screen.addstr(1, 1, message)

def main(screen):
    a = App(screen)
    a.window.border()
    screen.getch()
    a.window.views['view2'].clear()
    a.window.views['view2'].refresh()
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)