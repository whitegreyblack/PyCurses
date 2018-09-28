"""Test right window vertical and vertical splitting coordinates"""
class Direction:
    VERTICAL = 0
    HORIZONTAL = 1

class Window:
    def __init__(self, box):
        self.x, self.y, self.w, self.h = box
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.w}, {self.h}"

    def split(self, direction=Direction.VERTICAL):
        if direction == Direction.VERTICAL and self.w <= 5:
            return

        if direction == Direction.HORIZONTAL and self.h <= 5:
            return

        if not self.right:
            if direction == Direction.VERTICAL:
                self.right = Window((self.w//2 + self.x, self.y, self.w//2, self.h))
            else:
                self.right = Window((self.x, self.h//2 + self.y, self.w, self.h//2))
            print(self.right)
        else:
            self.right.split()

if __name__ == "__main__":
    w = Window((0, 0, 80, 24))
    print(w)
    i = input()
    while i != 'q' and i != 'Q':
        if i == 'h':
            w.split(Direction.HORIZONTAL)
        else:
            w.split()
        i = input()