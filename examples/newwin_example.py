# newwin_example.py

import curses

def main(screen):
    curses.curs_set(0)
    width, height = curses.COLS, curses.LINES
    win1 = curses.newwin(height//2, width//2, 0, 0)
    win2 = curses.newwin(height//2-1, width//2-1, height//2-1, width//2-1)
    # win2.border()
    # win2.addch(win2.getch())
    i = 0
    while True:
        win1.border()
        win1.addstr(1, 1, str(i%10))
        win2.border()
        i += 1
        screen.refresh()
        win1.refresh()
        win2.refresh()
        if win1.getch() == 27:
            break

    # win2.refresh()
    # screen.refresh()
    # screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)
