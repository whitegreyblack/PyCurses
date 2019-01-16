"""__main__.py: receipt Viewer App
Handles building application within curses environment. Initializes
curses settings then sends the screen into the application to be built
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

def initialize_environment_settings(logger=None):
    """Sets up environment variables for the application"""
    # TODO: revert the environment_settings back to original values
    #       on application exit
    # Reduce the delay when pressing escape key on keyboard.
    os.environ.setdefault('ESCDELAY', '25')

def application(screen, folderpath, demo, rebuild, logger=None):
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
    # curses only options.
    initialize_curses_settings()
    
    # initialize application object and build front/back end
    app = Application(
        folderpath,
        screen=screen,
        logger=logger
    )

    # should we create a new function that calls all 4 functions?
    # or manually call individual functions in here?
    # app.setup() -- each demo will setup their own database
    #app.build_windows(screen)
    # app.build_windows()
    if not rebuild:
        getattr(app, demo)()
    else:
        getattr(app, demo)(rebuild=rebuild)
    app.draw()
    app.run()

# TODO: need a way to run main without needing a folder
# TODO: need a way to run main with multiple folders
# TODO: need a way to run main with export folder specified
@click.command()
@click.option('-f', "folder", nargs=1,
              help="Folder containing yaml data files")
@click.option('--demo', "demo", nargs=1,
              help="Specified which demo application to run")
@click.option('--rb', "rebuild", nargs=1, default=None,
              help="Rebuild tables before inserting files")
def main(folder, demo, rebuild):
    """Handles argument parsing using click framework before calling the
    curses wrapper handler function
    """

    # special case. Dot notation usually means current folder within the file
    # system. Prevent this case in order to stop importing all subfiles
    # within the currently selected folder.
    if folder == '.':
        print("Invalid folder specified: cannot use dot")
        return

    if demo and demo not in ("notes", "note", "tree", "todos", "todo", "receipts", "receipt"):
        print("Invalid demo specified: not found in demo list")
        return
    elif demo in ("receipt", "receipts"):
        demo = "build_receipt_viewer"
    elif demo in ("todo", "todos"):
        demo = "build_todo_tasks"
    elif demo in ("notes", "note"):
        demo = "build_note_viewer"
    elif demo in ("tree",):
        demo = "build_file_explorer"
    else:
        demo = "build_windows"
    # Format the given path for the correct path delimiter and the check if
    # that path exists as a directory within the filesystem. Exit early if
    # false.
    filepath = None
    if folder:
        filepath = utils.format_directory_path(folder)
        if not utils.check_directory_path(filepath):
            print("Folder argument is not a directory")
            return 

    initialize_environment_settings()

    # logger class before we enter main curses loop
    logargs = utils.logargs(application, __file__)
    logger = utils.setup_logger_from_logargs(logargs)
    curses.wrapper(application, folder, demo, rebuild, logger)

if __name__ == "__main__":
    main()
