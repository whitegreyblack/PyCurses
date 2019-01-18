"""window.py"""

import curses
from source.utils import Event
from source.keymap import EventMap
from math import ceil, floor

class WindowProperty(object):
    __slots__ = [
        'title',
        'title_centered',
        'focused',
        'showing',
        'border',
    ]
    def __new__(cls, props):
        print("WP new obj")
        i = super().__new__(cls)
        i.title = None
        i.title_centered = False
        i.focused = False
        i.showing = True
        i.border = False
        return i
    
    def __init__(self, props):
        print("WP init obj")
        print(props)
        for prop, value in props.items():
            if not prop in self.__slots__:
                raise AttributeError(f"Invalid attribute: {prop}")
            setattr(self, prop, value)

    def __repr__(self):
        attrs = ', '.join(f'{k}: {getattr(self, k)}' for k in self.__slots__)
        return f"WindowProperty({attrs})"

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
            keypresses=None):
        """Main parent window which all other windows derive from"""
        # Window.window_ids[2**w] = self
        self.wid = 2**Window.window_ids
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

        self.on_focus_changed = Event()

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

    def focus(self, sender, **kwargs):
        """Focus event handler"""
        self.focused = True

    def unfocus(self, sender, **kwargs):
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

    def show(self, sender):
        self.showing = True

    def hide(self, sender):
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
            self.keypress[key] = Event()
        self.keypresses[key].append(handler)

    def add_handlers(self, key, *handlers):
        for handler in handlers:
            print(handler)
            print(handler.__name__)
            self.add_handler(key, handler)

    def handle_key(self, key):
        print(f"{self}: handling key {key}")
        self.keypresses.trigger(key, self)
        # if key in self.keypress_events.keys():
        #     self.keypress_events[key](self)

# more specific classes
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
            for y, x, s in self.dataobject.display(1, 1, mx, my, 2):
                if len(s) > mx:
                    raise BaseException(s)
                self.window.addstr(y, x, s)
        else:
            self.window.addstr(1, 1, "No data present")


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


class ScrollableWindow(Window):
    def __init__(
            self, 
            window, 
            title=None,
            title_centered=False,
            data=None, 
            focused=False,
            border=True,
            data_changed_handlers=None,
            eventmap=None):
        super().__init__(
            window, 
            title=title, 
            title_centered=title_centered, 
            focused=focused, 
            border=border, 
            eventmap=eventmap
        )
        self.on_data_changed = Event()
        self.keypress_up_event = Event()
        self.keypress_down_event = Event()
        self.keypress_a_event = Event()

        if data_changed_handlers:
            for handler in data_changed_handlers:
                self.on_data_changed.append(handler)

        self.data = data
        self.selected = -1
        self.index = 0 if self.data else -1

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        self.__data = data
        self.data_changed(self)
    
    def data_changed(self, sender, **kwargs):
        if self.__data and self.index > -1:
            self.on_data_changed(self, self.index)

    def draw(self):
        if not self.showing:
            return

        super().draw()

        if not self.data:
            self.window.addstr(1, 1, "No data")
            return

        rows_in_view = None
        s, e = 0, self.height
        halfscreen = self.height // 2

        if len(self.data) > self.height:
            if self.index < halfscreen:
                pass
            elif self.index > len(self.data) - halfscreen - 1:
                s = len(self.data) - self.height
                e = s + self.height + 1
            else:
                s = self.index - halfscreen
                e = s + self.height
            rows_in_view = self.data[s:e]
        else:
            s = 0
            rows_in_view = self.data

        for i, r in enumerate(rows_in_view):
            count_string = f"({s + i + 1}/{len(self.data)})"
            l = r[:self.width-len(count_string)-1]
            available = self.width - len(l) - len(count_string)
            l = f"{l}{' '*(self.width-len(count_string)-len(l))}{count_string}"
            c = curses.color_pair(1)
            if s + i == self.index:
                if self.focused:
                    c = curses.color_pair(2)
                else:
                    c = curses.color_pair(3)
            # c = curses.color_pair((s + i == self.index) * 2)
            self.window.addstr(i + 1, 1, l, c)

class ScrollableWindowWithBar(ScrollableWindow):
    def __init__(
            self, 
            window, 
            title=None, 
            data=None, 
            focused=False,
            border=True,
            data_changed_handlers=None):
        super().__init__(
            window, 
            title, 
            data, 
            focused, 
            border, 
            data_changed_handlers
        )
        self.offset = 1

    def draw(self):
        super().draw()
        self.draw_scroll_bar()

    def draw_scroll_bar(self):
        if len(self.data) <= self.height:
            return

        # color entire bar before individual blocks
        char = curses.ACS_BLOCK
        color = curses.color_pair(4)
        for y in range(self.height):
            self.window.addch(
                self.offset + y, 
                self.width + 1, 
                char, 
                color
            )

        # char = curses.ACS_BLOCK
        # color = curses.color_pair(4)
        # for y in range(self.scrollbar_height):
        #     try:
        #         self.window.addch(
        #             self.offset + self.scrollbar_offset + y, 
        #             self.width + 1, 
        #             char, 
        #             color
        #         )
        #     except curses.error:
        #         raise Exception(y)

def keypress_down(obj):
    t = obj.index + 1
    if t < len(obj.data):
        obj.index = t
        obj.on_data_changed()

def keypress_up(obj):
    t = obj.index - 1
    if t >= 0:
        obj.index = t
        obj.on_data_changed()
        
def keypress_a(obj):
    obj.data.append(str(len(obj.data)))
    obj.calculate_scroll_bar()
