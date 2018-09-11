"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import os
import curses
from controls import Window, ScrollList, Card, ProductForm
from models import Product
# from keymap import KeyMap

terminal_width, terminal_height = 0, 0

def initialize():
    """Curses related settings"""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

def setup_windows():
    """Create UI components and add to the screen"""
    window = Window('Viewer', terminal_width, terminal_height)

    card1 = Card(Product('Leevers  $2.31'))
    card2 = Card(Product('example2'))
    scroller = ScrollList(1, 1, window.width // 4, window.height, 'Reciepts', selected=True)
    scroller.add_items([card1, card2])
    form = ProductForm((window.width // 4) + 1, # add 1 for offset
                       1,
                       window.width - (window.width // 4) - 1, 
                       window.height,
                       Product('example'))
    window.add_windows([scroller, form])

    keymap = dict()
    keymap[(curses.KEY_UP, scroller.wid)] = scroller.wid
    keymap[(curses.KEY_DOWN, scroller.wid)] = scroller.wid
    keymap[(curses.KEY_ENTER, scroller.wid)] = form.wid
    # 10 : New Line Character
    keymap[(10, scroller.wid)] = form.wid
    # 27 : Escape Key Code
    keymap[(27, scroller.wid)] = None
    keymap[(27, form.wid)] = scroller.wid
    keymap[(ord('q'), scroller.wid)] = None
    window.add_keymap(keymap)
    return window

def input_handler(screen):
    screen.getch()

def main(screen):
    """
    Overview:

    Take files from Yaml folder 'Reciepts' and pass it into the yaml
    parser and then the database.

    Then we build the main screen using the curses views files.

    Finally we bring in the data from db into the models to view onto the
    screen
    """
    global terminal_width, terminal_height
    terminal_width = curses.COLS
    terminal_height = curses.LINES

    initialize()
    window = setup_windows()
    window.draw(screen)
    while 1:
        key = screen.getch()
        retval = window.send_signal(key)
        if not retval:
            break
        screen.erase()
        window.draw(screen)

if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
    curses.endwin()
