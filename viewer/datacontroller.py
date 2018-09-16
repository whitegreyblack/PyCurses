"""Datacontroller.py"""
__author__ = "Samuel Whang"

from utils import setup_logger
from utils import Event, EventArg

class DataController:
    """Handles requests for data and responses from database"""
    logger_name = 'controller'
    logger_file = 'controller.log'
    logger_args = {'currentfile': __file__}

    def __init__(self, connection, logger=None):
        self.connection = connection
        if not logger:
            logger = setup_logger(logger_name, logger_file, extra=logger_args)
        self.logger = logger

    def request_reciept(self, recieptfile):
        pass

    def response_reciept(self):
        pass

    def request_product(self):
        pass

    def response_product(self):
        pass

    def request(self):
        pass

    def response(self):
        pass
