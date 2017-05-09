import background as bg

class Tab:
    def __init__(self, name, parent, tab):
        self.name = name
        self.parent = parent
        self.tab = tab
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

    def toggle_all_on(self):
        """
        Draws normal border and tab title
        """
        self.toggle_border_on()
        self.toggle_name_on()
        #self.child.toggle_on()
        self.tab.refresh()
        
    def toggle_on(self):
        self.toggle_border_active()
        self.toggle_name_on()
    
    def toggle_active(self):
        self.toggle_border_active()
        self.toggle_name_on()

    def toggle_inactive(self):
        self.toggle_border_inactive()
        self.toggle_name_on()

    def toggle_name_on(self):
        """ Writes tab title to window """
        self.tab.addstr(1, 1, "{}".format(self.name),bg.re)
        self.toggle_name = True
        self.tab.refresh()
    
    def toggle_border_on(self):
        """ 
        Draws tab border 
        """
        self.tab.border()
        if self.toggle_name: 
            self.toggle_name_on()
        self.toggle_border = True
        self.tab.refresh()

    def toggle_border_active(self, cl=None):
        self.tab.border(bg.li, bg.li, bg.li, bg.li,
            bg.li, bg.li, bg.li, bg.li)
        self.tab.refresh()

    def toggle_border_inactive(self, cl=None):
        self.tab.border(bg.bd, bg.bd, bg.bd, bg.bd,
            bg.bd, bg.bd, bg.bd, bg.bd)
        self.tab.refresh()

    def toggle_all_off(self, cl):
        """
        Changes border color to dark and brings up child window
        Args:
            cl: color of tab border
        """
        self.toggle_border_off()
        self.toggle_name()
        self.tab.refresh()

    def toggle_off(self):
        self.toggle_border_inactive()
        self.toggle_name_on()

    def toggle_name_off(self):
        """
        Clears window of name, redraws border if border is on
        """
        self.tab.clear()
        if self.toggle_border:
            self.toggle_border_on()
        self.tab.refresh()

    def toggle_border_off(self):
        """
        Clears window of border, writes name if name is on
        """
        self.tab.clear()
        if self.toggle_name:
            self.toggle_name_on()
        self.tab.refresh()

    def load(self):
        """ 
        Calls child load function to load sql data 
        """
        #@self.child.load()
        pass