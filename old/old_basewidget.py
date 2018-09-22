class BaseWidget:
    def __init__(self, name, parent, widget):
        """
        Args:
            title: tab name
            parent: reference to parent object (should be type <tabmanager>)
            widget: reference to curses window object
        """
        self.name = name
        self.ny, self.nx = 0, 0
        self.parent = parent
        self.widget = widget
        self.y, self.x = widget.getmaxyx()
        self.toggle_name = False
        self.toggle_border = False
        self.toggle_style = 0
        self.active = 0

    # -- all variables functions beg --
    def toggle_on(self):
        ''' default toggle turns on border and name '''
        self.toggle_border_on()
        self.toggle_name_on()
    def toggle_off(self):
        self.widget.clear()
    # -- all variables functions end --

    # -- widget name functions beg -- 
    def toggle_name_on(self):
        ''' add name to self window '''
        self.widget.addstr(self.ny, self.nx, "{}".format(self.name))

    def toggle_name_off(self):
        ''' clears window and adds border if flag on '''
        self.widget.clear()
        if self.toggle_border == 2:
            self.toggle_border_active()
        elif self.toggle_border == 1:
            self.toggle_border_inactive()
        else:
            self.toggle_border_on()
    # -- widget name functions end --
   
    # -- widget border functions beg --
    def toggle_border_on(self):
        ''' add default border to widget '''
        self.widget.border()

    def toggle_border_active(self):
        ''' add active border to widget '''
        self.widget.border(bg.li, bg.li, bg.li, bg.li,
            bg.li, bg.li, bg.li, bg.li)

    def toggle_border_inactive(self):
        ''' add inactive border to widget '''
        self.widget.border(bg.bd, bg.bd, bg.bd, bg.bd,
             bg.bd, bg.bd, bg.bd, bg.bd)
        
    def toggle_border_off(self):
        ''' clears window and adds name if flag on '''
        self.widget.clear()
        if self.toggle_name:
            self.toggle_name_on()
    # -- weiget border functions end --