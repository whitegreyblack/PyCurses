import click
from examples.calendargrid import MonthGrid, DateNode

@click.command()
@click.option("--debug", "debug", is_flag=True)
@click.option("--screen", "screen", default=None)
def main(debug, screen):
    if not screen:
        termprint(debug)
    elif screen == "curses" or screen == "c":
        main_curses()
    elif screen == "bear" or screen == "blt":
        main_blt()
    else:
        print("incorrect args")


def termprint(debug):
    m = MonthGrid(11, 2018)
    if debug:
        mstring = f"{repr(m)}"
    else:
        mstring = f"{m.header()}\n{m}"
    print(mstring)


def main_curses():
    def wrapped(t):
        t.getch()

    import curses
    curses.wrapper(wrapped)


def main_blt():
    from bearlibterminal import terminal
    terminal.set("window.title='Calendar Grid'")
    terminal.set("input.filter={keyboard, mouse+}")
    escape_codes = [terminal.TK_Q, terminal.TK_ESCAPE, 224]

    m = MonthGrid(11, 2018)
    n = MonthGrid(12, 2018, events=None)

    m.add_event(19, "PTO")
    m.add_event(16, "Turn in library book")
    m.add_event(18, "Game Day")
    m.add_events(22, 23, "Thanksgiving")

    n.add_event(24, "Christmas Eve")
    n.add_event(25, "Christmas")
    n.add_event(31, "New Year's Eve")

    options = ['Add', 'Edit', 'Delete', 'Save']
    footer =   '  '.join(f"[color=red]{o[0]}[/color][color=grey]{o[1:]}[/color]" for o in options)

    terminal.open()
    char = None
    while True:
        terminal.clear()
        # terminal.composition(True)
        # terminal.puts(1, 1, m.blt_data())
        terminal.puts(0, 0, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(0, 23, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(1, 23, footer)
        terminal.puts(1, 0, f"[color=black]{'File  Edit  View  Help'}[/color]")
        terminal.puts(1, 2, m.blt(colored=True))
        terminal.puts(1, 10, n.blt())
        # terminal.composition(False)
        events = m.events()
        if events:
            terminal.puts(30, 2, "Events:")
            terminal.puts(30, 3, events)
        if char:
            terminal.puts(0, 24, str(char))
        terminal.refresh()
        char = terminal.read()
        if char in escape_codes:
            break
        if char == terminal.TK_DOWN:
            m.select_next_week() 
        if char == terminal.TK_UP:
            m.select_prev_week()
        if char == terminal.TK_LEFT:
            m.select_prev_day()
        if char == terminal.TK_RIGHT:
            m.select_next_day()


if __name__ == "__main__":
    main()