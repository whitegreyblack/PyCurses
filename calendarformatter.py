import itertools
import calendar
import re
import random
import curses
import braille
import source.config as config
import source.resources as strings
from collections import namedtuple

date = namedtuple("Date", "Year Month Day")

class CalendarGrid:
    """Takes in all available dates and builds a graph between each
    available date

    Ex. first two weeks of Sep 2018 would have a graph:
       _____________________(1)
      /   /   /   /   /   /  |
    (2)-(3)-(4)-(5)-(6)-(7)-(8)

    While all nodes in the second week would only go from left and right,
    they would also be able to go to node 1 on an up key due to the single
    node in the second week. However a down key from node 1 would result in
    going to node 8.

    TODO: implement the class
    """
    pass

def iter_months_years(startDate: object, endDate: object) -> tuple:
    """Returns years and months based on given start and end dates. Expected
    date format is YYYY-MM-DD. Ex. 2012-07-15
    """
    
    # TODO: Make the function an iterable

    months = []
    # begin with all years between start and end date
    years = [year for year in range(startDate.Year, endDate.Year + 1)]

    if len(years) > 1:
        # covering more than a single year, find the months being used
        for year in range(len(years)):
            monthsRange = (1, 13) # normal year covers between months 1-12
            if year == 0:
                monthsRange = (startDate.Month, 13)  # first year in list
            elif year == len(years) - 1:
                monthsRange = (1, endDate.Month + 1) # last year in list

            months.append([month for month in range(*monthsRange)])
    else:
        # dates are in the same year. grab the months between the dates
        months.append([i for i in range(startDate.Month, endDate.Month + 1)])

    return [(year, m) for year, month in zip(years, months) for m in month]

def parse_date(datestring: str) -> object:
    """Takes in a string object representing a formatted date. If not
    formatted correctly, will raise an error giving description of the correct
    format. Returns a date object with year, month, date properties
    """
    if not re.match(config.DATE_FORMAT_REGEX, datestring):
        error = f"{strings.DATE_FORMAT_INVALID} {strings.DATE_FORMAT_EXPECTED}"
        raise ValueError(error)

    return date(*[int(i) for i in datestring.split('-')])

def dateFold(m):
    def parse(l):
        return modify(list(filter(lambda x: x != '', l.split(" "))))

    def modify(l):
        return [' ' + x if int(x) < 9 else x for x in l]

    while len(m) > 1:
        m1 = list(filter(lambda l: len(l) > 1, m.pop(-2)))

        if len(m1[-1].split(" ")) == 7:
            m1.extend(m.pop(-1))
        else:
            m2 = m.pop()
            m1[-1] = " ".join((m1[-1].split(" ") + parse(m2[0])))
            m1.extend(m2[1::])

        if not len(m1[-1]):
            m1.pop(-1)

        m.append(m1)
    
    return m[0]

def tablize(m):
    for i in range(len(m)):
        m[i] = list(filter(lambda x:x!="",m[i].split(" ")))
    return m

def initialize_curses_settings():
    curses.curs_set(0)

def main(window):
    """Creates a navigatable calendar widget for the dates passed in. Later on
    should use min/max dates from the database holding the date infos.
    """
    initialize_curses_settings()

    loc = 0
    # dateParser(db.getMinDate, db.getMaxDate)
    start = parse_date("2018-5-28")
    end = parse_date("2018-6-28")

    tc = calendar.TextCalendar()
    # called to set the start day when formatmonth returns
    tc.setfirstweekday(calendar.SUNDAY)
    
    # monthdatescalendar -> returns Wx7 matrix of datetime objects
    # monthdays2calendar -> returns Wx7 matrix of tuple objects (day number, day enum val)
    # monthdayscalendar -> returns Wx7 matrix of ints representing the date

    for year, month in iter_months_years(start, end):
        pass

    '''
    months=[]
    for i in range(len(y)):
        for j in range(len(m[i])):
            months.append(tc.formatmonth(y[i], m[i][j]).split("\n")[2::])
    '''
    window.border()
    y, x = window.getmaxyx()
    window.vline(1, 8, curses.ACS_VLINE, y - 2)
    
    line = 2
    window.addstr(1, 1, "SMTWTFS")

    '''
    for i in tablize(dateFold(months)):
        for j in range(len(i)):
            window.addstr(line, j + 1, "X")
        line += 1
        if (line % 5) == 0:
            line += 1
    ''' 
    
    #sub=curses.newpad(y//2, x//2)
    #sub.addstr(1,1,'asdfasdfasd')
    #sub.refresh(3, 3, 10, 10,8, 1)

    window.getch()

if __name__ == "__main__":
    curses.wrapper(main)
