import db_connection
import background as bg
import tabmanager as tm
import winmanager as wm

class Manager:
    def __init__(self, window):
        """
        Creates new connection and uses titles to add tabs to manager
        Args:
            window: the curses window object
        """
        self.y, self.x = window.getmaxyx()
        self.window = window
        self.tm = tm.TabManager(self)
        self.wm = wm.WinManager(self)

        self.active = 0

    def toggle_on(self):
        self.toggle_border_on()
        self.toggle_title_on()

    def toggle_off(self):
        self.toggle_border_off()
        self.toggle_title_off()
    def toggle_border_on(self):
        self.window.border()

    def toggle_border_off(self):
        self.window.clear()

    def toggle_title_on(self):
        self.window.addstr(0,1,"{}".format("Manager"))

    def toggle_title_off(self):
        self.toggle_border_on()

    def add_tabs(self, titles):
        self.tm.add_tabs(titles)

    def add_wins(self, titles):
        self.wm.add_wins(titles)

    def toggle_tabs_name(self):
        self.tm.toggle_tabs_name()

    def toggle_tabs_border(self):
        self.tm.toggle_tabs_border()

    def toggle_tabs_border_inactive(self, cl):
        self.tm.toggle_tabs_border_inactive(cl)

    def toggle_tabs_border_active(self, cl):
        self.tm.toggle_tabs_border_active(cl)

    def toggle_tab_border_active(self, cl):
        self.tm.toggle_tab_border_active(cl, self.active)

    def toggle_wins_name(self):
        self.wm.toggle_wins_name()
    
    def toggle_wins_border(self):
        self.wm.toggle_wins_border()

    def toggle_win_border_active(self, cl):
        self.wm.toggle_win_border_active(cl, self.active)

    def toggle_active(self, i):
        #self.tm.toggle_active(i)
        #self.wm.toggle_active(i)
        pass

    def scroll(self, i):
        self.tm.scroll(i)
        self.wm.scroll(i)
    '''
    def active(self):
        self.active = self.tabs[0]
    def update(self,i,j):
        self.tabs[i].toggle_off()
        self.tabs[j].toggle_on()
        self.active = self.tabs[j]
    def load(self, conn):
        [i.load() for i in self.tabs]
    '''

    def del_all(self):
        del self.tm
        del self.wm

    def del_tabs(self, title):
        del self.tm

    def del_wins(self, title):
        del self.wm