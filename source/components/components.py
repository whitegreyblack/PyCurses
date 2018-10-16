"""UI Component for Filter Prompt"""

__author__ = "Samuel Whang"

import curses

from source.controls import UIControl

class FilterPrompt(UIControl):
    def __init__(self, x, y, width, height, title=None, buttons=None):
        super().__init__(x, y, width, height, title)
        self.buttons = buttons
