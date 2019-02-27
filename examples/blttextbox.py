from bearlibterminal import terminal
from source.utils import TextBox, point

def main():
    terminal.open()
    terminal.set("window.title='Scrollable Calendar Grid'")
    terminal.set("input.filter={keyboard, mouse+}")
    escape_codes = [terminal.TK_Q, terminal.TK_ESCAPE, 224]

    b = TextBox(point(0, 0), 80, 25, "asdf" * 10)
    b.split_x()
    b.l.split_y()
    b.r.split_y()

    c = None
    while True:
        terminal.clear()
        for (x, y, s) in b.blt_border():
            terminal.puts(x, y, s)
        for (x, y, s) in b.blt_text():
            terminal.puts(x, y, s)
        terminal.refresh()
        c = terminal.read()

        if c in escape_codes:
            break
        if b.l.split:
            b.l.join()
            continue
        elif b.r.split:
            b.r.join()
            continue
        b.join()

if __name__ == "__main__":
    main()