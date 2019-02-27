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
    elif screen.lower() in ("bear", "blt", "b"):
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

    c = ScrollableCalendar(YearMonthDay(2018, 7), YearMonthDay(2019, 8))

    footer_options = ['Add', 'Edit', 'Delete', 'Save', 'Import', 'Export']
    footer = '  '.join(f"[color=orange]{o[0]}[/color][color=grey]{o[1:]}[/color]" 
                            for o in footer_options)

    if debug:
        print(Options.options(options))

    char = None
    while True:
        terminal.clear()

        monthstring = c.format_print(Options.SingleMonth, blt=True)

        # add borders between calendar, events, and form
        for y in range(24):
            terminal.puts(39, y, "[bkcolor=grey] [/bkcolor]")
        for x in range(40):
            terminal.puts(x, 4 + len(monthstring.split('\n')), "[bkcolor=grey] [/bkcolor]")
        
        # box characters
        terminal.puts(1, 0, "\u250C") # top left corner
        terminal.puts(0, 1, "\u2500" * 80) # horizontal line, top screen
        terminal.puts(0, 23, "\u2500" * 80) # horizontal line, bottom screen
        for y in range(1, 23):
            terminal.puts(79, y, "\u2502") # vertical bar, right screen
        terminal.puts(39, 1, "\u252C") # T bar 
        terminal.puts(79, 1, "\u2510") # top right corner
        terminal.puts(79, 23, "\u2518") # bottom right corner

        # form fields
        terminal.puts(41, 2, "Add Event Form")
        terminal.puts(41, 5, f"Title       [bkcolor=grey]{' '*26}[/bkcolor]")
        terminal.puts(41, 8, f"Start Date  [bkcolor=grey]{' '*26}[/bkcolor]")
        terminal.puts(41, 11, f"End Date    [bkcolor=grey]{' '*26}[/bkcolor]")
        terminal.puts(41, 14, f"Description [bkcolor=grey] ADF{' '*22}[/bkcolor]")
        terminal.puts(41, 17, f"Category    [bkcolor=grey]{' '*26}[/bkcolor]")
        
        # button placements
        terminal.puts(50, 20, "[bkcolor=grey]Save[/bkcolor]")
        terminal.puts(65, 20, "[bkcolor=grey]Cancel[/bkcolor]")

        # header buttons
        terminal.puts(0, 0, f"[bkcolor=white]{' '*80}[/bkcolor]")
        terminal.puts(1, 0, f"[color=black]{'File  Edit  View  Help'}[/color]")

        # footer buttons
        terminal.puts(0, 24, f"[bkcolor=white]{' '*80}[/bkcolor]")        
        terminal.puts(1, 24, footer)

        # col 1
        terminal.puts(1, 2, f"{c.graph[c.j][c.i].year}") # year
        terminal.puts(1, 3, f"{calendar.month_name[c.graph[c.j][c.i].month]}") # month

        # col 2
        terminal.puts(11, 2, c.format_blt_header(Options.check(options, Options.ColoredHeader))) # day header
        terminal.puts(10, 3, c.format_print(Options.SingleMonth, blt=True)) # days

        # event window/fields
        events = None
        if events:
            terminal.puts(30, 2, "Events:")
            terminal.puts(30, 3, "\n".join(events))
        if char:
            terminal.puts(0, 23, str(char))

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