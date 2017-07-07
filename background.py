#  background.py
import curses

curses.initscr()
curses.start_color()
bd = curses.ACS_BOARD
li = curses.ACS_CKBOARD
re = curses.A_REVERSE
bl = curses.ACS_BULLET
dg = curses.ACS_DEGREE
di = curses.ACS_DIAMOND
vl = curses.ACS_VLINE
hl = curses.ACS_HLINE
curses.endwin()
