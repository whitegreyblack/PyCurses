"""
File: scrollablecalendartest.py
Runs application for the scrollable calendar class
"""
import click
import calendar
from examples.calendargrid import ScrollableCalendar, MonthGrid, DateNode, Options, YearMonthDay

@click.command()
@click.option("--debug", "debug", default=False)
@click.option("--options", "options", default=0x3)
@click.option("--screen", "screen", default=None)
def main(debug, options, screen):
    if not screen:
        termprint(options, debug)
    elif screen.lower() in ["bear", "blt", "b"]:
        main_blt(options, debug)
    else:
        print("incorrect args")


def termprint(options, debug=False):
    c = ScrollableCalendar(YearMonthDay(2018, 10), YearMonthDay(2018, 12))
    print(c.format_print())
    print()
    print(c.format_print(Options.SingleMonth))

def main_blt(options, debug):
    from bearlibterminal import terminal

    terminal.open()
    terminal.set("window.title='Scrollable Calendar Grid'")
    terminal.set("input.filter={keyboard, mouse+}")

    escape_codes = [terminal.TK_Q, terminal.TK_ESCAPE, 224]

    c = ScrollableCalendar(YearMonthDay(2018, 10), YearMonthDay(2018, 11))

    footer_options = ['Add', 'Edit', 'Delete', 'Save']
    footer = '  '.join(f"[color=red]{o[0]}[/color][color=grey]{o[1:]}[/color]" 
                            for o in footer_options)

    if debug:
        print(Options.options(options))

    char = None
    while True:
        terminal.clear()
        terminal.puts(0, 0, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(0, 23, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(1, 23, footer)
        terminal.puts(1, 0, f"[color=black]{'File  Edit  View  Help'}[/color]")
        terminal.puts(11, 2, c.format_blt_header(Options.check(options, Options.ColoredHeader))) # day header
        terminal.puts(1, 2, f"{c.graph[c.j][c.i].year}") # year
        terminal.puts(1, 3, f"{calendar.month_name[c.graph[c.j][c.i].month]}") # month
        terminal.puts(10, 3, c.format_print(Options.SingleMonth, blt=True)) # days
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
            c.select_next_week()
        if char == terminal.TK_UP:
            c.select_prev_week()
        if char == terminal.TK_LEFT:
            c.select_prev_day()
        if char == terminal.TK_RIGHT:
            c.select_next_day()

if __name__ == "__main__":
    main()