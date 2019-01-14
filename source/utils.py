"""utils.py 
Common utility functions used throughout the program. Includes path 
manipulation and checking using the os library, a custom curses border
drawer, and variable formatting.
"""

__author__ = "Samuel Whang"

import os
import yaml
import curses
import logging
import datetime
import textwrap
import cerberus
from math import floor, ceil
from source.YamlObjects import Reciept
from source.config import YAML_FILE_NAME_REGEX
from typing import Union, Tuple
from collections import namedtuple
from itertools import chain

Currency = Union[int, float]

point = namedtuple('Point', 'x y')
size = namedtuple('Size', 'width height')
box = namedtuple('Box', 'x y width height')

EventArg = namedtuple('EventArg', 'sender msg')


class Event(list):
    # def __call__(self, sender, event):
    #     for fn in self:
    #         fn(sender, event)
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)
    def __repr__(self):
        return f"Event({s})"
'''
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
'''

button_appearances = {
    "default": "", # white 0/8
    "info": "", # blue 2/4/10/12
    "success": "", # green 3/11
    "warning": "", # orange/yellow? 7/15
    "danger": "", # red? 5/13
}

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
    screen.vline(y, x + dx - 1, curses.ACS_SBSB, dy)
    screen.hline(y, x, curses.ACS_BSBS, dx)
    screen.hline(y + dy - 1, x, curses.ACS_BSBS, dx)
    screen.addch(y, x, curses.ACS_BSSB)
    screen.addch(y, x + dx - 1, curses.ACS_BBSS)
    screen.addch(y + dy - 1, x, curses.ACS_SSBB)
    screen.addch(y + dy - 1, x + dx - 1, curses.ACS_SBBS)


def initialize_curses_settings(logger=None):
    """Sets settings for cursor visibility and color pairings"""
    if logger:
        logger.info('main(): initializing curses library settings')
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_RED)


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

def unicode(word):
    """Only takes in a string without digits"""
    assert type(word) is str
    try:
        int(word)
    except ValueError:
        return sum(map(ord, word))
    raise ValueError(f"Word {word} contains integer(s)")

def sort_unicode(words, keyfunc=lambda x: unicode(x)):
    """Returns a list of words sorted by unicode value of their strings"""
    return sorted(words, key=keyfunc)

def load_yaml_object(path, doc=False):
    with open(path, 'r') as f:
        lines = f.read()
        o = yaml.load(lines)
        if doc:
            o = o.serialized()
    return o


def validate(document, schema):
    v = cerberus.Validator()
    return v.validate(document, schema)

def validate_from_path(doc_path, schema_path):
    document = load_yaml_object(doc_path, doc=True)
    schema = load_yaml_object(schema_path)
    return validate(document, schema)

def validate_filename(filename):
    schema = {
        'filename': {
            'type': 'string', 
            'regex': YAML_FILE_NAME_REGEX
        }
    }
    v = cerberus.Validator(schema)
    print(v.validate({'filename': filename}))

def partition(distance, partitions, length=1, operator=round):
    return operator(distance/partitions*length)