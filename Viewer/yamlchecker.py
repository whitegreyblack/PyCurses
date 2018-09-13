"""
yamlchecker.py: YamlChecker provides methods to iterate through and validate
                yaml files. It can be used as a stand alone script to check
                the files as they are written for any errors. Used before
                inserting data into the database.
"""

__author__ = "Samuel Whang"

import re
import yaml
import click
import logging
import decorators as wrap
from os import walk
from datetime import date
from YamlObjects import Reciept
import utils

border = "-" * 80

class YamlChecker:
    def __init__(self, folder='reciepts', logger=None):
        self.logargs = {'classname': self.__class__.__name__}

        self.logger = logger
        if not self.logger:
            self.logger = utils.setup_logger(name='yamlcheckerlogger',
                                            logfile='filechecks.log')

        self.log("Initializing yaml checker")

        self.folder = folder
        self.startdate = None

        self.log(f"Initialized yaml checker: folderpath '{self.folder}'")

    def __exit__(self):
        self.log("Deleting yaml checker object")

    def log(self, message):
        self.logger.info(message, extra=self.logargs)

    @wrap.trace
    def files_safe(self):
        """Iterate through each file in directory"""
        self.log(f"Verifying yaml files in {self.folder}")
        delete = []  # files to delete/modify
        commit = []  # files to be committed into db
        for _, _, files in walk(self.folder):
            files = sorted(files)
            for file_name in files:
                filename, extension = utils.filename_and_extension(file_name)
                if extension == ".yaml":
                    # passes the filename test
                    ret = (self.file_safe(file_name) 
                           and self.yaml_safe(file_name))
                    if not ret:  # and db_safe()
                        delete.append(file_name)
                    else:
                        commit.append(file_name)
        # TODO: self.files_delete(delete)
        self.log("Finished verification")
        self.log("Number of files to commit: {len(commit)}") 
        return commit, delete

    def files_delete(self, files):
        """Verify delete from user before removal"""
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

    @wrap.trace
    def file_safe(self, file):
        """Calls file checks in order of serial encounter"""
        self.log(f"{''.join(wrap.spacer)}Using: {file}")
        return (self.file_regex(file)
            and self.file_read(file)
            and self.file_load(file))

    @wrap.trace
    @wrap.printer(False)
    @wrap.truefalse
    def file_regex(self, file):
        """Checks file name match,non empty file,syntax"""
        regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
        matches = re.compile(regex).match(file)
        self.log("{} matches regex: {}".format(
            file, matches is not None))
        return re.compile(regex).match(file)

    @wrap.trace
    @wrap.printer(False)
    @wrap.truefalse
    def file_read(self, file):
        """Check file content and assert not empty"""
        with open(self.folder + file) as f:
            lines = f.read()
            self.log("{} was read: {}".format(file, lines is not None))
            return lines

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def file_load(self, file_name):
        """check file is a yaml object after file load"""
        self.log(f"Opening file for reading: {self.folder + file_name}")
        with open(self.folder + file_name) as yamlfile:
            self.log("Reading lines from yaml file")
            lines = yamlfile.read()
            self.log("Finished reading lines")
            self.log("Loading lines into yaml loader")
            yamlobj = yaml.load(lines)
            self.log("Loaded yaml object")
            valid_yaml = isinstance(yamlobj, yaml.YAMLObject)
            self.log(f"Valid YamlObject: {valid_yaml}")
            return isinstance(yamlobj, yaml.YAMLObject)

    @wrap.trace
    def yaml_read(self, file):
        """Creates and returns yaml object"""
        with open(self.folder + file) as f:
            obj = yaml.load(f.read())
            valid_yaml = isinstance(obj, Reciept)
            self.log(f"Valid YamlObject: {valid_yaml}")
            return obj

    @wrap.trace
    @wrap.printer(False)
    def yaml_safe(self, file):
        """Check contents of yaml object"""
        obj = self.yaml_read(file)
        return (self.yaml_store(file, obj)
                and self.yaml_date(file, obj)
                and self.yaml_prod(file, obj)
                and self.yaml_card(file, obj))

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def yaml_store(self, file, obj):
        """Check yaml store with store in filename"""
        fname = file.split('.')[0].split('-')[1]
        store = obj.store.replace(" ", "").lower()
        self.log('Store Name: {}'.format(fname))
        self.log('{} in {}: {}'.format(fname, store, (fname in store)))
        return fname in store

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def yaml_date(self, file, obj):
        """Check yaml date with file date"""
        y, m, d = obj.date
        if not self.startdate:
            self.startdate = date(y, m, d)
        end = date.today()
        filedate = date(y, m, d)
        self.log('Start Date: {}\nFile Date: {}\nEnd Date: {}'.format(
            self.startdate.isoformat(),
            filedate.isoformat(),
            end.isoformat()))
        return self.startdate <= filedate < end

    @wrap.trace
    @wrap.printer(False)
    def yaml_prod(self, file, obj):
        # iterate through yaml object[prod]:{str:int,[...]}
        for key in obj.products.keys():
            if not isinstance(key, str):
                self.log(f"Product Key({key}) is not a string object")
                return False
            if len(key) > 25:
                self.log(f"key({key}) is too big")
                return False
            if not isinstance(obj.products[key], float):
                self.log(f"prod({obj.products[key]}) is not float")
                return False
            if len(str(obj.products[key])) > 6:
                self.log(f"prod({obj.products[key]}) is too big")
                return False
            self.log('{}: {}'.format(key, obj.products[key]))
        self.log(f"Products Passed: {len(obj.products.keys())}")
        return True

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def yaml_card(self, file, obj):
        # check payment identifiers in yaml object
        def mul(x):
            return x * 100
        get = [obj.products[key] for key in obj.products.keys()]
        get = int(mul(sum(get)))
        subtotal = int(mul(obj.subtotal))
        add = int(mul(obj.subtotal + obj.tax))
        total = int(mul(obj.total))
        self.log('calculated subtotal: {}\nobject subtotal: {}\ntax: {}\ntotal: {}'.format(
            get, subtotal, int(mul(obj.tax)), total))
        return get == subtotal and add == total

def usage():
    return """
USAGE: -f [arg] -[ p | l | d ]
    -f -> folder containing yaml files
    -p -> print mode flag
    -l -> logger mode flag
    -d -> debug mode flag
"""[1:]

@click.command()
@click.option('-f', help='Folder Containing Yaml Files')
@click.option('-p', is_flag=True, help='MODE: Print')
@click.option('-l', is_flag=False, help='MODE: Logger')
@click.option('-d', is_flag=False, help='MODE: Debug')
def main(f, p, l, d):
    # check required input args -- exit if incorrect
    if not f:
        print('ERROR: incorrect arg - no input folder flag and arg specified')
        print(usage()) 
        exit()

    logargs = {'classname': YamlChecker.__name__ + 'main()'}
    logger = utils.setup_logger('yamlchecker.main', 'filecheck-main.log')

    filepath = utils.format_directory_path(f)
    if not utils.check_directory_path(filepath):
        print(filepath)
        print('ERROR: File specified is not a directory')
        exit()

    logger.info(f"checking files in {filepath}", extra=logargs)
    commits, deletes = YamlChecker(filepath).files_safe()
    
    if deletes:
        logger.info("files to delete:", extra=logargs)
        for delete in deletes:
            logger.info(wrap.tab + delete, extra=logargs)

    if commits:
        logger.info("files to commit:", extra=logargs)
        for commit in commits:
            logger.info('+' + wrap.tab + commit, extra=logargs)

    logger.info("completed checking files", extra=logargs)

if __name__ == "__main__":
    main()
