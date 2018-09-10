"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import curses
from controls import Window, ScrollList, Card, ProductForm
from models import Product

terminal_width, terminal_height = 0, 0

def initialize():
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    return curses.COLS, curses.LINES

def setup_windows():
    window = Window('Viewer',
                    terminal_width,
                    terminal_height)

    product1 = Product('example1')
    product2 = Product('example2')
    scroller = ScrollList(1, 1, 16, terminal_height - 2, 'Reciepts', True)
    card1 = Card(product1)
    card2 = Card(product2)
    scroller.add_item(card1)
    scroller.add_item(card2)
    window.add_window(scroller) 

    window.add_window(ProductForm(17,
                                  1, 
                                  terminal_width - 2 - 17,
                                  terminal_height - 2,
                                  Product('example')))
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
        if key == 27 or key == ord('q'):
            break
        elif key == curses.KEY_DOWN or key == curses.KEY_UP:
            window.send_signal(key) 
        screen.erase()
        window.draw(screen)

if __name__ == "__main__":
    curses.wrapper(main)
