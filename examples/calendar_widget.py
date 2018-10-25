"""Calendar_widget.py"""
import re
import curses
import random
import calendar
import itertools
import source.config as config
from collections import namedtuple

date = namedtuple("Date", "Year Month Day")

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

    # return [(year, m) for year, month in zip(years, months) for m in month]
    for year, month in zip(years, months):
        for m in month:
            yield (year, m)


def days_in_month_year(startDate, endDate):
    """Returns the day/date tuple combination for each month/year input passed
    into the calendar.TextCalendar class method months2calendar(year, month).
    
    Differences in TextCalendar methods (W => number of weeks in the month):
        monthdatescalendar -> returns Wx7 matrix of datetime objects
        monthdays2calendar -> returns Wx7 matrix of tuple objects (date, day)
        monthdayscalendar -> returns Wx7 matrix of ints representing the date
    """

    # setup calendar settings to retrieve dates based on year/month pairs
    tc = calendar.TextCalendar()
    tc.setfirstweekday(6) # set to sunday as first day

    days_per_monthyear = dict()
    for year, month in iter_months_years(startDate, endDate):
        days_per_monthyear[(year, month)] = tc.monthdays2calendar(year, month)

    return days_per_monthyear


def parse_date(datestring: str) -> object:
    """Takes in a string object representing a formatted date. If not
    formatted correctly, will raise an error giving description of the correct
    format. Returns a date object with year, month, date properties
    """
    if not re.match(config.DATE_FORMAT_REGEX, datestring):
        error = f"{config.DATE_FORMAT_INVALID} {config.DATE_FORMAT_EXPECTED}"
        raise ValueError(error)

    return date(*[int(i) for i in datestring.split('-')])


def initialize_curses_settings():
    """Curses settings that need to be called before the rest of program"""
    curses.curs_set(0)


def main(window):
    """Creates a navigatable calendar widget for the dates passed in. Later on
    should use min/max dates from the database holding the date infos.
    """
    initialize_curses_settings()

    loc = 0
    # dateParser(db.getMinDate, db.getMaxDate)
    start = parse_date("2017-12-1")
    end = parse_date("2018-2-1")

    # we should now have a list of lists matrix holding weeks per month/year
    monthtable = days_in_month_year(start, end) 
    
    window.border()
    y, x = window.getmaxyx()
    window.vline(1, 8, curses.ACS_VLINE, y - 2)
 
    verticaloffset = 2
    horizontaloffset = 1   
    
    window.addstr(1, 1, "SMTWTFS")
    
    for month in monthtable.values():
        for week in month:
            window.addstr(verticaloffset, horizontaloffset + 9, str(week))
            weekdayindex = 0
            for date, dayofweek in week:
                if (date) != 0:
                    window.addstr(verticaloffset, 
                                  horizontaloffset + weekdayindex, 
                                  'o')
                weekdayindex += 1
            verticaloffset += 1
    
    window.getch()
    # TODO: implement program loop involving vertical/horiontal scrolling


if __name__ == "__main__":
    curses.wrapper(main)
