import curses
w = None
class Window:
    def __init__(self, window):
        self.w = window
        self.w.border()
        self.w.refresh()
        self.left = None
        self.right = None

    def split_v(self):
        self.w.erase()
        y, x = self.w.getbegyx()
        h, w = self.w.getmaxyx()
        self.left = Window(self.w.subwin(h, w // 2, y, x))
        self.right = Window(self.w.subwin(h, w // 2, y, w // 2))

    def clear(self):
        if not self.left and not self.right:
            self.w.clear()
            return

        if self.left:
            self.left.w.clear()

        if self.right:
            self.right.w.clear()

def main(scr):
    global w
    w = Window(scr)
    c = scr.getch()
    while c != ord('q'):
        if c == ord('h'):
            w.split_v()           
        c = scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
    print(w.left.w.getmaxyx())
    print(w.right.w.getmaxyx())