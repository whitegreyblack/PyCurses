import tabs

class TabManager:
    def __init__(self, parent):
        """
        Creates new tabs  based on number of titles passed to manager
        Args:
            parent: reference to parent object
        """
        self.tx = 1
        self.tabs = []
        self.parent = parent
        self.y, self.x = parent.window.getmaxyx()
        self.window = parent.window.subwin(3, self.x, 0,0)
        self.active = 0

    def add_tabs(self, titles):
        ty, ny = 0, 3
        for i in titles:
            nx = len(i)+2
            self.tabs.append(tabs.Tab(i, self, self.window.subwin(
                ny, nx, ty, self.tx)))
            self.tx += self.tabs[-1].x+1

    def toggle_border_on(self):
        self.window.border()

    def toggle_border_off(self):
        self.window.clear()
    
    def toggle_name_on(self):
        self.window.addstr(0, self.x-11, "{}".format("TabManager"))

    def toggle_name_off(self):
        self.window.clear()

    def toggle_tab_border(self, i):
        self.tabs[i].toggle_border_on()

    def toggle_tabs_border(self):
        for i in self.tabs:
            i.toggle_border_on()

    def toggle_tabs_border_inactive(self, cl):
        for i in self.tabs:
            i.toggle_border_inactive()

    def toggle_tabs_border_active(self, cl):
        for i in self.tabs:
            i.toggle_border_active()

    def toggle_tab_border_active(self, cl, i):
        self.tabs[i].toggle_border_active()

    def toggle_tab_name(self, i):
        self.tabs[i].toggle_name_on()

    def toggle_tabs_name(self):
        for i in self.tabs:
            i.toggle_name_on()

    def toggle_activate(self):
        if self.tabs:
            self.active = self.tabs[0]
    
    def scroll(self, i):
        self.tabs[self.active].toggle_inactive()
        self.active += i
        if self.active < 0:
            self.active = 0
        if self.active > len(self.tabs)-1:
            self.active = len(self.tabs)-1
        self.tabs[self.active].toggle_active()
