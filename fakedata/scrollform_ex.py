"""Scrollform example"""
from bearlibterminal import terminal as t
from forms import ScrollForm, ScrollFormModel, Form, Window
from itertools import chain

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

# the 'scrollable object
s = ScrollForm()
s.subwin = Window(x=35, y=0, mx=45, my=12, showing=False)
for i, d in enumerate(directions):
    s.texts.append((36, 13 + i, d))

user_mapping = {
    t.TK_A: lambda x: x.add_row(
        ScrollFormModel(
            f"added row {len(x.rows) + 1}", 
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
    for x, y, rows in s.forms:
        t.puts(x, y, rows)
    t.puts(1, 23, str(s))
    t.puts(15, 0, f"I: {s.index}, Rows: {len(s.rows)}")
    # t.puts(40, 2, printable_directions)
    t.refresh()
    ch = t.read()
    if ch in exit_codes:
        break
    if ch in user_mapping.keys():
        user_mapping[ch](s)
