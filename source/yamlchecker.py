"""yamlchecker.py 
YamlChecker provides methods to iterate through and validate
yaml files. It can be used as a stand alone script to check
the files as they are written for any errors. Used before
inserting data into the database.
"""

__author__ = "Samuel Whang"

import re
import os
import yaml
import click
import logging
import datetime
from collections import namedtuple

import source.utils as utils
import source.config as config
import source.decorators as wrap
from source.YamlObjects import Reciept

# TODO: change verbiage from '(UN)COMMIT' -> '(UN)VERIFIED' 
#       commit should only be used in relation to db loads

class YamlChecker:
    """Processes yaml files in specified folder for both file integrity and
    yaml safe syntax
    """

    logger_name = "filechecker"
    logger_file = "filechecker.log"
    logger_args = {"currentfile": __file__}

    def __init__(self, folder="reciepts", logger=None):
        self.logargs = {'classname': self.__class__.__name__}

        self.logger = logger
        if not self.logger:
            self.logger = utils.setup_logger(YamlChecker.logger_name,
                                             YamlChecker.logger_file,
                                             extra=YamlChecker.logger_args)
            self.log("No logger passed into constructor. Creating new logger.")

        self.folder = folder
        if not self.folder:
            raise ValueError("Folder parameter cannot be none")

        self.verified = []
        self.unverified = []
        self.skipped = []

        self.log(f"Initialized YamlChecker. Using folderpath: '{self.folder}'")

    def __exit__(self):
        self.log("Deleting yaml checker object")

    @property
    def verified_files(self):
        return { vf: self.yaml_read(vf) for vf in self.verified }

    def log(self, message, level=logging.INFO):
        """Prints the message to the logger instead of to the terminal as with 
        logging level of INFO.
        """
        formatted_message = f"{self.__class__.__name__}: {message}"
        if level == logging.INFO:
            self.logger.info(formatted_message)
        elif level == logging.WARNING:
            self.logger.warning(formatted_message)
        else:
            raise ValueError("Parameter level does not match logging levels")

    def verify_file_states(self, loaded_files=None):
        """Iterate through each file in directory to verify if the file is
        safe to load into the database.

        Args:
            loaded_files => file names pulled from database passed in to 
                            skip future checking and loading during the 
                            verification process.
        """
        def convert_int(floatval):
            return int(floatval * 100)
        commit = []
        change = []
        skipped = []

        for _, _, files in os.walk(self.folder):
            sortedfiles = sorted(files)
            self.log(f"Verifying {len(sortedfiles)} files")
            for file_name in files: 
                filename, extension = utils.filename_and_extension(file_name)

                # check for dot files in the verify beginning
                if file_name[0] == ".":
                    error = f"{file_name} begins with a dot. Skipping."
                    self.log(error)
                    skipped.append(error)
                    continue

                # verify file not already loaded in db. 
                # if true then skip over to next file
                if loaded_files and filename in loaded_files:
                    self.log(f"File is already loaded. Skipping.")
                    skipped.append(filename)
                    continue

                # verify file extension is yaml
                if extension != config.YAML_FILE_EXTENSION:
                    error = f"{filename}: is not a yaml file."
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue
                
                # now check regex for filename
                regex = re.compile(config.YAML_FILE_NAME_REGEX)
                if not regex.match(filename):
                    error = f"{filename} does not match the config file regex"
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue

                # try opening the files without error
                try:
                    with open (self.folder + file_name) as f:
                        lines = f.read()
                except Exception as e:
                    change.append(e)
                    continue

                # try loading the lines if not an empty file
                if not lines:
                    error = f"{filename} is an empty file. Nothing to read"
                    self.log(error, level=logging.WARNING)
                    change.append(e)
                    continue

                try:
                    yamlobj = yaml.load(lines)
                except Exception as e:
                    self.log(e, level=Logging.WARNING)
                    change.append(e)
                    continue

                # check all properties in the object for non null existance
                attributeError = False
                propertyTypeError = False
                validationError = False
                for prop, (types, vdter, fmter) in yamlobj.properties.items():
                    try:
                        p = getattr(yamlobj, prop)
                    except AttributeError:
                        attributeError = True
                        break
                    
                    if not isinstance(p, types):
                        propertyTypeError = True
                        break

                    if vdter:
                        if not vdter(filename, p):
                            validationError = True
                            break

                    if fmter:
                        newval = fmter(filename, p)
                        setattr(yamlobj, prop, newval)

                # some reason the property got an attribute error
                if attributeError:
                    error = f"{filename}: missing reciept property '{prop}'"
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue

                # some reason the property type failed
                if propertyTypeError:
                    if isinstance(types, (list, tuple)):
                        ptypes = ", ".join(str(t) for t in ptype)
                    else:
                        ptypes = types
                    error = f"{filename}: {prop} is not of type(s) {ptypes}"
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue

                # some reason property failed validation
                if validationError:
                    error = f"{filename}: {prop} failed validation. Check property"
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue

                transactionError = False
                productSumInt = convert_int(sum(yamlobj.products.values()))
                subtotalInt = convert_int(yamlobj.subtotal)
                subtotalError = productSumInt != subtotalInt

                subtaxInt = convert_int(yamlobj.subtotal + yamlobj.tax)
                totalInt = convert_int(yamlobj.total)
                subtaxtotalError = subtaxInt != totalInt

                paymentInt = convert_int(yamlobj.payment)
                totalpayError = totalInt != paymentInt

                if subtotalError or subtaxtotalError or totalpayError:
                    transactionError = True

                if transactionError:
                    error = f"{filename}: "
                    if subtotalError:
                        error += "Product subtotal does not match reciept subtotal. "
                        error += f"Got: {sum(yamlobj.products.values())} != {yamlobj.subtotal}"
                    elif subtaxtotalError:
                        error += "Subtotal and tax does not match total. "
                        error += f"Got: {yamlobj.subtotal + yamlobj.tax} != {yamlobj.total}"
                    else:
                        error += "Total does not match payment. "
                        error += f"Got: {yamlobj.total} != {yamlobj.payment}"
                    self.log(error, level=logging.WARNING)
                    change.append(error)
                    continue

                # all properties came back with a value. now check that value
                self.log(f"  + Verified {filename}")
                commit.append(filename)

            self.verified = [c + '.yaml' for c in commit]

            return {
                "COMMITTED": commit,
                "SKIPPED": skipped,
                "UNCOMMITTED": change,
                }

    def files_safe(self, loaded_files=None):
        """Iterate through each file in directory to verify if the file is
        safe to load into the database.

        2018-9-25: Function now depracated. Should use verify_file_states()
        instead.
        """
        self.log(f"Verifying yaml files in '{self.folder}'")

        delete = []  # files to delete/modify
        commit = []  # files to be committed into db
        for _, _, files in os.walk(self.folder):
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
        self.log(f"Number of files uncommmitted: {len(delete)}")
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
        return obj

    def yaml_safe(self, filepath):
        """Check contents of yaml object"""
        obj = self.yaml_read(filepath)

        # just because no error is raised when checking object does not mean
        # object is a correct Reciept object. Only that all values have been
        # loaded and no syntax errors found. Still need to check properties.
        valid_yaml = isinstance(obj, Reciept)
        self.log(f"Valid YamlObject: {valid_yaml}")

        for prop in obj.properties:
            try:
                getattr(obj, prop)
            except AttributeError as e:
                self.log(e)
                return False
        
        self.startdate = None
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

    def yaml_date(self, file, obj):
        """Check yaml date with file date"""
        try: 
            y, m, d = obj.date

            if not self.startdate:
                self.startdate = datetime.date(y, m, d)

            end = datetime.date.today()
            filedate = datetime.date(y, m, d)

            self.log(f"\tStart Date: {self.startdate.isoformat()}")
            self.log(f"\tFile Date: {filedate.isoformat()}")
            self.log(f"\tEnd Date: {end.isoformat()}")

            return self.startdate <= filedate < end
        except Exception as e:
            self.log(e)
            return False

    def yaml_prod(self, file, obj):
        """iterate through yaml object[prod]:{str:int,[...]}"""
        self.log(f"Checking product and price syntax.")
        if not hasattr(obj, 'products'):
            self.log(f"\tThis file has no products property")
            return False

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
USAGE: -f [ arg ] [ -p ]
    -f  => folder flag with expecting argument
    arg => folder name containing yaml files
    -p  => print mode flag
