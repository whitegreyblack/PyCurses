import sys
import curses
from populate import Populate, logging, log
from db_connection import sqlite3, Connection

hi, bd, li, key, limit = None, None, None, None, 30
tabnames = ["RECIEPT",
            "GROCERY",
            ]

class Tab:
    def __init__(self, title, parent, window, child):
        self.title = title
        self.parent = parent
        self.window = window
        self.child = child
        self.child.setparent(self)
        self.x,self.y = window.getmaxyx()
    def toggle_on(self):
        self.window.border(bd,bd,bd,bd,bd,bd,bd,bd)
        self.toggle_name()
        self.window.refresh()
        self.child.toggle_on()
    def toggle_off(self):
        self.window.border(li,li,li,li,li,li,li,li)
        self.toggle_name()
        self.window.refresh()
        self.child.toggle_off()
    def toggle_name(self):
        self.window.addstr(1, 1, "{}".format(self.title))
    def load(self):
        self.child.load()
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
        if self.parent.title.lower()=="reciept":
            i = 2
            for store, date, _, _, _, _, total in self.datahead:
                self.window.addstr(i,2,"{} {} {:.2f}".format(store, date, total))
                i+=2
            self.window.addstr(i,1,"{}".format(len(self.datahead)))
        if self.parent.title.lower()=="grocery":
            i = 2
        if self.parent.title.lower()=="payment":
            self.window.addstr(7,1,'{} active'.format(self.parent.title))
        self.window.overwrite(self.mainscr)
        self.window.refresh()
    def toggle_off(self):  
        self.window.clear()
        self.border()
        self.window.refresh()
    def border(self):
        self.window.border(bd,bd,bd,bd,bd,bd,bd,bd)
    def load(self):
        if self.parent.title.lower()=="reciept":
            self.datahead = [(row) for row in self.parent.parent.conn.load()]
        elif self.parent.title.lower()=="grocery":
            logging.debug(log.sql_slct_try.format("type",self.parent.title.lower()))
            self.data = self.parent.parent.conn.loadByGroup("type",self.parent.title.lower())
class SubWindow:
    def __init__(self, mainscr, parent):
        self.mainscr = mainscr
        self.parent = parent

class ListManager:
    pass

class TabsManager:
    def __init__(self, parent):
        self.conn = Connection()
        y, x = parent.getmaxyx()
        self.tabs = [Tab(tabnames[i], self, parent.subwin(2, 9, 0, i*10), Window(parent,parent.subwin(y-2, x, 2, 0))) for i in range(len(tabnames))]
        self.count = len(self.tabs)
        [(i.toggle_off(), i.child.load()) for i in self.tabs]
        self.tabs[0].toggle_on()
        parent.hline(2, 0, bd, x)
    def update(self,i,j):
        self.tabs[i].toggle_off()
        self.tabs[j].toggle_on()
    def load(self, conn):
        [i.load() for i in self.tabs]

def main(mainscreen):
    # fill sqlite db
    Populate()

    # variables
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    pos = newpos = 0
    global bd, li, keys
    bd, li, keys = curses.ACS_CKBOARD, curses.ACS_BOARD, {curses.KEY_LEFT:-1,curses.KEY_RIGHT:1,ord('\t'):1,curses.KEY_BTAB:-1}
    hkeys = dict([(49,0),(50,1),(51,2)])
    vkeys = [curses.KEY_UP, curses.KEY_DOWN]
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
            tm.update(pos,newpos)
            pos = newpos
        elif char in vkeys:
            if char == vkeys[0]:
                pass
            if char == vkeys[1]:
                pass
        char = mainscreen.getch()
    curses.endwin()
    print(chr(27)+"[2J")
    sys.stderr.write("\x1b2J\x1b[H")
if __name__ == "__main__":
    logging.basicConfig(filename='debug.log', format='%(message)s', level=logging.DEBUG)
    curses.wrapper(main)
