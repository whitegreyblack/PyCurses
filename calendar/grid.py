# grid.py

"""
Takes in all available dates and builds a graph between each available date
This would allow for a interfaceable calendar with interactive dates.

    Ex. first two weeks of Sep 2018 would have a graph:
       +---+---+---+---+---+(1)
      /   /   /   /   /   /  ||
    (2)=(3)=(4)=(5)=(6)=(7)=(8)
    ||  /   /   /   /   /   /
    (9)+---+---+---+---+---+

    While all nodes in the second week would only go from left and right,
    they would also be able to go to node 1 on an up key due to the single
    node in the second week. However a down key from node 1 would result in
    going to node 8.

    Structure:
        Internally the Calendar grid would use the calendar class as the 
        underlying module. All this class is doing is adding nodes for each
        of the dates supplied by the call to days in month in the calendar,
        which would allow it to be navigateable.
        The path to each node can either be None, Single Direction, or Bi-
        Directional. Using the example above, Node 1 and Node 8 would be
        Bi-Directional. However, Node 1 to Node 7 would be None but Node 7
        to Node 1 would be Directional.

    Notes:
        When moving from top to bottom, if no direct node is below the 
        starting node, node searches the leftmost node. For example, if the
        starting node were to be 3 and end node was 9, then the path down
        from node 3 would lead to node 9. This does not mean the path up
        from node 9 would lead to node 3. Only that 3 can access 9 in a 
        single direction. If the starting node were to be 9 and end node 3,
        then node 9 would have to navigate to node 2 before being able to
        reach node 3.

Would need an architecture allowing us to navigate from month to month for
a multi-month or even a multi-year calendar. Start from the smallest unit
possible: the day node

Could use a hashmap using a tuple of (daydate, dayofweek) as a key to a 
class that holds everything we need. It would be an unordered map that
would hold links of each path that a day could navigate to using the tuple
value that each day mapped to.
"""

import calendar
import collections


unicode_arrows = {
    "n": u'\u2191',
    "s": u'\u2193',
    "e": u'\u2192',
    "w": u'\u2190',
}

# just found out this is already implemented by str.center(width)
class String(object):
    @staticmethod
    def center(word, width):
        if len(word) >= width:
            return word
        padding = width - len(word)
        left = right = padding // 2
        right += (padding % 2 == 1)
        return f"{' ' * left}{word}{' ' * right}"

class Days(object):
    days = "Sunday Monday Tuesday Wednesday Thursday Friday Saturday"
    @staticmethod
    def abbrv(l=2):
        return [d[:l] for d in Days.days.split()]

    @staticmethod
    def names():
        return Days.days.split()

class Options:
    NoHeaders = 0x0
    MonthHeader = 0x1
    DayHeader = 0x2
    ColoredHeader = 0x4
    BorderedHeader = 0x8
    SingleMonth = 0x16

    @staticmethod
    def options(options:int) -> str:
        optionstring = []
        optionslist = [
            [Options.NoHeaders, "NoHeaders"],
            [Options.MonthHeader, "MonthHeader"],
            [Options.DayHeader, "DayHeader"],
            [Options.ColoredHeader, "ColoredHeader"],
            [Options.BorderedHeader, "Bordered"],
        ]
        for opt, optstr in optionslist:
            if Options.check(options, opt):
                optionstring.append(optstr)
        return "\n".join(optionstring)

    @staticmethod
    def check(options:int, option:int) -> bool:
        return options & option == option

class EmptyDateNode:
    def __init__(self, daydate, weekday):
        self.daydate = daydate
        self.weekday = weekday

    def __str__(self):
        return "  "
    
    def __repr__(self):
        return f"{' ' * 8}"

    def blt(self, selected=False):
        return self.format_before_print()

    def format_before_print(self):
        # if self.weekday == 5:
        #     return f" {self}"
        # elif self.weekday == 6:
        #     return f"{self} "
        return f" {self} "

    # def blt_data(self):
    #     return " " * 4

