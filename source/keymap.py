"""keymap.py

Handles key inputs to actions for curses applications
"""
import curses
from source.utils import Event
from collections.abc import MutableMapping

class EventMap(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __repr__(self):
        kvpairs = ", ".join(f"{k}, {v}" for k, v in self.store.items())
        return f"EventMap({kvpairs})"

    def __getitem__(self, key):
        tkey = self.__keytransform__(key)
        if not tkey in self.store.keys():
            self.store[tkey] = Event()
        return self.store[tkey]

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

    @staticmethod
    def fromkeys(seq, value=None):
        t = EventMap()
        for key in seq:
            t.store[key] = value if value else Event()
        return t

    # def add_handler_map(self, keymap):
    #     self.update(keymap)

if __name__ == "__main__":
    em = EventMap().fromkeys((1,2,3,4,5,6))
    for k, v in em.__dict__.items():
        print(k, v)