import curses
import source.utils as utils
from source.utils import initialize_curses_settings
from source.utils import point
from source.mouse import MouseEvent as mouse
from source.button import Button, Control

if __name__ == "__main__":
    def main(term):
        initialize_curses_settings()

        filebtn = Button("File", size=utils.size(1, 4), flags=Control.NOBORDER)
        editbtn = Button("Edit", size=utils.size(1, 4), flags=Control.NOBORDER)
        viewbtn = Button("View", size=utils.size(1, 4), flags=Control.NOBORDER)
        helpbtn = Button("Help", size=utils.size(1, 4), flags=Control.NOBORDER)

        while True:
            term.erase()

            filebtn.draw(term, point(1, 0))
            editbtn.draw(term, point(7, 0))
            viewbtn.draw(term, point(13, 0))
            helpbtn.draw(term, point(19, 0))

            ch = term.getch()
            if ch == ord('q'):
                break
    curses.wrapper(main)