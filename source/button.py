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
    BORDERED = 8
    CENTERED = 16

    def __init__(self):
        Control.elements.append(self)

class Button(Control):
    # defaults for button class without arguments passed in
    height = 3
    width = 8
    label = "Button"

    def __init__(self, label=None, box=None, flags=None):
        super().__init__()
        # the flags would have the properties with boolean?(undeterminded)
        self.label = label if label else Button.label
        
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
            self.bordered = flags & Control.BORDERED | Control.bordered # (flag & enum | default)
            self.centered = flags & Control.CENTERED

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

    def draw(self, term, x, y):
        '''     
            +------+
            |Button|
            +------+ 3
                   8
        '''
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
            px = x + 1

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

        term.addstr(y+1, px, label, color)

if __name__ == "__main__":
    import curses
    from source.utils import initialize_curses_settings
    def main(term):
        initialize_curses_settings()
        default = Button()
        selected = Button('Text')
        centered = Button('Text', flags=Control.CENTERED)
        large = Button('Large', box=utils.size(14, 6))
        flagged = Button('Flagged', flags=Control.SELECTED) # selected through constructor flags parameter
        selected_centered = Button('Text', flags=Control.SELECTED|Control.CENTERED)
        selected.select() # manual select
        while True:
            term.erase()
            default.draw(term, 0, 0)
            selected.draw(term, 8, 0)
            large.draw(term, 16, 0)
            flagged.draw(term, 30, 0)
            centered.draw(term, 39, 0)
            selected_centered.draw(term, 47, 0)

            term.addstr(7, 0, "Default button shows button with all defaults.")
            term.addstr(8, 0, "Selected button shows button with selected property as true manually.")
            term.addstr(9, 0, "Large button shows button with a size input. ex. Size=(14, 6).")
            term.addstr(10, 0, "Flagged button shows button with selected property as true through constructor.")
            term.addstr(11, 0, "Next button shows button initialized with multiple flags: Selected and Centered.")

            # term.refresh()
            key = term.getch()
            if key == ord('q'):
                break
            if key == ord('s'):
                default.select()
            if key == ord('S'):
                default.unselect()

    curses.wrapper(main)
