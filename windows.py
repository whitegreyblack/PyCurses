import background as bg

class Window:
    def __init__(self, name, parent, win):
        self.name = name
        self.parent = parent
        self.win = win
        self.y, self.x = self.win.getmaxyx()
        self.toggle_border, self.toggle_name = False, False
    
    def toggle_on(self):
        self.toggle_border_active()
        self.toggle_name_on()

    def toggle_border_on(self):
        self.win.border()
        if self.toggle_name:
            self.toggle_name_on()
        self.win.refresh()

    def toggle_name_on(self):
        self.win.addstr(0,1,"{}".format(self.name))
        self.win.refresh()

    def toggle_border_active(self, cl=None):
        self.win.border(bg.li, bg.li, bg.li, bg.li,
            bg.li, bg.li, bg.li, bg.li)
            
    def toggle_off(self):
        self.win.clear()

'''
        y, x = mainscr.getmaxyx()
        self.window = window
        self.mainscr = mainscr
        self.left = window.subwin(y-4, x//2-1, 3, 1)
        self.right = window.subwin(y-4, x//2-1, 3, x//2)
        self.border()
        self.left.border(), self.right.border()
        self.datapos = 0
        self.months = WinCalendar(self, self.right)

    def setparent(self, parent):
        self.parent = parent
    def toggle_on(self):
        if self.parent.title.lower()=="reciept":
            i = 2
            for store, date, _, _, _, _, total in self.datahead.data:
                if i // 2 - 1 == self.datahead.pos:
                    self.window.addstr(i,2,"{d} | {n:{l}} | {t:5.2f}".format(
                        n=store, 
                        l=self.datahead.maxas,
                        d=date,
                        t=total
                        ), curses.A_REVERSE)
                else:
                    self.window.addstr(i,2,"{d} | {n:{l}} | {:5.2f}".format(
                        total,
                        n=store, 
                        l=self.datahead.maxas,
                        d=date,
                        ))
                i+=2
            i = 2
            for m in self.datahead.month:
                self.window.addstr(i, 60, "{:6} : {:6.2f}".format(
                    calendar.month_name[m[0]], m[1]))
                i+=2
            self.window.addstr(i, 60, "Total = {}".format(self.datahead.total))
        """
        if self.parent.title.lower()=="grocery":
            i = 2
        if self.parent.title.lower()=="payment":
            self.window.addstr(7,1,'{} active'.format(self.parent.title))
        """
        self.window.overwrite(self.mainscr)
        #self.window.refresh()
        self.toggleMonths()
        self.window.refresh()
    def toggle_off(self):  
        self.window.clear()
        self.border()
        self.window.refresh()
    def toggleMonths(self):
        if self.parent.title.lower()=="reciept":
            for m in self.datahead.month:
                i = 40
                #month = self.months.year.formatmonth(2017, m[0])
                #self.window.addstr(i, 60, "{}".format(type(month)))
                #self.window.addstr(i, 3, "{}".format(self.months.year.formatmonth(2017, m[0])))
                #i+= 5
                # for l in self.months.year.formatmonth(2017, m[0]):
                #     self.window.addstr(35, 3, "{}".format(l))
                #     i+=1
                
    def refresh(self, i, j):
        s, d, _, _, _, _, t = self.datahead.data[i]
        self.window.addstr(i+2, 2, "{} {} {:2f}".format(s, d, t))
        s, d, _, _, _, _, t = self.datahead.data[j]
        self.window.addstr(j+2, 2, "{} {} {:2f}".format(s, d, t), curses.A_REVERSE)
    def border(self):
        self.window.border(bd,bd,bd,bd,bd,bd,bd,bd)
    def load(self):
        if self.parent.title.lower()=="reciept":
            self.datahead = RecieptData([row for row in self.parent.parent.conn.load()])
            self.databody = self.parent.parent.conn.load_body("asdf")
        elif self.parent.title.lower()=="grocery":
            self.data = self.parent.parent.conn.loadByGroup("type",self.parent.title.lower())
'''