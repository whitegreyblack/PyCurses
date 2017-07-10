import windows as wins


class WinManager:
    def __init__(self, parent):
        """
        Creates new windows based on number of titles passed to manager
        Args:
            parent: reference to parent object
        """
        self.wins = []
        self.parent = parent
        self.y, self.x = self.parent.window.getmaxyx()
        self.window = self.parent.window.subwin(self.y-2, self.x, 2, 0)
        self.active = 0

    def add_wins(self, titles):
        ty, tx = 2, 0
        for title in titles:
            self.wins.append(wins.Window(
                title,
                self,
                self.window.subwin(
                    self.y-2,
                    self.x,
                    ty,
                    tx)))

    def toggle_border_on(self):
        self.window.border()

    def toggle_border_off(self):
        self.window.border()

    def toggle_name_on(self):
        self.window.addstr(0, self.x-11, "{}".format("WinManager"))

    def toggle_name_off(self):
        self.window.clear()

    def toggle_win_border(self, i):
        self.wins[i].toggle_border_on()

    def toggle_wins_border(self):
        for i in self.wins:
            i.toggle_border_on()

    def toggle_win_border_active(self, cl, i):
        self.wins[i].toggle_border_active(cl)

    def toggle_win_name(self, i):
        self.wins[i].toggle_name_on()

    def toggle_wins_name(self):
        for i in self.wins:
            i.toggle_name_on()

    def scroll(self, i):
        self.wins[self.active].toggle_off()
        self.active += i
        if self.active < 0:
            self.active = 0
        if self.active > len(self.wins)-1:
            self.active = len(self.wins)-1
        self.wins[self.active].toggle_on()
