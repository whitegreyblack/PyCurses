# simple_menu tester for WINDOWS cmd prompt size=80x80
import curses
import manager
import tabs
import signal
import os
import time

bd = None
li = None
titles = ['reciepts', 'random']

def main(main_screen):
    global bd, li
    li = curses.ACS_BOARD
    bd = curses.ACS_CKBOARD

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    y,x = main_screen.getmaxyx()
    main_screen.border()
    m = manager.Manager(main_screen)
    m.toggle_border_on()
    m.toggle_title_on()
    m.add_tabs(titles)
    m.add_wins(titles)
    m.tm.toggle_border_on()
    c = main_screen.getch(0,0)
    curses.endwin()

if __name__=="__main__":
    curses.wrapper(main) 