"""calendargrid.py"""

import calendar

"""Notes:
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

unicode_arrows = {
    "n": u'\u2191',
    "s": u'\u2193',
    "e": u'\u2192',
    "w": u'\u2190',
}

class EmptyDateNode:
    def __init__(self, daydate, weekday):
        self.daydate = daydate
        self.weekday = weekday

    def __str__(self):
        return '  '
    
    def __repr__(self):
        return f"{' ' * 8}"

    def blt(self, selected=False):
        return str(self)

    # def blt_data(self):
    #     return " " * 4

class DateNode(EmptyDateNode):
    """
    TODO: include the year?
    TODO: Add unselectable nodes that return [COLOR=Grey] on str return
    """
    def __init__(self, daydate, weekday):
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
        self.data = None

    def blt(self, selected=False):
        if selected:
            return f"[bkcolor=white][color=black]{self}[/color][/bkcolor]"
        elif self.data:
            return f"[bkcolor=gray]{self}[/bkcolor]"
        else:
            return str(self)

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


class MonthGrid:
    """
    TODO: implement the class
    TODO: Add nodes outside of the current month
    TODO: Show outside nodes as grey and unselectable
    """
    def __init__(self, month, year):
        self.month = month
        self.month_name = calendar.month_name[month]
        self.year = year
        self.__calendar = calendar.Calendar(firstweekday=6)

        # some UI properties
        self.focused = False
        self.selected = 3
        self.last_day = None
        self.build()

    def build(self):
        """Takes the calendar function which returns a tuple of daydate and
        day of the week value for each day in the calendar month into a NxM
        matrix of DateNodes which will be used to print the same exact
        calendar as the TextCalendar but with our own datastructure
        """
        self.grid = self.__calendar.monthdays2calendar(self.year, self.month)
        # convert nodes to datanode objects
        for j, week in enumerate(self.grid):
            for i, (date, weekday) in enumerate(week):
                if date is not 0:
                    self.last_day = date
                    self.grid[j][i] = DateNode(date, weekday)
                else:
                    self.grid[j][i] = EmptyDateNode(date, weekday)

        # they should all be DateNodes now or at least using EmptyDateNode as a fallback
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                # skips non-dates in the calendar
                if day.daydate == 0:
                    continue

                # connect nodes if within bounds, probably could rewrite this
                # north
                prevweek = j - 1
                if prevweek >= 0:
                    val = self.grid[prevweek][i].daydate
                    if val < 1:
                        val = 1
                    self.build_link(i, j, "n", val)

                # south
                nextweek = j + 1
                if nextweek <= len(self.grid) - 1:
                    val = self.grid[nextweek][i].daydate
                    if val < 1:
                        val = self.last_day
                    self.build_link(i, j, "s", val)

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

    def __str__(self):
        return "\n".join(" ".join(str(d) for d in w) for w in self.grid)

    def __repr__(self):
        return "\n".join("  ".join(repr(d) for d in w) for w in self.grid)

    def date(self, day):
        if 0 < day <= self.last_day:
            for week in self.grid:
                for date in week:
                    if date.daydate == day:
                        return date
        return None

    def blt(self, month_name=True):
        header = self.header(month_name=month_name)
        body = "\n".join(" ".join(d.blt(self.selected==d.daydate)
                                            for d in w) 
                                                for w in self.grid)
        return f"{header}\n{body}"

    def blt_data(self):
        header = ""
        body = "\n".join(" ".join(d.blt_data() for d in w) for w in self.grid)
        return f"{header}\n{body}"

    def events(self):
        date = self.date(self.selected)
        if date and date.data:
            return date.data

    def header(self, month_name=True, extended=False):
        month_header = self.month_name if month_name else ""
        if extended:
            days = "Sunday Monday Tuesday Wednesday Thursday Friday Saturday"
            month_header += "\n" + "".join(f"{d: <10}" for d in days.split())
        else:
            month_header += "\nSu Mo Tu We Th Fr Sa"
        return month_header

    def draw(self, term, pivot):
        """Used for drawing the calendar month onto a curses terminal"""
        term.addstr(*pivot, str(self))

    def add_event(self, day, event):
        date = self.date(day)
        if date:
            date.data = event

    def add_events(self, day_begin, day_end, event):
        for day in range(day_begin, day_end+1):
            self.add_event(day, event)

    def select_prev_week(self):
        prevweekdate = self.selected - 7
        if prevweekdate > 0:
            self.selected = prevweekdate
            return # all is good. exit early

        # try a fallback value
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

class CalendarGrid:
    """
    TODO: implement the class
    """
    def __init__(self, year):
        pass