import curses
from source.controls import Window, View, OptionsBar, OptionsList, Label

def initialize_curses_settings(logger=None):
    """Sets settings for cursor visibility and color pairings"""
    if logger:
        logger.info('main(): initializing curses library settings')
    curses.curs_set(0)
    curses.start_color()
    for i in range(16):
        curses.init_pair(i + 1, 0, 7)
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)

def main(screen):
    initialize_curses_settings()
    height, width = screen.getmaxyx()
    window = Window('Application', width, height)  
    v1 = View(screen.subwin(1, width, 0, 0))
    optbar = OptionsBar(v1.width)
    v1.add_element(optbar)
    file_options = OptionsList(screen, ("longoption", "shortopt"))
    optbar.add_option('File', file_options)
    optbar.add_option('Edit', None)
    optbar.add_option('Select', None)
    optbar.add_option('Help', None)
    window.add_view(v1)

    window.draw(screen)
    c = screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)