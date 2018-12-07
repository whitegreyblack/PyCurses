class Box:
    TLC = "\u250C"
    HBR = "\u2500"
    VBR = "\u2502"
    TBR = "\u252C"
    TRC = "\u2510"
    BRC = "\u2518"
    BLC = "\u2514"

    def __init__(self, p, width, height, parent):
        self.a = p
        self.b = point(p.x + width - 1, p.y + height - 1)
        self.p = parent
        self.l, self.r = None, None

    @property
    def width(self):
        return self.b.x - self.a.x + 1

    @property
    def height(self):
        return self.b.y - self.a.y + 1

    @property
    def split(self):
        return self.l and self.r

    def join(self, cls=None):
        self.l, self.r = None, None

    def split_x(self, cls=None):
        x = self.width
        lx = rx = x // 2
        rx += (x % 2 == 1)
        c = point(self.a.x + lx, self.a.y)
        if not cls:
            cls = self.__class__
        self.l = cls(self.a, lx, self.height, self)
        self.r = cls(c, rx, self.height, self)

    def split_y(self, cls=None):
        y = self.height
        ly = ry = y // 2
        ry += (y % 2 == 1)
        c = point(self.a.x, self.a.y + ly)
        if not cls:
            cls = self.__class__
        self.l = cls(self.a, self.width, ly, self)
        self.r = cls(c, self.width, ry, self)

    def format_border(self):
        chmap = [[" " for _ in range(self.width)] 
                    for _ in range(self.height)]

        for y in (0, self.height - 1):
            for x in range(self.width):
                chmap[y][x] = self.HBR
        
        for x in (0, self.width - 1):
            for y in range(self.height):
                chmap[y][x] = self.VBR 

        coords = [
            (0, 0), 
            (0, self.height - 1), 
            (self.width - 1, self.height - 1), 
            (self.width - 1, 0)
        ]

        corners = [
            self.TLC, 
            self.BLC, 
            self.BRC, 
            self.TRC
        ]

        for (x, y), ch in zip(coords, corners):
            chmap[y][x] = ch

        return "\n".join("".join(row) for row in chmap)
    def blt_border(self):
        boxes = []
        for box in (self.l, self.r):
            if box:
                boxes.append(box.blt_border())
        if boxes:
            return list(chain.from_iterable(boxes))
        return [(self.a.x, self.a.y, self.format_border())]

def BoxTree:
    def __init__(self):
        self.root = None
        self.current = None

    def add_box(self, box):
        if not self.root:
            self.current = self.root = box
    
    def split_x(self):
        if not self.root:
            

    def boxleaves(self):
        """
        Get all boxes at the bottom of the tree
        """

    def left(self):
        return self.root.l
    
    def right(self):
        return self.root.l