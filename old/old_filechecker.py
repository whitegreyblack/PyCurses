import os
import re
import sys
import yaml
import logging
import datetime
import functools
from reciept import Reciept
import strings_checker as strings

# logging info
FORMAT = '%(message)s'
logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
logging.debug("-- LOGGER :- FileChecker() --")

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
                    logging.debug("[{}]({:02}):- {}".format(
                        strings.passfail[fn.__name__][ret],
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

# handles non-true/false returns and converts into true or false values
def truefalse(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):        
        return True if fn(*args, **kwargs) else False
    return wrapper    

class YamlChecker:
    """ Iterates through each yaml file in target folder and checks for 
        file and yaml syntax and context before returning a list of 
        verified files to be used in insertion into database 
    """

    def __init__(self, folder='reciepts'):
        """ initialize the folder holding files to check """
        FORMAT = '%(message)s'
        logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
        logging.debug("-- LOGGER :- FileChecker() --")
        self.folder = folder
        self.files = sum([1 for _, _, files in os.walk(folder) for f in files])

    def fs_safe_timed(self):
        delete = []
        commit = []
        for _, _, files in os.walk(self.folder):
            pass

    def fs_safe(self):
        """ iterate through each file in directory """
        delete = []
        commit = []
        for _, _, files in os.walk(self.folder):
            for f in files:
                # will pass down an existing file name in directory
                if not (self.f_safe(f) and self.y_safe(f)):
                    delete.append(f)
                else:
                    commit.append(f)
        #self.fs_delete(delete)
        return commit

    def fs_delete(self, files):
        """ verify delete from user before removal """
        for i in range(len(files)):
            query = "{:02})/{:02}) Delete {}?: "
            if input(query.format(i+1,len(files), files[i]))=="yes":
                    pass

    def f_safe(self, file):
        """ calls file checks in order of serial encounter """
        return self.f_regex(file) and self.f_read(file) and self.f_load(file)

    @printer(False)
    @truefalse
    def f_regex(self, file):
        """ checks file name match & non empty file & syntax correctness """ 
        return re.compile("[0-9]{6}-[a-z]{,25}\.yaml").match(file)

    def f_open(self, file):
        """ returns contents of parameter file """
        with open(self.folder+file) as f: return f.read()

    @printer(False)
    @truefalse
    def f_read(self, file):
        """ check file is not empty and creates a valid yaml obj """
        return self.f_open(file)

    @printer(False)
    @tryexcept
    def f_load(self, file):
        """ check file is a yaml object after file load """
        return isinstance(yaml.load(self.f_open(file)), Reciept)

    #@printer(False)
    @tryexcept
    def y_read(self, file):
        """ creates and returns yaml object """
        with open(self.folder+file) as f:
            return yaml.load(f.read())
    
    @printer(True)
    def y_safe(self, f):
        """ check contents of yaml object """
        o = self.y_read(f)
        return self.y_store(f, o) and self.y_date(f, o) and self.y_prod(f, o) and self.y_card(f, o)

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
        start, end = datetime.date(2017,1,1), datetime.date.today()
        return start < datetime.date(o.date[0], o.date[1], o.date[2]) <= end

    @printer(False)
    def y_prod(self, file, obj):
        """ check prod identifier in yaml object """
        """ iterate through yaml object[prod]:{str:int,[...]} """
        instances = [not(isinstance(key, str) and isinstance(obj.prod[key], float)) for key in obj.prod.keys()]
        return False if any(instances) else True
    
    @printer(False)
    @tryexcept
    def y_card(self, file, obj):
        """ check payment identifiers in yaml object """
        get = int(sum([obj.prod[key] for key in obj.prod.keys()])*100)
        sub = int(obj.sub*100)
        add = int((obj.sub+obj.tax)*100)
        tot = int(obj.tot*100)
        return True if get == sub and add == tot else False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.debug("Folder To Use Empty")
        logging.debug("Debug File Unspecified")
        exit(-1)
    check = YamlChecker(sys.argv[1])
    print(check.fs_safe())
