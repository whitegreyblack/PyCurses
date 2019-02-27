"""
forms.py:
Includes Scrolling Window
"""
from bearlibterminal import terminal as t
from itertools import chain
DEF_X = 0
DEF_Y = 0
MAX_X = 80
MAX_Y = 24

class ScrollListModel:
    def __init__(self, topic, info):
        self.topic = topic
        self.info = info
    def __str__(self):
        return self.topic

class Window(object):
    def __init__(self, x=DEF_X, y=DEF_Y, mx=MAX_X, my=MAX_Y, showing=True):
        # outer bounding box
        self.x = x
        self.y = y
        self.mx = mx
        self.my = my

        # inner bounding box -- possibly modify based on inputs/args
        self.sx = x + 1
        self.xy = y + 1
        self.ex = mx - 1
        self.ey = my - 1

        # object box properties
        self.width = self.mx
        self.height = self.my
        
        # view/visual properties
        self.showing = showing

        # child objects
        self.texts = []
        self.children = []

    def __repr__(self):
        return f"Window({self.x}, {self.y}, {self.width}, {self.height})"

    @property
    def rows(self):
        mx = self.mx - 2
        # character map
        rows = []

        # border map
        for y in range(self.my+1):
            e, d, f = "\u2502", " " * mx, "\u2502"
            if y == 0:
                e, d, f = "\u250c", "\u2500" * mx, "\u2510"
            elif y == self.my:
                e, d, f = "\u2514", "\u2500" * mx, "\u2518"
            rows.append(f"{e}{d}{f}")
    
        # for x, y, text in self.texts:
        #     rows[y] = f"|{text.rjust(x+len(text)).ljust(mx)}|"

        return '\n'.join(rows)

    @property
    def windows(self):
        if self.showing:
            yield self.x, self.y, self.rows

        for c in self.children:
            for x, y, rows in c.windows:
                yield x, y, rows

    def add_window(self, window):
        self.children.append(window)

class Form(object):
    def __init__(self, x=DEF_X, y=DEF_Y, mx=MAX_X, my=MAX_Y, showing=True):
        # outer bounding box
        self.x = x
        self.y = y
        self.mx = mx
        self.my = my
        
        self.sx = x + 1
        self.xy = y + 1
        self.ex = mx - 1
        self.ey = my - 1
        
        self.width = self.mx
        self.height = self.my
        
        self.showing = showing
        self.texts = []

    def __repr__(self):
        return f"Form({self.width}, {self.height})"

    @property
    def form(self):
        mx = self.mx - 2
        rows = []
        for y in range(self.my+1):
            e, d = "|", " "
            if y in (0, self.my):
                e, d = "+", "-"
            rows.append(f"{e}{d*mx}{e}")
        return '\n'.join(rows)

    @property
    def forms(self):
        yield self.x, self.y, self.form

class Text(Window):
    SCROLLABLE = 1
    TEXTWRAP = 2
    BORDERED = 4
    def __init__(self, x=DEF_X, y=DEF_Y, mx=MAX_X, my=MAX_Y, text=None):
        super().__init__(x, y, mx, my)
        self.index = 0
        self.text = text if text else None

    @property
    def form(self):
        return self.text

    @property
    def forms(self):
        self.x, self.y, self.form

class ScrollList(Window):
    def __init__(self, x=DEF_X, y=DEF_Y, mx=MAX_X, my=MAX_Y, data=None):
        super().__init__(x, y, mx, my)
        self.index = 0
        self.data = data if data else []
        self.showing = True
        self.subwin = None
        self.texts = []

    def change_subwin(self):
        if self.subwin.showing:
            self.close_subwin()
        else:
            self.open_subwin()

    def open_subwin(self):
        self.subwin.showing = True
        self.subwin.texts = [(3, 1, self.rows[self.index].info)]
    
    def close_subwin(self):
        self.subwin.showing = False

    def add_row(self, row):
        self.rows.append(row)
        self.subwin.showing = True
        self.subwin.texts = [(3, 1, self.rows[self.index].info)]

    def sub_row(self, index=-1):
        """
        >>> import forms
        >>> f = forms.ScrollList()
        >>> f.sub_row()
        >>> f.subwin.showing
        False
        >>> f.add_row("test row")
        >>> f.subwin.showing
        True
        >>> f.rows
        ['test row']
        >>> f.sub_row()
        >>> f.rows
        []
        """
        if self.rows:
            self.rows.pop(index)

        if not self.rows:
            self.subwin.showing = False

    def inc_index(self):
        within_bounds = self.index + 1 < len(self.rows)
        if self.rows and within_bounds:
            self.index += 1
            self.subwin.texts = [(3, 1, self.rows[self.index].info)]

    def dec_index(self):
        within_bounds = self.index - 1 >= 0
        if self.rows and within_bounds:
            self.index -= 1
            self.subwin.texts = [(3, 1, self.rows[self.index].info)]

    @property
    def rows(self):
        mx = self.mx - 2
        rows = []

        for y in range(self.x + self.mx):
            e, d = "\u2502", " " * mx
            if y == 0:
                e, d, f = "\u250c", "\u2500" * mx, "\u2510"
            elif y == self.my:
                e, d, f = "\u2514", "\u2500" * mx, "\u2518"
            rows.append(f"{e}{d}{f}")

        rows_in_view = None
        s, e = 0, self.height - 1
        halfscreen = self.height // 2

        if len(self.data) > self.height - 1:
            if self.index < halfscreen:
                pass
            elif self.index > len(self.data) - halfscreen:
                s = len(self.data) - self.height - 1
                e = s + self.height - 1
            else:
                s = self.index - halfscreen
                e = s + self.height - 1
            rows_in_view = self.data[s:e]        
        else:
            s = 0
            rows_in_view = self.data

        for i, r in enumerate(rows_in_view):
            rows[i+1] = f"\u2502{str(r).ljust(mx)}\u2502"
            if self.index == s + i:
                rows[i+1] = f"\u2502[bkcolor=grey][color=white]{str(r).ljust(mx)}[/color][/bkcolor]\u2502"

        # for x, y, text in self.texts:
        #     rows[y] = f"|{text.rjust(x + len(text)).ljust(mx)}|"

        return '\n'.join(rows)

if __name__ == "__main__":
    f = Form()
    print(f)
    t.open()
    t.puts(f.x, f.y, f.form)
    t.refresh()
    t.read()

    import doctest            
    doctest.testmod()