"""keymap.py

Handles key inputs to actions
"""

__author__ = "Samuel Whang"

import curses

class KeyMap(dict):
    def add_handler(self, key, curr_win_wid, next_win_wid):
        if (key, curr_win_wid) in self:
            raise ValueError("Duplicate key mapping")
        self[(key, curr_win_wid)] = next_win_wid

    def add_handler_map(self, keymap):
        self.update(keymap)

if __name__ == "__main__":
    km = KeyMap()
    km.add_handler(0, 1, 3)
