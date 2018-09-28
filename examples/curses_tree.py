import curses
win = None
x, y, h, w = 0, 0, 0, 0

def dimensions(screen):
    y, x = screen.getbegyx()
    h, w = screen.getmaxyx()
    return x, y, w, h

class Window:
    def __init__(self, screen):
        # self.x, self.y, self.w, self.h = box
        self.screen = screen
        self.x, self.y , self.w, self. h = dimensions(screen)
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.w}, {self.h}"

    def split(self):
        if self.w <= 5:
            return

        if not self.right and not self.left:
            odd_offset = 0
            if self.w % 2 != 0:
                odd_offset = 1
            self.left = Window(self.screen.subwin(self.h, self.w//2, self.y, self.x))
            self.right = Window(self.screen.subwin(self.h, self.w//2 + odd_offset, self.y, self.w//2 + self.x))

        else:
            self.right.split()
            self.left.split()

    def draw(self):
        self.screen.border()
        if self.right:
            self.right.draw()
        if self.left:
            self.left.draw()

def main(screen):
    w = Window(screen)
    w.draw()
    i = screen.getch()
    while i != ord('q'):
        w.split()
        w.draw()
        i = screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)