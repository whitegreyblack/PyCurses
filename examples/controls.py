import curses
from source.controls import MainWindow, View

v = None
def main(screen):
    global v
    x, y = screen.getbegyx() # start x, y
    h, w = screen.getmaxyx() # full height, width
    subwin = screen.subwin(h - 1, w - 1, y + 1, x + 1)
    v = View(screen)
    v.screen.border()
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)
    print(v.x1, v.y1, v.x2, v.y2, v.w, v.h)