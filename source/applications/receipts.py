# application

""" Main class that builds all other objects and runs the curses loop """

import curses
import datetime
import logging
import math
import os
import random

import cerberus
import yaml

import source.config as config
import source.utils as utils
from source.controllers import (ExplorerController, NotesController,
                                PersonController, ReceiptController)
from source.database import Connection, NoteConnection, ReceiptConnection
from source.keymap import EventMap
from source.logger import Loggable
from source.models.models import (Receipt, Task, Text, Transaction, Label, 
                                  LabelList)
from source.models.product import Product
from source.schema import (SQLType, Table, build_products_table,
                           build_receipts_table)
from source.window import (DisplayWindow, PromptWindow, ScrollableWindow, 
                           ListWindow, Window, WindowProperty, keypress_down, 
                           keypress_up)
from source.yamlchecker import YamlChecker
from source.YamlObjects import Receipt as Yamlreceipt
from source.applications.application import Application
from source.window.property import WindowProperty


class ReceiptApplication(Application):

    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()
        print('----------', height, width)
        # main window
        self.window = Window(screen, title='Application Example 1')

        # first window half screen vertical
        sub1 = ListWindow(
            screen.subwin(
                height - 1,
                utils.partition(width, 2, 1),
                0, 
                0
            ),
            title="Sub-win 1",
            data=[
                "label 1", 
                "label 2", 
                "label 3" 
            ],
            properties=WindowProperty(
                focused=True, 
                showing=True, 
                border=True
            )
        )

        # second window quarter screen top right
        sub2 = DisplayWindow(
            screen.subwin(
                utils.partition(height-1, 2, 1, math.ceil),
                utils.partition(width, 2, 1), 
                0,
                utils.partition(width, 2, 1), 
            ),
            title="Sub-win 2",
            dataobj=Text.random()
        )
        print(utils.partition(height-1, 2, 1, math.ceil),sub2.height)

        sub3 = DisplayWindow(
            screen.subwin(
                utils.partition(height-1, 2, 1),
                utils.partition(width, 2, 1), 
                utils.partition(height-1, 2, 1, math.ceil),
                utils.partition(width, 2, 1), 
            ),
            title="Sub-win 3",
            dataobj=Text.random()
        )
        print(sub3.height)
        print(sub2.height + sub3.height + 4)
        
        # Handlers need windows to be built before adding them.
        # Could use string names and methods which get called
        # by getattr instead so that handlers can be created
        # during object creation

        # win 1 handlers
        sub1.add_handler(27, self.keypress_escape)
        sub1.add_handlers(
            9,
            sub1.unfocus,
            sub2.focus,
            self.on_focus_changed
        )
        sub1.add_handlers(
            351,
            sub1.unfocus,
            sub3.focus,
            self.on_focus_changed
        )

        # window 2 handlers
        sub2.add_handler(27, self.keypress_escape)
        sub2.add_handlers(
            351, 
            sub2.unfocus,
            sub1.focus,
            self.on_focus_changed
        )
        sub2.add_handlers(
            9,
            sub2.unfocus,
            sub3.focus,
            self.on_focus_changed
        )

        # window 3 handlers
        sub3.add_handler(27, self.keypress_escape)
        sub3.add_handlers(
            351, 
            sub3.unfocus,
            sub2.focus,
            self.on_focus_changed
        )
        print('adding handlerrs for subwin3')
        sub3.add_handlers(
            9,
            sub3.unfocus,
            sub1.focus,
            self.on_focus_changed
        )
        print('adding window')
        self.window.add_windows(sub1, sub2, sub3)
        self.on_focus_changed(self)

def main(screen):    
    a = RecieptApplication('./receipts/', screen)
    a.setup()
    a.build_windows()
    a.run()
    for table in a.database.tables:
        print(table)

if __name__ == "__main__":
    curses.wrap(main)

