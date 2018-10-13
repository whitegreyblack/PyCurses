"""UI Button component"""
from collections import namedtuple

box = namedtuple("Box", "x y width height")

# TODO: Create a button with internal handling and external api to add more
#       handlers
#     : Add config settings for buttons. Could add to the config file or
#       as properties under the class
# A single call to this class should have the button initialized and ready
# to be drawn to the screen
class Button:
    height = 3
    width = 7
    label = "Button"

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
        self.focused = False
        self.selected = False
        self.disabled = False # property changes the border color
        self.border = False
        self.background = None

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

    def draw(self, term):
        pass

if __name__ == "__main__":
    import curses
    def main(term):
        button = Button()
        while True:
            key = term.getch()
            if key == ord('q'):
                break
            term.erase()
            button.draw(term)

    curses.wrapper(main)
