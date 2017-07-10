# -----------------------------------------------------------------------------
# Author: Sam Whang | whitegreyblack
# FileName: checker.py
# FileInfo: Parser object to verify valid yaml files
# -----------------------------------------------------------------------------
import re
import sys
import yaml
import click
import logging
import functools
from os import walk
from datetime import date
from reciept import Reciept
from strings import passfail, ORG, GRN, RED, END

# used by printer to print number of files printed
file_num = 1
file_str = "\t[{}]({:02}):- {}"
spacer = []
tab = "  "
# to printer -- create second to printer


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
    ''' handles exceptions and returns false instead '''
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaseException:
            return False
    return wrapper


def truefalse(fn):
    ''' handles converting return vals to boolean '''
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return True if fn(*args, **kwargs) else False
    return wrapper


def tin(func, *args, **kwargs):
    global spacer
    logging.info(
        "".join(spacer) +
        "Entering: [{}]".format(
            ORG +
            func.__name__ +
            END))
    # print("Entering: [{}]".format(func.__name__))


def tout(result, func, *args, **kwargs):
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


def trace(pre, post):
    def decorate(func):
        def call(*args, **kwargs):
            global spacer
            spacer.append(tab)
            pre(func, *args, **kwargs)
            result = func(*args, **kwargs)
            post(result, func, *args, **kwargs)
            spacer.pop()
            return result
        return call
    return decorate


