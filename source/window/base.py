# base.py

""" Base window class which all other windows derive from """

import curses
from math import ceil, floor

from source.keymap import EventMap
from source.utils import EventHandler


class Window:
    window_ids = 0
    def __init__(
            self, 
            window, 
            title=None, 
            title_centered=False,
            focused=False, 
            showing=True,
            border=False,
            eventmap=None,
            keypresses=None
    ):
        # keep track of current window id based on number of initialized 
        # windows
        self.wid = 1 << Window.window_ids
        Window.window_ids += 1

        self.title = title
        self.title_centered = title_centered
        y, x = window.getmaxyx()
        self.term_width = x
        self.term_height = y
        self.window = window
        self.parent = None
        self.child = False
        self.border = border
        self.width = x - 2
        self.height = y - 2
        self.components = []
        self.windows = []
        self.views = []
        self.index = 0

        self.changes = EventMap.fromkeys((
            'focused',
            'showing'
        ))

        self.showing = showing
        self._focused = focused

        self.keypresses = keypresses if keypresses else EventMap()

        self.on_focus_changed = EventHandler()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title if self.title else self.wid})"

    @property
    def currently_focused(self):
        if self.focused:
            print(f"{self} is currently focused. returning")
            return self
        for w in self.windows:
            t = w.currently_focused
            if t:
                print(f"{t} was found to be focused. {t.focused}")
                return t
        return None

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        print(f"{self}: setting focus={value}")
        self._focused = value
        print(f"{self}: setting focus is now {value}")
        self.changes.trigger('focused', self)

    def focus(self, sender=None, **kwargs):
        """Focus event handler"""
        self.focused = True

    def unfocus(self, sender=None, **kwargs):
        """Focus event handler"""
        self.focused = False

    def property_changed(self, prop):
        self.property_change_handlers(prop, self)

    def add_component(self, component):
        self.components.append(component)

    @property
    def windows(self):
        for window in self.__windows:
            # if hasattr(window, 'selected') and window.selected:
            yield window

    @windows.setter
    def windows(self, value):
        self.__windows = value

    def add_window(self, window):
        # print("add", window, window.focused, window.focused and self.focused)
        print(f"Adding window: {window}")
        window.parent = self
        window.border = True
        # if window.focused and self.focused:
        #     self.focused = not self.focused
            # print(window, "focused", self.focused)
        self.__windows.append(window)

    def add_windows(self, *windows):
        for w in windows:
            self.add_window(w)

    def add_keymap(self, keymap):
        self.keymap = keymap

    def change_window(self):
        self.window.selected = False

    def get_window(self, window_id):
        for window in self.windows:
            if window.wid == window_id:
                return window

    def toggle_showing(self):
        if self.showing:
            self.hide_window()
        else:
            self.show_window()

    def show(self, sender=None):
        self.showing = True

    def hide(self, sender=None):
        self.showing = False

    def draw(self):
        """
        Handles erasing of window, border drawing and title placement.
        Then calls children object draw functions
        """
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

    def erase(self):
        self.window.erase()

    def clear(self):
        for view in self.views:
            view.clear()

    def draw_border(self):
        if self.border:
            self.window.border()
    
    def add_handler(self, key, handler):
        if key not in self.keypresses.keys():
            self.keypress[key] = EventHandler()
        self.keypresses[key].append(handler)

    def add_handlers(self, key, *handlers):
        for handler in handlers:
            print(f'adding {key}, {handler}, "{handler.__name__}"')
            self.add_handler(key, handler)

    def handle_key(self, key):
        print(f"{self}: handling key {key}")
        self.keypresses.trigger(key, self)

