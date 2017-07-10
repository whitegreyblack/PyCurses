from os import walk
import unittest
from re import compile
import yaml
from reciept import Reciept
folder = 'reciepts/'


class YamlTester(unittest.TestCase):

    def setUp(self):
        self.folder = folder

    def test_directory(self):
        """ Test if directory is not empty """
        self.assertNotEqual(len([f for _, _, files in walk(self.folder)
                                for f in files]), 0)

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
        emsg = 'filename does not match store variable in file'
        regex = compile("[0-9]{6}-[a-z]{,25}\.yaml")
        for _, _, files in walk(folder):
            for file in files:
                if regex.match(file):
                    with open(folder+file) as f:
                        try:
                            print(file.split('.')[0].split('-')[1])
                            self.assertEqual(file.split('.')[0].split('-')[1],
                                                yaml.load(f.read()))
                        except AssertionError as e:
                            e.args = ("FILE: {} - {}".format(file, emsg),)
                            raise
if __name__ == "__main__":
    unittest.main()
