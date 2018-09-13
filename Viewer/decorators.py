"""
decorators.py: Contains decorator utility functions
"""

__author__ = "Samuel Whang"

import platform
import functools
import logging
import sys
import utils
from strings import passfail, ORG, GRN, RED, END, pop

# used by printer to print number of files printed
file_num = 1
file_str = "[{}]({:02}):- {}"
spacer = []
tab = "  "
exc_err = False

logargs = {'classname': 'wrapper'}
decoratorlog = utils.setup_logger('wrapperlog', 'wrapper.log')
'''
logging.basicConfig(filename='decorators.log',
                    format='%(message)s',
                    level=log)
'''
def log(message):
    decoratorlog.info(message, extra=logargs)

def printer(enabled):
    # allows print statements to stdout as well as logging
    def wrapper(fn):
        @functools.wraps(fn)
        def log(*args, **kwargs):
            global file_num
            ret = fn(*args, **kwargs)
            if enabled == ret:
                try:
                    # moving everything to logger
                    fmtstr = file_str.format(passfail[fn.__name__][ret],
                                             file_num,
                                             args[1].split('.')[0])
                    print(fmtstr)
                    log(fmtstr)
                    file_num += 1
                except BaseException:
                    # print(args)
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
    fn_name = func.__name__
    if platform.system() is not "Windows":
        fn_name = ORG + fn_name + END
    log(f"Entering: [{fn_name}]")

def tout(result, func, *args, **kwargs):
    # wrapper to trace function exit
    global spacer
    fn_name = func.__name__
    if platform.system() is not "Windows":
        if result:
            fn_name = GRN + fn_name + END
        else:
            fn_name = RED + fn_name + END
    log(f"Exitting: [{fn_name}]")

def trace(func):
    def call(*args, **kwargs):
        global spacer
        
        tin(func, *args, **kwargs)
        result = func(*args, **kwargs)
        tout(result, func, *args, **kwargs)

        return result
    return call

def logger(msgs):
    # wrapper to raise exceptions for functions
    try_msg, fail_msg, pass_msg = msgs

    def wrapper(fn):
        @functools.wraps(fn)
        def log(*args, **kwargs):
            global exc_err
            if len(args):
                logging.debug(try_msg.format(args[0]))
            try:
                ret = fn(*args, **kwargs)
                logging.debug(pass_msg)
                return ret
            except:
                logging.debug(fail_msg)
                exc_err = True
        return log
    return wrapper

def exitter(err, nrm):
    # creates initial logger messages
    def wrapper(fn):
        @functools.wraps(fn)
        def handle(*args, **kwargs):

            # some logging strings
            logging.debug("-"*80)
            logging.debug("Populate")
            logging.debug(pop['sql_populate'])

            if not exc_err:
                # log normal execution
                logging.debug(nrm)

                # get statistics from populate
                count, total = fn(*args)
                count = [int(j) for i in count for j in i].pop()
                total = [float(j) for i in total for j in i]
                avrgs = sum(total)/count

                # print statistics
                logging.debug("\tFiles Loaded: {:6}".format(len(args[1])))
                logging.debug("\tFiles in DB : {:6}".format(count))
                logging.debug("\tTotal Usage : {:6.2f}".format(sum(total)))
                logging.debug("\tAverage/File: {:6.2f}".format(avrgs))
                logging.debug("-"*80)
            else:
                # log error during runtime
                logging.debug(err)
        return handle
    return wrapper
