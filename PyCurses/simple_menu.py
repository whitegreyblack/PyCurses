import curses
import sys

bd, li, key, limit = None, None, None, 30
tabnames = ["REVIEWS",
            "EXPENSE",
            "GROCERY", 
            "PAYMENT",
            "CARLOAN",
            "MONTHLY",
            "STKINFO",
            "SOMETHI",
            "RECIPES",]
class Tab(object):
    def __init__(self, title, parent, window, child):
        self.title = title
        self.parent = parent
        self.window = window
        self.child = child
        self.child.parent(self)
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
class Window:
    def __init__(self, mainscr, window):
        y, x = mainscr.getmaxyx()
        self.window = window
        self.mainscr = mainscr
        self.left = window.subwin(y-4, x//2-1, 3, 1)
        self.right = window.subwin(y-4, x//2-1, 3, x//2)
        self.border()
        self.left.border(), self.right.border()
    def parent(self, parent):
        self.parent = parent
    def toggle_on(self):
        if self.parent.title.lower()=="expense":
            self.window.addstr(5,5,'{} active'.format(self.parent.title))
        if self.parent.title.lower()=="grocery":
            self.window.addstr(6,5,'{} active'.format(self.parent.title))
        if self.parent.title.lower()=="payment":
            self.window.addstr(7,5,'{} active'.format(self.parent.title))
        self.window.overwrite(self.mainscr)
        self.window.refresh()
    def toggle_off(self):  
        self.window.clear()
        self.border()
        self.window.refresh()
    def border(self):
        self.window.border(bd,bd,bd,bd,bd,bd,bd,bd)
class SubWindow:
    def __init__(self, mainscr, parent):
        self.mainscr = mainscr
        self.parent = parent

class TabsManager(object):
    def __init__(self, parent):
        y, x = parent.getmaxyx()
        self.tabs = [Tab(tabnames[i], parent, parent.subwin(2, 9, 0, i*10), Window(parent,parent.subwin(y-2, x, 2, 0))) for i in range(len(tabnames))]
        self.count = len(self.tabs)
        [i.toggle_off() for i in self.tabs]
        self.tabs[0].toggle_on()
        parent.hline(2, 0, bd, x)
    def update(self,i,j):
        self.tabs[i].toggle_off()
        self.tabs[j].toggle_on()

def main(mainscreen):
    conn = Connection()
    curses.curs_set(0)
    pos = 0
    global bd, li, keys
    bd, li, keys = curses.ACS_CKBOARD, curses.ACS_BOARD, {curses.KEY_LEFT:-1,curses.KEY_RIGHT:1,ord('\t'):1,curses.KEY_BTAB:-1}
    tm = TabsManager(mainscreen)
    char = mainscreen.getch()
    while char != ord('q'):
        if char in keys.keys():
            newpos = pos+keys[char]
            if newpos < 0:
                newpos = tm.count-1
            if newpos > tm.count-1:
                newpos = 0
            tm.update(pos,newpos)
            pos = newpos
        char = mainscreen.getch()
    curses.endwin()
    print(chr(27)+"[2J")
    sys.stderr.write("\x1b2J\x1b[H")
if __name__ == "__main__":
    curses.wrapper(main)
