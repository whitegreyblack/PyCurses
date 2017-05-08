class Tab:
    def __init__(self, title, parent, window):
        """
        Args:
            title: tab name
            parent: reference to parent object (should be type <tabmanager>)
            window: reference to curses window object
            child: reference to child window object
        """
        self.title = title
        self.parent = parent
        self.window = window
        self.child = None
        self.x,self.y = window.getmaxyx()

    def toggle_on(self, cl):
        """
        Changes border color to light and brings up child window
        Args:
            cl: color of tab border
        """
        self.toggle_border(cl)
        self.toggle_name()
        self.child.toggle_on()
        self.window.refresh()

    def toggle_off(self, cl):
        """
        Changes border color to dark and brings up child window
        Args:
            cl: color of tab border
        """
        self.toggle_border(cl)
        self.toggle_name()
        self.window.refresh()
        self.child.toggle_off()
        self.window.refresh()

    def toggle_border(self, cl):
        """
        Changes border color to input color
        Args:
            cl: color of tab border
        """
        self.window.border(cl,cl,cl,cl,cl,cl,cl,cl)

    def toggle_name(self):
        """ Writes tab title to window """
        self.window.addstr(1, 1, "{}".format(self.title))

    def load(self):
        """ Calls child load function to load sql data """
        self.child.load()