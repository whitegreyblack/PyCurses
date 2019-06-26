"""Datacontroller.py"""
import json
import os

import source.config as config
from source.database import NoteConnection, ReceiptConnection
from source.models.models import Note, Person, Product, Receipt, Transaction
from source.utils import (EventHandler, EventArg, format_date,
                          parse_date_from_database, setup_logger)


class Node:
    def __init__(self, curdir, files):
        pass


class Args:
    def __init__(self, *args, **kwargs):
        pass


class Controller:
    """Handles requests for data and responses from database"""
    logger_name = 'controller'
    logger_file = 'controller.log'
    logger_args = {'currentfile': __file__}
    # def __init__(self, connection=None, logger=None):
    def __init__(self, connection=None, reinsert=False):
        print(self.__class__.__name__, reinsert)
        self.connection = connection
    
        if reinsert:
            self.read_data_file()
    
    def read_data_file(self):
        if not self.data_file_path:
            raise NotImplementedError
        try:
            with open(self.data_file_path, "r") as f:
                d = json.loads(f.read())
        except FileNotFoundError:
            print("Could not open file. File does not exist.")
        else:
            # Note.nid = self.get_next_note_id() + 1
            for obj in d:
                # o = Note(
                #     obj['title'],
                #     created=obj['created'], 
                #     modified=obj['modified'], 
                #     note=obj['note']
                # )
                self.connection.insert(obj)
    

class QuizController(Controller):
    data_file_path = config.DATA_FILE_PATH_QUIZ
    def request_questions(self):
        for qdata in self.connection.select_questions():
            yield qdata
        else:
            yield None


class NotesController(Controller):
    """
    TODO: need a schema written to hold data
    Notes:
        idNote   int,
        title    varchar(50),
        created  datetime,
        modified datetime, -- last modified or every modification?
        note     varchar(250),
    """
    data_file_path = config.DATA_FILE_PATH_NOTES
    def get_next_note_id(self):
        return self.connection.select_max_note_id()
    
    def request_note(self, nid):
        pass
    
    def request_notes(self):
        notes = self.connection.select_from_table()
        return [Note.from_database(*n) for n in notes]

    def add_to_database(self, obj):
        self.connection.insert_note(obj)


class ExplorerController(Controller):
    ignore_folders = ['.git', '.vscode','tests', '__pycache__']
    def __init__(self):
        super().__init__(None)

        # yes, this shouldn't be in the controller, but currently no class
        # in project does this yet. Doing the prototype here, then refactoring
        self.build_explorer()

    def build_explorer(self):
        for root, folders, files in os.walk('.'):
            skip_root = False
            for ignore in self.ignore_folders:
                if ignore in root:
                    skip_root = True
            if skip_root:
                continue
            print(root)
            for name in files:
                print(name)
            # for folder in folders:
            #     print(os.path.join(root, folder))
            # for name in files:
            #     print(os.path.join(root, name))
            # print(f)
            # print(files)

    def request_tree(self):
        return None


class ProductController(Controller):
    def request_product(self, pid):
        pass

    def request_products(self):
        return list(Product.test_products())


class PersonController(Controller):
    def request_person(self, pid):
        if not self.connection:
            return Person()


class ReceiptController(Controller):
    def request_receipt(self, rid=None, rfile=None):
        if not rid and not rfile:
            raise BaseException("Either rid or rfile must be supplied")
        elif rid:
            self.request_receipt_by_id(rid)
        else:
            self.request_receipt_by_file(rfile) 

    def request_receipt_by_id(self, rid):
        pass

    def request_receipt_by_file(self, rfile):
        pass

    def request_receipts(self):
        for rdata in self.connection.select_receipts():
            rid = rdata.rid
            store = self.connection.select_store(rdata.sid)
            category = self.connection.select_category(store.cid)
            products = list(self.connection.select_receipt_products(rid))
            t = Transaction(
                rdata.total, 
                rdata.payment, 
                rdata.subtotal, 
                rdata.tax
            )
            r = Receipt(
                store.store,
                store.store,
                rdata.purchased_on,
                rdata.purchased_on,
                category,
                [
                    Product(p.product, p.price) 
                        for p in products
                ], 
                t
            )
            yield r

if __name__ == "__main__":
    # e = ExplorerController()
    n = NotesController(NoteConnection())
    print(n.request_notes())
