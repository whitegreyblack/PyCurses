import curses
import source.utils as utils
from source.utils import initialize_curses_settings
from source.utils import point
from source.mouse import MouseEvent as mouse
from source.button import Button2 as Button, Control

def main(term):
    initialize_curses_settings()
    height, width = term.getmaxyx()

    default = Button()
    default.draw(term, utils.point(0, 0))
    term.getch()

curses.wrapper(main)