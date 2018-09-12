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
    def __init__(self, folder='reciepts'):
        logging.basicConfig(filename='yamlchecker.log', level=logging.INFO)
        logging.info(border)
        logging.info(f"{self.__class__.__name__}: Initializing yaml checker")
        self.folder = folder
        self.startdate = None
        logging.info(f"{self.__class__.__name__}: Initialized yaml checker")

    def __del__(self):
        logging.info(f"{self.__class__.__name__}: Deleting yaml checker")
        logging.info(border)

    @wrap.trace
    def files_safe(self):
        # iterate through each file in directory
        delete = []  # files to delete/modify
        commit = []  # files to be committed into db
        logging.info("".join(wrap.spacer) + "Using: {}".format(self.folder))
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

    @wrap.trace
    def file_safe(self, file):
        # calls file checks in order of serial encounter
        logging.info(f"{''.join(wrap.spacer)}Using: {file}")
        return (self.file_regex(file)
            and self.file_read(file)
            and self.file_load(file))

    @wrap.trace
    @wrap.printer(False)
    @wrap.truefalse
    def file_regex(self, file):
        ''' checks file name match,non empty file,syntax '''
        regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
        matches = re.compile(regex).match(file)
        logging.info("\t{} matches regex: {}".format(
            file, matches is not None))
        return re.compile(regex).match(file)

    @wrap.trace
    @wrap.printer(False)
    @wrap.truefalse
    def file_read(self, file):
        ''' check file content and assert not empty '''
        with open(self.folder + file) as f:
            lines = f.read()
            logging.info("\t{} was read: {}".format(file, lines is not None))
            return lines

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def file_load(self, file_name):
        ''' check file is a yaml object after file load '''
        logging.info(f"\tOpening file for reading: {self.folder + file_name}")
        with open(self.folder + file_name) as yamlfile:
            logging.info("\tReading lines from yaml file")
            lines = yamlfile.read()
            logging.info("\tFinished reading lines")
            logging.info("\tLoading lines into yaml loader")
            yamlobj = yaml.load(lines)
            logging.info("\tLoaded yaml object")
            valid_yaml = isinstance(yamlobj, yaml.YAMLObject)
            logging.info(f"\tValid YamlObject: {valid_yaml}")
            return isinstance(yamlobj, yaml.YAMLObject)

    @wrap.trace
    def yaml_read(self, file):
        ''' creates and returns yaml object '''
        with open(self.folder + file) as f:
            obj = yaml.load(f.read())
            valid_yaml = isinstance(obj, Reciept)
            logging.info(f"\tValid YamlObject: {valid_yaml}")
            return obj

    @wrap.trace
    @wrap.printer(False)
    def yaml_safe(self, file):
        ''' check contents of yaml object '''
        obj = self.yaml_read(file)
        return (self.yaml_store(file, obj)
                and self.yaml_date(file, obj)
                and self.yaml_prod(file, obj)
                and self.yaml_card(file, obj))

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
    def yaml_store(self, file, obj):
        ''' check yaml store with store in filename '''
        fname = file.split('.')[0].split('-')[1]
        store = obj.store.replace(" ", "").lower()
        logging.info('\tStore Name: {}'.format(fname))
        logging.info('\t{} in {}: {}'.format(fname, store, (fname in store)))
        return fname in store

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
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

    @wrap.trace
    @wrap.printer(False)
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

    @wrap.trace
    @wrap.printer(False)
    @wrap.tryexcept
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
    logging.basicConfig(filename="yamlchecker.log", level=logging.INFO)

    # check required input args -- exit if incorrect
    if not f:
        print('ERROR: incorrect arg - no input folder flag and arg specified')
        print(usage()) 
        exit()

    logging.info(border)
    logging.info("main(): checking files")

    c, d = YamlChecker(f.replace("\\", '/')).files_safe()

    logging.info("main(): files to delete:")
    for i in d:
        logging.info(wrap.tab + i)

    logging.info("main(): files to commit:")
    for i in c:
        logging.info(wrap.tab + i)

    logging.info("main(): completed checking files")
    logging.info(border)

if __name__ == "__main__":
    main()
