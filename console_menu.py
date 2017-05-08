# simple_menu tester for WINDOWS cmd prompt size=80x80
import curses
import tabsmanager
import tabs

bd = None
li = None
titles = ['reciept']
def main(main_screen):
    global bd, li
    li = curses.ACS_BOARD
    bd = curses.ACS_CKBOARD

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    y,x = main_screen.getmaxyx()
    if y < 80 | x < 80:
        curses.resize_term(80,80)

    main_screen.border()
    tm = tabsmanager.TabsManager(main_screen)
    tm.toggle_border_on()
    tm.toggle_title_on()
    c = main_screen.getch(0,0)
    curses.endwin()

if __name__=="__main__":
    curses.wrapper(main) 