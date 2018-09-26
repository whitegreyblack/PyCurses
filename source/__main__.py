"""__main__.py: Reciept Viewer App
Handles building application within curses environment
"""

__author__ = "Samuel Whang"

import os
import sys
import click
import curses
import source.utils as utils
from source.application import Application

def initialize_curses_settings(logger=None):
    """Sets settings for cursor visibility and color pairings"""
    if logger:
        logger.info('main(): initializing curses library settings')
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)

def application(screen, folderpath, rebuild):
    """Initializes the Application object which builds the rest of the
    necessary frontend/backend objects.

    The main loop however if handled here as well as signal processing,
    screen drawing and erasing.

    We build the logger at this top level to print from this function
    as well as pass in to application and child objects under application.
    However we could also not build the logger and have the application
    object handle logger building and only the app and app children would
    have access to the logger.
    """
    logargs = utils.logargs(application)
    logger = utils.setup_logger_from_logargs(logargs)
    
    # curses only options.
    initialize_curses_settings()
    
    # initialize application object and build front/back end
    app = Application(folderpath, logger=logger, rebuild=rebuild)
    app.setup()
    app.build_windows(screen)
    app.draw(screen)

    # TODO: May be place this in a .Run() function inside app?
    while True:
        key = screen.getch()
        if key in app.keymap.keys():
            app.keyhandler(key)
        else:
            retval = app.send_signal(key)
            if not retval:
                break
        screen.erase()
        app.draw(screen)

@click.command()
@click.option('-f', "folder", nargs=1, required=True,
              help="Folder containing yaml data files")
@click.option('--rb', "rebuild", is_flag=True, default=False,
              help="Rebuild tables before inserting files")
def main(folder, rebuild):
    """Handles argument parsing using click framework before calling the
    curses wrapper handler function
    """

    # special case. Dot notation usually means current folder within the file
    # system. Prevent this case in order to stop importing all subfiles
    # within the currently selected folder.
    if folder == '.':
        print("Invalid folder specified: cannot use dot")
        return

    # Format the given path for the correct path delimiter and the check if
    # that path exists as a directory within the filesystem. Exit early if
    # false.
    filepath = utils.format_directory_path(folder)
    if not utils.check_directory_path(filepath):
        print("Folder argument is not a directory")
        return 

    # Reduce the delay when pressing escape key on keyboard.
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(application, folder, rebuild)

if __name__ == "__main__":
    main()
