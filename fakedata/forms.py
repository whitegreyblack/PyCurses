"""
forms.py:
Includes Scrolling Window
"""
from bearlibterminal import terminal as t

DEF_X = 0
DEF_Y = 0
MAX_X = 80
MAX_Y = 24

class Form(object):
    def __init__(self, x=DEF_X, y=DEF_Y, mx=MAX_X, my=MAX_Y):
        self.x = x
        self.y = y
        self.sx = x + 1
        self.xy = y + 1
        self.ex = mx - 1
        self.ey = my - 1
        self.mx = mx
        self.my = my
        self.width = self.mx - self.x
        self.height = self.my - self.y
        print(f"Height: {self.height}")

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
class ScrollForm(Form):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.rows = []
    def add_row(self, row):
        self.rows.append(row)
    def sub_row(self, index=-1):
        if self.rows:
            self.rows.pop(index)
    def inc_index(self):
        within_bounds = self.index + 1 < len(self.rows)
        if self.rows and within_bounds:
            self.index += 1
    def dec_index(self):
        within_bounds = self.index - 1 >= 0
        if self.rows and within_bounds:
            self.index -= 1
    @property
    def form(self):
        mx = self.mx - 2
        rows = []
        for y in range(self.mx+1):
            e, d = "|", " " * mx
            if y in (0, self.my):
                e, d = "+", "-" * mx
            rows.append(f"{e}{d}{e}")
        rows_in_view = None
        s, e = 0, self.height - 1
        halfscreen = self.height // 2
        if len(self.rows) > self.height - 1:
            if self.index < halfscreen:
                pass
            elif self.index > len(self.rows) - halfscreen:
                s = len(self.rows) - self.height + 1
                e = s + self.height - 1
            else:
                s = self.index - halfscreen
                e = s + self.height - 1
            rows_in_view = self.rows[s:e]        
        else:
            s = 0
            rows_in_view = self.rows
        for i, r in enumerate(rows_in_view):
            rows[i+1] = f"|{r.ljust(mx)}|"
            if self.index == s + i:
                rows[i+1] = f"|[color=orange]{r.ljust(mx)}[/color]|"
        return '\n'.join(rows)

if __name__ == "__main__":
    f = Form()
    print(f)
    t.open()
    t.puts(f.x, f.y, f.form)
    t.refresh()
    t.read()
    del f
    s = ScrollForm()
    for i in range(50):
        s.add_row(f"row {i}")
    t.puts(s.x, s.y, s.form)
    t.refresh()
    t.read()
    s.index = 25
    t.puts(s.x, s.y, s.form)
    t.refresh()
    t.read()
