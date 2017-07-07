import itertools
import calendar
import re
import random
import curses
import braille

def getMonths(s, e):
    s = dateParser(s)
    e = dateParser(e)
    years = [i for i in range(s['year'], e['year']+1)]
    months=[]
    if len(years)>1:
        for i in range(len(years)):
            if not i:
                months.append([i for i in range(s['month'],13)])
            elif i==len(years)-1:
                months.append([i for i in range(1,e['month']+1)])
            else:
                months.append([i for i in range(1, 13)])
    else:
        months.append([i for i in range(s['month'], e['month']+1)])
    return years, months

def dateParser(d):
    d = d.split("-")
    return {
        "year":int(d[0]),
        "month":int(d[1]),
        "day":int(d[2]),
        }

def dateFold(m):
    def parse(l):
        return modify(list(filter(lambda x: x!='',l.split(" "))))
    def modify(l):
        return [' '+x if int(x) < 9 else x for x in l]
    while len(m) > 1:
        m1 = list(filter(lambda l:len(l)>1, m.pop(-2)))
        if len(m1[-1].split(" ")) == 7:
            m1.extend(m.pop(-1))
        else:
            m2 = m.pop()
            m1[-1] = " ".join((m1[-1].split(" ")+parse(m2[0])))
            m1.extend(m2[1::])
        if not len(m1[-1]):
            m1.pop(-1)
        m.append(m1)
    return m[0]

def tablize(m):
    for i in range(len(m)):
        m[i] = list(filter(lambda x:x!="",m[i].split(" ")))
    return m

def main(window):
    loc = 0
    # dateParser(db.getMinDate, db.getMaxDate)
    d1, d2 = dateParser("2017-2-28"), dateParser("2017-7-6")

    y, m = getMonths("2015-1-12", "2015-3-6")
    tc = calendar.TextCalendar()
    tc.setfirstweekday(6)
    months=[]
    for i in range(len(y)):
        for j in range(len(m[i])):
            months.append(tc.formatmonth(y[i], m[i][j]).split("\n")[2::])
    window.border()
    line = 1
    for i in tablize(dateFold(months)):
        for j in range(len(i)):
            window.addstr(line, j+1, "X")
        line += 1
    y, x=window.getmaxyx()
    #sub=curses.newpad(y//2, x//2)
    #sub.addstr(1,1,'asdfasdfasd')
    #sub.refresh(3, 3, 10, 10,8, 1)
    window.vline(1,8,curses.ACS_VLINE,y-1)
    window.getch()
    #sub.getch()
if __name__ == "__main__":
    curses.wrapper(main)
