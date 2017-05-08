import calendar
import curses
import re

folder='\x1b[0;34;40m'
GRN ="\x1b[1;32;40m"
yellow='\x1b[0;33;40m'
RED ='\x1b[1;31;40m'
END ='\x1b[0m'

def main(scr):
    cal = calendar.TextCalendar()
    a = cal.formatmonth(2017,3).split('\n')
    b = cal.formatmonth(2017,4).split('\n')
    c = cal.formatmonth(2017,5).split('\n')
    scr.border()
    #bd = curses.ACS_CKBOARD
    #li = curses.ACS_BOARD
    j = 1
    for i in range(len(a)):
        scr.addstr(j,1 ,"{}".format(a[i]))
        scr.addstr(j,20,"{}".format(b[i]))
        scr.addstr(j,40,"{}".format(c[i]))
        j+= 1
    scr.getch(0,0)
    curses.endwin()


if __name__=="__main__":
    curses.wrapper(main)
