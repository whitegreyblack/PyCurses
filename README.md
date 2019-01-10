# PyCurses

## Description
  Build and run a simple curses application

## How to run (Python 3)
  `python -m source

## Dependancies
- pyyaml : file parsing and extension for data files
- curses : front end of application
- sqlite : back end of application
- cerberus : data validation tool
- faker: random data generator
- click: used in some files for standalone functionality and argsparsing

## Standard Python Libraries
- logging : for all debug and normal output statements created at runtime
- functools : used in wrappers class for decorators functionality
- datetime: used in creating date objects for verification of variable dates

## Folder structure:
- source: app folder
  - __main__.py: application file that runs the main loop
  - yamlchecker.py: yaml file loader and validation tool (DEPRECATED: now using cerberus for yaml validation)
  - database.py: sqlite3 connection object to execute sql queries during runtime
  - controls.py: holds user interface classes to display model classes
  - models.py: holds classes that represent data objects within the application
  - YamlObjects: holds yaml model data classes for yaml file loading
  - utils.py: various shared methods used in all files within the source folder

- fakedata: random data tools
  - basic.py: random age, money amount
  - name: random male or female names with prefix and suffixes
  - phonenumber: random telephone number generator

- data: folder holding data files used in app. Includes bulk names, validation schemas and example yaml files.

- reciepts: folder used to hold exported reciept data objects. Currently holds depracted yaml files. Ongoing task to convert them.

- tests: holds test data to run failure tests.
  - singlefail: holds test which fail in yamlchecker

- old: holds depracated widget classes. May be used later on so not yet deleted.

- example: Old applications based on old code. Holds examples like tabs, color, and mouse clicking

## Overview
The project will be broken down into several portions which may be revisited if need be:
- Loading yamlfiles into database:
  - The yamlchecker and database files are currently psuedo-tightly coupled in that the
    yamlchecker uses the database to check for previously inserted files and the database 
    uses files from yamlchecker to check for new files to insert. The functions for each
    files differed enough to need two separate classes. (YAMLCHECKER is DEPRACATED)
  - The YamlObjects file holds the data model the data files use when loading the files
    in the yaml loader.

- Building the screen:
  - Models are used to hold the data retrieved from the database during data retrieval.
  - Controls hold the window classes to be able to draw the screen with the correct data.