class DateNode(EmptyDateNode):
    """
    TODO: include the year?
    TODO: Add unselectable nodes that return [COLOR=Grey] on str return
    """
    def __init__(self, daydate, weekday, selectable=True):
        """
        this is a lot of references to other nodes
        using the image example above, week 1 would have 
                           1 |  1
         3  4  4  4  4  4  3 | 26
         1                   |  1
                               28 references excluding other 4 weeks.
        unless instead of having the date object be saved as a reference,
        we only save the date number so it would be 8 bytes instead of 28.

        if no paths then keep paths at 0? use binary flags instead of val?
        if had south and east paths then self.paths == 6
        """
        super().__init__(daydate, weekday)
        self.paths = 0
        self.n = None   # path |= 1
        self.s = None   # path |= 2
        self.e = None   # path |= 4
        self.w = None   # path |= 8
        self.events = None
        self.max_event_size = 10
        self.selectable = selectable

    def __str__(self):
        return f"{self.daydate:2}"

    def __repr__(self):
        def format_path(path, unicode=False):
            val = getattr(self, path)
            if unicode:
                return "_" if not val else unicode_arrows[path]
            
            return "__" if not val else f"{val:02}"
        paths = ", ".join(map(lambda x: format_path(x, True), 
                              "n s e w".split()))
        return f"Date({self.daydate:2}, {paths})"
        # return f"Date({self.daydate:2})"

    def term(self, selected=False, blt=False) -> str:
        """No colors for WIN10 terminal. Womp Womp"""
        formatted_self = self.format_before_print()
        if self.selectable:
            if blt and selected:
                return f"[bkcolor=white][color=black]{formatted_self}[/color][/bkcolor]"
            elif blt and self.events:
                return f"[bkcolor=gray]{formatted_self}[/bkcolor]"
            return formatted_self
        if blt:
            return f"[color=grey]{formatted_self}[/color]"
        return f"{''.join(' ' for i in formatted_self)}"

    # def blt_data(self):
    #     if self.data:
    #         return u"\u1F53"
    #     else:
    #         return " " * 4

    # def __new__(cls, daydate, weekday):
    #     print(daydate, weekday)
    #     if daydate == 0:
    #         return super(DateNode, cls).__new__(cls, 0, 0)
    #     return super(DateNode, cls).__new__(cls, daydate, weekday)

