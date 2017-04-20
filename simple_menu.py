import curses
import sys
windows = 0
tabs = ['Finances','Expenses','Income','Grocery']

# main window object
class Window(object):
    
    def __init__(self, scr):
        self.scr = scr
        self.tab = []

# tab object holding subwindow and header
class Tab(object):
    def __init__(self, win):
        self.win = win
        self.winyx = win.getmaxyx()
        self.tabyx = (0,0)
        self.active = 1
        self.border()
        self.addHome()
    def border(self):
        self.win.border(0)
        self.win.hline(0,0,' ',self.winyx[1]-1)
        self.win.vline(0,self.winyx[1]-1,' ',3)
        self.win.addch(2,0,curses.ACS_LTEE)
        try:
            self.win.addch(2,115,curses.ACS_URCORNER)
        except Exception as e:
            pass
        #self.win.addch(0,self.win.getmaxyx()[1]-1,curses.ACS_VLINE)
        self.win.refresh()
    def addHome(self):
        self.addTab("Home")
    def addTab(self, string):
        y,x = self.tabyx
        self.win.hline(y,x,curses.ACS_HLINE,3+len(string))        # top h line
        self.win.vline(y,x,curses.ACS_VLINE,2)
        self.win.vline(y,x+3+len(string),curses.ACS_VLINE,2)      # right line
        self.win.addch(y,x,curses.ACS_ULCORNER)                   # top left corner
        self.win.addch(y,x+3+len(string),curses.ACS_URCORNER)     # top right corner
        self.win.addstr(y+1,x+2,string)                           # title
        self.win.hline(y+2,x,curses.ACS_HLINE,self.winyx[1]-1)    # bot h line
        self.win.hline(y+2,x,' ',4+len(string))                   # active h line
        self.win.addch(y+2,x,curses.ACS_BTEE)
        if x == 0:
            self.win.addch(y+2,x,curses.ACS_LTEE)
        self.win.addch(y+2,x+3+(len(string)),curses.ACS_BTEE)
        self.win.refresh()
        self.tabyx = (self.tabyx[0],self.tabyx[1]+4+len(string))
    def draw(self, scr):
        pass        

def addTab(scr, string):
    # maybe build the corners first? (uy,ux, ly,lx) (topleft, bottomright)
    y0,x0 = scr.getmaxyx()
    y,x, = 0,0
    tpos = []

    # remove top portion of border
    scr.hline(y,x,' ',x0)
    scr.vline(y,x0-1,' ',2)

    for i in string:
        tpos.append((y,x))
        # build three sides of box (LEFT, TOP, RIGHT)
        scr.vline(y,x,curses.ACS_VLINE,2)                 # left
        scr.vline(y,x+len(i)+3,curses.ACS_VLINE,2)  # right
        scr.hline(y,x,curses.ACS_HLINE,len(i)+4) 
        # build corners
        scr.addch(y,x,curses.ACS_ULCORNER)
        scr.addch(y,x+len(i)+3, curses.ACS_URCORNER)
        #scr.addch(y+2,x+len(i)+3, curses.ACS_LLCORNER)
        # write tab title
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        scr.addstr(y+1,x+2,"{}".format(i),curses.color_pair(1))
        x += 2+len(i)+2

    # active first tab
    y,x = tpos[0]
    y += 2
    x += 3+len(string[0])
    #scr.addch(y,x,curses.ACS_BTEE)
    scr.hline(y,0,curses.ACS_HLINE,x0)
    scr.hline(y,1,' ',x)
    scr.addch(y,0,curses.ACS_VLINE)
    scr.addch(y,x,curses.ACS_LLCORNER)
    scr.addch(y,x0-1,curses.ACS_URCORNER)

def main(mainscreen):
    y,x = mainscreen.getmaxyx()
    tabs = Tab(mainscreen.subwin(3,x-1,0,0))
    wins = mainscreen.subwin(y-3,x-1,3,0)
    wins.border()
    wins.hline(0,0,' ',x-1)
    wins.addch(0,0,curses.ACS_VLINE)
    wins.addch(0,x-2,curses.ACS_VLINE)
    tabs.addTab('random')
    #mainscreen.border(0) 
    #mainscreen.refresh()
    mainscreen.keypad(1)
    keys = {curses.KEY_RIGHT:'r',
            curses.KEY_LEFT:'l',
            ord('\t'): 'tab',
            curses.KEY_BTAB:'bt',
            curses.KEY_BACKSPACE: 'bs',
            }
    '''
    char = mainscreen.getch()
    while char != ord('q'):
        if char in keys.keys():
            mainscreen.addstr(5,5,keys[char])
        elif char == '\t':
            mainscreen.addstr(5,5,'tab')
        else:
            mainscreen.addstr(5,5,"nope")
        mainscreen.refresh()
        char = mainscreen.getch()
    '''
    mainscreen.getch()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage = "usage: python [filename] [tabs [...]]"
        print(usage)
        exit()
    curses.wrapper(main)
