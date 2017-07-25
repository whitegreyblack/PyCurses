import sys
import curses
import background as bg
from checker import YamlChecker
from populate import Populate
from database import Connection
import logging


hi, bd, li, key = None, None, None, None
tabnames = ["RECIEPT",
            "GROCERY",
            "EXERCISE",
            "PAYMENTS",
            "CALENDAR",
            "CONTACTS",]


class Tab:
    def __init__(self, title, parent, window, child):
        self.title = title
        self.parent = parent
        self.window = window
        self.child = child
        self.child.setparent(self)
        self.x, self.y = window.getmaxyx()

    def toggle_on(self):
        self.window.border(bd, bd, bd, bd, bd, bd, bd, bd)
        self.toggle_name()
        self.window.refresh()
        self.child.toggle_on()

    def toggle_off(self):
        self.window.border(li, li, li, li, li, li, li, li)
        self.toggle_name()
        self.window.refresh()
        self.child.toggle_off()

    def toggle_name(self):
        self.window.addstr(1, 1, "{}".format(self.title[0:7]))
        pass

    def load(self):
        self.child.load()


class Data:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.pos = 0

    def scroll(self, n):
        old = self.pos
        self.pos = max(min(self.size-1, self.pos+n), 0)
        return old, self.pos


class Window:
    def __init__(self, mainscr, window):
        y, x = mainscr.getmaxyx()
        self.window = window
        self.mainscr = mainscr
        self.left = window.subwin(y-4, x//2-1, 3, 1)
        self.right = window.subwin(y-4, x//2-1, 3, x//2)
        self.border()
        self.left.border(), self.right.border()
        self.datapos = 0

    def setparent(self, parent):
        self.parent = parent

    def toggle_on(self):
        if self.parent.title.lower() == "reciept":
            i = 2
            for store, date, _, _, _, _, total in self.datahead.data:
                if i // 2 - 1 == self.datahead.pos:
                    self.window.addstr(i, 2, "{:15} {:11} {:6.2f}".format(
                        store, date, total), curses.A_REVERSE)
                else:
                    self.window.addstr(i, 2, "{:15} {:11} {:6.2f}".format(
                        store, date, total))
                i += 2
            # self.window.addstr(10, 2, "{}".format(self.datahead.pos))
        if self.parent.title.lower() == "grocery":
            i = 2
        if self.parent.title.lower() == "payment":
            self.window.addstr(7, 1, '{} active'.format(
                self.parent.title))
        self.window.overwrite(self.mainscr)
        self.window.refresh()

    def toggle_off(self):
        self.window.clear()
        self.border()
        self.window.refresh()

    def refresh(self, i, j):
        s, d, _, _, _, _, t = self.datahead.data[i]
        self.window.addstr(i+2, 2, "{:15} {:12} {:6.2f}".format(s, d, t))
        s, d, _, _, _, _, t = self.datahead.data[j]
        self.window.addstr(
                j+2, 2, "{:15} {:12} {:6.2f}".format(s, d, t),
                curses.A_REVERSE)

    def border(self):
        self.window.border(bd, bd, bd, bd, bd, bd, bd, bd)

    def load(self):
        if self.parent.title.lower() == "reciept":
            self.datahead = Data(
                    [row for row in self.parent.parent.conn.load()])
        elif self.parent.title.lower() == "grocery":
            self.data = self.parent.parent.conn.loadByGroup(
                    "type",
                    self.parent.title.lower())


class SubWindow:
    def __init__(self, mainscr, parent):
        self.mainscr = mainscr
        self.parent = parent


class ListManager:
    pass


class TabsManager:
    def __init__(self, parent):
        self.conn = Connection()
        self.parent = parent
        self.tabs = []
        self.add()
    def add(self):
        y, x = self.parent.getmaxyx()
        for i in range(len(tabnames)):
            t = Tab(tabnames[i], self, self.parent.subwin(2, 9, 0, i*10),
                    Window(self.parent, self.parent.subwin(y-2, x, 2, 0)))
            self.tabs.append(t)
        self.count = len(self.tabs)
        for i in self.tabs:
            i.toggle_off()
            i.child.load()
        self.tabs[0].toggle_on()
        self.active = self.tabs[0]
        self.parent.hline(2, 0, bd, x)

    def update(self, i, j):
        self.tabs[i].toggle_off()
        self.tabs[j].toggle_on()
        self.active = self.tabs[j]

    def load(self, conn):
        for i in self.tabs:
            i.load()
        # [i.load() for i in self.tabs]


def setup():
    global bd, li, keys
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    bd = bg.bd
    li = bg.li

    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    TAB = ord('\t')
    BTAB = curses.KEY_BTAB

    # change tabs
    keys = {LEFT: -1, RIGHT: 1, TAB: 1, BTAB: -1}
    # tab selection
    hkeys = dict([(49, 0), (50, 1), (51, 2)])
    # content scroll
    vkeys = [UP, DOWN]
    
    return hkeys, vkeys, keys


def main(mainscreen):
    # variables
    hkeys, vkeys, keys = setup()
    pos = newpos = 0

    # tabs and child windows
    tm = TabsManager(mainscreen)

    # user input
    char = mainscreen.getch()
    while char != ord('q'):
        if char in keys.keys() or char in hkeys.keys():
            if char in keys.keys():
                newpos = pos+keys[char]
                if newpos < 0:
                    newpos = tm.count-1
                if newpos > tm.count-1:
                    newpos = 0
            elif char in hkeys.keys():
                newpos = hkeys[char]
            tm.update(pos, newpos)
            pos = newpos
        elif char in vkeys:
            if char == vkeys[0]:
                tm.active.child.datahead.scroll(-1)
                # tm.active.child.refresh(tm.active.child.datapos, -1)
            if char == vkeys[1]:
                tm.active.child.datahead.scroll(1)
                # tm.active.child.refresh(tm.active.child.datapos, 1)
            tm.active.child.toggle_on()
        char = mainscreen.getch()
    curses.endwin()
    print(chr(27)+"[2J")
    #sys.stderr.write("\x1b2J\x1b[H")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("No target folder\nExitting...")

    # fill sqlite db
    folder = sys.argv[1].replace("\\", "/")
    commit, modify = YamlChecker(folder).files_safe()
    Populate(folder, commit)

    curses.wrapper(main)
