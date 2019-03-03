import sys
import curses
from datetime import date
import source.utils as utils
from source.database import Connection
from source.yamlchecker import YamlChecker

# from data import receiptData
# from tabs import Tab
# import calendar

hi = None
bd = None
li = None
key = None
limit = 30

tabnames = ["receipt",]

class WinCalendar:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.year = calendar.TextCalendar()

class Window:
    def __init__(self, mainscr, window):
        y, x = mainscr.getmaxyx()
        self.window = window
        self.mainscr = mainscr
        self.left = window.subwin(y - 4, x // 2 - 1, 3, 1)
        self.right = window.subwin(y - 4, x // 2 - 1, 3, x // 2)
        self.border()
        self.left.border(), self.right.border()
        self.datapos = 0
        self.months = WinCalendar(self, self.right)

    def setparent(self, parent):
        self.parent = parent

    def toggle_on(self):
        if self.parent.title.lower() == "receipt":
            i = 2
            for store, date, _, _, _, _, total in self.datahead.data:
                if i // 2 - 1 == self.datahead.pos:
                    self.window.addstr(i, 2, "{d} | {n:{l}} | {t:5.2f}".format(
                        n=store,
                        l=self.datahead.maxas,
                        d=date,
                        t=total
                    ), curses.A_REVERSE)
                else:
                    self.window.addstr(i, 2, "{d} | {n:{l}} | {:5.2f}".format(
                        total,
                        n=store,
                        l=self.datahead.maxas,
                        d=date,
                    ))
                i += 2
            i = 2
            for m in self.datahead.month:
                self.window.addstr(i, 60, "{:6} : {:6.2f}".format(
                    calendar.month_name[m[0]], m[1]))
                i += 2
            self.window.addstr(i, 60, "Total = {}".format(self.datahead.total))
        '''
        if self.parent.title.lower()=="grocery":
            i = 2
        if self.parent.title.lower()=="payment":
            self.window.addstr(7,1,'{} active'.format(self.parent.title))
        '''
        self.window.overwrite(self.mainscr)
        # self.window.refresh()
        self.toggleMonths()
        self.window.refresh()

    def toggle_off(self):
        self.window.clear()
        self.border()
        self.window.refresh()

    def toggleMonths(self):
        if self.parent.title.lower() == "receipt":
            for m in self.datahead.month:
                i = 40
                #month = self.months.year.formatmonth(2017, m[0])
                #self.window.addstr(i, 60, "{}".format(type(month)))
                #self.window.addstr(i, 3, "{}".format(self.months.year.formatmonth(2017, m[0])))
                #i+= 5
                # for l in self.months.year.formatmonth(2017, m[0]):
                #     self.window.addstr(35, 3, "{}".format(l))
                #     i+=1

    def refresh(self, i, j):
        s, d, _, _, _, _, t = self.datahead.data[i]
        self.window.addstr(i + 2, 2, 
                           f"{s} {d} {t:2f}")

        s, d, _, _, _, _, t = self.datahead.data[j]
        self.window.addstr(j + 2, 2,
                           f"{s} {d} {t:2f}", 
                           curses.A_REVERSE)

    def border(self):
        self.window.border(bd, bd, bd, bd, bd, bd, bd, bd)

    def load(self):
        if self.parent.title.lower() == "receipt":
            self.datahead = receiptData(
                [row for row in self.parent.parent.conn.load()])
            self.databody = self.parent.parent.conn.load_body("asdf")
        elif self.parent.title.lower() == "grocery":
            self.data = self.parent.parent.conn.loadByGroup(
                "type", self.parent.title.lower())

class TabsManager:
    def __init__(self, parent):
        self.conn = Connection()
        y, x = parent.getmaxyx()
        self.tabs = [Tab(tabnames[i], self, parent.subwin(2, 9, 0, i * 10), Window(
            parent, parent.subwin(y - 2, x, 2, 0))) for i in range(len(tabnames))]
        self.count = len(self.tabs)
        [(i.toggle_off(), i.child.load()) for i in self.tabs]
        self.tabs[0].toggle_on()
        self.active = self.tabs[0]
        parent.hline(2, 0, bd, x)

    def update(self, i, j):
        self.tabs[i].toggle_off()
        self.tabs[j].toggle_on()
        self.active = self.tabs[j]

    def load(self, conn):
        [i.load() for i in self.tabs]

def initialize_curses_settings():
    global bd, li, keys
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    bd = curses.ACS_CKBOARD
    li = curses.ACS_BOARD
    keys = {
        curses.KEY_LEFT: -1,
        curses.KEY_RIGHT: 1,
        ord('\t'): 1,
        curses.KEY_BTAB: -1,
        }

def main(mainscreen):
    """Sets up application settings and initializes windows objects"""
    
    if (len(sys.argv) < 2):
        exit("No input folder specified")
 
    logger = utils.setup_logger('simple', 
                                'simple.log',
                                extra={'filename': __file__})
    
    # check yaml files
    checker = YamlChecker(utils.format_directory_path(sys.argv[1]))
    commits, deletes = checker.files_safe()

    initialize_curses_settings()

    # variables
    pos = newpos = 0

    hkeys = dict([
        (49, 0), 
        (50, 1), 
        (51, 2)
        ])

    vkeys = [
        curses.KEY_UP, 
        curses.KEY_DOWN
        ]

    # tabs and child windows
    # tm = TabsManager(mainscreen)

    # user input
    '''
    char = mainscreen.getch()
    while char != ord('q'):
        if char in keys.keys() or char in hkeys.keys():
            if char in keys.keys():
                newpos = pos + keys[char]
                if newpos < 0:
                    newpos = tm.count - 1
                if newpos > tm.count - 1:
                    newpos = 0
            elif char in hkeys.keys():
                newpos = hkeys[char]
            tm.update(pos, newpos)
            pos = newpos
        elif char in vkeys:
            if char == vkeys[0]:
                tm.active.child.datahead.scroll_dn()
                #tm.active.child.refresh(tm.active.child.datapos, -1)
                tm.active.child.toggle_on()
            if char == vkeys[1]:
                tm.active.child.datahead.scroll_up()
                #tm.active.child.refresh(tm.active.child.datapos, 1)
                tm.active.child.toggle_on()
        char = mainscreen.getch()
    '''

    char = mainscreen.getch()
    # print(chr(27) + "[2J")
    # sys.stderr.write("\x1b2J\x1b[H")

if __name__ == "__main__":
    curses.wrapper(main)
