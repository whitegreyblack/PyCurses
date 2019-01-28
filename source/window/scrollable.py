"""scrollable.py"""
from source.window.base import Window

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
        self.on_data_changed = EventHandler()
        self.keypress_up_event = EventHandler()
        self.keypress_down_event = EventHandler()
        self.keypress_a_event = EventHandler()

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
