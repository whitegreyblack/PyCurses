import os
import yaml
import sqlite3
import logging
import logstrings as log
from connection import Connection, sys
from reciept_yaml import YamlReciept
from reciept_py import RecieptHeader, RecieptBody

folder = 'reciepts/'

def exit_handler_err(errstr):
    logging.warning(sys.exc_info()[0])
    logging.debug(errstr)
    logging.debug(log.sys_exit_err)
    logging.debug("")
    exit(-1)

def exit_handler_nrm(conn):
    conn_exit(conn)
    logging.debug(log.sql_conn_cls)
    logging.debug(log.sys_exit_nrm)
    logging.debug("")
    #exit(0)

def func_handler(enter, err, scs, fnc, *args):
    logging.debug(enter)
    try:
        return fnc(*args)
    except:
        exit_handler_err(err)

def conn_exit(conn):
    del conn
def conn_func(unneeded):
    return Connection()

def push_func(conn, head, body):
    conn.insert(head, body)

def read_func(file):
    return file.read()

def load_func(file):
    return yaml.load(file)

def open_func(args):
    with open(args, 'r') as file:
            obj = func_handler(
                log.yml_load_try.format(args),
                log.yml_load_err,
                log.yml_load_scs,
                load_func,
                func_handler(
                    log.sys_read_try.format(args),
                    log.sys_read_err,
                    log.sys_read_scs,
                    read_func,
                    file)
                )
            h,b = obj.build()
            return h, b
            
def Populate():
    logging.debug(log.sql_populate)
    conn = func_handler(
                log.sql_conn_try, 
                log.sql_conn_err, 
                log.sql_conn_scs, 
                conn_func, 
                None)
    
    for _,_,files in os.walk(folder):
        for file in files:
            h, b = func_handler(
                log.sys_open_try.format(folder+file), 
                log.sys_open_err, 
                log.sys_open_scs, 
                open_func, 
                folder+file)
            logging.debug(log.sql_push_try.format(h,b))
            func_handler(
                log.sql_push_try.format(h,b),
                log.sql_push_err,
                log.sql_push_scs,
                push_func,
                conn, h, b)
    exit_handler_nrm(conn)

if __name__ == "__main__":
    logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
    Populate()
