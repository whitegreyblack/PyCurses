import curses
import time
import sys
import os
import random
import threading

class MainScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen.bkgd(" ", curses.color_pair(1))
        self.screen.border()
        screen.addstr(0, 2, "Main Window", curses.color_pair(2))
        self.y, self.x = screen.getmaxyx()
        self.world = [[-1 for i in range(self.x)] for j in range(self.y)]
        self.childs = []
    def subwins(self, cls):
        for i in cls:
            self.childs.append([i,len(self.childs)])
            # overwrites most recently added box
            self.overwrite(self.childs[len(self.childs)-1])

    def overwrite(self, cls):
            cy, cx = cls[0].screen.getbegyx()
            dy, dx = cls[0].screen.getmaxyx()
            for j in range(dy):
                for i in range(dx):
                    self.world[cy+j][cx+i] = cls[1]
    
    def change_order(self, i):
        child = self.childs.pop(i)
        childs.add(i)

    def check(self, y, x):
        if self.world[y][x] == -1:
            self.screen.addstr(6,5,"SCR: {}".format(
                self.__class__.__name__
            ))
        else:
            self.overwrite(self.childs[self.world[y][x]])
            child, num = self.childs[self.world[y][x]]
            child.translate(y, x)

    def active_child(self):
        self.overwrite(self.childs[len(self.childs)-1])
        self.childs[len(self.childs)-1][0].active()

class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.screen.border()
        self.y, self.x = screen.getmaxyx()
        self.screen.addch(1,1,'+')
        self.screen.addch(1,2,'-')
        self.toggle = False
    def translate(self, y, x):
        wy,wx = self.screen.getbegyx()
        self.active()
        if y == 1 & x == 1:
            if not self.toggle:
                self.screen.clear()
                self.screen.addstr(2,1,"asdf")
                self.screen.addstr(3,1,"ffss")
                self.screen.addstr(4,1,"ssss")
                self.screen.border()
                self.screen.addch(1,1,"-")
                self.screen.refresh()
                self.toggle = True
            else:
                self.toggle = False
                self.screen.addstr(0,1,"clicked")
        self.screen.addstr(2,2,"{} {}".format(y-wy, x-wx))
        self.screen.addstr(3,3,"{}".format(self.toggle))
        for i in range(1,self.x-1):
            self.screen.addch(2,i, curses.ACS_HLINE)
        self.screen.addch(2,0,curses.ACS_LTEE)
        self.screen.addch(2,self.x-1, curses.ACS_RTEE)
        self.screen.refresh()

    def active(self):
        self.screen.clear()
        self.screen.border()
        self.screen.addch(1,1,"+")
        self.screen.refresh()
        
def main(scr):
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    mc = MainScreen(scr)
    mc.subwins(
        [Screen(scr.subwin(10,10,10,10)),Screen(scr.subwin(6, 20,12, 6))])
    mc.active_child()
    mc.screen.addch(30,1,u'\u2580')
    mc.screen.addch(30,2,u'\u2800')
    mc.screen.addch(30,3,u'\u2801')
    mc.screen.addch(30,4,u'\u2802')
    mc.screen.addch(30,5,u'\u2584')
    mc.screen.addch(30,6,u'\u2803')
    mc.screen.addch(30,7,u'\u28CF')
    mc.screen.addch(30,8,u'\u28F9')
    mc.screen.addch(30,9,u'\u2588')
    mc.screen.addch(30,10,u'\u28FF')
    mc.screen.addch(30,11,u'\u282A')
    mc.screen.addch(30,12,u'\u2815')
    ch = u'\u28FF'
    for i in range(15):
        mc.screen.addch(30,i+1,ch)
    
    mc.screen.addstr(29,1,"a"*15)

    c = ''
    while c != ord('q'):
        if c == curses.KEY_DOWN:
            pass
        if c == curses.KEY_MOUSE:
            scr.addstr(4,5,"true")
            _, x, y, _, _ = curses.getmouse()
            mc.screen.addstr(5,5,'X:{} Y:{}'.format(x, y))
            mc.check(y, x)
        for i in range(30):
            for j in range(30):
                mc.screen.addch(
                    i,j+30,"{}".format(mc.world[i][j]+1))
        scr.refresh()
        c = scr.getch()
        scr.addstr(6,5," "*15)
        scr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)

'''
def printtime(scr):
    threading.Timer(1.0, printtime, [scr]).start()
    a = time.time()
    os.system('ping google.com -n 1 > time.log')
    with open('time.log') as f:
        lines = f.read().split('\n')
        for line in lines:
            if 'average' in line.lower():
                avg = (line.strip().split(', ')[2].split(' = ')[1])
                return(avg, time.time()-a)
    #scr.refresh()
while True:
    a, b = printtime("")
    print("{}".format(b))
'''
'''
def main(scr):
    a,b = printtime(scr)
    c = ' '
    while c != ord('q'):
        scr.addstr(1,1,"{}".format(b))
        if c == curses.KEY_DOWN:
            scr.addch(5,5,'d')
        if c == curses.KEY_UP:
            scr.addch(5,5,'u')
        c = scr.getch()
        scr.refresh()
    curses.endwin()
if __name__ == "__main__":
    curses.wrapper(main)
'''
