import sys
import yaml
import logging
import functools
import strings_log as log
import db_connection as conn
from checker import YamlChecker

# used for exit system message at end of program
exc_err = False


def logger(try_msg, fail_msg, pass_msg):
    ''' wrapper to raise exceptions for functions '''
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
    ''' creates initial logger messages '''
    def wrapper(fn):
        @functools.wraps(fn)
        def handle(*args, **kwargs):
            logging.basicConfig(
                filename='debug.log',
                format='%(message)s',
                level=logging.DEBUG)
            logging.debug(log.sql_populate)
            fn(*args)
            if exc_err:
                logging.debug(err)
            else:
                logging.debug(nrm)
        return handle
    return wrapper


@logger(log.sql_conn_try, log.sql_conn_err, log.sql_conn_scs)
def conn_func(*args):
    return conn.Connection()


@logger(log.yml_load_try, log.yml_load_err, log.yml_load_scs)
def load_func(file, data):
    return yaml.load(data)


@logger(log.sys_read_try, log.sys_read_err, log.sys_read_scs)
def read_func(file, fin):
    return fin.read()


@logger(log.sys_open_try, log.sys_open_err, log.sys_open_scs)
def open_func(file):
    with open(file, 'r') as f:
        return read_func(file, f)


@logger(log.sql_push_try, log.sql_push_err, log.sql_push_scs)
def push_func(file, conn, head, body):
    conn.insert(head, body)


@exitter(log.sys_exit_err, log.sys_exit_nrm)
def Populate(folder, files):
    con = conn_func()
    for file in files:
        dat = open_func(folder+file)
        obj = load_func(folder+file, dat)
        h, b = obj.build()
        push_func(file, con, h, b)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Unspecified Folder")
        exit(-1)
    folder = sys.argv[1].replace("\\", "/")
    files = YamlChecker(sys.argv[1].replace("\\", '/')).files_safe()
    Populate(folder, files)
