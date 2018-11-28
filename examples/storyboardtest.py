"""Storyboard Test

Tests the storyboard application with mock data
"""
import click
from examples.storyboard import Board, DataFormat

@click.command()
@click.option("--debug", "debug", is_flag=True)
@click.option("--screen", "screen", default=None)
def main(debug, screen):
    if not screen:
        termprint(debug)
    elif screen == "curses" or screen == "c":
        main_curses()
    elif screen == "bear" or screen == "b":
        main_blt()
    else:
        print("incorrect args")

def termprint(debug):
    b = Board()
    print(b.board)
    b.import_using(DataFormat.JSON, "examples/storyboard.json")
    b.import_using(DataFormat.JSON, "examples/storyboard2.json")

def main_curses():
    def wrapped(t):
        t.getch()

    import curses
    curses.wrapper(wrapped)

def main_blt():
    from bearlibterminal import terminal as t
    escape_codes = [t.TK_Q, t.TK_ESCAPE, 224]
    t.open()
    t.set("window.title='Storyboard'")
    t.set("input.filter={keyboard, mouse+}")
    t.refresh()
    char = None
    while True:
        char = t.read()
        if char in escape_codes:
            break

if __name__ == "__main__":
    main()