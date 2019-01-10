"""Datacontroller.py"""
__author__ = "Samuel Whang"

from source.models.models import Person
from source.utils import setup_logger
from source.utils import Event, EventArg

class Args:
    def __init__(self, *args, **kwargs):
        pass

class Controller:
    """Handles requests for data and responses from database"""
    logger_name = 'controller'
    logger_file = 'controller.log'
    logger_args = {'currentfile': __file__}
    def __init__(self, connection=None, logger=None):
        self.connection = connection
        if not logger:
            logger = setup_logger(
                self.logger_name, 
                self.logger_file, 
                extra=self.logger_args
            )
        self.logger = logger

class ProductController(Controller):
    def request_product(self, pid):
        pass

class PersonController(Controller):
    def request_person(self, pid):
        if not self.connection:
            return Person()
        

class RecieptController:
    def request_reciept(self, rid=None, rfile=None):
        if not rid and not rfile:
            raise BaseException("Either rid or rfile must be supplied")
        elif rid:
            self.request_reciept_by_id(rid)
        else:
            self.request_reciept_by_file(rfile)

    def request_reciept_by_id(self, rid):
        pass

    def request_reciept_by_file(self, rfile):
        pass

#     def response_reciept(self):
#         pass

#     def request_product(self):
#         pass

#     def response_product(self):
#         pass

#     def request(self):
#         pass

#     def response(self):
#         pass