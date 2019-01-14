"""BLT components"""

from collections import namedtuple
from source.utils import border

"""Multiple cases:
- p1
    p2
-   p1
  p2
- p2
    p1
-   p1
  p2
- p1 p2
- p2 p1
"""

def slope(p, q):
    y_difference = (q.y - p.y)
    x_difference = (q.x - p.y)
    if y_difference == 0 or x_difference == 0:
        return 0.0
    return y_difference / x_difference

# Calculating box. If two points are in opposite quadrants laying
# in 1 or 3: recalculate so box points lay in 4 and 2; p1=q4, p2=q2
class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x_increment = -1, 1 # don't know yet.
        self.y_increment = -1, 1 # Calculate for x and y
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = self.w = max(x1, x2) - min(x1, x2)
        self.height = self.h = max(y1, y2) - min(y1, y2)
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def width(self):
        return self._w
    @width.setter
    def width(self):
        self._w = value
    @property
    def w(self):
        return self._w
    @w.setter
    def width(self):
        self._w = value
    @property
    def height(self):
        return self._h
    @height.setter
    def height(self, value):
        self._h = value
    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, value):
        self._h = value
    @classmethod
    def from_points(cls, p1, p2):
        """Allows usage of point tuples/namedtuples"""
        return Box(p1.x, p1.y, p2.x, p2.y)
    def points(self):
        return set((x, y) for x in range(self.w) for y in range(self.h))