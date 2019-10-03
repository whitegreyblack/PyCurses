# intersections.py

def intersect(*rects):
    intersections = set()
    rects = list(rects)
    for rect in rects:
        for other in rects:
            if rect == other:
                continue
            if (rect.x1 < other.x2 and 
                rect.x2 > other.x1 and 
                rect.y1 < other.y2 and 
                rect.y2 > other.y1):
                if (rect, other) not in intersections:
                    intersections.add((rect, other))
    return intersections

class Rect:
    rect_id = 0
    def __init__(self, x, y, width, height): 
        self.rid = Rect.rect_id
        Rect.rect_id += 1
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
    def __repr__(self):
        return f"Rect({self.rid})"

if __name__ == "__main__":
    pairs = intersect(Rect(0, 0, 10, 10),
                      Rect(10, 10, 10, 10),
                      Rect(5, 5, 10, 10))
    for p, q in pairs:
        print(p, q)

