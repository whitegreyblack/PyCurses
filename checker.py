from os import walk, remove
import re
import sys
from reciept_yaml import Reciept
from strings_checker import strings
import logging
import yaml
import functools
from datetime import date

# used by printer to print number of files printed
f_num = 1
# to printer -- create second to printer
def printer(enabled):
    def wrapper(fn):
        @functools.wraps(fn)
        def log(*args, **kwargs):
            global f_num
            ret = fn(*args, **kwargs)
            if enabled == ret:
                try:
                    print("[{}]({:02}):- {}".format(strings[fn.__name__][ret],
                        f_num,args[1].split('.')[0]))
                    f_num += 1
                except:
                    raise
            return ret
        return log
    return wrapper

# handles exceptions and returns false instead
def tryexcept(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except:
            return False
    return wrapper

def truefalse(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):        
        return True if fn(*args, **kwargs) else False
    return wrapper    

class YamlChecker:

    def __init__(self, folder='reciepts'):
        """ initialize the folder holding files to check """
        self.folder = folder

    def fs_safe(self):
        """ iterate through each file in directory """
        delete = []
        commit = []
        for _, _, files in walk(self.folder):
            for file in files:
                # will pass down an existing file name in directory
                if not (self.f_safe(file) and self.y_safe(file)): # and db_safe()
                    delete.append(file)
                else:
                    commit.append(file)
        self.fs_delete(delete)
        return commit

    def fs_delete(self, files):
        """ verify delete from user before removal """
        for i in range(len(files)):
            if input("({:02}/{:02}) Delete {}?: ".format(
                i+1,len(files), files[i]))=="yes":
                pass

    def f_safe(self, file):
        """ calls file checks in order of serial encounter """
        return self.f_regex(file) and self.f_read(file) and self.f_load(file)

    @printer(False)
    @truefalse
    def f_regex(self, file):
        """ checks file name match & non empty file & syntax correctness """ 
        return re.compile("[0-9]{6}-[a-z]{,25}\.yaml").match(file)

    @printer(False)
    @truefalse
    def f_read(self, file):
        """ check file is not empty and creates a valid yaml obj """
        with open(self.folder+file) as f:
            return f.read()

    @printer(False)
    @tryexcept
    def f_load(self, file):
        """ check file is a yaml object after file load """
        with open(self.folder+file) as f:
            return isinstance(yaml.load(f.read()), Reciept)

    def y_read(self, file):
        """ creates and returns yaml object """
        with open(self.folder+file) as f:
            return yaml.load(f.read())
    
    @printer(True)
    def y_safe(self, f):
        """ check contents of yaml object """
        o = self.y_read(f)
        return self.y_store(f, o) and self.y_date(f, o) and self.y_prod(f, o)

    @printer(False)
    @tryexcept
    def y_store(self, f, o):
        """ check store identifier in yaml object """
        return f.split('.')[0].split('-')[1] in o.store.replace(" ","").lower()

    @printer(False)
    @tryexcept
    def y_date(self, f, o):
        """ check date identifier in yaml object """
        y, m , d = o.date
        start, end = date(2017,1,1), date.today()
        return start < date(o.date[0], o.date[1], o.date[2]) < end

    def y_prod(self, file, obj):
        """ check prod identifier in yaml object """
        """ iterate through yaml object[prod]:{str:int,[...]} """
        for key in obj.prod.keys():
            val = obj.prod[key]
            return True

if __name__ == "__main__":
    FORMAT = '%(message)s'
    logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
    logging.info("Checking Files")
    check = YamlChecker(sys.argv[1]) if len(sys.argv) == 2 else YamlChecker('testfolder/')
    print(check.fs_safe())
    #check = YamlChecker('testfolder/')
    #print(check.fs_safe())
    #print(YamlChecker('testfolder/').fs_safe())
