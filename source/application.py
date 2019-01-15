"""Application.py: 
Main class that builds all other objects and runs the curses loop
"""
import os
import yaml
import math
import random
import curses
import logging
import datetime
import cerberus
from source.keymap import EventMap
import source.utils as utils
import source.config as config
from source.logger import Loggable
from source.controllers import (
    PersonController,
    ExplorerController,
    NotesController,
)
from source.schema import (
    Table, 
    SQLType, 
    build_products_table,
    build_reciepts_table
)
from source.yamlchecker import YamlChecker
from source.database import (
    Connection,
    NoteConnection
)
from source.models.models import Reciept, Transaction, Task
from source.models.product import Product
from source.YamlObjects import Reciept as YamlReciept
from source.window import (
    Window,
    ScrollableWindow,
    PromptWindow,
    DisplayWindow,
    on_keypress_down,
    on_keypress_up
)

class Application(Loggable):
    """Overview:
    Builds the database and yamlchecker objects. (They are tightly coupled. May
    need to change in the future.) The data from the yaml files found in using
    the folder path paramter are first checked by the yamlchecker before
    loading into the database.

    With loading finished, the front end is created and views are initialized,
    using data from the database.

    Then the application is looped to draw the views onto the screen using 
    curses framework.
    """
    def __init__(self, folder, screen=None, logger=None, rebuild=False):
        super().__init__(self, logger=logger)
        self.screen = screen
        self.window = None
        self.folder = folder
        self.export = "./export/"
        # self.checker = YamlChecker(folder, logger=logger)

        self.keymap = dict()
        self.keymap[ord('e')] = self.export_reciepts
        self.keymap[ord('Q')] = None
        self.keymap[ord('q')] = None

        self.database = Connection(logger=logger, rebuild=rebuild)
        self.controller = None

        self.data_changed_event = utils.Event()
        self.events = EventMap.fromkeys((
            curses.KEY_DOWN,
            curses.KEY_UP,
            ord('\t'),
            curses.KEY_BTAB
        ))
        # self.events = {
        #     curses.KEY_DOWN: utils.Event(),
        #     curses.KEY_UP: utils.Event(),
        #     ord('\t'): utils.Event(),
        #     curses.KEY_BTAB: utils.Event()
        # }

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
        # print(f'Yaml Filename is valid {filename}')

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
        while True:
            key = self.screen.getch()
            if key in self.keymap.keys():
                if self.keymap[key] == None:
                    break
                self.keyhandler(key)
            elif key in self.events.keys():
                self.events[key](key)
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

    def build_reciepts(self):
        """Generates View Reciept objects from database"""
        for rdata in self.database.select_reciepts():
            reciept = rdata.filename
            rproducts = list(self.database.select_reciept_products(reciept))
            t = Transaction(
                rdata.total, 
                rdata.payment, 
                rdata.subtotal, 
                rdata.tax
            )
            d = utils.parse_date_from_database(rdata.date)
            r = Reciept(
                rdata.store,
                rdata.short,
                utils.format_date(d, config.DATE_FORMAT['L']),
                utils.format_date(d, config.DATE_FORMAT['S']),
                rdata.category,
                [Product(p.product, p.price) for p in rproducts], t
            )
            yield r

    def build_reciepts_for_export(self):
        """Generates Yaml Reciept objects from database"""

        # TODO: adding a serialize function in YamlReciept will help
        #       shorten this function
        for r in self.database.select_reciepts():
            products = {
                p.product: p.price
                    for p in self.database.select_reciept_products(r.filename)
            }

            # separates date into list of int values again
            datelist = utils.parse_date_from_database(r.date)

            # reuse yaml object to export
            reciept = YamlReciept(
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
            yield (r.filename, reciept)

    def export_reciepts(self):
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
        for filename, reciept in self.build_reciepts_for_export():
            filepath = formatpath + filename + config.YAML_FILE_EXTENSION
            with open(filepath, 'w') as yamlfile:
                yamlfile.write(yaml.dump(reciept))
        self.log("Finished exporting.")

    def generate_reports(self):
        """Basically does a join on all the files in the database for common
        data comparisons. Could use a handler to generate all the reports
        specific to the database being used.
        """
        pass

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

        reciept_cards = [ Card(r) for r in self.build_reciepts() ]
        scroller = ScrollList(v1.x, v1.y, v1.width // 4, v1.height)
        scroller.add_items(reciept_cards)

        form = RecieptForm(
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

    def on_data_changed(self, sender, sid, arg):
        model = self.data[arg]
        self.data_changed_event(sender, sid, model)

    def build_file_explorer(self):
        """Work on putting folder/file names in window"""
        screen = self.screen
        height, width = screen.getmaxyx()
        self.controller = ExplorerController()
        self.data = [
            self.controller.request_tree()
        ]

    def build_todo_tasks(self):
        """Builds a todo app"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.data = [
            Task(f"task {i}", random.randint(0, 3), datetime.datetime.today())
                for i in range(50)
        ]

        self.window = Window(screen, title="Tasks To Do")

        task_win = DisplayWindow(
            screen.subwin(
                utils.partition(height-2, 2, 1),
                width,
                utils.partition(height, 2, 1),
                0
            )
        )
        self.data_changed_event.append(task_win.on_data_changed)

        none_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1, 
                0
            ),
            title="No Status",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 0],
            data_changed_handlers=(self.on_data_changed,)
        )

        todo_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 1)
            ),
            title="Todo",
            title_centered=True,
            focused=True,
            data=[task.title for task in self.data if task.status_id == 1],
            data_changed_handlers=(self.on_data_changed,)
        )
        todo_win.keypress_up_event = on_keypress_up
        todo_win.keypress_down_event = on_keypress_down
        self.events[ord('\t')].append(todo_win.handle_key)
        self.events[curses.KEY_BTAB].append(todo_win.handle_key)
        self.events[curses.KEY_DOWN].append(todo_win.handle_key)
        self.events[curses.KEY_UP].append(todo_win.handle_key)

        work_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 2)
            ),
            title="In-progress",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 2],
            data_changed_handlers=(self.on_data_changed,)
        )

        done_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 3)
            ),
            title="Finished",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 3],
            data_changed_handlers=(self.on_data_changed,)
        )

        self.window.add_windows(
            none_win,
            todo_win,
            work_win,
            done_win,
            task_win
        )

    def build_note_viewer(self):
        """Builds an application to view all notes"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.controller = NotesController(NoteConnection())
        self.data = self.controller.request_notes()

        self.window = Window(screen, title='Note Viewer Example')

        note_display = DisplayWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 2),
                1,
                utils.partition(width, 3, 1)
            )
        )
        self.data_changed_event.append(note_display.on_data_changed)
        self.window.add_window(note_display)

        note_explorer = ScrollableWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 1),
                1,
                0
            ),
            title="Explorer",
            data=[n.title for n in self.data],
            data_changed_handlers=(self.on_data_changed,)
        )
        note_explorer.keypress_up_event = on_keypress_up
        note_explorer.keypress_down_event = on_keypress_down
        self.window.add_window(note_explorer)
        self.events[curses.KEY_DOWN].append(note_explorer.handle_key)
        self.events[curses.KEY_UP].append(note_explorer.handle_key)

    def build_windows1(self):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()
        self.controller = PersonController()
        self.data = [
            self.controller.request_person(pid)
                for pid in range(10)
        ]
        # main window
        self.window = Window(screen, title='Application Example 1')

        # display window
        display = DisplayWindow(
            screen.subwin(
                11,
                utils.partition(width, 5, 3),
                1, 
                utils.partition(width, 5, 2)
            ),
            title="Profile"
        )
        self.data_changed_event.append(display.on_data_changed)

        # scroll window
        scroller = ScrollableWindow(
            screen.subwin(
                height - 2, 
                utils.partition(width, 5, 2), 
                1, 
                0
            ),
            title="Directory",
            data=[str(n.name) for n in self.data],
            focused=True,
            data_changed_handlers=(self.on_data_changed,)
        )

        # secondary display -- currently unused
        # adding sub windows to parent window
        unused = Window(
            screen.subwin(
                height - 13, 
                utils.partition(width, 5, 3),
                12, 
                utils.partition(width, 5, 2)
            ), 
            title='verylongtitlescree'
        )

        # prompt screen
        prompt = PromptWindow(screen.subwin(3, width, height - 4, 0))

        self.window.add_windows([
            scroller,
            display,
            unused,
            prompt
        ])

        # add window key handlers to application event mapping
        self.events[curses.KEY_DOWN].append(scroller.handle_key)
        self.events[curses.KEY_UP].append(scroller.handle_key)

    def build_windows(self):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()
        self.controller = PersonController()
        self.data = [
            self.controller.request_person(pid)
                for pid in range(10)
        ]

        # main window
        self.window = Window(screen, title='Application Example 1')

        # display window
        display = DisplayWindow(
            screen.subwin(
                11,
                utils.partition(width, 5, 3),
                1, 
                utils.partition(width, 5, 2)
            ),
            title="Profile"
        )
        self.data_changed_event.append(display.on_data_changed)

        # scroll window
        scroller = ScrollableWindow(
            screen.subwin(
                height - 2, 
                utils.partition(width, 5, 2), 
                1, 
                0
            ),
            title="Directory",
            data=[str(n.name) for n in self.data],
            focused=True,
            data_changed_handlers=(self.on_data_changed,)
        )
        scroller.keypress_up_event.append(on_keypress_up)
        scroller.keypress_down_event.append(on_keypress_down)
        # secondary display -- currently unused
        # adding sub windows to parent window
        unused = Window(
            screen.subwin(
                height - 13, 
                utils.partition(width, 5, 3),
                12, 
                utils.partition(width, 5, 2)
            ), 
            title='verylongtitlescree'
        )

        # prompt screen
        prompt = PromptWindow(screen.subwin(3, width, height - 4, 0))

        self.window.add_windows([
            scroller,
            display,
            unused,
            prompt
        ])

        # add window key handlers to application event mapping
        self.events[curses.KEY_DOWN].append(scroller.handle_key)
        self.events[curses.KEY_UP].append(scroller.handle_key)

        # v1 = View(screen.subwin(height - 1, width, 1, 0), columns=2, rows=2)
        # self.window.add_view(v1)

        # scroller = ScrollList(1, 1,
        #                       self.window.width // 4,
        #                       self.window.height,
        #                       title='Reciepts',
        #                       selected=True)

        # reciept_cards = [ Card(r) for r in self.build_reciepts() ]
        # scroller.add_items(reciept_cards)
        # form = RecieptForm(
        #     (self.window.width // 4) + 1, # add 1 for offset
        #     1,
        #     self.window.width - (self.window.width // 4) - 1, 
        #     self.window.height,
        #     scroller.model
        # )

        # promptwin = screen.subwin(
        #     self.window.height // 3, 
        #     self.window.width // 2, 
        #     self.window.height // 3,
        #     self.window.width // 4
        # )

        # exitprompt = Prompt(
        #     promptwin, 
        #     'Exit Prompt', 
        #     'Confirm', 
        #     'Cancel', 
        #     logger=self.logger
        # )

        # self.window.add_windows([scroller, form, exitprompt])

        keymap = dict()
        keymap[(curses.KEY_DOWN, 1)] = 1
        # keymap[(curses.CTL_ENTER)] -- prompt control CTRLEnter: show/hide, ENTER: command
        # keymap[(curses.KEY_UP, scroller.wid)] = scroller.wid
        # keymap[(curses.KEY_DOWN, scroller.wid)] = scroller.wid
        # keymap[(curses.KEY_ENTER, scroller.wid)] = form.wid
        # keymap[(curses.KEY_RIGHT, scroller.wid)] = form.wid
        # keymap[(curses.KEY_LEFT, form.wid)] = scroller.wid
        # keymap[(curses.KEY_LEFT, exitprompt.wid)] = exitprompt.wid
        # keymap[(curses.KEY_RIGHT, exitprompt.wid)] = exitprompt.wid
        # keymap[(ord('\t'), exitprompt.wid)] = exitprompt.wid
        # # keymap[(curses.KEY_F1,)] = 'Reciepts'
        # # 10 : New Line Character
        # keymap[(10, scroller.wid)] = form.wid
        # keymap[(10, exitprompt.wid)] = scroller.wid
        # # 27 : Escape Key Code
        # keymap[(27, scroller.wid)] =  exitprompt.wid
        # keymap[(27, exitprompt.wid)] = None
        # keymap[(27, form.wid)] = scroller.wid
        # keymap[(ord('y'), exitprompt.wid)] = None
        # keymap[(ord('n'), exitprompt.wid)] = form.wid
        # keymap[(curses.KEY_ENTER, exitprompt.wid)] = None
        self.window.add_keymap(keymap)

    def draw(self):
        # self.screen.addstr(0, 0, ' ' * (self.window.width + 2), curses.color_pair(2))
        # self.screen.insstr(self.window.height + 1,
        #                    0,
        #                    ' ' * (self.window.width + 2),
        #                    curses.color_pair(3))
        # self.screen.addstr(0, 1, "File", curses.color_pair(2))
        # self.screen.addstr(0, 7, "Edit", curses.color_pair(2))
        # self.screen.addstr(0, 13, "Selection", curses.color_pair(2))

        # self.screen.addstr(1, 2, "Options:")
        # self.screen.addstr(2, 2, "[e] export files")
        # self.screen.addstr(4, 2, "[E] export current file")

        # self.screen.addstr(2, self.window.width // 8, "[Reciepts]")
        # self.screen.addstr(2, self.window.width // 8 + 11, "[Products]")
        # self.screen.addstr(2, self.window.width // 8 + 22, "[Stores]")
        # self.window.draw(self.screen)

        if not self.window:
            raise Exception("No window to draw")

        # send in the screen to all window objects
        if self.window.showing:
            self.window.draw()

    def send_signal(self, signal):
        return self.window.send_signal(signal)

if __name__ == "__main__":
    a = Application('./reciepts/')
    a.setup()
    a.build_windows()
    a.run()
    for table in a.database.tables:
        print(table)
