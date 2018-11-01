"""calendargrid.py"""

import calendar

"""Notes:
Takes in all available dates and builds a graph between each available date
This would allow for a interfaceable calendar with interactive dates.

    Ex. first two weeks of Sep 2018 would have a graph:
       +---+---+---+---+---+(1)
      /   /   /   /   /   /  |
    (2)-(3)-(4)-(5)-(6)-(7)-(8)
     |  /   /   /   /   /   /
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
"""

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
        self.n = None
        self.s = None
        self.e = None
        self.w = None
    def format_path(self, path):
        r = "__" if not path else f"{path:02}"
        return r
    def __str__(self):
        return f"Date({self.daydate:02}, {self.weekday}, {self.format_path(self.n)})"
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
        self.grid = self.__calendar.monthdays2calendar(self.year, self.month)
        # convert nodes to datanode objects
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                self.grid[j][i] = DateNode(*day)
        
        # they should all be DateNodes now
        for j, week in enumerate(self.grid):
            for i, day in enumerate(week):
                # connect nodes
                # north
                try:
                    self.grid[j-1][i]
                except IndexError:
                    pass
                else:
                    self.grid[j][i].n = self.grid[j-1][i].daydate

                # south
                try:
                    self.grid[j+1][i]
                except IndexError:
                    pass
                else:
                    self.grid[j][i].s = self.grid[j][i].daydate

    def __str__(self):
        return "\n".join(", ".join(str(day) for day in week) for week in self.grid)

    def __repr__(self):
        return str(self)

class CalendarGrid:
    """
    TODO: implement the class
    """
    def __init__(self, year):
        pass