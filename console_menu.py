# simple_menu tester for WINDOWS cmd prompt size=80x80
import os
import tabs
import time
import curses
import signal
import manager
import background as bg

titles = ['reciepts', 'random']

def main(main_screen):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
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
    c = main_screen.getch(0,0)
    while c != ord('q'):
        if c in hkeys.keys():
            m.scroll(hkeys[c])
        '''
        if char in keys.keys() or char in hkeys.keys():
            if char in keys.keys():
                newpos = pos+keys[char]
                if newpos < 0:
                    newpos = tm.count-1
                if newpos > tm.count-1:
                    newpos = 0
            elif char in hkeys.keys():
                newpos = hkeys[char]
            tm.update(pos,newpos)
            pos = newpos
        elif char in vkeys:
            if char == vkeys[0]:
                tm.active.child.datahead.scroll_dn()
                #tm.active.child.refresh(tm.active.child.datapos, -1)
                tm.active.child.toggle_on()
            if char == vkeys[1]:
                tm.active.child.datahead.scroll_up()
                #tm.active.child.refresh(tm.active.child.datapos, 1)
                tm.active.child.toggle_on()
        char = mainscreen.getch()
        
        c = main_screen.getch()
        '''
        c = main_screen.getch()

    curses.endwin()

if __name__=="__main__":
    curses.wrapper(main) 
