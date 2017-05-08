import db_connection
import tabs
import background as bg

class TabsManager:
    def __init__(self, parent):
        """
        Creates new connection and uses titles to add tabs to manager
        Args:
            titles: the title for each tab object
            parent: reference to parent object
            window: the curses window object
        """
        self.parent = parent
        y, x = parent.getmaxyx()
        self.window = parent.subwin(5,x,0,0)
        self.tabs = None

        #self.tabs = [Tab(tabnames[i], self, parent.subwin(2, 9, 0, i*10), Window(parent,parent.subwin(y-2, x, 2, 0))) for i in range(len(tabnames))]
        #self.count = len(self.tabs)
        #[(i.toggle_off(), i.child.load()) for i in self.tabs]
        #self.tabs[0].toggle_on()
        #parent.hline(2, 0, bd, x)
        
    def toggle_border_on(self):
        self.window.border()
    def toggle_border_off(self):
        self.window.clear()
    def toggle_title_on(self):
        self.window.addstr(0,1,"{}".format("Tab Manager"))
    def toggle_title_off(self):
        self.toggle_border_on()
    def add_tab(self, title):
        ox, oy, nx, ny = None, None, None, None




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