from os import walk
import re
import sys
from reciept_yaml import Reciept
from strings_checker import passfail as strings
import logging
import yaml
import functools
from datetime import date

# used by printer to print number of files printed
file_num = 1
file_str = "[{}]({:02}):- {}"
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
                    logging.debug("a")
                    print(file_str.format(
                        strings[fn.__name__][ret],
                        file_num,
                        args[1].split('.')[0].split('-')[1]))
                    file_num += 1
                except:
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
        except:
            return False
    return wrapper


def truefalse(fn):
    ''' handles converting return vals to boolean '''
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return True if fn(*args, **kwargs) else False
    return wrapper


class YamlChecker:
    ''' whitebox: (input:-folder str, output:-list) '''
    def __init__(self, folder='reciepts'):
        ''' initialize the folder holding files to check '''
        self.folder = folder

    def files_safe(self):
        ''' iterate through each file in directory '''
        delete = []  # files to delete/modify
        commit = []  # files to be committed into db
        for _, _, files in walk(self.folder):
            for file in files:
                print(file)
            for file in files:
                ''' passes the filename down '''
                ret = self.file_safe(file) \
                    and self.yaml_safe(file)
                if not ret:  # and db_safe()
                    delete.append(file)
                else:
                    commit.append(file)
        self.files_delete(delete)
        return commit

    def files_delete(self, files):
        ''' verify delete from user before removal '''
        check = "({:02}/{}) Delete {}?: "
        keywords = ["yes", "no"]
        for i in range(len(files)):
            confirm = input(check.format(
                i+1,
                len(files),
                files[i]))
            if confirm in keywords:
                pass
                #TODO -- deletion
            #elif TODO: -- modification
            else:
                pass
                #TODO -- skip

    def file_safe(self, file):
        ''' calls file checks in order of serial encounter '''
        return self.file_regex(file) \
            and self.file_read(file) \
            and self.file_load(file)

    @printer(False)
    @truefalse
    def file_regex(self, file):
        ''' checks file name match,non empty file,syntax '''
        regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
        return re.compile(regex).match(file)

    @printer(False)
    @truefalse
    def file_read(self, file):
        ''' check file content and creates a valid yaml obj '''
        with open(self.folder+file) as f:
            return f.read()

    @printer(False)
    @tryexcept
    def file_load(self, file):
        ''' check file is a yaml object after file load '''
        with open(self.folder+file) as f:
            return isinstance(yaml.load(f.read()), Reciept)

    def yaml_read(self, file):
        ''' creates and returns yaml object '''
        with open(self.folder+file) as f:
            return yaml.load(f.read())

    @printer(True)
    def yaml_safe(self, file):
        ''' check contents of yaml object '''
        obj = self.yaml_read(file)
        return self.yaml_store(file, obj) \
            and self.yaml_date(file, obj) \
            and self.yaml_prod(file, obj) \
            and self.yaml_card(file, obj)

    @printer(False)
    @tryexcept
    def yaml_store(self, file, obj):
        ''' check yaml store with store in filename '''
        fname = file.split('.')[0].split('-')[1]
        store = obj.store.replace(" ", "").lower()
        return fname in store

    @printer(False)
    @tryexcept
    def yaml_date(self, file, obj):
        ''' check yaml date with file date '''
        y, m, d = obj.date
        start, end = date(2017, 1, 1), date.today()
        filedate = date(obj.date[0], obj.date[1], obj.date[2])
        return start < filedate < end

    @printer(False)
    def yaml_prod(self, file, obj):
        ''' iterate through yaml object[prod]:{str:int,[...]} '''
        for key in obj.prod.keys():
            if not isinstance(key, str):
                return False
            if len(key) > 25:
                return False
            if not isinstance(obj.prod[key], float):
                return float
            if len(str(obj.prod[key])) > 6:
                return False
            return True

    @printer(False)
    @tryexcept
    def yaml_card(self, file, obj):
        ''' check payment identifiers in yaml object '''
        get = [obj.prod[key] for key in obj.prod.keys()]
        get = int(sum(get)*100)
        sub = int(obj.sub*100)
        add = int((obj.sub+obj.tax)*100)
        tot = int(obj.tot*100)
        return True if get == sub and add == tot else False


if __name__ == "__main__":
    ''' Check input args - exit if incorrect '''
    if len(sys.argv) < 2:
        print("incorrect args")
        exit(-1)
    ''' Setup basic logger '''
    logging.basicConfig(
            filename='debug.log',
            format='%(message)s',
            level=logging.DEBUG)
    logging.info("Checking Files")
    print(YamlChecker(sys.argv[1]).files_safe())
