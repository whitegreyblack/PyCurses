#!/usr/env/bin python3
"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import curses
from Views import WindowView
from Views.ViewCard import ViewCard
from Models.product import Product
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
    window = WindowView.Window('Reciepts',
                               terminal_width,
                               terminal_height)

    window.add_window(Card(Product('example')))
    
    window.draw(screen)
    screen.getch()
if __name__ == "__main__":
    curses.wrapper(main)
