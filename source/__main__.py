"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import os
import sys
import click
import curses
from source.controls import (
        Window, ScrollList, Card, RecieptForm, Prompt, Button
        )

from source.models.models import Reciept, Transaction
from source.models.product import Product
from source.database import Connection
from source.yamlchecker import YamlChecker
from collections import namedtuple
import source.utils as utils

terminal_width, terminal_height = 0, 0

def initialize():
    """Sets Curses related settings"""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # color enum num 6 - cyan
    curses.init_pair(2, curses.COLOR_BLACK, 
                     curses.COLOR_BLUE | curses.COLOR_GREEN)

def setup_database(yaml_objs, rebuild=True, logger=None):
    """Builds database connection and calls startup methods"""
    connection = Connection(logger=logger)
    if rebuild:
        connection.drop_tables()
        connection.build_tables()
    connection.insert_files(yaml_objs)
    return connection

def setup_cards(reciept_objs: dict):
    """Builds reciept cards from dictionary of reciept objects"""
    cards = []
    for reciept, products in reciept_objs.items():
        transaction = Transaction(reciept.total, reciept.payment, 
                                  reciept.subtotal, reciept.tax)

        r = Reciept(reciept.store, reciept.date, reciept.category,
                    products, transaction)

        c = Card(r)
        cards.append(c)
    return cards

def setup_test_cards():
    """List of example product cards used in testing"""
    return [Card(Product(fruit, price))
            for fruit, price in zip(
                ['Apples', 'Oranges', 'Pears', 'Watermelons', 'Peaches'],
                [3, 5, 888, 24, 55])]

def setup_windows(reciept_objs, screen):
    """Create UI components and add to the screen"""
    window = Window('Application', terminal_width, terminal_height)


    scroller = ScrollList(1, 1, 
                          window.width // 4, 
                          window.height, 
                          'Reciepts', 
                          selected=True)

    reciept_cards = setup_cards(reciept_objs)
    scroller.add_items(setup_cards(reciept_objs))
    form = RecieptForm((window.width // 4) + 1, # add 1 for offset
                       1,
                       window.width - (window.width // 4) - 1, 
                       window.height,
                       scroller.model)
    
    subwin = screen.subwin(window.height // 3, 
                           window.width // 2, 
                           window.height // 3,
                           window.width // 4)

    exitprompt = Prompt(subwin, 'Exit Prompt', 'Confirm', None)

    window.add_windows([scroller, form, exitprompt])

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
    keymap[(27, scroller.wid)] =  exitprompt.wid
    keymap[(27, exitprompt.wid)] = None
    keymap[(27, form.wid)] = scroller.wid
    keymap[(ord('q'), scroller.wid)] = None
    keymap[(curses.KEY_ENTER, exitprompt.wid)] = None
    window.add_keymap(keymap)
    return window

def application(screen, folderpath):
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

    fields = 'filename store date category subtotal tax total payment'
    reciepttuple = namedtuple('Reciept', fields)

    logger = utils.setup_logger('applicationlogger',
                                'app.log',
                                extra={'currentfile': __file__})

    logger.info('main(): initializing curses library settings')
    initialize()
    logger.info('main(): done')

    checker = YamlChecker(folderpath, logger)
    valid_files, other_files = checker.files_safe()
    
    yaml_objs = {
        valid_file: checker.yaml_read(valid_file)
            for valid_file in valid_files
    }
    
    connection = setup_database(yaml_objs, logger=logger)
    reciepts = [reciepttuple(*r) for r in list(connection.select_reciepts())]

    logger.info(f"main(): Reciepts: {reciepts}")

    reciept_objs = {
        reciept: connection.select_reciept_products(reciept.filename)
            for reciept in list(reciepts)
    }
    logger.info(f"main(): Number of reciepts: {len(reciept_objs)}")
    logger.info(f"main(): Reciept object keys: {reciept_objs.keys()}")

    window = setup_windows(reciept_objs, screen)
    window.draw(screen)

    while 1:
        key = screen.getch()
        retval = window.send_signal(key)
        if not retval:
            break
        screen.erase()
        window.draw(screen)

@click.command()
@click.option('-f', help="Folder containing yaml data files")
def main(f):
    if not f:
        print("no data folder specified")
        print(usage())
        return

    if f == '.':
        print("Invalid folder specified: cannot use dot")
        return

    filepath = utils.format_directory_path(f)
    if not utils.check_directory_path(filepath):
        print("Folder argument is not a directory")

    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(application, f)

def usage():
    return("Usage: python -m source -f [args]")

if __name__ == "__main__":
    main()
