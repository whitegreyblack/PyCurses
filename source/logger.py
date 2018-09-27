"""Logger implements the loggable class that holds the log methods every
class uses to print to the log file.
"""
__author__ = "Samuel Whang"
import logging
import source.utils as utils
from collections import namedtuple

class Loggable:
    """Creates a logger for the subclasses of this class. Handles printing of
    log messages to log file.
    """
    def __init__(self, child=None, logger=None):
        """Sets the class logger if passed in. If no logger then uses the
        secondary option of creating a logger using the logargs argument.
        If no child is passed in, meaning this class is not being subclassed
        but rather used as a standalone object, then it will set its own
        child as itself.
        """
        self.child = child
        if not child:
            self.child = self

        self.logger = logger
        if not self.logger:
            logargs = utils.logargs(child.__class__, __file__)
            self.logger = utils.setup_logger(logargs.name,
                                             logargs.file,
                                             extra=logargs.extra)
            self.log("No logger passed into constructor. Creating new logger.")

    def log(self, message, level=logging.INFO):
        """Prints the message to the logger instead of to the terminal as with
        logging level of INFO.
        """
        formatted_message = f"{self.child.__class__.__name__}: {message}"
        if level == logging.INFO:
            self.logger.info(formatted_message)
        elif level == logging.WARNING:
            self.logger.warning(formatted_message)
        else:
            raise ValueError("Parameter level does not match logging levels")

class Tester(Loggable):
    def __init__(self, logger=None):
        super().__init__(self, logger=logger)

if __name__ == "__main__":
    Tester().log("Logging to tester.log")    
    l = utils.setup_logger('logger', 
                           'logger.log', 
                           extra={'currentfile': __file__})
    Tester(l).log("Logging to logger.log")
