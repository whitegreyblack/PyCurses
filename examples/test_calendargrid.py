import click
from examples.calendargrid import MonthGrid, DateNode

@click.command()
@click.option("--screen", "screen", default=None)
def main(screen):
    if not screen:
        termprint()
    elif screen == "curses" or screen == "c":
        main_curses()
    elif screen == "bear" or screen == "blt":
        main_blt()
    else:
        print("incorrect args")


def termprint():
    m = MonthGrid(11, 2018)
    print(repr(m))


def main_curses():
    def wrapped(t):
        t.getch()

    import curses
    curses.wrapper(wrapped)


def main_blt():
    from bearlibterminal import terminal

    m = MonthGrid(11, 2018)

    terminal.open()
    char = None
    while True:
        terminal.clear()
        terminal.puts(10, 9, m.month_name)
        terminal.puts(10, 10, m.blt())
        if char:
            terminal.puts(1, 1, str(char))
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
    # terminal.refresh()
    # terminal.clear()
    # terminal.read()


if __name__ == "__main__":
    main()