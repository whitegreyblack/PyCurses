# from imports import *
import curses
months=['jan','feb','mar','apr','may']
# gggdot = dot['to']

def addvline(scr, y, x, dv):
    vl = curses.ACS_VLINE
    scr.vline(y, x, vl, dv)
    scr.addch(y, x, curses.ACS_TTEE)
    scr.addch(dv - 1, x, curses.ACS_BTEE)

def addhline(scr, y, x, dh):
    hl = curses.ACS_HLINE
    scr.hline(y, x, hl, dh)
    scr.addch(y, x, curses.ACS_LTEE)
    scr.addch(y, dh - 1, curses.ACS_RTEE)

def main(scr):
    scr.border()
    y, x = scr.getmaxyx()
    scr.addstr(5, 5, str(x))
    scr.addstr(6, 5, str(y))
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)

    li = curses.ACS_BOARD
    bd = curses.ACS_CKBOARD
    re = curses.A_REVERSE
    bl = curses.ACS_BULLET
    dg = curses.ACS_DEGREE
    di = curses.ACS_DIAMOND

    addhline(scr, 10, 0, x)
    addvline(scr, 0, 4, y)
    scr.addstr(1, 1, " 17")
    
    for i in range(5):
        scr.addstr(i+2, 1, months[i])
    
    scr.addch(13, 10, scr.inch(10, 5))
    scr.addch(11, 10, curses.ACS_HLINE)
    scr.addch(12, 10, curses.ACS_VLINE)
    
    # scr.addch(1,5,dot[5])
    scr.addch(15, 1, bl, curses.color_pair(1))
    scr.addch(16, 1, di, curses.color_pair(2))
    scr.addch(17, 1, dg, curses.color_pair(3))
    scr.addch(18, 1, bd, curses.color_pair(4))
    scr.addch(19, 1,'o', curses.color_pair(4));
    
    char=scr.getch()
    while char != ord('q') and char != 27:
        char=scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
