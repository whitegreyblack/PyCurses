#  background.py
import curses

curses.initscr()
curses.start_color()
bd = curses.ACS_CKBOARD
li = curses.ACS_CKBOARD
re = curses.A_REVERSE
curses.endwin()