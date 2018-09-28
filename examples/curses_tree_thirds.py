"""Test right window vertical and vertical splitting using curses"""
import curses

class Direction:
    VERTICAL = 0
    HORIZONTAL = 1

def dimensions(screen):
    y, x = screen.getbegyx()
    h, w = screen.getmaxyx()
    return x, y, w, h

class Window:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y , self.w, self. h = dimensions(screen)
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.w}, {self.h}"

    def split_uneven(self, direction):
        pass

    def split(self, direction=Direction.VERTICAL):
        if direction == Direction.VERTICAL and self.w <= 5:
            return

        if direction == Direction.HORIZONTAL and self.h <= 5:
            return

        if not self.right and not self.left:
            if direction == Direction.VERTICAL:
                odd_offset = 0
                if self.w % 2 != 0:
                    odd_offset = 1
                self.left = Window(self.screen.subwin(self.h, 
                                                      self.w//2, 
                                                      self.y, 
                                                      self.x))
                self.right = Window(self.screen.subwin(self.h, 
                                                       self.w//2 + odd_offset, 
                                                       self.y, 
                                                       self.w//2 + self.x))
            else:   
                odd_offset = 0
                if self.h % 2 != 0:
                    odd_offset = 1
                self.left = Window(self.screen.subwin(self.h//2, 
                                                      self.w, 
                                                      self.y, 
                                                      self.x))
                self.right = Window(self.screen.subwin(self.h//2 + odd_offset, 
                                                       self.w, 
                                                       self.h//2 + self.y, 
                                                       self.x))
        else:
            if self.right:
                self.right.split(direction)
            if self.left:
                self.left.split(direction)

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
        if i == ord('v'):
            w.split()
        if i == ord('h'):
            w.split(Direction.HORIZONTAL)
        w.draw()
        i = screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)