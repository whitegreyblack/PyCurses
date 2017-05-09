#  background.py
import curses

curses.initscr()
curses.start_color()
bd = curses.ACS_BOARD
li = curses.ACS_CKBOARD
re = curses.A_REVERSE
curses.endwin()