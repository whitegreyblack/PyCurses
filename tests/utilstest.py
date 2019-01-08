"""Utility tester file"""
import unittest
import source.utils as utils

def test_check_or_create_folder():
    pass


def test_logargs():
    pass


def test_setup_logger_from_logargs():
    pass


def test_setup_logger():
    pass


def test_log_message():
    pass


def test_format_directory_path():
    pass


def test_check_directory_path():
    pass


def test_parse_file_from_path():
    pass


def test_filename_and_extension():
    pass


def test_border():
    pass


def test_format_float():
    pass


def test_parse_date_from_database():
    pass


def test_format_date():
    pass

def test_load_yaml_object_document():
    o = utils.load_yaml_object('./data/store.yaml', doc=True)
    assert o['store'] == 'Leevers'

def test_load_yaml_object_schema():
    o = utils.load_yaml_object('./data/schema.yaml')
    assert isinstance(o['store'], dict)

def test_validate_document_schema():
    d = utils.load_yaml_object('./data/store.yaml', doc=True)
    s = utils.load_yaml_object('./data/schema.yaml')
    assert utils.validate(d, s) == True