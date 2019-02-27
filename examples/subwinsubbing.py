import curses

def main(scr):
    subwin = scr.subwin(22, 78, 1, 1)
    subwinsubwin = subwin.subwin(20, 76, 2, 2)

    scr.border()
    subwin.border()
    subwinsubwin.border()

    scr.refresh()

    scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)