class MonthGrid:
    """
    TODO: implement the class
    TODO: Add nodes outside of the current month
    TODO: Show outside nodes as grey and unselectable
    """
    def __init__(self, month, year, border=False, events=None):
        self.month = month
        self.month_name = calendar.month_name[month]
        self.year = year
        self.__calendar = calendar.Calendar(firstweekday=6)

        # some UI properties
        self.focused = False
        self.selected = 3
        self.last_day = None
        self.border = border

        self.build()

    def __str__(self):
        month = "\n ".join("  ".join(str(d) for d in w) for w in self.grid)
        return f" {month}"

    def __repr__(self):
        header = self.month_header()
        month = "\n".join("  ".join(repr(d) for d in w) for w in self.grid)
        return f"{header}\n{month}"

    def build(self):
        """Takes the calendar function which returns a tuple of daydate and
        day of the week value for each day in the calendar month into a NxM
        matrix of DateNodes which will be used to print the same exact
        calendar as the TextCalendar but with our own datastructure
        """
        year_prev = year_next = self.year
        month_prev = self.month - 1
        if month_prev == 0:
            month_prev = 12
            self.year_prev = self.year - 1

        self.grid_prev = self.__calendar.monthdays2calendar(year_prev, 
                                                            month_prev)

        # could probably use modulus expression
        month_next = self.month + 1
        if month_next == 13:
            month_next = 1
            year_next = self.year + 1

        self.grid_next = self.__calendar.monthdays2calendar(year_next, 
                                                            month_next)

        self.grid = self.__calendar.monthdays2calendar(self.year, self.month)
        # convert nodes to datanode objects
        for j, week in enumerate(self.grid):
            for i, (date, weekday) in enumerate(week):
                if date is not 0:
                    self.last_day = date
                    self.grid[j][i] = DateNode(date, weekday)
                elif j == 0:
                    self.grid[j][i] = DateNode(*self.grid_prev[-1][i],
                                               selectable=False)
                elif j == len(self.grid) - 1:
                    self.grid[j][i] = DateNode(*self.grid_next[0][i],
                                               selectable=False)
                else: # any other case
                    self.grid[j][i] = EmptyDateNode(date, weekday)

        # they should all be DateNodes now or at least using EmptyDateNode as a fallback
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                # skips non-dates in the calendar
                if day.daydate == 0 or not day.selectable:
                    continue

                # connect nodes if within bounds, probably could rewrite this
                # north
                prevweek = j - 1
                if prevweek >= 0:
                    calendarday = self.grid[prevweek][i]
                    date = calendarday.daydate
                    if not calendarday.selectable:
                        date = 1
                    self.build_link(i, j, "n", date)

                # south
                nextweek = j + 1
                if nextweek <= len(self.grid) - 1:
                    calendarday = self.grid[nextweek][i]
                    date = calendarday.daydate
                    if not calendarday.selectable:
                        date = self.last_day
                    self.build_link(i, j, "s", date)

                # east
                nextday = i + 1
                if i + 1 <= len(self.grid[0]) - 1:
                    self.build_link(i, j, "e", self.grid[j][nextday].daydate)

                # west
                prevday = i - 1
                if prevday >= 0:
                    self.build_link(i, j, "w", self.grid[j][prevday].daydate)

    def build_link(self, i, j, path, val):
        if val > 0:
            setattr(self.grid[j][i], path, val)

    def date(self, day):
        if 0 < day <= self.last_day:
            for week in self.grid:
                for date in week:
                    if date.daydate == day:
                        return date
        return None

    def term(self, options:int=0x0, blt=False):
        # TODO: draw border for body cells on border?
        # +----------------------------------+
        # | ## | ## | ## | ## | ## | ## | ## |
        # +----------------------------------+
        # | ## | ## | ## | ## | ## | ## | ## |
        # +----------------------------------+
        # | ## | ## | ## | ## | ## | ## | ## |
        # +----------------------------------+
        # | ## | ## | ## | ## | ## | ## | ## |
        # +----------------------------------+
        month = self.term_header(options=options)
        month += "\n" if month else ""
        month += "\n".join("".join(d.term(self.selected==d.daydate, blt=blt)
                                            for d in w) 
                                                for w in self.grid)
        return month

    def month_header(self):
        return f"{self.month_name} {self.year}"

    def term_header(self, options:int=0x0):
        """No color for WIN10 term. Color only for blt screen"""
        month = ""
        if Options.check(options, Options.MonthHeader):
            month += f" {self.month_header()}"
        if Options.check(options, Options.DayHeader):
            if bool(month):
                month += "\n"
            days = "  ".join(Days.abbrv())
            if Options.check(options, Options.ColoredHeader):
                days = f"[color=orange]{days}[/color]"
            month += f" {days}"
        return month

    def blt_data(self):
        # TODO: draw border
        if self.border: pass
        header = ""
        body = "\n".join("".join(d.blt_data() for d in w) for w in self.grid)
        return f"{header}\n{body}"

    def events(self):
        date = self.date(self.selected)
        # check for object existence, then object property existence
        if date and date.events:
            return date.events

    def draw(self, term, pivot):
        """Used for drawing the calendar month onto a curses terminal"""
        term.addstr(*pivot, str(self))

    '''we have 4 cases of inputs to handle

    1. 1:1 date to event. Simplest input. Date check, event type check.
        - self.add_event(date, event) Done.
    2. 1:N date to multiple events. Date check, event type checks.
        - for event in events:
              self.add_event(date, event) Done.
    3. N:1 multiple dates to event. Date checks, event type check.
        - for date in dates:
              self.add_event(date, event) Done.
    4. N:N multiple date to multiple events. Not going to handle these.
    '''

    def add_event(self, day, event):
        date = self.date(day)
        if date:
            # event already exists. just add on
            if date.events:
                date.events.append(event)
            else:
                if not isinstance(event, list):
                    if isinstance(event, str):
                        event = [event]
                    else:
                        event = list(event)
                date.events = event

    def add_events(self, day_begin, day_end, event):
        for day in range(day_begin, day_end+1):
            self.add_event(day, event)

    def add_events_json(self, filename:str):
        pass
    
    def add_events_yaml(self, filename:str):
        pass

    def export_events_json(self, filename:str):
        pass

    def export_events_yaml(self, filename:str):
        pass

    def select_prev_week(self):
        prevweekdate = self.selected - 7
        if prevweekdate > 0:
            self.selected = prevweekdate
            return # all is good. exit early

        prevweekdate = self.select_day_from_date(self.selected, "n")
        if prevweekdate:
            self.selected = prevweekdate

    def select_next_week(self):
        nextweekdate = self.selected + 7
        if nextweekdate < self.last_day + 1:
            self.selected = nextweekdate
            return

        nextweekdate = self.select_day_from_date_reverse(self.selected, "s")
        if nextweekdate:
            self.selected = nextweekdate
    
    def select_prev_day(self):
        prevdaydate = self.selected - 1
        if prevdaydate > 0:
            self.selected = prevdaydate

    def select_next_day(self):
        nextdaydate = self.selected + 1
        if nextdaydate < self.last_day + 1:
            self.selected = nextdaydate

    def select_day_from_date(self, day, select) -> int:
        for week in self.grid:
            for date in week:
                if date.daydate == day:
                    return getattr(date, select)
        return 0

    def select_day_from_date_reverse(self, day, select) -> int:
        for week in self.grid[::-1]:
            for date in week[::-1]:
                if date.daydate == day:
                    return getattr(date, select)
        return 0