class YamlChecker:
    # whitebox: (input:-folder str, output:-list)
    def __init__(self, folder='reciepts'):
        # initialize the folder holding files to check
        self.folder = folder
        self.startdate = None

    @trace(tin, tout)
    def files_safe(self):
        # iterate through each file in directory
        delete = []  # files to delete/modify
        commit = []  # files to be committed into db
        logging.info("".join(spacer) + "Using: {}".format(self.folder))
        for _, _, files in walk(self.folder):
            for file in files:
                ext = (file.split('.'))[-1]
                if ext == "yaml":
                    # passes the filename test
                    ret = self.file_safe(file) \
                        and self.yaml_safe(file)
                    if not ret:  # and db_safe()
                        delete.append(file)
                    else:
                        commit.append(file)
        #logging.info("To Delete: {}".format(delete))
        #logging.info("TO Commit: {}".format(commit))
        # self.files_delete(delete)
        return commit, delete

    def files_delete(self, files):
        # verify delete from user before removal
        check = "({:02}/{}) Delete {}?: "
        keywords = ["yes", "no"]
        for i in range(len(files)):
            confirm = input(check.format(
                i + 1,
                len(files),
                files[i]))
            if confirm in keywords:
                pass
            else:
                pass

    @trace(tin, tout)
    def file_safe(self, file):
        # calls file checks in order of serial encounter
        logging.info("".join(spacer) + "Using: {}".format(file))
        return self.file_regex(file) \
            and self.file_read(file) \
            and self.file_load(file)

    @trace(tin, tout)
    @printer(False)
    @truefalse
    def file_regex(self, file):
        ''' checks file name match,non empty file,syntax '''
        regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
        matches = re.compile(regex).match(file)
        logging.info("\t{} matches regex: {}".format(
            file, matches is not None))
        return re.compile(regex).match(file)

    @trace(tin, tout)
    @printer(False)
    @truefalse
    def file_read(self, file):
        ''' check file content and assert not empty '''
        with open(self.folder + file) as f:
            lines = f.read()
            logging.info("\t{} was read: {}".format(file, lines is not None))
            return lines

    @trace(tin, tout)
    @printer(False)
    @tryexcept
    def file_load(self, file):
        ''' check file is a yaml object after file load '''
        with open(self.folder + file) as f:
            obj = yaml.load(f.read())
            logging.info("\t{} is {}: {}".format(file,
                                                 'YAMLObject',
                                                 isinstance(obj, yaml.YAMLObject)))
            # print("{} is {}: {}".format(file, "Reciept", isinstance(obj, Reciept)))
            return isinstance(obj, yaml.YAMLObject)

    @trace(tin, tout)
    def yaml_read(self, file):
        ''' creates and returns yaml object '''
        with open(self.folder + file) as f:
            obj = yaml.load(f.read())
            logging.info("\t{} is {}: {}".format(file,
                                                 'Reciept',
                                                 isinstance(obj, Reciept)))
            return obj

    @trace(tin, tout)
    @printer(True)
    def yaml_safe(self, file):
        ''' check contents of yaml object '''
        obj = self.yaml_read(file)
        return self.yaml_store(file, obj) \
            and self.yaml_date(file, obj) \
            and self.yaml_prod(file, obj) \
            and self.yaml_card(file, obj)

    @trace(tin, tout)
    @printer(False)
    @tryexcept
    def yaml_store(self, file, obj):
        ''' check yaml store with store in filename '''
        fname = file.split('.')[0].split('-')[1]
        store = obj.store.replace(" ", "").lower()
        logging.info('\tStore Name: {}'.format(fname))
        logging.info('\t{} in {}: {}'.format(fname, store, (fname in store)))
        return fname in store

    @trace(tin, tout)
    @printer(False)
    @tryexcept
    def yaml_date(self, file, obj):
        # check yaml date with file date
        y, m, d = obj.date
        if not self.startdate:
            self.startdate = date(y, m, d)
        end = date.today()
        filedate = date(y, m, d)
        logging.info('\tS: {}\n\tF: {}\n\tE: {}'.format(
            self.startdate.isoformat(),
            filedate.isoformat(),
            end.isoformat()))
        return self.startdate <= filedate < end

    @trace(tin, tout)
    @printer(False)
    def yaml_prod(self, file, obj):
        # iterate through yaml object[prod]:{str:int,[...]}
        for key in obj.prod.keys():
            if not isinstance(key, str):
                logging.info('\tkey({}) is not str'.format(key))
                return False
            if len(key) > 25:
                logging.info('\tkey({}) is too big'.format(key))
                return False
            if not isinstance(obj.prod[key], float):
                logging.info('\tprod({}) is not float'.format(obj.prod[key]))
                return False
            if len(str(obj.prod[key])) > 6:
                logging.info('\tprod({}).is too big'.format(obj.prod[key]))
                return False
            logging.info('\t{}: {}'.format(key, obj.prod[key]))
        logging.info('\tProducts Passed: {}'.format(len(obj.prod.keys())))
        return True

    @trace(tin, tout)
    @printer(False)
    @tryexcept
    def yaml_card(self, file, obj):
        # check payment identifiers in yaml object
        def mul(x):
            return x * 100
        get = [obj.prod[key] for key in obj.prod.keys()]
        get = int(mul(sum(get)))
        sub = int(mul(obj.sub))
        add = int(mul(obj.sub + obj.tax))
        tot = int(mul(obj.tot))
        logging.info('\tsum: {}\n\tsub: {}\n\ttax: {}\n\ttot: {}'.format(
            get, sub, int(mul(obj.tax)), tot))
        return get == sub and add == tot


@click.command()
@click.option('-f', help='Folder Containing Yaml Files')
@click.option('-p', is_flag=True, help='MODE: Print')
@click.option('-l', is_flag=False, help='MODE: Logger')
@click.option('-d', is_flag=False, help='MODE: Debug')
def main(f, p, l, d):
    # check input args -- exit if incorrect
    if not f:
        exit('Incorrect Args')
    logging.info("-" * 80)
    logging.info("\nChecking Files")
    c, d = YamlChecker(f.replace("\\", '/')).files_safe()
    logging.info("Files to DELETE:")
    for i in d:
        logging.info(tab + i)
    logging.info("Files to COMMIT:")
    for i in c:
        logging.info(tab + i)
    logging.info("Checking Finished\n")
    logging.info("-" * 80)


if __name__ == "__main__":
    # Setup basic logger
    logging.basicConfig(
        filename='debug.log',
        format='%(message)s',
        level=logging.DEBUG)
    main()
