import tabs

class TabManager:
    def __init__(self, parent):
        self.tx = 1
        self.tabs = []
        self.parent = parent
        self.y, self.x = parent.window.getmaxyx()
        self.window = parent.window.subwin(3, self.x, 0,0)
    def add_tabs(self, titles):
        ty, ny = 0, 3
        for i in titles:
            nx = len(i)+2
            self.tabs.append(tabs.Tab(i, self, self.window.subwin(
                ny, nx, ty, self.tx)))
            self.tx += self.tabs[-1].x+2  
    
    def toggle_border_on(self):
        self.window.border()
    def toggle_tab_border(self, i):
        self.tabs[i].toggle_border_on()

    def toggle_tabs_border(self):
        for i in self.tabs:
            i.toggle_border_on()

    def toggle_tab_name(self, i):
        self.tabs[i].toggle_name_on()

    def toggle_tabs_name(self):
        for i in self.tabs:
            i.toggle_name_on()