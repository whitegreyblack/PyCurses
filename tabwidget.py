import basewidget


class Tab(basewidget.BaseWidget):
    def __init__(self, name, parent, tab):
        super(Tab, self).__init__(name, parent, tab)
        self.ny = 1
        self.nx = 1

    def toggle_active(self):
        super(Tab, self).toggle_border_active()
        super(Tab, self).toggle_name_on()

    def toggle_inactive(self):
        super(Tab, self).toggle_border_inactive()
        super(Tab, self).toggle_name_on()
