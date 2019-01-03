"""Scrollform example"""
from bearlibterminal import terminal as t
from forms import ScrollForm

# blt keycodes to break loop
exit_codes = [t.TK_ESCAPE, t.TK_CLOSE, t.TK_Q]

# instructions on using demo
directions = [
    "<a>    - Add line",
    "<s>    - Remove last line",
    "<DOWN> - Move index pointer down one",
    "<UP>   - Move index pointer up one"
    ]

# change to string type to be able to print to term
printable_directions = "\n".join(directions)

# the 'scrollable object
s = ScrollForm()

user_mapping = {
    t.TK_A: lambda x: x.add_row(f"added row {len(x.rows) + 1}"),
    t.TK_S: lambda x: x.sub_row(),
    t.TK_UP: lambda x: x.dec_index(),
    t.TK_DOWN: lambda x: x.inc_index(),
    }

# main demo
t.open()
while True:
    t.puts(s.x, s.y, s.form)
    t.puts(1, 0, str(s))
    t.puts(15, 0, f"I: {s.index}, Rows: {len(s.rows)}")
    t.puts(40, 2, printable_directions)
    t.refresh()
    ch = t.read()
    if ch in exit_codes:
        break
    if ch in user_mapping.keys():
        user_mapping[ch](s)
