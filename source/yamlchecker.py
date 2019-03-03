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
from source.logger import Loggable
from source.YamlObjects import receipt

class YamlChecker(Loggable):
    """Processes yaml files in specified folder for both file integrity and
    yaml safe syntax
    """
    def __init__(self, folder, logger=None):
        super().__init__(self, logger=logger)

        self.folder = folder
        if not self.folder:
            raise ValueError("Folder parameter cannot be None")

        self.verified = []
        self.unverified = []
        self.skipped = []

        self.log(f"Initialized YamlChecker. Using folderpath: '{self.folder}'")

    def __exit__(self):
        self.log("Deleting yaml checker object")

    @property
    def verified_files(self):
        return { vf: self.yaml_read(vf) for vf in self.verified }

    @property
    def unverified_files(self):
        return self.unverified

    def verify_file_states(self, loaded_files=None):
        """Iterate through each file in directory to verify if the file is
        safe to load into the database.

        Parameters:
            loaded_files => file names pulled from database passed in to 
                            skip future checking and loading during the 
                            verification process.
        """
        def convert_int(floatval):
            return int(floatval * 100)

        verified = []
        unverified = []
        skipped = []

        # iterate through each file in given folder path. Checks file name,
        # file extension, and contents before adding them to the verified list
        for _, _, files in os.walk(self.folder):
            # sortedfiles = sorted(files)
            self.log(f"Verifying {len(files)} files")

            for file_name in files:
                filename, extension = utils.filename_and_extension(file_name)

                # check for dot files in the verify beginning. Usually configs
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
                    unverified.append(error)
                    continue
                
                # now check regex for filename
                regex = re.compile(config.YAML_FILE_NAME_REGEX)
                if not regex.match(filename):
                    error = f"{filename} does not match the config file regex"
                    self.log(error, level=logging.WARNING)
                    unverified.append(error)
                    continue

                # try opening the files without error
                try:
                    with open (self.folder + file_name) as f:
                        lines = f.read()
                except Exception as e:
                    unverified.append(e)
                    continue

                # try loading the lines if not an empty file
                if not lines:
                    error = f"{filename} is an empty file. Nothing to read"
                    self.log(error, level=logging.WARNING)
                    unverified.append(e)
                    continue

                try:
                    yamlobj = yaml.safe_load(lines)
                except Exception as e:
                    self.log(e, level=Logging.WARNING)
                    unverified.append(e)
                    continue

                # check all properties in the object for non null existance
                attributeError = False
                propertyTypeError = False
                validationError = False
                for prop, (types, vdter, fmter) in yamlobj.properties.items():
                    # access the property. Error means not set or nonexistant
                    try:
                        p = getattr(yamlobj, prop)
                    except AttributeError:
                        attributeError = True
                        break
                    
                    # check value against the types allowable for the property
                    if not isinstance(p, types):
                        propertyTypeError = True
                        break

                    # if property came with validator, check against it
                    if vdter:
                        if not vdter(filename, p):
                            validationError = True
                            break

                    # if property came with formatter, format the value
                    if fmter:
                        newval = fmter(filename, p)
                        setattr(yamlobj, prop, newval)

                # some reason the property got an attribute error
                if attributeError:
                    error = f"{filename}: missing receipt property '{prop}'"
                    self.log(error, level=logging.WARNING)
                    unverified.append(error)
                    continue

                # some reason the property type failed
                if propertyTypeError:
                    if isinstance(types, (list, tuple)):
                        ptypes = ", ".join(str(t) for t in ptype)
                    else:
                        ptypes = types
                    error = f"{filename}: {prop} is not of type(s) {ptypes}"
                    self.log(error, level=logging.WARNING)
                    unverified.append(error)
                    continue

                # some reason property failed validation
                if validationError:
                    error = f"{filename}: {prop} failed validation. Check property"
                    self.log(error, level=logging.WARNING)
                    unverified.append(error)
                    continue

                # these are more receipt object specific checks. Could place them
                # in the receipt class as a callback handler after regular checks
                # have finished. For now keep here but remember TODO refactoring.
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
                        error += "Product sum does not match subtotal. "
                        error += f"Got: {productSumInt} != {subtotalInt}"
                    elif subtaxtotalError:
                        error += "Subtotal and tax does not match total. "
                        error += f"Got: {subtaxInt} != {totalInt}"
                    else:
                        error += "Total does not match payment. "
                        error += f"Got: {totalInt} != {paymentInt}"
                    self.log(error, level=logging.WARNING)
                    unverified.append(error)
                    continue

                # Checking finished. No errors found. Add to verified list
                self.log(f"  + Verified {filename}")
                verified.append(filename)

            # add the file extension back to the files that were verified
            self.verified = [v + ".yaml" for v in verified]

            return {
                "VERIFIED": verified,
                "SKIPPED": skipped,
                "UNVERIFIED": unverified,
            }

    # !DEPRACATED CODE! TODO: REMOVE CODE ONCE ALL FUNCTIONS HAVE BEEN MOVED
    # def files_safe(self, loaded_files=None):
    #     """Iterate through each file in directory to verify if the file is
    #     safe to load into the database.

    #     2018-9-25: Function now depracated. Should use verify_file_states()
    #     instead.
    #     """
    #     self.log(f"Verifying yaml files in '{self.folder}'")

    #     delete = []  # files to delete/modify
    #     commit = []  # files to be committed into db
    #     for _, _, files in os.walk(self.folder):
    #         files = sorted(files)
    #         for file_name in files:
    #             filename, extension = utils.filename_and_extension(file_name)

    #             if extension == ".yaml":
    #                 # passes the filename test
    #                 ret = (self.file_safe(file_name) 
    #                        and self.yaml_safe(file_name))

    #                 if not ret:  # and db_safe()
    #                     delete.append(file_name)
    #                 else:
    #                     commit.append(file_name)

    #     # TODO: self.files_delete(delete)
    #     self.log("Finished verification")
    #     self.log(f"Number of files to commit: {len(commit)}") 
    #     for filename in commit:
    #         self.log(f"\t+ {filename}")
    #     self.log(f"Number of files uncommmitted: {len(delete)}")
    #     return commit, delete

    # def files_delete(self, files):
    #     """Verify delete from user before removal"""
    #     check = "({:02}/{}) Delete {}?: "
    #     keywords = ["yes", "no"]
    #     for i in range(len(files)):
    #         confirm = input(check.format(
    #             i + 1,
    #             len(files),
    #             files[i]))
    #         if confirm in keywords:
    #             pass
    #         else:
    #             pass

    # def file_safe(self, file):
    #     """Calls file checks in order of serial encounter"""
    #     self.log(f"{''.join(wrap.spacer)}Using: {file}")
    #     return (self.file_regex(file)
    #         and self.file_read(file)
    #         and self.file_load(file))

    # @wrap.truefalse
    # def file_regex(self, file):
    #     """Checks file name match,non empty file,syntax"""
    #     regex = "[0-9]{6}-[a-z_]{,25}\.yaml"
    #     matches = re.compile(regex).match(file)
    #     self.log("{} matches regex: {}".format(
    #         file, matches is not None))
    #     return re.compile(regex).match(file)

    # @wrap.truefalse
    # def file_read(self, file):
    #     """Check file content and assert not empty"""
    #     with open(self.folder + file) as f:
    #         lines = f.read()
    #         self.log("{} was read: {}".format(file, lines is not None))
    #         return lines

    # @wrap.tryexcept
    # def file_load(self, file_name):
    #     """check file is a yaml object after file load"""
    #     self.log(f"Opening file for reading: {self.folder + file_name}")
    #     with open(self.folder + file_name) as yamlfile:
    #         self.log("Reading lines from yaml file")
    #         lines = yamlfile.read()
    #         self.log("Finished reading lines")
    #         self.log("Loading lines into yaml loader")
    #         yamlobj = yaml.safe_load(lines)
    #         self.log("Loaded yaml object")
    #         valid_yaml = isinstance(yamlobj, yaml.YAMLObject)
    #         self.log(f"Valid YamlObject: {valid_yaml}")
    #         return isinstance(yamlobj, yaml.YAMLObject)

    def yaml_read(self, file):
        """Creates and returns yaml object"""
        with open(self.folder + file) as f:
            obj = yaml.safe_load(f.read())
        return obj

    # def yaml_safe(self, filepath):
    #     """Check contents of yaml object"""
    #     obj = self.yaml_read(filepath)

    #     # just because no error is raised when checking object does not mean
    #     # object is a correct receipt object. Only that all values have been
    #     # loaded and no syntax errors found. Still need to check properties.
    #     valid_yaml = isinstance(obj, receipt)
    #     self.log(f"Valid YamlObject: {valid_yaml}")

    #     for prop in obj.properties:
    #         try:
    #             getattr(obj, prop)
    #         except AttributeError as e:
    #             self.log(e)
    #             return False
        
    #     self.startdate = None
    #     return (self.yaml_store(filepath, obj)
    #             and self.yaml_date(filepath, obj)
    #             and self.yaml_prod(filepath, obj)
    #             and self.yaml_card(filepath, obj))

    # @wrap.tryexcept
    # def yaml_store(self, file, obj):
    #     """Check yaml store with store in filename"""
    #     fname = file.split('.')[0].split('-')[1]
    #     store = obj.store.replace(" ", "").lower()
    #     self.log('Store Name: {}'.format(fname))
    #     self.log('{} in {}: {}'.format(fname, store, (fname in store)))
    #     return fname in store

    # def yaml_date(self, file, obj):
    #     """Check yaml date with file date"""
    #     try: 
    #         y, m, d = obj.date

    #         if not self.startdate:
    #             self.startdate = datetime.date(y, m, d)

    #         end = datetime.date.today()
    #         filedate = datetime.date(y, m, d)

    #         self.log(f"\tStart Date: {self.startdate.isoformat()}")
    #         self.log(f"\tFile Date: {filedate.isoformat()}")
    #         self.log(f"\tEnd Date: {end.isoformat()}")

    #         return self.startdate <= filedate < end
    #     except Exception as e:
    #         self.log(e)
    #         return False

    # def yaml_prod(self, file, obj):
    #     """iterate through yaml object[prod]:{str:int,[...]}"""
    #     self.log(f"Checking product and price syntax.")
    #     if not hasattr(obj, 'products'):
    #         self.log(f"\tThis file has no products property")
    #         return False

    #     for product, price in obj.products.items():
    #         nonstring = not isinstance(product, str)
    #         invalidlen = 2 <= len(product) <= 25
    #         nonfloat = not isinstance(price, float)
    #         invalid_v_len = len(str(price)) > 6
            
    #         self.log(f"\t'{product}': '{price}'")

    #         if not isinstance(product, str):
    #             self.log(f"\tProduct '{product}' is not a string object")
    #             return False

    #         if len(product) > 25:
    #             self.log(f"\tProduct '{product}' length is too long")
    #             return False

    #         if not isinstance(price, float):
    #             self.log(f"\tPrice '{price}' for '{product}' is not float")
    #             return False

    #         if len(str(price)) > 6:
    #             self.log(f"\tPrice '{price}' is too long")
    #             return False

    #     self.log(f"Number of products passed: {len(obj.products.keys())}")
    #     return True

    # @wrap.tryexcept
    # def yaml_card(self, file, obj):
    #     """check payment identifiers in yaml object"""
    #     def mul(x):
    #         return x * 100

    #     get = [obj.products[key] for key in obj.products.keys()]
    #     get = int(mul(sum(get)))
    #     subtotal = int(mul(obj.subtotal))
    #     add = int(mul(obj.subtotal + obj.tax))
    #     total = int(mul(obj.total))

    #     self.log(f"\tcalculated subtotal: {get}")
    #     self.log(f"\tobject subtotal: {subtotal}")
    #     self.log(f"\ttax: {int(mul(obj.tax))}")
    #     self.log(f"\ttotal: {total}")

    #     return get == subtotal and add == total

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
    """Log function specific to yamlchecker to view file results from class"""
    totalfiles = sum(len(batch) for batch in batches.values())
    totalmessage = config.YAML_CHECKER_RESULTS_TOTAL.format(totalfiles)
    log(logger, totalmessage, toconsole)

    for batchtype, batch in batches.items():
        if batch:
            batchmessage = config.YAML_CHECKER_BATCH_MSG.format(batchtype,
                                                                len(batch))
            log(logger, batchmessage, toconsole)
            for index, b in enumerate(batch):
                symbol = config.YAML_CHECKER_BATCH_SYMBOL[batchtype]
                message = config.YAML_CHECKER_FILE_MSG.format(
                    symbol,
                    index + 1,
                    len(batch),
                    b
                )
                log(logger, message, toconsole)
        else:
            batchmessage = config.YAML_CHECKER_NO_BATCH.format(batchtype)
            log(logger, batchmessage, toconsole)

@click.command()
@click.option('-f', "folder", nargs=1, type=str, required=True,
              help="folder holding yaml data files")
@click.option('-p', is_flag=True, help="print results to terminal screen")
def main(folder, p):
    filepath = utils.format_directory_path(folder)
    if not utils.check_directory_path(filepath):
        exit(config.ARGS_PATH_IS_NOT_DIR)

    logargs = utils.logargs(type("yc_main", (), dict()))
    logger = utils.setup_logger_from_logargs(logargs)

    checker = YamlChecker(filepath, logger)
    fileresults = checker.verify_file_states()

    log_file_results(logger, fileresults, p)

if __name__ == "__main__":
    main()