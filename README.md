"# PyCurses" 
A Python Curses based Project

This program will be a multi step development on the Windows platform. Currently on Step 1 backtesting and Step 2 development

The aim of this project is to create a program that allows for the ETL of yaml objects using several technologies.
The project will be broken down into several portions which may be revisited if need be
 
- Step 1 will be getting basic front end, file handling, and back end connection classes created
    - Tab and Window Objects
    - Yaml Objects to process yaml files
    - SQLite3 Connection Object
- Step 2 will be connecting back end to front end and string output
    - Layering of user created objects
    - Database querying methods 
    - String formatting for output 
- [UPDATE|CURRENT STEP]: Step 2A will be cleaning up backend functionality and code
    - Refactoring and Restyling of currently existing files
    - Adding a larger number of yaml files to be used in the database
    - Adding statistics output to logging files
    - Transitioning all print outputs to logging
- Step 3 will be diversification of front end window objects
    - I would like several differnt windows for a layered application
    - These will include Finance Tab, Grocery/Recipe Tab and Schedule Tab

Dependancies
- pyyaml : file parsing and extension
- Curses : front end of application
- sqlite : back end of application
- [UPDATE]:
	- logging : for all debug and normal output stmts created at runtime
	- functools : used in wrappers class for wrapping functionality
	- datetime: used in creating date objects for verification of object dates
	- click: used in some files for standalone functionality and argsparsing
Files:
- [UPDATE]: merged strings_sql and strings_log into one strings.py file
	- strings_sql.py - holds py strings containing common sql queries
	- strings_log.py - holds py strings containing common logger output
- [UPDATE]: merged reciept_yaml and reciept_py into one file containing a single flexible object
	- reciept_yaml.py - holds yaml object that parses yaml reciepts
	- reciept_py.py - holds object that might be used to interact between front and backend
- [UPDATE]: renamed db_connection into database.py file holding a connection object
	- db_connection.py - sqlite3 connection class that holds cursor object for db
- simple_menu - main front end driver, handles user input and visuals
- [UPDATE]: refactored populate and checker to create a wrappers file holding decorator functions
	- populate - back end driver, called once to populate the database if not already populated
	- checker - back end yaml file that verifies yaml files found in files folder
Additional TODOS: exception handling for delicate interacting functions
