"""UI Button component"""
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

    def __init__(self, label=None, box=None, flags=None):
        super().__init__()
        # the flags would have the properties with boolean?(undeterminded)
        self.label = label if label else Button.label
        
        # begin with starting point (0, 0) initially and overwrite on draw
        self.pivot = utils.point(0, 0)
        self.bounds = None # will be a tuple of two points
        if not box:
            if len(self.label) < Button.width - 2:
                self.width = Button.width
            else:
                self.width = len(self.label) + 2    
            self.height = Button.height
        else:
            # these are manually set so assume they are correct
            self.width = box.width
            self.height = box.height 

        if flags:
            self.focused = False
            self.selected = flags & Control.SELECTED
            self.disabled = False # property changes the border color
            self.bordered = Control.bordered
            if flags & Control.NOBORDER:
                self.bordered = False # | Control.bordered # (flag & enum | default)
                if not box:
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
            p2 = utils.point(pivot.x + self.width - 1, pivot.y + self.height - 1)
            self.bounds = pivot, p2

        x, y = self.pivot

        color = curses.color_pair(1)
        if self.selected:
            color = curses.color_pair(2)

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

if __name__ == "__main__":
    import curses
    from source.utils import initialize_curses_settings
    from source.utils import point
    def main(term):
        initialize_curses_settings()
        default = Button()
        selected = Button('Text')
        centered = Button('Text', flags=Control.CENTERED)
        large = Button('Large', box=utils.size(14, 6))
        
        # selected through constructor flags parameter
        flagged = Button('Flagged', flags=Control.SELECTED)
        # both selected and centered properties
        selected_centered = Button('Text1', 
                                   flags=Control.SELECTED | Control.CENTERED)
        selected.select() # manual select

        unbordered = Button('NoBorder', flags=Control.NOBORDER) # should be

        mouse_down = False
        element_clicked = None
        point_clicked = None
        mouse_scroll = 0
        mouse_move = False
        px, py = 0, 0
        while True:
            term.erase()

            if mouse_down:
                term.addstr(13, 0, "Mouse click")

            if mouse_move:
                term.addstr(14, 0, "Mouse moved")

            if element_clicked:
                term.addstr(15, 0, "element")
                element_clicked.clicked(term)
            elif point_clicked:
                term.addstr(15, 0, f"point(x={point_clicked[0]}, y={point_clicked[1]})")
                term.addstr(16, 0, f"other(a={other_mouse[0]}, buttonmask={other_mouse[1]})")

            if mouse_scroll:
                term.addstr(17, 0, f"scrolling {'up' if mouse_scroll == 1 else 'down'}")
            
            default.draw(term, point(0, 0))
            selected.draw(term, point(8, 0))
            large.draw(term, point(16, 0))
            flagged.draw(term, point(30, 0))
            centered.draw(term, point(39, 0))
            selected_centered.draw(term, point(47, 0))
            unbordered.draw(term, point(55, 0))
            term.addstr(7, 0, "Default button shows button with all defaults.")
            term.addstr(8, 0, "Selected button shows button with selected property as true manually.")
            term.addstr(9, 0, "Large button shows button with a size input. ex. Size=(14, 6).")
            term.addstr(10, 0, "Flagged button shows button with selected property as true through constructor.")
            term.addstr(11, 0, "Next button shows button initialized with multiple flags: Selected and Centered.")

            # term.refresh()
            key = term.getch()
            term.addstr(6, 0, str(key))
            if key == ord('q'):
                break
            if key == ord('s'):
                default.select()
            if key == ord('S'):
                default.unselect()
            if key == curses.KEY_MOUSE:
                # probably need to write a mouse handler
                # ex curses_mouse_handler as mouse
                mouse_down = True
                a, px, py, _, mask = curses.getmouse()

                e = 0
                for element in Control.elements:
                    if element.covers(point(px, py)):
                        element_clicked = element
                        point_clicked = None
                        break
                else:
                    if mask == 65536:
                        mouse_scroll = 1
                    elif mask == 2097152:
                        mouse_scroll = 2
                    element_clicked = None
                    point_clicked = px, py
                    other_mouse = a, mask
            else:
                mouse_down = False
                element_clicked = None
            if key == curses.KEY_MOVE:
                mouse_move = True
            else:
                mose_move = False
    curses.wrapper(main)
