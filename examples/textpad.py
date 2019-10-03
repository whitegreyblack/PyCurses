# textpad.py

import curses
import curses.textpad

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    win = curses.newwin(5, 100, 5, 15)
    win.addstr(0, 0, "asdf")

    tb = curses.textpad.Textbox(win, insert_mode=True)
    tb.stripspaces = True
    text = tb.edit()
    curses.flash()
    win.clear()
    has_newline = '\n' in text
    print(text, repr(text), text.split('\n'))
    for y, string in enumerate(text.split('\n')):
        print(string.strip())
        win.addstr(y, 0, string.strip())
    win.refresh()
    win.getch()

curses.wrapper(main)
