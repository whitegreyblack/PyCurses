#!/usr/env/bin python3
"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import curses
from Views import WindowView
from Views.ViewCard import ViewCard
from Models.product import Product
def main():
    """
    Overview:

    Take files from Yaml folder 'Reciepts' and pass it into the yaml
    parser and then the database.

    Then we build the main screen using the curses views files.

    Finally we bring in the data from db into the models to view onto the
    screen
    """
    WindowView.cards = [ViewCard(Product("example")),
                        ViewCard(Product("asdfa"))]
    curses.wrapper(WindowView.main)

if __name__ == "__main__":
    main()
