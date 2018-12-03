"""
File: storyboardtest.py
Tests the storyboard application with mock data
"""

import click
from examples.storyboard import Board, DataFormat

@click.command()
@click.option("--debug", "debug", is_flag=True)
@click.option("--screen", "screen", default=None)
@click.option("--options", "options", default=0x0)
def main(debug, screen, options):
    if not screen:
        termprint(debug)
    elif screen == "bear" or screen == "b":
        main_blt(options)
    else:
        print("incorrect args")

def termprint(debug):
    b = Board()
    print(b.board)
    b.import_using(DataFormat.JSON, "data/storyboard.json")
    b.import_using(DataFormat.JSON, "data/storyboard2.json")
    print(b.board)
    print(b.stories)

def main_blt(options):
    from bearlibterminal import terminal as t
    escape_codes = [t.TK_Q, t.TK_ESCAPE, 224]
    t.open()
    t.set("window.title='Storyboard'")
    t.set("input.filter={keyboard, mouse+}")
    b = Board(options)
    b.import_using(DataFormat.JSON, "data/storyboard.json")
    b.import_using(DataFormat.JSON, "data/storyboard2.json")
    t.puts(0, 1, b.board)

    footer_options = ['Add', 'Edit', 'Delete', 'Save']
    footer = '  '.join(f"[color=red]{o[0]}[/color][color=grey]{o[1:]}[/color]" 
                            for o in footer_options)
    t.puts(0, 0, f"[bkcolor=grey]{' '*80}[/bkcolor]")
    t.puts(0, 24, f"[bkcolor=white]{' '*80}[/bkcolor]")
    t.puts(1, 24, footer)
    t.puts(1, 0, f"[color=white]{'File  Edit  View  Help'}[/color]")

    t.refresh()
    char = None
    while True:
        char = t.read()
        if char in escape_codes:
            break

if __name__ == "__main__":
    main()