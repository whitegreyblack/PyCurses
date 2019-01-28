"""encyclopedia.py"""

import json
import random
from source.applications.application import Application
from source.window import (
    Window,
    WindowProperty,
    DisplayWindow,
    ScrollableWindow,
    PromptWindow
)

# from source.models.models import Dictionary
import source.utils as utils

def open_data_file(datafile):
    with open(datafile, 'r') as f:
        data = json.loads(f.read())
    return data

class Encyclopedia(Application):
    CLI_NAMES = ('encyclopedia', 'spaceship', 'space')
    def build_application(self, rebuild=False, reinsert=False, examples=False):
        screen = self.screen
        height, width = screen.getmaxyx()

        self.data = open_data_file(".\data\spaceship.json")
        exit()