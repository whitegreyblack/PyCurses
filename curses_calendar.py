import curses
import calendar

c = calendar.Calendar()
print(c.monthdays2calendar(2017,3))

tc = calendar.TextCalendar()
tc.prmonth(2017,3)

