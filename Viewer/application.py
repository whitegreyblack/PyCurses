"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import os
import curses
from controls import Window, ScrollList, Card, ProductForm
from models import Product
from database import Connection
from yamlchecker import YamlChecker
# from keymap import KeyMap

terminal_width, terminal_height = 0, 0

def initialize():
    """Curses related settings"""
    curses.curs_set(0)
    curses.init_pair(1, 
                     curses.COLOR_BLACK, 
                     curses.COLOR_WHITE)
    curses.init_pair(2, 
                     curses.COLOR_BLACK, 
                     curses.COLOR_BLUE | curses.COLOR_GREEN)

def setup_database():
    connection = Connection()
    connection.drop_tables()
    connection.build_tables()
    return connection

def setup_cards():
    return [Card(Product(fruit, price))
            for fruit, price in zip(
                ['Apples', 'Oranges', 'Pears', 'Watermelons', 'Peaches'],
                [3, 5, 888, 24, 55])]

def setup_windows():
    """Create UI components and add to the screen"""
    window = Window('Viewer', terminal_width, terminal_height)

    scroller = ScrollList(1, 1, window.width // 4, window.height, 'Products', selected=True)
    scroller.add_items(setup_cards())
    form = ProductForm((window.width // 4) + 1, # add 1 for offset
                       1,
                       window.width - (window.width // 4) - 1, 
                       window.height,
                       Product('example', 4))
    window.add_windows([scroller, form])

    keymap = dict()
    keymap[(curses.KEY_UP, scroller.wid)] = scroller.wid
    keymap[(curses.KEY_DOWN, scroller.wid)] = scroller.wid
    keymap[(curses.KEY_ENTER, scroller.wid)] = form.wid
    keymap[(curses.KEY_RIGHT, scroller.wid)] = form.wid
    keymap[(curses.KEY_LEFT, form.wid)] = scroller.wid
    keymap[(curses.KEY_F1,)] = 'Reciepts'
    # 10 : New Line Character
    keymap[(10, scroller.wid)] = form.wid
    # 27 : Escape Key Code
    keymap[(27, scroller.wid)] = None
    keymap[(27, form.wid)] = scroller.wid
    keymap[(ord('q'), scroller.wid)] = None
    window.add_keymap(keymap)
    return window

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
    checker = YamlChecker('../testdata/')
    valid_files, _ = checker.files_safe()
    yaml_objs = {
        valid_file: checker.yaml_read(valid_file)
                    for valid_file in valid_files
    }
    connection = setup_database()
    connection.insert_reciepts(yaml_objs)
    window = setup_windows()
    window.draw(screen)
    screen.addstr(0, 0, f"{len(yaml_objs)}")
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
