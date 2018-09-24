# PyCurses

## Description
  Builds a curses application using yaml python files.

## How to run (Python 3)
  `python -m source -f ./data/`

## Dependancies
- pyyaml : file parsing and extension
- Curses : front end of application
- sqlite : back end of application
- logging : for all debug and normal output stmts created at runtime
- functools : used in wrappers class for wrapping functionality
- datetime: used in creating date objects for verification of object dates
- click: used in some files for standalone functionality and argsparsing

## Folder structure:
- source: app folder
  - __main__.py: application file that runs the main llop
  - yamlchecker.py: yaml file loader and validation tool
  - database.py: sqlite3 connection object to execute sql queries during runtime
  - controls.py: holds view model data classes
  - models.py: holds model data classes
  - YamlObjects: holds yaml model data classes for yaml file loading
  - utils.py: various shared methods used in all files within the source folder

- reciepts: currently depracted yaml files. Ongoing task to convert them.
- data: holds current yaml files which pass yamlchecking. Used for testing yamlchecker
        and running the main app
- tests: holds test data to run failure tests.
  - singlefail: holds test which fail in yamlchecker

- old: holds depracated widget classes. May be used later on so not yet deleted.

- example: Old applications based on old code. Holds examples like tabs, color, and mouse clicking

# Overview
The project will be broken down into several portions which may be revisited if need be:
- Loading yamlfiles into database:
  - The yamlchecker and database files are currently psuedo-tightly coupled in that the
    yamlchecker uses the database to check for previously inserted files and the database 
    uses files from yamlchecker to check for new files to insert. The functions for each
    files differed enough to need two separate classes.
  - The YamlObjects file holds the data model the data files use when loading the files
    in the yaml loader.

- Building the screen:
  - Models are used to hold the data retrieved from the database during data retrieval.
  - Controls hold the screen and models to be able to draw the screen with the correct data.
