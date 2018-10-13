"""utils.py 
Common utility functions used throughout the program. Includes path 
manipulation and checking using the os library, a custom curses border
drawer, and variable formatting.
"""

__author__ = "Samuel Whang"

import os
import curses
import logging
import datetime
from typing import Union, Tuple
from collections import namedtuple

Currency = Union[int, float]

point = namedtuple('Point', 'x y')
size = namedtuple('Size', 'width height')
box = namedtuple('Box', 'x y width height')


EventArg = namedtuple('EventArg', 'sender msg')


class Event(list):
    def __call__(self, sender, event):
        for fn in self:
            fn(sender, event)


class Permissions(Enum): 
    flags = {
        'READ': 1 << 0,
        'WRITE': 1 << 1,
        'DELETE': 1 << 2,
    }

    @classmethod
    def check(cls, flags: int):
        index = 1
        while index <= flags:
            if ((flags & index) != 0):
                print([k for k, v in cls.flags.items() if v == index])
            index = index << 1


default_log_format = "[%(asctime)s] %(currentfile)s: %(message)s"
default_log_noargs = "[%(asctime)s] %(message)s"


def parse_args(argv):
    pass


class LogColor:
    GREEN='\x1b[1;32;40m'
    RED='\x1b[1;31;40m'
    BLUE='\x1b[0;34;40m'
    YELLOW='\x1b[0;33;40m'
    END='\x1b[0m'


def check_or_create_folder(foldername):
    full_path = os.path.join(os.path.abspath('.'), foldername)
    formatted_path = format_directory_path(full_path)
    if not os.path.exists(formatted_path):
        os.makedirs(formatted_path)
    return formatted_path


args = namedtuple("Logargs", "name file extra")


def logargs(cls, fromfile):
    classname = cls.__name__.lower()
    filepath = format_directory_path(fromfile)
    fileonly = parse_file_from_path(filepath)
    return args(classname, classname + ".log", {"currentfile": fileonly})


def setup_logger_from_logargs(logargs):
    return setup_logger(logargs.name, logargs.file, extra=logargs.extra)


def setup_logger(logname,
                 logfile,
                 logfolder='./logs',
                 extra=None, 
                 level=logging.INFO, 
                 logformat=None):

    """Handles creation of multiple loggers
    logname   => name of the logger

    logfile   => name of file the logger will log to

    logfolder => name of the folder the logfile will be created in

    extra     => dictionary of provided arguments to a formatted log message

    level     => the filter level of the log

    logformat => if logformat is not provided, then function expects user to
                 want the default log formats provided by utils. Extra is then
                 checked to verify which of the default messages user was 
                 expecting.
    """
    if not logformat:
        if extra:
            logformat = default_log_format
        else:
            logformat = default_log_noargs

    formatter = logging.Formatter(logformat, "%H:%M:%S")

    # TODO: option for keeping old logs
    # makes sure logs folder exists
    path = check_or_create_folder('logs')
    
    # if it exists clear it first for new messages only
    path = format_directory_path(path)
    with open(path + logfile, 'w'):
        pass

    handler = logging.FileHandler(path + logfile)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logname)
    logger.setLevel(level)
    logger.addHandler(handler)

    # extra is checked to see whether the logger or loggerAdapter is returned
    if extra:
        extra['currentfile'] = parse_file_from_path(extra['currentfile'])
        logger = logging.LoggerAdapter(logger, extra)

    return logger


def log_message(logger, message, extra=None):
    """Simple log function given a logger and message"""
    # TODO: allow level of log passed in as parameter. 
    #       Use getattr(logger, lvl)
    logger.info(message, extra)


def format_directory_path(path: str) -> str:
    """Replaces windows style path seperators to forward-slashes and adds
    another slash to the end of the string.
    """
    if path == ".":
        return path
    formatted_path = path.replace('\\', '/')
    if formatted_path[-1] is not '/':
        formatted_path += '/'
    return formatted_path


def check_directory_path(path: str) -> bool:
    """Wrapper for os's isdir function"""
    return os.path.isdir(path)


def parse_file_from_path(path: str) -> str:
    """Given the absolute path to a file, returns the file name only"""
    formattedpath = format_directory_path(path)
    return formattedpath.split('/')[-2]


def filename_and_extension(path: str) -> Tuple[str, str]:
    """Returns a tuple with the filename and extension elements"""
    return os.path.splitext(path)


def border(screen: object, x: int, y: int, dx: int, dy: int) -> None:
    """
    Draws a box with given input parameters using the default characters
    """
    screen.vline(y, x, curses.ACS_SBSB, dy)
    screen.vline(y, x + dx, curses.ACS_SBSB, dy)
    screen.hline(y, x, curses.ACS_BSBS, dx)
    screen.hline(y + dy, x, curses.ACS_BSBS, dx)
    screen.addch(y, x, curses.ACS_BSSB)
    screen.addch(y, x + dx, curses.ACS_BBSS)
    screen.addch(y + dy, x, curses.ACS_SSBB)
    screen.addch(y + dy, x + dx, curses.ACS_SBBS)


def format_float(number: Union[int, float]) -> float:
    """Returns a formatted float up to 10 spaces and 2 precision places"""
    return f"{number:10.2f}"


def parse_date_from_database(date: str) -> list:
    """Returns a list of ints denoting Year, Month, Date in that order"""
    return [int(d) for d in date.split('-')]


def format_date(date: list, dateformat: str=None) -> str:
    """Creates a date string using the date format paramter. If no parameter
    is provided then returns the string in the default datetime isoformat
    """
    newdate = datetime.date(*date)
    if dateformat:
        return newdate.strftime(dateformat)
    return newdate.isoformat()
