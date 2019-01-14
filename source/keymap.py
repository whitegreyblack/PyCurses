"""keymap.py

Handles key inputs to actions for curses applications
"""
import curses
from source.utils import Event
from collections.abc import MutableMapping


class KeyMap(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
    # def __setitem__(self, )
    # def add_handler(self, key, curr_win_wid, next_win_wid):
    #     if (key, curr_win_wid) in self:
    #         raise ValueError("Duplicate key mapping")
    #     self[(key, curr_win_wid)] = next_win_wid

    # def add_handler_map(self, keymap):
    #     self.update(keymap)

if __name__ == "__main__":
    km = KeyMap()
    km.keys()
    # km.add_handler(0, 1, 3)
