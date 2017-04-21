import curses
import sys
import sqlite3

bd, li, key = None, None, None
tabnames = ["EXPENSE","GROCERY","PAYMENT"]

class Tab(object):
    def __init__(self, title, win):
        self.title = title
        self.window = win
        self.x,self.y = win.getmaxyx()
    def deactive(self):
        self.window.border(li,li,li,li,li,li,li,li)
        self.name()
    def name(self):
        self.window.addstr(1,1,"{}".format(self.title))
        self.window.refresh()
    def active(self):
        self.window.border(bd,bd,bd,bd,bd,bd,bd,bd)
        self.name()
class TabsManager(object):
    ''' 
    Descriptions:    
        holds all tab headers and dynamically resizes and positions all tabs
        each tab should be connected to a single windows which should dissapear when window is exited
    '''
    def __init__(self, lt):
        self.count = len(lt)
        self.tablist = lt
        self.tabBorders()
        self.tablist[0].active()
        #self.current = 0
    def tabBorders(self):
        [i.deactive() for i in self.tablist]
    def tabUpdate(self,i,j):
        self.tablist[i].deactive()
        self.tablist[j].active()

class ExpenseWindow(object):
    def __init__(self, win):
        self.window = win

class GroceryWindow(object):
    def __init__(self, win):
        self.window = win

class PaymentWindow(object):
    def __init__(self, win):
        self.window = win

class WindowManager(object):
    def __init__(self, lw):
        self.count = len(lw)
        self.windowlist = lw
        self.winBorders()
    def winBorders(self):
        [i.border(bd,bd,bd,bd,bd,bd,bd,bd) for i in self.windowlist]
def main(mainscreen):
    curses.curs_set(0)
    pos = 0
    global bd, li, keys
    keys = {curses.KEY_LEFT:-1,curses.KEY_RIGHT:1,ord('\t'):1,curses.KEY_BTAB:-1}
    bd, li = curses.ACS_CKBOARD, curses.ACS_BOARD
    y,x = mainscreen.getmaxyx()
    tm = TabsManager([Tab(tabnames[i],mainscreen.subwin(2,9,0,i*10)) for i in range(len(tabnames))])
    wm = WindowManager([mainscreen.subwin(y-2,x,2,0) for i in range(len(tabnames))]) 
    mainscreen.addch(5,5,'o')
    mainscreen.addch(5,6,'O')
    mainscreen.hline(2,0,bd,x)
    char = mainscreen.getch()
    while char != ord('q'):
        if char in keys.keys():
            mainscreen.addstr(7,7,str(char))
            newpos = pos+keys[char]
            if newpos < 0:
                newpos = tm.count-1
            if newpos > tm.count-1:
                newpos = 0
            mainscreen.addstr(10,10,str(pos))
            tm.tabUpdate(pos,newpos)
            pos = newpos
        char = mainscreen.getch()
    curses.endwin()
    print(chr(27)+"[2J")
    sys.stderr.write("\x1b2J\x1b[H")
if __name__ == "__main__":
    curses.wrapper(main)
