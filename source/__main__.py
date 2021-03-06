"""__main__.py: Receipt Viewer App
Handles building application within curses environment. Initializes
curses settings then sends the screen into the application to be built
"""

__author__ = "Samuel Whang"

import curses
import os
import pprint
import sys

import click

import source.utils as utils
from source.applications import (Application, Applications,
                                 ContactsApplication, Encyclopedia,
                                 NoteApplication, QuizApplication,
                                 SystemApplication, TaskApplication)


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

def run_application(screen, folderpath, app, demo, rebuild, reinsert, logger=None):
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
    a = app(folderpath, screen=screen, logger=logger)

    # should we create a new function that calls all 4 functions?
    # or manually call individual functions in here?
    # app.setup() -- each demo will setup their own database
    #app.build_windows(screen)
    # app.build_windows()
    a.build_application(rebuild, reinsert, demo)
    # if not rebuild:
    #     getattr(app, demo)()
    # else:
    #     getattr(app, demo)(rebuild=rebuild)
    a.draw()
    a.run()

# TODO: need a way to run main without needing a folder
# TODO: need a way to run main with multiple folders
# TODO: need a way to run main with export folder specified
@click.command()
@click.option('-f', "folder", nargs=1,
              help="Folder containing yaml data files")
@click.option('--app', "app", nargs=1,
              help="Specified which demo application to run [notes, tree, tasks, receipts, quiz]")
@click.option('-x', "demo", nargs=1, is_flag=True, default=False,
              help="Use fake data to build the app")
@click.option('-r', "rebuild", nargs=1, is_flag=True, default=False,
              help="Rebuild tables before inserting files")
@click.option('-i', "reinsert", nargs=1, is_flag=True, default=False,
              help="Reinsert data for specified application")
def main(folder, app, demo, rebuild, reinsert):
    """Handles argument parsing using click framework before calling the
    curses wrapper handler function
    """
    demos = dict()
    for a in Applications:
        if hasattr(a, 'CLI_NAMES'):
            for name in getattr(a, 'CLI_NAMES'):
                demos.update({name: a})

    # these apps have not been built yet but we want to keep their names in the 
    # demo list for future use. For now they will call the default app program
    demos.update({
        "receipts": Application,
        "receipt": Application,
    })

    # pprint.pprint(demos)

    # special case. Dot notation usually means current folder within the file
    # system. Prevent this case in order to stop importing all subfiles
    # within the currently selected folder.
    if folder == '.':
        print("Invalid folder specified: cannot use dot")
        return

    # determine which application to run
    application = Application
    if app:
        if app not in demos.keys():
            print("Invalid demo specified: not found in demo list")
            return
        application = demos[app]

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
    curses.wrapper(run_application, folder, application, demo, rebuild, reinsert, logger)

if __name__ == "__main__":
    main()