class YearMonthDay(object):
    def __init__(self, year, month, day=1):
        self.year = year
        self.month = month
        self.day = day
        self.month_name = calendar.month_name[month]
    def __str__(self):
        return f"YearMonthDay({self.day} {self.month_name} {self.year})"
    def __repr__(self):
        return f"YearMonthDay(year={self.year}, month={self.year}, day={self.day})"
    def __iter__(self):
        return iter((self.year, self.month, self.day))
    @classmethod
    def from_json(cls, data):
        """
        Returns a class instance with json data as attributes as long as the
        data is well-formed
        """
        try:
            return cls(data['year'], data['month'], data['day'])
        except:
            raise

class CalendarGrid:
    """
    TODO: implement the class
    """
    def __init__(self, year:(int, int), startdate=None):
        if isinstance(year, int):
            self.year_beg = self.year_end = year
        elif isinstance(year, tuple):
            try:
                self.year_beg, self.year_end = year
            except ValueError:
                self.year_beg = self.year_end = year[0]
        else:
            raise ValueError("""Invalid input for year: Format [year:int] || ([year:int], [year:int])""")
        self.init_build_months()

        if startdate:
            self.year, self.month, self.day = startdate
        else:
            self.year, self.month, self.day = self.year_beg, 1, 1

    @property
    def month(self):
        return self.months[self.year][self.__month-1]

    @month.setter
    def month(self, value):
        self.__month = value

    def init_build_months(self) -> None:
        self.months = {year:[] for year in range(self.year_beg, self.year_end + 1)}
        for year, months in self.months.items():
            for month in range(12):
                months.append(MonthGrid(month + 1, year))

    def format_months(self) -> str:
        data = ""
        for year, months in self.months.items():
            for month in months:
                data += repr(month)
                data += "\n"
        return data

    def term(self, options:int=0x0, blt:bool=False) -> str:
        if Options.check(options, Options.SingleMonth):
            data = ""
            for year, months in self.months.items():
                data += "\n\n".join(month.term(options=options, blt=blt) 
                                    for month in months)
            return data
        return self.month.term(options=options, blt=blt)

class Node:
    def __init__(self, year, month, day, dayofweek, selectable=True):
        self.year = year
        self.month = month
        self.day = day
        self.dayofweek = dayofweek
        self.events = None
        self.max_event_size = 10
        self.selectable = selectable
    def __str__(self):
        return f"{self.day:2}"
    def __eq__(self, val):
        if isinstance(val, Node):
            val = (val.year, val.month, val.day)
        yeq = self.year == val[0]
        meq = self.month == val[1]
        deq = self.day == val[2]
        return yeq and meq and deq
    def blt(self, selected, month):
        s = str(self)
        if self.selectable:
            if selected:
                return f"[bkcolor=white][color=black] {self} [/color][/bkcolor]"
            if self.month == month:
                return f"[color=white] {self} [/color]"
        return f"[color=grey] {self} [/color]"

