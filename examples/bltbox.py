from bearlibterminal import terminal
from source.utils import point
from source.box import Box, BoxTree

def main():
    terminal.open()
    terminal.set("window.title='Scrollable Calendar Grid'")
    terminal.set("input.filter={keyboard, mouse+}")
    escape_codes = [terminal.TK_Q, terminal.TK_ESCAPE, 224]

    b = Box(point(0, 0), 80, 25)
    b.split_x()
    b.l.split_y()
    c = None
    while True:
        terminal.clear()
        for (x, y, s) in b.blt_border():
            terminal.puts(x, y, s)
        terminal.refresh()
        c = terminal.read()

        if c in escape_codes:
            break

if __name__ == "__main__":
    main()