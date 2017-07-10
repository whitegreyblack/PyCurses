# -----------------------------------------------------------------------------
# Author  : Sam Whang | whitegreyblack
# Filename: wrapper.py
# FileInfo: Contains wrapper definitions used in pycurses
# ---------------------------------------------------------------------------- 

import functools
import logging
from strings import passfail, ORG, GRN, RED, END
# used by printer to print number of files printed
file_num = 1
file_str = "\t[{}]({:02}):- {}"
spacer = []
tab = "  "

def printer(enabled):
    ''' allows print statements to stdout as well as logging '''
    def wrapper(fn):
        @functools.wraps(fn)
        def log(*args, **kwargs):
            global file_num
            ret = fn(*args, **kwargs)
            if enabled == ret:
                try:
                    print(file_str.format(
                        passfail[fn.__name__][ret],
                        file_num,
                        args[1].split('.')[0]))
                    logging.info(file_str.format(
                        passfail[fn.__name__][ret],
                        file_num,
                        args[1].split('.')[0]))
                    file_num += 1
                except BaseException:
                    print(args)
                    raise
            return ret
        return log
    return wrapper


def tryexcept(fn):
    # handles exceptions and returns false instead
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaseException:
            return False
    return wrapper


def truefalse(fn):
    # handles converting return vals to boolean
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return True if fn(*args, **kwargs) else False
    return wrapper


def tin(func, *args, **kwargs):
    # wrapper to trace function enter
    global spacer
    logging.info(
        "".join(spacer) +
        "Entering: [{}]".format(
            ORG +
            func.__name__ +
            END))
    # print("Entering: [{}]".format(func.__name__))


def tout(result, func, *args, **kwargs):
    # wrapper to trace function exit
    global spacer
    if result:
        logging.info(
            "".join(spacer) +
            "Exitting: [{}]".format(
                GRN +
                func.__name__ +
                END))
    else:
        logging.info(
            "".join(spacer) +
            "Exitting: [{}]".format(
                RED +
                func.__name__ +
                END))
    # print("Exitting: [{}]".format(func.__name__))


def trace(func):
    def call(*args, **kwargs):
        global spacer
        spacer.append(tab)
        tin(func, *args, **kwargs)
        result = func(*args, **kwargs)
        tout(result, func, *args, **kwargs)
        spacer.pop()
        return result
    return call


