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
import source.decorators as wrap
from os import walk
from datetime import date
from source.YamlObjects import Reciept
import source.utils as utils

border = "-" * 80

class YamlChecker:
    """Processes yaml files in specified folder for both file integrity and
    yaml safe syntax
    """

    logger_name = 'filechecker'
    logger_file = 'filechecker.log'
    logger_args = {'currentfile': __file__}

    file_extensions = [".yaml",]

    def __init__(self, folder='reciepts', logger=None):
        self.logargs = {'classname': self.__class__.__name__}

        self.logger = logger
        if not self.logger:
            logger.info("no logger")
            self.logger = utils.setup_logger(YamlChecker.logger_name,
                                             YamlChecker.logger_file,
                                             extra=YamlChecker.logger_args)

        self.log("Initializing yaml checker")

        self.folder = folder
        self.startdate = None

        self.log(f"Initialized yaml checker: folderpath '{self.folder}'")

    def __exit__(self):
        self.log("Deleting yaml checker object")

    def log(self, message):
        self.logger.info(f"{self.__class__.__name__}: {message}")

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
        self.log(f"Number of files to commit: {len(commit)}") 
        for filename in commit:
            self.log(f"\t+ {filename}")
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

    def file_safe(self, file):
        """Calls file checks in order of serial encounter"""
        self.log(f"{''.join(wrap.spacer)}Using: {file}")
        return (self.file_regex(file)
            and self.file_read(file)
            and self.file_load(file))

    @wrap.truefalse
    def file_regex(self, file):
        """Checks file name match,non empty file,syntax"""
        regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
        matches = re.compile(regex).match(file)
        self.log("{} matches regex: {}".format(
            file, matches is not None))
        return re.compile(regex).match(file)

    @wrap.truefalse
    def file_read(self, file):
        """Check file content and assert not empty"""
        with open(self.folder + file) as f:
            lines = f.read()
            self.log("{} was read: {}".format(file, lines is not None))
            return lines

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

    def yaml_read(self, file):
        """Creates and returns yaml object"""
        with open(self.folder + file) as f:
            obj = yaml.load(f.read())
            valid_yaml = isinstance(obj, Reciept)
            self.log(f"Valid YamlObject: {valid_yaml}")
            return obj

    def yaml_safe(self, filepath):
        """Check contents of yaml object"""
        obj = self.yaml_read(filepath)
        return (self.yaml_store(filepath, obj)
                and self.yaml_date(filepath, obj)
                and self.yaml_prod(filepath, obj)
                and self.yaml_card(filepath, obj))

    @wrap.tryexcept
    def yaml_store(self, file, obj):
        """Check yaml store with store in filename"""
        fname = file.split('.')[0].split('-')[1]
        store = obj.store.replace(" ", "").lower()
        self.log('Store Name: {}'.format(fname))
        self.log('{} in {}: {}'.format(fname, store, (fname in store)))
        return fname in store

    @wrap.tryexcept
    def yaml_date(self, file, obj):
        """Check yaml date with file date"""
        y, m, d = obj.date

        if not self.startdate:
            self.startdate = date(y, m, d)

        end = date.today()
        filedate = date(y, m, d)

        self.log(f"\tStart Date: {self.startdate.isoformat()}")
        self.log(f"\tFile Date: {filedate.isoformat()}")
        self.log(f"\tEnd Date: {end.isoformat()}")

        return self.startdate <= filedate < end

    def yaml_prod(self, file, obj):
        """iterate through yaml object[prod]:{str:int,[...]}"""
        self.log(f"Checking product and price syntax.")
        for product, price in obj.products.items():
            # TODO -- better if statements, early exit on condition match
            nonstring = not isinstance(product, str)
            invalidlen = 2 <= len(product) <= 25
            nonfloat = not isinstance(price, float)
            invalid_v_len = len(str(price)) > 6
            
            self.log(f"\t'{product}': '{price}'")

            if not isinstance(product, str):
                self.log(f"\tProduct '{product}' is not a string object")
                return False

            if len(product) > 25:
                self.log(f"\tProduct '{product}' length is too long")
                return False

            if not isinstance(price, float):
                self.log(f"\tPrice '{price}' for '{product}' is not float")
                return False

            if len(str(price)) > 6:
                self.log(f"\tPrice '{price}' is too long")
                return False

        self.log(f"Number of products passed: {len(obj.products.keys())}")
        return True

    @wrap.tryexcept
    def yaml_card(self, file, obj):
        """check payment identifiers in yaml object"""
        def mul(x):
            return x * 100

        get = [obj.products[key] for key in obj.products.keys()]
        get = int(mul(sum(get)))
        subtotal = int(mul(obj.subtotal))
        add = int(mul(obj.subtotal + obj.tax))
        total = int(mul(obj.total))

        self.log(f"\tcalculated subtotal: {get}")
        self.log(f"\tobject subtotal: {subtotal}")
        self.log(f"\ttax: {int(mul(obj.tax))}")
        self.log(f"\ttotal: {total}")

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

    logger = utils.setup_logger('yamlcheck', 
                                'filechecks.log',
                                extra={'currentfile': __file__})

    filepath = utils.format_directory_path(f)
    if not utils.check_directory_path(filepath):
        print(filepath)
        print('ERROR: File specified is not a directory')
        exit()

    logger.info(f"checking files in {filepath}")
    checker = YamlChecker(filepath, logger)
    commits, deletes = checker.files_safe()
    
    if deletes:
        logger.info("files to delete:")
        for delete in deletes:
            logger.info(wrap.tab + delete)

    if commits:
        logger.info("files to commit:")
        for commit in commits:
            logger.info('+' + wrap.tab + commit)

    logger.info("completed checking files")

if __name__ == "__main__":
    main()
