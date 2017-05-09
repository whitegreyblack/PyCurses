import windows as wins

class WinManager:
    def __init__(self, parent):
        self.wins = []
        self.parent = parent
        self.y, self.x = self.parent.window.getmaxyx()
        self.window = self.parent.window.subwin(self.y-3, self.x, 3, 0) 

    def add_wins(self, titles):
        for title in titles:
            self.wins.append(wins.Window(title, self, self.window.subwin(
                self.y-3, self.x, 3, 0)))

    def toggle_border_on(self):
        self.window.border()

    def toggle_win_border(self, i):
        self.wins[i].toggle_border_on()

    def toggle_wins_border(self):
        for i in self.wins:
            i.toggle_border_on()

    def toggle_win_name(self):
        self.wins[i].toggle_name_on()

    def toggle_wins_name(self):
        for i in self.wins:
            i.toggle_name_on()