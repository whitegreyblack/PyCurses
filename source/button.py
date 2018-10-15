"""UI Button component"""
import source.utils as utils
# TODO: Create a button with internal handling and external api to add more
#       handlers
#     : Add config settings for buttons. Could add to the config file or
#       as properties under the class
# A single call to this class should have the button initialized and ready
# to be drawn to the screen
class Button:
    # defaults for buttons without arguments passed in
    height = 3
    width = 8
    label = "Button"

    # default state
    focused = False
    selected = False
    disabled = False
    border = False
    background = None

    # determine flags to use on init constructor
    DEFAULT = 0
    FOCUSED = 1
    SELECTED = 2
    DISABLED = 4
    BORDER = 8

    def __init__(self, label=None, box=None, flags=None):
        # the flags would have the properties with boolean?(undeterminded)
        if not box:
            self.width = Button.width
            self.height = Button.height
        else:
            self.width = box.width
            self.height = box.height
        
        self.label = label if label else Button.label

        if flags:
            self.focused = False
            self.selected = flags & Button.SELECTED
            self.disabled = False # property changes the border color
            self.border = False

    # these should be core methods in every button but unsure whether to
    # have only one of the focus or select vs both.
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
        utils.border(term, x, y, self.width, self.height)
        color = curses.color_pair(1)
        if self.selected:
            color = curses.color_pair(2)
        term.addstr(y+1, x+1, self.label, color)

if __name__ == "__main__":
    import curses
    from source.utils import initialize_curses_settings
    def main(term):
        initialize_curses_settings()
        default = Button()
        selected = Button('Text')
        large = Button('Large', box=utils.box(0, 0, 14, 6))
        flagged = Button('Flagged', flags=Button.SELECTED) # auto selected
        selected.select() # manual select
        flagged.draw(term, 24, 0)
        selected.draw(term, 8, 0)
        default.draw(term, 0, 0)
        large.draw(term, 16, 0)
        while True:
            key = term.getch()
            if key == ord('q'):
                break
            if key == ord('s'):
                default.select()
            if key == ord('S'):
                default.unselect()
            term.erase()
            default.draw(term, 0, 0)
            selected.draw(term, 8, 0)
            large.draw(term, 16, 0)
            flagged.draw(term, 24, 0)
            term.refresh()
    curses.wrapper(main)