"""[1:]

def log(logger, message, consoleprint):
    """Prints messages in info mode. If consoleprint is true then also prints
    to terminal as well.
    """
    logger.info(message)
    if consoleprint:
        print(message)

def log_file_results(logger, batches, toconsole):
    totalfiles = sum(len(batch) for batch in batches.values())
    totalmessage = f"Total number of files checked: {totalfiles}"
    log(logger, totalmessage, toconsole)

    for batchtype, batch in batches.items():
        if batch:
            batchmessage = config.YAML_CHECKER_BATCH_MSG.format(batchtype,
                                                                len(batch))
            log(logger, batchmessage, toconsole)
            for index, b in enumerate(batch):
                symbol = config.YAML_CHECKER_BATCH_SYMBOL[batchtype]
                message = config.YAML_CHECKER_FILE_MSG.format(symbol,
                                                              index + 1,
                                                              len(batch),
                                                              b)
                log(logger, message, toconsole)
        else:
            batchmessage = config.YAML_CHECKER_NO_BATCH.format(batchtype)
            log(logger, batchmessage, toconsole)

@click.command()
@click.option('-f', nargs=1, type=str, help="folder holding yaml data files")
@click.option('-p', is_flag=True, help="print results to terminal screen")
def main(f, p):
    # check required input args -- exit if incorrect
    if not f:
        print("ERROR: incorrect arg - no input folder flag and arg specified")
        print(usage()) 
        exit()

    logger = utils.setup_logger("yamlcheck",
                                "filechecks.log",
                                extra={'currentfile': __file__})

    filepath = utils.format_directory_path(f)
    if not utils.check_directory_path(filepath):
        print(filepath)
        print("ERROR: File specified is not a directory")
        exit()

    checker = YamlChecker(filepath, logger)
    fileresults = checker.verify_file_states()

    log_file_results(logger, fileresults, p)

if __name__ == "__main__":
    main()
