import curses
import calendar
import re
import random
import braille
class Box:
    def __init__(self, screen):
        self.screen = screen

def main(scr):
    board = curses.ACS_BULLET
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    tc = calendar.TextCalendar()

    scr.addstr(10,10, "{}".format(curses.COLORS))
    sub = scr.subwin(15, 15, 15, 15)
    scr.border()
    scr.bkgd(" ", curses.color_pair(1))
    #scr.bkgd(curses.ACS_BOARD,curses.color_pair(3))

    lines = tc.formatmonth(2017, 3).split("\n")
    mores = tc.formatmonth(2017, 4).split("\n")
    x, y = 0, 0
    # month
    # days
    # 2-6 weeks
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j].isdigit():
                #if j+1 <= len(lines[i])-1 and lines[i][j+1].isdigit():
                #    scr.addch(i, j, braille.dot['to'][int(lines[i][j])])
                #else:
                scr.addch(i + 1,j + 1, board)
            else:
                scr.addch(i + 1,j + 1, lines[i][j])
        y+=1

    for i in range(len(mores)):
        for j in range(len(mores[i])):
            if mores[i][j].isdigit():
                scr.addch(i + 1, j + 22, board)
            else:
                scr.addch(i + 1, j + 22, mores[i][j])

    evens=tc.formatmonth(2017,5).split("\n")
    for i in range(len(evens)):
        for j in range(len(evens[i])):
            if evens[i][j].isdigit():
                scr.addch(i + 1, j + 44, board)
            else:
                scr.addch(i + 1, j + 44, evens[i][j])
    #for i in range(7):
    #    for j in range(10):
    #        scr.addch(i,j,curses.ACS_BOARD)
        #scr.addstr(i,0,line[i])
    '''
    for i in range(len(lines)):
        if i != 1:
            for j in range(len(lines)):
                for k in range(len(i)):
                    if k != ' ':
                        scr.addch(i)
    '''
    #sub.bkgdset('/',curses.color_pair(3))
    #sub.bkgd('/',curses.color_pair(2))
    sub.clear()
    sub.addstr(0,0,"{}".format("second win"))
    sub.bkgd(" ",curses.color_pair(1))
    sub.border()
    #sub.refresh()
    #sub.border()
    c = scr.getch()
    if c != ord('q'):
        if c == curses.KEY_MOUSE:
            sub.addstr(1,0,"mouseclicked")
        c = scr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
