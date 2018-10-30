import curses
from ctypes import windll, byref, Structure, c_ulong

class Point(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]

def main(t):
    curses.curs_set(0)
    a, b = curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    t.addstr(2, 0, f"a={a}, b={b}")
    
    pt = Point()

    curses.delay_output(100)
    mx, my = 0, 0
    while True:
        # draw
        t.addstr(0, 0, f"x={mx}, y={my}")
        a, mx, my, _, mask = curses.getmouse()

        t.addstr(4, 0, f"x={pt.x}, y={pt.y}")

        # input
        windll.user32.GetCursorPos(byref(pt))
        c = t.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_MOUSE:
            t.addstr(1, 0, "MOUSE")
            a, mx, my, _, mask = curses.getmouse()
if __name__ == "__main__":
    curses.wrapper(main)