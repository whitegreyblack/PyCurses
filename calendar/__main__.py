"""
__main__.py: Runs calendar\grid within blt or curses.
"""

import click
from grid import CalendarGrid, MonthGrid, DateNode, Options, YearMonthDay

@click.command()
@click.option("--debug", "debug", default=False)
@click.option("--options", "options", default=0x3)
@click.option("--screen", "screen", default=None)
def main(debug, options, screen):
    if not screen:
        termprint(options, debug)
    elif screen == "curses" or screen == "c":
        main_curses(options, debug)
    elif screen == "bear" or screen == "b":
        main_blt(options, debug)
    else:
        print("incorrect args")


def termprint(options, debug=False):
    m = MonthGrid(11, 2018)
    if debug:
        mstring = f"{repr(m)}"
    else:
        mstring = m.term(options)
    print(mstring)


def main_curses(options, debug):
    def wrapped(t):
        # q and ESC
        escape_codes = [ord('q'), 27]

        year = CalendarGrid(2018, startdate=YearMonthDay(2018, 12))

        char = None
        while True:
            t.clear()

            t.addstr(1, 2, year.term(options=options))

            t.refresh()
            t.getch()
            break

    import curses
    curses.wrapper(wrapped)


def main_blt(options, debug):
    from bearlibterminal import terminal

    terminal.open()
    terminal.set("window.title='Calendar Grid'")
    terminal.set("input.filter={keyboard, mouse+}")

    # 224 is gui window exit key
    escape_codes = [terminal.TK_Q, terminal.TK_ESCAPE, 224]

    year = CalendarGrid(2018, startdate=YearMonthDay(2018, 12))

    # m = MonthGrid(11, 2018, border=False)
    # n = MonthGrid(12, 2018, events=None)

    # # add some events to November
    # m.add_event(19, "8:00 AM - 5:00 PM: PTO")
    # m.add_event(16, "3:30 PM: Turn in library book")
    # m.add_event(18, "3:00 PM - 8:00 PM: Game Day")
    # m.add_events(22, 23, "Thanksgiving")

    # # add some events to December
    # n.add_event(24, "Christmas Eve")
    # n.add_event(25, "Christmas")
    # n.add_event(31, "New Year's Eve")

    footer_options = ['Add', 'Edit', 'Delete', 'Save']
    footer = '  '.join(f"[color=red]{o[0]}[/color][color=grey]{o[1:]}[/color]" 
                            for o in footer_options)

    if debug:
        print(Options.options(options))

    char = None
    while True:
        terminal.clear()
        # terminal.composition(True)
        # terminal.puts(1, 1, m.blt_data())
        terminal.puts(0, 0, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(0, 23, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(1, 23, footer)
        terminal.puts(1, 0, f"[color=black]{'File  Edit  View  Help'}[/color]")
        terminal.puts(1, 2, year.term(options=options, blt=True))
        # terminal.puts(1, 10, n.blt(options=options))
        # terminal.composition(False)
        # events = m.events()
        events = None
        if events:
            terminal.puts(30, 2, "Events:")
            terminal.puts(30, 3, "\n".join(events))
        if char:
            terminal.puts(0, 24, str(char))
        terminal.refresh()
        char = terminal.read()
        if char in escape_codes:
            break
        if char == terminal.TK_A:
            year.month.add_event(m.selected, 'New Event')
        if char == terminal.TK_DOWN:
            year.month.select_next_week() 
        if char == terminal.TK_UP:
            year.month.select_prev_week()
        if char == terminal.TK_LEFT:
            year.month.select_prev_day()
        if char == terminal.TK_RIGHT:
            year.month.select_next_day()


if __name__ == "__main__":
    main()

