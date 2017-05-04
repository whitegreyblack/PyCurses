from reciept_yaml import Reciept
from os import walk
import unittest
import sys
import yaml
from re import compile, match

folder = 'reciepts/'


class YamlTester(unittest.TestCase):
    def test_directory(self):
        """ Test if directory is not empty """
        self.assertNotEqual(len([f for root,dirs,files in walk('reciepts') for f in files]), 0)
    '''
    def test_files(self):

        self.test_file_name()
        self.test_file_store()

    def test_file_name(self):
        regex = compile("[0-9]{6}-[a-z]{,25}\.yaml")
        for _, _, files in walk(folder):
            for file in files:
                try:
                    self.assertTrue(regex.match(file))
                except AssertionError as e:
                    e.args = ("FILE: {}".format(file),)
                    raise
    def test_file_store(self):
        regex = compile("[0-9]{6}-[a-z]{,25}\.yaml")
        for _, _, files in walk(folder):
            for file in files:
                if regex.match(file):
                    with open(folder+file) as f:
                        try:
                            print(file.split('.')[0].split('-')[1])
                            self.assertEqual(file.split('.')[0].split('-')[1], yaml.load(f.read()))
                        except AssertionError as e:
                            e.args = ("FILE: {} - filename does not match store variable in file".format(file),)
                            raise
    '''
if __name__ == "__main__":
    unittest.main()