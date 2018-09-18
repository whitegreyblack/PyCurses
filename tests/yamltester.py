"""Tests for yaml files"""

__author__ = "Samuel Whang"

import sys
sys.path.append('..')

import os
import unittest
import yaml
from re import compile
from source.YamlObjects import Reciept

FOLDER = 'singlefail/'

class YamlTester(unittest.TestCase):

    def setUp(self):
        self.folder = FOLDER

    def test_directory(self):
        """ Test if directory is not empty """
        _, _, files = list(os.walk(self.folder)).pop()
        self.assertNotEqual(len(files), 0)

    def test_file_name(self):
        regex = compile("[0-9]{6}-[a-z]{,25}\.yaml")
        for _, _, files in list(os.walk(self.folder)):
            for filename in files:
                try:
                    self.assertTrue(regex.match(filename))
                except AssertionError as e:
                    e.args = (f"FILE: {filename}",)
                    raise

    def test_file_store(self):
        regex = compile("[0-9]{6}-[a-z]{,25}\.yaml")
        for _, _, files in list(os.walk(self.folder)):
            for file in files:
                if regex.match(file):
                    with open(self.folder + file) as f:
                        try:
                            yobj = yaml.load(f.read())
                            self.assertEqual(file.split('.')[0].split('-')[1],
                                             yobj.store.replace(' ','').lower())
                        except:
                            raise

if __name__ == "__main__":
    if not os.path.isdir(FOLDER):
        raise ValueError('Path given is not a directory')

    unittest.main()
