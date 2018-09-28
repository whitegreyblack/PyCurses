x, y, h, w = 0, 0, 0, 0

class Window:
    def __init__(self, box):
        self.x, self.y, self.w, self.h = box
        print(self)
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.w}, {self.h}"

    def split(self):
        if self.w <= 5:
            return

        # if not self.left and not self.right:
        #     self.left = Window((self.x, self.y, self.w//2, self.h))
        if not self.right:
            self.right = Window((self.w//2 + self.x, self.y, self.w//2, self.h))

        else:
        # if self.right:
            self.right.split()


    def split_v(self):
        global x, y, h, w
        try:
            if not self.left and not self.right:
                x, y, w, h = dimensions(self.w)
                if w <= 5:
                    return

                self.left = Window(self.w.subwin(h, w // 2, y, x))
                self.right = Window(self.w.subwin(h, w // 2, y, w // 2))
                return

            # if self.left:
            #     self.left.split_v()

            if self.right:
                # raise ValueError(self.right)
                self.right.split_right()
            # if self.right:
            #     self.right.split_v()
        except:
            raise ValueError(x, y, w // 2, h)

if __name__ == "__main__":

    w = Window((0, 0, 80, 24))
    i = input()
    while i != 'q' and i != 'Q':
        w.split()
        i = input()