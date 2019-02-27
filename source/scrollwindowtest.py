import curses
from source.utils import EventHandler
from source.window import (
    ScrollableWindowWithBar, 
    on_keypress_up, 
    on_keypress_down, 
    on_keypress_a
)

def initialize_curses_settings(logger=None):
    """Sets settings for cursor visibility and color pairings"""
    if logger:
        logger.info('main(): initializing curses library settings')
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

def application(screen):
    events = {
        curses.KEY_UP: EventHandler(),
        curses.KEY_DOWN: EventHandler(),
        ord('a'): EventHandler()
    }
    s = ScrollableWindowWithBar(screen, data=[str(i) for i in range(25)])
    s.keypress_up_event.append(on_keypress_up)
    s.keypress_down_event.append(on_keypress_down)
    s.keypress_a_event.append(on_keypress_a)

    events[curses.KEY_UP].append(s.handle_key)
    events[curses.KEY_DOWN].append(s.handle_key)
    events[ord('a')].append(s.handle_key)

    initialize_curses_settings()

    s.draw()
    while True:
        key = s.window.getch()
        if key in events.keys():
            events[key](key)
        elif key == 27 or key == ord('q'):
            break
        s.erase()
        s.draw()

def main():
    curses.wrapper(application)

if __name__ == "__main__":
    main()