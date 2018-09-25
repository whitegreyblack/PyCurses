import curses
import logging
import datetime

import source.utils as utils
import source.config as config
from source.yamlchecker import YamlChecker
from source.database import Connection
from source.models.models import Reciept, Transaction
from source.models.product import Product
from source.controls import Window, ScrollList, Card, RecieptForm, Prompt, Button

def setup_test_cards():
    """List of example product cards used in testing"""
    return [Card(Product(fruit, price))
            for fruit, price in zip(
                ['Apples', 'Oranges', 'Pears', 'Watermelons', 'Peaches'],
                [3, 5, 888, 24, 55])]

class Application:
    def __init__(self, folder, logger, rebuild=False):
        self.logger = logger
        self.checker = YamlChecker(folder, logger=logger)
        self.database = Connection(logger=logger, rebuild=rebuild)

    def log(self, message):
        self.logger.info(f"{self.__class__.__name__}: {message}")

    def setup(self):
        # TODO: need a setting to determine behavior of previously loaded data
        self.database.rebuild_tables()
        inserted = self.database.inserted_files()

        self.checker.verify_file_states(loaded_files=inserted)
        files = self.checker.verified_files

        self.database.insert_files(files)
        self.log(f"Committed:")
        for commit in files:
            self.log(f"+ {commit}")

    def build_reciepts(self):
        reciepts = []
        for rdata in self.database.select_reciepts():
            reciept = rdata.filename
            rproducts = list(self.database.select_reciept_products(reciept))
            t = Transaction(rdata.total, rdata.payment, 
                            rdata.subtotal, rdata.tax)

            d = utils.format_database_date(rdata.date)
            r = Reciept(rdata.store,
                        rdata.short,
                        utils.format_date(d, config.DATE_FORMAT['L']),
                        utils.format_date(d, config.DATE_FORMAT['S']),
                        rdata.category,
                        [Product(p.product, p.price) for p in rproducts], t)
            reciepts.append(r)
        return reciepts

    def build_windows(self, screen):
        height, width = screen.getmaxyx()
        self.window = Window('Application', width, height)
        
        scroller = ScrollList(1, 1,
                              self.window.width // 4,
                              self.window.height,
                              'Reciepts',
                              selected = True)

        reciepts = self.build_reciepts()
        reciept_cards = [Card(r) for r in reciepts]
        scroller.add_items(reciept_cards)
        form = RecieptForm((self.window.width // 4) + 1, # add 1 for offset
                       1,
                       self.window.width - (self.window.width // 4) - 1, 
                       self.window.height,
                       scroller.model)
    
        subwin = screen.subwin(self.window.height // 3, 
                               self.window.width // 2, 
                               self.window.height // 3,
                               self.window.width // 4)

        exitprompt = Prompt(subwin, 'Exit Prompt', 'Confirm', None)

        self.window.add_windows([scroller, form, exitprompt])

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
        self.window.add_keymap(keymap)

    def draw(self, screen):
        self.window.draw(screen)

    def send_signal(self, signal):
        return self.window.send_signal(signal)

if __name__ == "__main__":
    pass