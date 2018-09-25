"""Logger implements the loggable class that holds the log methods every
class uses to print to the log file.
"""
__author__ = "Samuel Whang"
import logging
import source.utils as utils
from collections import namedtuple

class Loggable:
    def __init__(self, childname, logargs=None, logger=False):
        self.childname = childname
        self.logger = logger
        if not self.logger:
            self.logger = utils.setup_logger(logargs.name,
                                             logargs.file,
                                             extra=logargs.extra)
            self.log("No logger passed into constructor. Creating new logger.")
            
    def log(self, message, level=logging.INFO):
        """Prints the message to the logger instead of to the terminal as with
        logging level of INFO.
        """
        formatted_message = f"{self.childname}: {message}"
        if level == logging.INFO:
            self.logger.info(formatted_message)
        elif level == logging.WARNING:
            self.logger.warning(formatted_message)
        else:
            raise ValueError("Parameter level does not match logging levels")

class Tester(Loggable):
    def __init__(self, logger=None):
        super().__init__(self.__class__.__name__,
                         logargs=utils.logargs(self.__class__), 
                         logger=logger)
        self.log("testing 1.2.3.")

if __name__ == "__main__":
    t = Tester()
    
    l = utils.setup_logger('logger', 
                           'logger.log', 
                           extra={'currentfile': __file__})
    t = Tester(logger=l)
