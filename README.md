"# PyCurses" 

This program will be a multi step development. Currently on Step 1 backtesting and Step 2 development

- Step 1 will be getting basic front end, file handling, and back end connection classes created
    - Tab and Window Objects
    - Yaml Objects to process yaml files
    - SQLite3 Connection Object
- Step 2 will be connecting back end to front end and string output
    - Layering of user created objects
    - Database querying methods 
    - String formatting for output 
- Step 3 will be diversification of front end window objects
    - I would like several differnt windows for a layered application
    - These will include Finance Tab, Grocery/Recipe Tab and Schedule Tab

Dependancies
    - pyyaml : file parsing and extension
    - Curses : front end of application
    - sqlite : back end of application

Files:
- strings_sql.py - holds py strings containing common sql queries
    - strings_log.py - holds py strings containing common logger output
    - reciept_yaml.py - holds yaml object that parses yaml reciepts
    - reciept_py.py - holds object that might be used to interact between front and backend
    - db_connection.py - sqlite3 connection class that holds cursor object for db
    - simple_menu - main front end driver, handles user input and visuals
    - populate - back end driver, called once to populate the database if not already populated

Additional TODOS: exception handling for delicate interacting functions
