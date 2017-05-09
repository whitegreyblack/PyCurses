import background as bg

class Tab:
    def __init__(self, title, parent, tab):
        """
        Args:
            title: tab name
            parent: reference to parent object (should be type <tabmanager>)
            window: reference to curses window object
            child: reference to child window object
        """
        self.title = title
        self.parent = parent
        self.tab = tab
        self.win = None
        self.y,self.x = tab.getmaxyx()
        self.toggle_name = False
        self.toggle_border = False

    def toggle_border_switch(self, cl):
        """
        Changes border color to input color
        Args:
            cl: color of tab border
        """
        self.tab.border(cl,cl,cl,cl,cl,cl,cl,cl)

    def toggle_all_on(self, cl):
        """
        Changes border color to light and brings up child window
        Args:
            cl: color of tab border
        """
        self.toggle_border_on(cl)
        self.toggle_name_on()
        #self.child.toggle_on()
        self.tab.refresh()
        
    def toggle_name_on(self):
        """ Writes tab title to window """
        self.tab.addstr(1, 1, "{}".format(self.title),bg.re)
        self.toggle_name = True
        self.tab.refresh()
    
    def toggle_border_on(self, cl=None):
        """ 
        Draws tab border 
        """
        if not cl:
            self.tab.border()
        else:
            slef.tab.border(cl, cl, cl, cl, cl, cl, cl, cl)
        if self.toggle_name: self.toggle_name_on()
        self.toggle_border = True
        self.tab.refresh()
    def toggle_border_active(self, cl=None):
        pass
    def toggle_all_off(self, cl):
        """
        Changes border color to dark and brings up child window
        Args:
            cl: color of tab border
        """
        self.toggle_border_switch(cl)
        self.toggle_name()
        self.tab.refresh()
        self.child.toggle_off()
        self.tab.refresh()

    def toggle_name_off(self):
        """
        Clears window of name, redraws border if border is on
        """
        self.tab.clear()
        if toggle_border:
            self.toggle_border_on()
        self.tab.refresh()

    def toggle_border_off(self):
        """
        Clears window of border, writes name if name is on
        """
        self.tab.clear()
        if toggle_name:
            self.toggle_name_on()
        self.tab.refresh()

    def load(self):
        """ 
        Calls child load function to load sql data 
        """
        self.child.load()