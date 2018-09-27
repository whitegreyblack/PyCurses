import curses

def main(screen):
    c = screen.getch()
    while c != ord('q'):
        if c == curses.KEY_SHIFT_L:
            screen.addstr('L_SHIFT')
        if c == ord('a'):
            screen.addch('a')
        if c == ord('A'):
            screen.addch('A')
        c = screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)