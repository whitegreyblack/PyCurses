import curses

class MouseEvent:
    """Wrapper class for curses.getmouse() events"""
    _curses_events = {
        # listing all known events that are used in application
        4: "LEFT_MOUSE_SINGLE_CLICK",
        8: "LEFT_MOUSE_DOUBLE_CLICK",
        4096: "RIGHT_MOUSE_SINGLE_CLICK",
        8192: "RIGHT_MOUSE_DOUBLE_CLICK",
    }

    NONE = 0
    CLICK = 1
    SCROLLUP = 1

    @staticmethod
    def last_action(self):
        return curses.getmouse()