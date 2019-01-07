"""ScrollList example"""
from bearlibterminal import terminal as t
from forms import ScrollList, ScrollListModel, Form, Window
from itertools import chain
from name import Name

# blt keycodes to break loop
exit_codes = [t.TK_ESCAPE, t.TK_CLOSE, t.TK_Q]

# instructions on using demo
directions = [
    "<a>     - Add line",
    "<s>     - Remove last line",
    "<DOWN>  - Move index pointer down one",
    "<UP>    - Move index pointer up one",
    "<ENTER> - View topic text"
    ]

# change to string type to be able to print to term
printable_directions = "\n".join(directions)

# the main screen object
w = Window()
# w.add_mapping()
w.add_window(ScrollList(mx=25, data=[Name.random((('female', 'first last'),)) for i in range(100)]))
w.add_window(Window(x=25, mx=55))
w.add_window(Window(x=20, y=6, mx=40, my=12))
print(w, w.children)
# the 'scrollable object
# s = ScrollList()
# s.subwin = Window(x=35, y=0, mx=45, my=12, showing=False)
# for i, d in enumerate(directions):
#     s.texts.append((36, 13 + i, d))

user_mapping = {
    t.TK_A: lambda x: x.add_row(
        ScrollListModel(
            f"{Name.random((('female', 'first last'),))}", 
            f"text for row {len(x.rows) + 1}"
        )),
    t.TK_S: lambda x: x.sub_row(),
    t.TK_UP: lambda x: x.dec_index(),
    t.TK_DOWN: lambda x: x.inc_index(),
    t.TK_ENTER: lambda x: x.change_subwin(),
    }

# main demo
t.open()
while True:
    for x, y, rows in w.windows:
        t.puts(x, y, rows)
    # for x, y, rows in s.forms:
    #     t.puts(x, y, rows)
    # t.puts(1, 24, str(s))
    # t.puts(15, 0, f"I: {s.index}, Rows: {len(s.rows)}")
    t.refresh()
    ch = t.read()
    if ch in exit_codes:
        break
    # if ch in user_mapping.keys():
    #     user_mapping[ch](s)
