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

class DateNode:
    # include the year?
    def __init__(self, daydate, weekday):
        self.daydate = daydate
        self.weekday = weekday
        # this is a lot of references to other nodes
        # using the image example above, week 1 would have 
        #                    1 |  1
        #  3  4  4  4  4  4  3 | 26
        #  1                   |  1
        #                        28 references excluding other 4 weeks.
        # unless instead of having the date object be saved as a reference,
        # we only save the date number so it would be 8 bytes instead of 28.

        # if no paths then keep paths at 0? use binary flags instead of val?
        # if had south and east paths then self.paths == 6
        self.paths = 0
        self.n = None   # path |= 1
        self.s = None   # path |= 2
        self.e = None   # path |= 4
        self.w = None   # path |= 8

    # def __new__(cls, daydate, weekday):
    #     print(daydate, weekday)
    #     if daydate == 0:
    #         return super(DateNode, cls).__new__(cls, 0, 0)
    #     return super(DateNode, cls).__new__(cls, daydate, weekday)

    def __str__(self):
        def format_path(path, unicode=False):
            val = getattr(self, path)
            if unicode:
                return "_" if not val else unicode_arrows[path]
            
            return "__" if not val else f"{val:02}"
        paths = ", ".join(map(lambda x: format_path(x, True), 
                              "n s e w".split()))
        return f"Date({self.daydate:02}, {self.weekday}, {paths})"

    def __repr__(self):
        return str(self)

class MonthGrid:
    """
    TODO: implement the class
    """
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.__calendar = calendar.Calendar(firstweekday=6)
        
    def build(self):
        self.grid = self.__calendar.monthdays2calendar(self.year, 
                                                       self.month)
        # convert nodes to datanode objects
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                self.grid[j][i] = DateNode(*day)
        
        # they should all be DateNodes now
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                if day.daydate == 0:
                    continue

                # connect nodes if within bounds, probably could rewrite this
                # north
                prevweek = j - 1
                if prevweek >= 0:
                    val = self.grid[prevweek][i].daydate
                    self.build_link(i, j, "n", self.grid[prevweek][i].daydate)

                # south
                nextweek = j + 1
                if nextweek <= len(self.grid) - 1:
                    self.build_link(i, j, "s", self.grid[nextweek][i].daydate)

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
        return "\n".join(", ".join(str(d) for d in w) for w in self.grid)

    def __repr__(self):
        return str(self)

class CalendarGrid:
    """
    TODO: implement the class
    """
    def __init__(self, year):
        pass