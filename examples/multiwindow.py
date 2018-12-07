import curses

def main(screen):
    y, x = screen.getbegyx()
    h, w = screen.getmaxyx()

    screen.border()

    # clearing an area shared by other screens also
    # clears subwin area.
    a = screen.subwin(h - 2, w - 2, y + 1, x + 1 )
    b = screen.subwin(h - 2, w - 2, y + 1, x + 1 )

    a.border()
    a.addstr(1, 1, "a")
    b.addstr(1, 2, 'b')

    screen.getch()
    a.erase()
    a.refresh()
    screen.getch()
    a.erase()
    a.border()
    a.refresh()
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)