import curses.ascii

def main(scr):
    for i in range(20):
        for j in range(15):
            scr.addch(j, i, curses.ascii.alt(i * j))
    scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
