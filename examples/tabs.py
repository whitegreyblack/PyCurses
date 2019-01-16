# simple_menu tester for WINDOWS cmd prompt size=80x80
import os
import tabs
import time
import curses
import signal
import manager
import background as bg

titles = ['receipts', 'random']

def initialize_curses_settings():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

def main(main_screen):
    initialize_curses_settings()

    # bind keyboard keys
    hkeys = {
        curses.KEY_LEFT: -1, 
        curses.KEY_RIGHT: 1,
        }
    vkeys = {
        curses.KEY_UP: -1, 
        curses.KEY_DOWN: 1
    }

    # basic setup
    y,x = main_screen.getmaxyx()
    main_screen.border()
    m = manager.Manager(main_screen)
    m.toggle_border_on()
    m.toggle_title_on()
    m.add_tabs(titles)
    m.add_wins(titles)
    m.toggle_border_on()
    m.toggle_title_on()
    m.toggle_tabs_name()
    m.toggle_tabs_border_inactive(bg.bd)
    m.toggle_tab_border_active(bg.li)
    m.toggle_win_border_active(bg.li)

    #m.load_data()
    
    # main loop
    c = main_screen.getch(0,0)
    while c != ord('q') and c != 27:
        if c in hkeys.keys():
            m.scroll(hkeys[c])
        c = main_screen.getch()

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main) 
