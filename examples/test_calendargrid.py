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

    m = MonthGrid(11, 2018)
    m.add_event(4, "Birthday")
    m.add_event(13, "Trip")
    m.add_events(20, 23, "Holiday")

    terminal.open()
    char = None
    while True:
        terminal.clear()
        # terminal.composition(True)
        # terminal.puts(1, 1, m.blt_data())
        terminal.puts(1, 1, m.blt())
        # terminal.composition(False)
        terminal.puts(30, 2, m.events())
        if char:
            terminal.puts(0, 24, str(char))
        terminal.refresh()
        char = terminal.read()
        if char in [terminal.TK_Q, terminal.TK_ESCAPE, 224]:
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