"""UI Button component"""
import curses
import source.utils as utils
# TODO: Create a button with internal handling and external api to add more
#       handlers
#     : Add config settings for buttons. Could add to the config file or
#       as properties under the class
# A single call to this class should have the button initialized and ready
# to be drawn to the screen

def fn(pre, f, post):
    pre()
    f()
    post()

def color(state):
    return utils.button_appearances[state]

# Possibly use metaclass instead.
# Allows all derived children of Control to be added to the elements list,
# thus having a single point of access to all children in the application.
class Control:
    elements = []

    # default state
    focused = False
    selected = False
    disabled = False
    bordered = True
    background = None
    centered = False

    # determine flags to use on init constructor
    DEFAULT = 0
    FOCUSED = 1
    SELECTED = 2
    DISABLED = 4
    NOBORDER = 8
    CENTERED = 16

    def __init__(self):
        Control.elements.append(self)

class Label(Control):
    pass

class Button(Control):
    # defaults for button class without arguments passed in
    height = 3
    width = 8
    label = "Button"

    def __init__(self, label=None, size=None, appearance=None, flags=None):
        super().__init__()
        # the flags would have the properties with boolean?(undeterminded)
        self.label = label if label else Button.label
        
        # begin with starting point (0, 0) initially and overwrite on draw
        self.pivot = utils.point(0, 0)
        self.bounds = None # will be a tuple of two points
        if not size:
            if len(self.label) < Button.width - 2:
                self.width = Button.width
            else:
                self.width = len(self.label) + 2    
            self.height = Button.height
        else:
            # these are manually set so assume they are correct
            self.width = size.width
            self.height = size.height 

        if appearance:
            self.appearance = color(appearance)
        else:
            self.appearance = curses.color_pair(1)

        if flags:
            self.focused = False
            self.selected = flags & Control.SELECTED
            self.disabled = False # property changes the border color
            self.bordered = Control.bordered
            if flags & Control.NOBORDER:
                self.bordered = False # | Control.bordered # (flag & enum | default)
                if not size:
                    self.height = 1
            self.centered = flags & Control.CENTERED

        self.handlers = dict()

    def covers(self, point):
        if not self.bounds:
            # not been drawn yet so coordinates are not known yet
            return False

        p1, p2 = self.bounds
        return p1.x <= point.x <= p2.x and p1.y <= point.y <= p2.y

    # key handlers
    def on_key(self, key):
        if key in self.handlers.keys():
            pass

    # these should be core methods in every button but unsure whether to
    # have only one of the focus or select vs both.
    # basically wrappers for properties but called using clearer names
    def focus(self):
        self.focused = True
    def unfocus(self):
        self.focused = False
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False

    # TODO: add handlers the attribute needs to be added with a name
    def handle(self, name, handler):
        setattr(self, name, None)

    def mouse(self, term, mousekey, mx, my):
        if mousekey == 1:
            self.clicked(term)

    def clicked(self, term):
        '''
            Define handler for clicked events
        '''
        if self.selected:
            self.unselect()
        else:
            self.select()
        term.addstr(14, 0, f"Box(w={self.width}, h={self.height}) with label '{self.label}' was clicked")
        

    def draw(self, term, pivot):
        '''     
            +------+
            |Button|
            +------+ 3
                   8
        '''
        if self.pivot != pivot:
            self.pivot = pivot

        p2 = utils.point(pivot.x + self.width , pivot.y + self.height)
        self.bounds = pivot, p2

        x, y = self.pivot

        color = curses.color_pair(1)
        if self.selected:
            color = curses.color_pair(7)

        if self.bordered:
            utils.border(term, x, y, self.width, self.height)

        # determine starting point for label
        if self.centered:
            # centered has no relation to y
            px = (self.width - len(self.label)) // 2 + x
        else:
            width_offset = 1 if self.bordered else 0
            px = x + width_offset

        label = self.label
        if len(self.label) != self.width - 2:
            label = self.label
            if px == x + 1:
                # default label placement, append to end
                label += " " * (self.width - len(self.label) - 2)
            else:
                # probably centered, anyways check length from ends of width - 2
                # check end first since label can start from 0 -> width-1 and 
                # can only overfill to the right
                # TODO
                pass

        height_offset = 1 if self.bordered else 0

        term.addstr(y + height_offset, px, label, color)
        # try:
        #     term.addstr(4, 0, f"P1={self.bounds[0]}")
        # except:
        #     pass
        # try:
        #     term.addstr(5, 0, f"p2={self.bounds[1]}")
        # except:
        #     pass
        # try:
        #     term.addstr(6, 0, f"piv={self.pivot}")
        # except:
        #     pass

if __name__ == "__main__":
    b = Button()