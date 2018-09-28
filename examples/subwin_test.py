import curses

def initialize_curses_settings():
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)

def main(scr):
    initialize_curses_settings()

    subwin = scr.subwin(5, 5, 10, 10)

    scr.border()
    subwin.bkgd(' ', curses.color_pair(2))
    subwin.border()
    scr.getch()
    subwin.bkgd(' ', curses.color_pair(1))
    subwin.erase()
    subwin.refresh()
    # scr.erase()
    # scr.border()
    scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)