"""Application.py : Reciept Viewer App

Handles application functionality between Views/Models/Controller
"""

__author__ = "Samuel Whang"

import os
import sys
import click
import curses
import source.utils as utils
from source.application import Application

def initialize_curses_settings():
    """Sets Curses related settings"""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) 

def application(screen, folderpath, rebuild):
    """Overview:
    Buids the database and yamlchecker objects. (They are tightly coupled. May
    need to change in the future.) The data from the yaml files found in using
    the folder path paramter are first checked by the yamlchecker before
    loading into the database.

    With loading finished, the front end is created and views are initialized,
    using data from the database.

    Then the application is looped to draw the views onto the screen using 
    curses framework.
    """
    logger = utils.setup_logger('applicationlogger',
                                'app.log',
                                extra={'currentfile': __file__})

    logger.info('main(): initializing curses library settings')
    initialize_curses_settings()
    logger.info('main(): done')
    
    app = Application(folderpath, logger=logger, rebuild=rebuild)
    app.setup()
    app.build_windows(screen)
    app.draw(screen)

    while True:
        key = screen.getch()
        retval = app.send_signal(key)
        if key == 10:
            logger.info(f"{retval}")
        if not retval:
            logger.info("GOT EXIT SIGNAL")
            break
        screen.erase()
        app.draw(screen)

def usage():
    return("Usage: python -m source -f [args]")

@click.command()
@click.option('-f', help="Folder containing yaml data files")
@click.option('--rb', "rebuild", is_flag=True, default=False, help="Rebuild tables before inserting files")
def main(f, rebuild):
    if not f:
        print("no data folder specified")
        print(usage())
        return

    if f == '.':
        print("Invalid folder specified: cannot use dot")
        return

    filepath = utils.format_directory_path(f)
    if not utils.check_directory_path(filepath):
        print("Folder argument is not a directory")
        return 

    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(application, f, rebuild)

if __name__ == "__main__":
    main()
