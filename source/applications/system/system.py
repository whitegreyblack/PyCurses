# system.py (tree/fileexplorer)
import curses
import random

import source.utils as utils
from source.applications.application import Application
from source.window import (DisplayWindow, PromptWindow, ScrollableWindow,
                           Window, WindowProperty)
from source.window.scrollable import (keypress_up, keypress_down)
from source.applications.system.models import SystemWindow
from source.applications.system.data import sysdat as data


class SystemApplication(Application):
    CLI_NAMES = ('tree', 'system', 'file', 'files', 'filesystem')
    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.data = data
        
        # main window
        self.window.title = 'File System Example'

        # scroll window
        scroller = SystemWindow(
            screen.subwin(height - 2, width, 1, 0),
            title="File Explorer",
            data=data,
            focused=True
            # data_changed_handlers=(self.on_data_changed,)
        )

        scroller.keypresses.on(
            (27, scroller.keypress_escape),
            (curses.KEY_DOWN, keypress_down),
            (curses.KEY_UP, keypress_up),
            (curses.KEY_ENTER, scroller.keypress_enter),
            (10, scroller.keypress_enter)
        )

        self.window.add_windows(
            scroller,
        )

        self.window.keypresses.on(
            (27, self.keypress_escape),
        )

        self.focused = self.window.currently_focused


if __name__ == "__main__":
    pass
