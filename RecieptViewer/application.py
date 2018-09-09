#!/usr/env/bin python3
"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import curses
from controls import Window, ScrollList, Card
from models import Product

def main(screen):
    """
    Overview:

    Take files from Yaml folder 'Reciepts' and pass it into the yaml
    parser and then the database.

    Then we build the main screen using the curses views files.

    Finally we bring in the data from db into the models to view onto the
    screen
    """
    terminal_width = curses.COLS
    terminal_height = curses.LINES
    curses.curs_set(0)

    window = Window('Reciepts',
                    terminal_width,
                    terminal_height)

    product1 = Product('example1')
    product2 = Product('example2')
    scroller = ScrollList(1, 1, 16, terminal_height - 2)
    card1 = Card(product1)
    card2 = Card(product2)
    scroller.add_item(card1)
    scroller.add_item(card2)
    window.add_window(scroller)
    
    window.draw(screen)
    screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)
