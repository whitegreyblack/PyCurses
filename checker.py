from os import walk, remove
import re
from reciept_yaml import Reciept
from strings_checker import strings
import logging
import yaml
import functools
from datetime import date

# used by printer to print number of files printed
file_num = 1
# to printer -- create second to printer
def printer(enabled):
    def wrapper(fn):
        @functools.wraps(fn)
        def log(*args, **kwargs):
            global file_num
            ret = fn(*args, **kwargs)
            if enabled == ret:
                try:
                    print("[{}]({:02}):- {}".format(strings[fn.__name__][ret],
                        file_num,args[1].split('.')[0].split('-')[1]))
                    file_num += 1
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

    def files_safe(self):
        """ iterate through each file in directory """
        delete = []
        commit = []
        for _, _, files in walk(self.folder):
            for file in files:
                # will pass down an existing file name in directory
                if not (self.file_safe(file) and self.yaml_safe(file)): # and db_safe()
                    delete.append(file)
                else:
                    commit.append(file)
        self.files_delete(delete)
        return commit

    def files_delete(self, files):
        """ verify delete from user before removal """
        for i in range(len(files)):
            if input("({:02}/{}) Delete {}?: ".format(
                i+1,len(files), files[i]))=="yes":
                pass

    def file_safe(self, file):
        """ calls file checks in order of serial encounter """
        return self.file_regex(file) and self.file_read(file) and self.file_load(file)

    @printer(False)
    @truefalse
    def file_regex(self, file):
        """ checks file name match & non empty file & syntax correctness """ 
        return re.compile("[0-9]{6}-[a-z]{,25}\.yaml").match(file)

    @printer(False)
    @truefalse
    def file_read(self, file):
        """ check file is not empty and creates a valid yaml obj """
        with open(self.folder+file) as f:
            return f.read()

    @printer(False)
    @tryexcept
    def file_load(self, file):
        """ check file is a yaml object after file load """
        with open(self.folder+file) as f:
            return isinstance(yaml.load(f.read()), Reciept)

    def yaml_read(self, file):
        """ creates and returns yaml object """
        with open(self.folder+file) as f:
            return yaml.load(f.read())
    
    @printer(True)
    def yaml_safe(self, file):
        """ check contents of yaml object """
        obj = self.yaml_read(file)
        name = self.yaml_store(file, obj)
        date = self.yaml_date(file, obj)
        prod = self.yaml_prod(file, obj)
        return name and date and prod

    @printer(False)
    @tryexcept
    def yaml_store(self, file, obj):
        return file.split('.')[0].split('-')[1] in obj.store.replace(" ","").lower()

    @printer(False)
    @tryexcept
    def yaml_date(self, file, obj):
        y, m , d = obj.date
        start, end = date(2017,1,1), date.today()
        return start < date(obj.date[0], obj.date[1], obj.date[2]) < end

    def yaml_prod(self, file, obj):
        """ iterate through yaml object[prod]:{str:int,[...]} """
        for key in obj.prod.keys():
            val = obj.prod[key]
            return True

if __name__ == "__main__":
    FORMAT = '%(message)s'
    logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
    logging.info("Checking Files")
    #check = YamlChecker('testfolder/')
    #print(check.files_safe())
    print(YamlChecker('testfolder/').files_safe())