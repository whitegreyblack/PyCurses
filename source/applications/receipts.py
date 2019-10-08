# application

""" Main class that builds all other objects and runs the curses loop """

import curses
import datetime
import logging
import os
import random
from math import ceil

import cerberus
import yaml

import source.config as config
from source.applications.application import Application
from source.controllers import (ExplorerController, NotesController,
                                PersonController, ReceiptController)
from source.database import Connection, NoteConnection, ReceiptConnection
from source.keymap import EventMap
from source.logger import Loggable
from source.models.models import (Label, LabelList, Receipt, Task, Text,
                                  Transaction)
from source.models.product import Product
from source.schema import (SQLType, Table, build_products_table,
                           build_receipts_table)
from source.utils import partition
from source.window import (DisplayWindow, ListWindow, PromptWindow,
                           ScrollableWindow, Window, WindowProperty,
                           keypress_down, keypress_up)
from source.window.property import WindowProperty
from source.yamlchecker import YamlChecker
from source.YamlObjects import Receipt as Yamlreceipt


class ReceiptApplication(Application):

    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        height, width = self.term.getmaxyx()
        # main window
        self.window = Window(
            self.term, 
            title='Application Example 1', 
            properties=WindowProperty(focusable=False, border=False),
            keymap={
                27: 'close'
            },
            windows=[
                # first window half screen vertical
                ListWindow(
                    self.term.subwin(height - 2, partition(width, 2), 1, 0),
                    title="Sub-win 1",
                    data=[
                        "label 1",
                        "label 2",
                        "label 3"
                    ],
                    properties=WindowProperty(),
                    keymap={
                        27: 'close',
                        9: 'unfocus',
                        351: 'unfocus',
                    }
                ),
                # second window quarter screen top right
                DisplayWindow(
                    self.term.subwin(
                        partition(height-2, 2, op=ceil),
                        partition(width, 2), 
                        1,
                        partition(width, 2), 
                    ),
                    title="Sub-win 2",
                    dataobj=Text.random(),
                    properties=WindowProperty(),
                    keymap={
                        27: 'close',
                        9: 'unfocus',
                        351: 'unfocus',
                    }
                ),
                # third window quarter screen bottom left
                DisplayWindow(
                    self.term.subwin(
                        partition(height-1, 2),
                        partition(width, 2),
                        partition(height-1, 2, op=ceil),
                        partition(width, 2), 
                    ),
                    title="Sub-win 3",
                    dataobj=Text.random(),
                    properties=WindowProperty(),
                    keymap={
                        27: 'close',
                        9: 'unfocus',
                        351: 'unfocus',
                    }
                )
            ]
        )
            
        # # Handlers need windows to be built before adding them.
        # # Could use string names and methods which get called
        # # by getattr instead so that handlers can be created
        # # during object creation
        # self.on_focus_changed(self)

def main(screen):    
    a = RecieptApplication('./receipts/', screen)
    a.setup()
    a.build_windows()
    a.run()
    for table in a.database.tables:
        print(table)

if __name__ == "__main__":
    curses.wrap(main)