class ScrollableCalendar:
    """
    Goal is to make a continuous calendar grid from startdate to enddate
    """
    def __init__(self, begdate, enddate, start=None):
        self.begdate = begdate
        self.enddate = enddate
        self.months = set()
        self.calendar = calendar.Calendar(firstweekday=6)
        self.init_build_months()
        self.assign_indices(start if start else begdate)

    @property
    def month(self):
        return self.months[self.year][self.__month-1]

    @month.setter
    def month(self, value):
        self.__month = value

    def iteryearmonths(self):
        """
        Uses calendar.nextmonth to get all (year, month) pairs between
        the start date and end date inclusive.
        """
        months = []
        current = (self.begdate.year, self.begdate.month)
        enddate = calendar.nextmonth(self.enddate.year, self.enddate.month)
        while current != enddate:
            months.append(current)
            current = calendar.nextmonth(*current)
        return months

    def dates_from_yearmonths(self, yearmonths):
        """
        Takes in a list of (year, month) tuples and returns them as 
        (year, month, day, dayofweek) tuples using calendar.itermonthdays4
        """
        dates = set()
        for year, month in yearmonths:
            vals = set(self.calendar.itermonthdays4(year, month))
            dates = dates.union(vals)
        dates = sorted(list(dates), key=lambda x: (x[0], x[1], x[2]))
        return dates

    def build_week_matrix(self, dates):
        """
        Returns a n x 7 matrix of date tuples from a list of unique date tuples
        """
        grid = []
        for w in range(0, len(dates), 7):
            grid.append(dates[w:w+7])
        return grid

    def days_to_nodes(self, grid):
        """
        Returns a n x 7 matrix of Node objects from a list of unique date tuples
        """
        graph = []
        for week in grid:
            nodeweek = []
            for date in week:
                y, m, d, w = date
                selectable = (y, m) in self.months
                n = Node(y, m, d, w, selectable)
                nodeweek.append(n)
            graph.append(nodeweek)
        return graph

    def init_build_months(self) -> None:
        """
        Using the (year, month, day, dayofweek) tuples, builds a continuous
        calendar of datenodes with no breaks between months or years.
        """
        yearmonths = self.iteryearmonths()
        self.months = yearmonths
        dates = self.dates_from_yearmonths(yearmonths)
        grid = self.build_week_matrix(dates)
        self.graph = self.days_to_nodes(grid)

    def assign_indices(self, date):
        """
        Sets the i, j pointers to the current day of the month and year
        """
        self.i = self.j = -1
        y, m, d = date.year, date.month, date.day
        for j, week in enumerate(self.graph):
            for i, day in enumerate(week):
                if (y, m, d) == day:
                    self.j = j
                    self.i = i
        if self.i + self.j == -2:
            raise ValueError("No indices with start date")

    def select_prev_week(self):
        temp = self.i, self.j
        self.j = max(self.j - 1, 0)
        if not self.graph[self.j][self.i].selectable:
            self.i, self.j = temp


    def select_next_week(self):
        temp = self.i, self.j
        self.j = min(self.j + 1, len(self.graph) - 1)
        if not self.graph[self.j][self.i].selectable:
            self.i, self.j = temp

    def select_next_day(self):
        temp = self.i, self.j
        self.i += 1
        if self.i > 6:
            self.i = 0
            self.select_next_week()
            # same week, so entire week belongs to the month
            if self.j == temp[1]:
                self.i, self.j = temp

        # went forward onde day but it was not selectable
        if not self.graph[self.j][self.i].selectable:
            self.i, self.j = temp

    def select_prev_day(self):
        temp = self.i, self.j
        self.i -= 1
        if self.i < 0:
            self.i = 6
            self.select_prev_week()
            # same week, so entire week belongs to the month
            if self.j == temp[1]:
                self.i, self.j = temp
        
        # went back one day but it was not selectable
        if not self.graph[self.j][self.i].selectable:
            self.i, self.j = temp

    def format_blt_header(self, colored=False):
        """No color for WIN10 term. Color only for blt screen"""
        days = "  ".join(Days.abbrv())
        if colored:
            days = f"[color=orange]{days}[/color]"
        return days

    def format_print(self, options=0x0, blt=False) -> str:
        """Returns the weeks based on the options input"""
        if Options.check(options, Options.SingleMonth):
            curnode = self.graph[self.j][self.i]
            year, month, select = curnode.year, curnode.month, curnode.day
            monthstring = []
            for week in self.graph:
                include = any((day.year, day.month) == (year, month) 
                                for day in week)
                if include and not blt:
                    monthstring.append(" ".join(str(day) for day in week))
                elif include and blt:
                    monthstring.append("".join(day.blt(day==curnode, month) 
                                        for day in week))
            return "\n".join(monthstring)

        if not blt:
            return "\n".join(" ".join(str(day) for day in week) 
                                for week in self.graph)
        return "\n".join("".join(day.blt) for day in week
                            for week in self.graph)

if __name__ == "__main__":
    cg = CalendarGrid((2018,))
    print(f"(beginning year={cg.year_beg}, end year={cg.year_end})")
    # print(cg.format_months())
    # print(cg.term(options=0x3))

    # print(cg.term(options=0x3))

    # m = MonthGrid(12, 2018)

    sg = ScrollableCalendar(YearMonthDay(2018, 10), YearMonthDay(2018, 12))
    print(sg.format_print(0))
    print()
    sg = ScrollableCalendar(YearMonthDay(2018, 10), 
                            YearMonthDay(2018, 12), 
                            YearMonthDay(2018, 11, 13))
    print(sg.format_print(0x16))
