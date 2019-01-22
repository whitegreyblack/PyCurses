"""Application.py: 
Main class that builds all other objects and runs the curses loop
"""
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
from source.models.models import Receipt, Task, Text, Transaction
from source.models.product import Product
from source.schema import (SQLType, Table, build_products_table,
                           build_receipts_table)
from source.window import (DisplayWindow, PromptWindow, ScrollableWindow,
                           Window, WindowProperty, keypress_down, keypress_up)
from source.yamlchecker import YamlChecker
from source.YamlObjects import receipt as Yamlreceipt


class Application(Loggable):
    """
    Builds the initial parent window using the initial curses screen passed in
    during initialization.

    Also saves export folder paths for data exporting.

    During build functions, creates window objects for the view, controller
    objects to retrieve data after requests are sent in, and moves model data
    into the correct window object.

    Then the application is looped to draw the views onto the screen using 
    curses framework.

    Handles two way data exchanges between windows if data needs transformation
    before reaching destination window from source window.
    """
    def __init__(self, folder, screen=None, logger=None):
        print(self.__class__.__name__)
        super().__init__(self, logger=logger)

        self.continue_app = True
        
        self.screen = screen
        self.window = Window(
            screen, 
            eventmap=EventMap.fromkeys((
                27,         # escape key
                113,        # letter q
                81          # letter Q
            ))
        )
        self.focused = self.window
        self.last_focused = None
        self.folder = folder
        self.export = "./export/"

        self.controller = None

        self.on_data_changed = utils.Event()
        self.on_data_added = utils.Event()

    def setup(self):
        # TODO: need a setting to determine behavior of previously loaded data
        # TODO: need a way to format paths before creating other objects
        self.formatted_import_paths = None
        self.formatted_export_path = None
        self.setup_database()

    def setup_database(self):
        self.database.rebuild_tables()
        inserted = self.database.previously_inserted_files()

        files = self.check_files(skip=inserted)
        yobjs = self.load_files(files)
        # self.checker.verify_file_states(loaded_files=inserted)
        # files = self.checker.verified_files

        self.database.insert_files(yobjs)
        self.log(f"Committed:")
        for commit in files:
            self.log(f"+ {commit}")

    def check_files(self, skip=None):
        filestates = []
        if not self.folder:
            return filestates
        for _, _, files in os.walk(self.folder):
            self.log(f"Validating {len(files)} files")
            
            for file_name in files:
                if skip and file_name in skip:
                    continue
                filename, extension = utils.filename_and_extension(file_name)
                self.check_file_name(filename)
                self.check_file_data(file_name)
                filestates.append(file_name)
        return filestates

    def check_file_name(self, filename):
        schema = {
            'filename': {
                'type': 'string', 
                'regex': config.YAML_FILE_NAME_REGEX
            }
        }
        v = cerberus.Validator(schema)
        if not v.validate({'filename': filename}):
            raise BaseException(f'Yaml Filename {filename} is invalid')

    def check_file_data(self, filename):
        v = utils.validate_from_path(
            self.folder + filename,
            './data/schema.yaml'
        )
        if not v:
            raise BaseException(f"File data for {filename} invalid")

    def load_files(self, files):
        yobjs = {}
        for f in files:
            with open(self.folder + f, 'r') as o:
                yobjs[f] = yaml.load(o.read())
        return yobjs

    def run(self):
        while self.continue_app:
            key = self.screen.getch()
            print(f"focused:{self.focused} | keypress map:{self.focused.keypresses}")
            if key in self.focused.keypresses.keys():
                self.focused.handle_key(key)
                # self.focused.eventmap[key]()
            # if key in self.keymap.keys():
            #     if self.keymap[key] == None:
            #         break
            #     self.keyhandler(key)
            # elif key in self.events.keys():
            #     self.events[key](key)
            else:
                retval = self.send_signal(key)
                if not retval:
                    break
            self.screen.erase()
            self.draw()
            y, x = self.screen.getmaxyx()
            self.screen.addstr(y-1, 1, str(key))

    def keyhandler(self, key):
        self.keymap[key]()

    def build_receipts_for_export(self):
        """Generates Yaml receipt objects from database"""

        # TODO: adding a serialize function in Yamlreceipt will help
        #       shorten this function
        for r in self.database.select_receipts():
            products = {
                p.product: p.price
                    for p in self.database.select_receipt_products(r.filename)
            }

            # separates date into list of int values again
            datelist = utils.parse_date_from_database(r.date)

            # reuse yaml object to export
            receipt = Yamlreceipt(
                r.store, 
                r.short, 
                datelist, 
                r.category, 
                products, 
                r.subtotal, 
                r.tax, 
                r.total,
                r.payment
            )
            yield (r.filename, receipt)

    def export_receipts(self):
        """Should create a folder that matches exactly the input folder"""
        # TODO: single file to hold all data vs multiple files
        # TODO: move file/folder existance checks to self.setup(). That way
        #       the export folder can be checked/created only once and not
        #       every time this function is called
        # verify folder exists. If not then create it
        exportpath = utils.format_directory_path(self.export)
        folderpath = utils.check_or_create_folder(self.export)
        formatpath = utils.format_directory_path(folderpath)
        self.log(f"Begin exporting to {formatpath}")
        for filename, receipt in self.build_receipts_for_export():
            filepath = formatpath + filename + config.YAML_FILE_EXTENSION
            with open(filepath, 'w') as yamlfile:
                yamlfile.write(yaml.dump(receipt))
        self.log("Finished exporting.")

    def generate_reports(self):
        """
        Basically does a join on all the files in the database for common
        data comparisons. Could use a handler to generate all the reports
        specific to the database being used.
        """
        pass

    def build_receipt_viewer(self, rebuild=False):
        screen = self.screen
        height, width = screen.getmaxyx()

        self.controller = ReceiptController(ReceiptConnection(rebuild=rebuild))

        self.data = list(self.controller.request_receipts())

        receipt_explorer = ScrollableWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 1),
                1,
                0
            ),
            title="receipt",
            title_centered=True,
            focused=True,
            data=[n.store for n in self.data],
            data_changed_handlers=(self.on_data_changed,)
        )
        receipt_explorer.keypress_up_event = on_keypress_up
        receipt_explorer.keypress_down_event = on_keypress_down
        self.window.add_window(receipt_explorer)
        self.events[curses.KEY_DOWN].append(receipt_explorer.handle_key)
        self.events[curses.KEY_UP].append(receipt_explorer.handle_key)

        self.focused = self.window.currently_focused
        if not self.focused:
            self.focused = self.window
        
    """
    def build_windows3(self, screen):
        height, width = screen.getmaxyx()
        self.screen = screen
        self.window = Window('Application', width, height)  
        v1 = View(screen.subwin(1, width, 0, 0))
        optbar = OptionsBar(v1.width)
        v1.add_element(optbar)
        file_options = OptionsList(screen, ("longoption", "shortopt"))
        optbar.add_option('File', file_options)
        optbar.add_option('Edit', None)
        optbar.add_option('Select', None)
        optbar.add_option('Help', None)
        self.window.add_view(v1)
    def build_windows2(self):
        screen = self.screen
        y, x = screen.getbegyx() # just a cool way of getting 0, 0
        height, width = screen.getmaxyx()
        # TODO: options manager, view manager, component manager
        self.window = Window('Application', width, height)

        v1 = View(screen.subwin(height - 1, width, 1, 0), columns=2, rows=2)

        receipt_cards = [ Card(r) for r in self.build_receipts() ]
        scroller = ScrollList(v1.x, v1.y, v1.width // 4, v1.height)
        scroller.add_items(receipt_cards)

        form = receiptForm(
            v1.width // 4,
            v1.y,
            (v1.width // 4) * 3,
            v1.height, scroller.model
        )

        v1.add_element(scroller)
        v1.add_element(form)
        # v2 = View(1, 1, width, height - 1)

        optionview1 = View(screen.subwin(4, 14, 1, 0))
        optionview2 = View(screen.subwin(4, 15, 1, 6))
        optionview3 = View(screen.subwin(4, 15, 1, 12))
        self.window.add_view(v1)
        self.window.add_view(optionview1)
        self.window.add_view(optionview2)
        self.window.add_view(optionview3)
        #self.window.add_view(View(1, 1, width, height - 1))
    """

    def on_focus_changed(self, sender, arg=None):
        self.focused = self.window.currently_focused

    def data_changed(self, sender, arg):
        self.on_data_changed(sender, model=self.data[arg])

    def data_added(self, sender, *args, **kwargs):
        data = kwargs['data']
        self.data.append(data)
        self.on_data_added(self, data=self.data)

    def keypress_escape(self, sender, arg=None):
        self.continue_app = False

    def build_file_explorer(self):
        """Work on putting folder/file names in window"""
        screen = self.screen
        height, width = screen.getmaxyx()
        self.controller = ExplorerController()
        self.data = [
            self.controller.request_tree()
        ]

        # add window key handlers to application event mapping
        self.events[curses.KEY_DOWN].append(scroller.handle_key)
        self.events[curses.KEY_UP].append(scroller.handle_key)

    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()

        # main window
        self.window = Window(screen, title='Application Example 1')

        # first window half screen vertical
        sub1 = DisplayWindow(
            screen.subwin(
                height - 1,
                utils.partition(width, 2, 1),
                0, 
                0
            ),
            title="Sub-win 1",
            focused=True
        )

        # second window quarter screen top right
        sub2 = DisplayWindow(
            screen.subwin(
                utils.partition(height-1, 2, 1),
                utils.partition(width, 2, 1), 
                0,
                utils.partition(width, 2, 1), 
            ),
            title="Sub-win 2"
        )

        sub3 = DisplayWindow(
            screen.subwin(
                utils.partition(height-2, 2, 1),
                utils.partition(width, 2, 1), 
                utils.partition(height-1, 2, 1),
                utils.partition(width, 2, 1), 
            ),
            title="Sub-win 3"
        )
        
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
        sub3.add_handlers(
            9,
            sub3.unfocus,
            sub1.focus,
            self.on_focus_changed
        )

        self.window.add_windows(sub1, sub2, sub3)
        self.on_focus_changed(self)

    def draw(self):
        if not self.window:
            raise Exception("No window to draw")

        # send in the screen to all window objects
        if self.window.showing:
            self.window.draw()

    def send_signal(self, signal):
        return self.window.send_signal(signal)

if __name__ == "__main__":
    a = Application('./receipts/')
    a.setup()
    a.build_windows()
    a.run()
    for table in a.database.tables:
        print(table)
