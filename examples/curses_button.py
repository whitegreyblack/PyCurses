import curses
import source.utils as utils
from source.utils import initialize_curses_settings
from source.utils import point
from source.mouse import MouseEvent as mouse
from source.button import Button, Control

def main(term):
    initialize_curses_settings()
    height, width = term.getmaxyx()
    default = Button()
    selected = Button('Text')
    centered = Button('Text', flags=Control.CENTERED)
    large = Button('Large', size=utils.size(14, 6))
    large_centered = Button('Large', size=utils.size(14, 6), flags=Control.CENTERED)
    
    # selected through constructor flags parameter
    flagged = Button('Flagged', flags=Control.SELECTED)
    # both selected and centered properties
    selected_centered = Button('Text1', 
                                flags=Control.SELECTED | Control.CENTERED)
    # manually select
    selected.select()

    unbordered = Button('NoBorder', flags=Control.NOBORDER)

    mouse_down = False
    element_clicked = None
    point_clicked = None
    mouse_scroll = 0
    mouse_move = False
    px, py = 0, 0
    i = 0
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
        large_centered.draw(term, point(30, 0))
        flagged.draw(term, point(44, 0))
        centered.draw(term, point(53, 3))
        selected_centered.draw(term, point(53, 0))
        unbordered.draw(term, point(61, 0))

        term.addstr(7, 0, "Default button shows button with all defaults.")
        term.addstr(8, 0, "Selected button shows button with selected property as true manually.")
        term.addstr(9, 0, "Large button shows button with a size input. ex. Size=(14, 6).")
        term.addstr(10, 0, "Flagged button shows button with selected property as true through constructor.")
        term.addstr(11, 0, "Next button shows button initialized with multiple flags: Selected and Centered.")

        term.addstr(20, 0, f"width={width}, height={height}")
        term.addstr(21, 0, f"Button1 release={curses.BUTTON1_RELEASED}")
        term.addstr(22, 0, f"Button1 pressed={curses.BUTTON1_PRESSED}")
        term.addstr(23, 0, f"Button1 clicked={curses.BUTTON1_CLICKED}")
        
        term.addstr(24, i % width, 'o')
        # i += 1

        # curses does not support mouse hover -- so button hover state is a no
        a, mx, my, c, mask = curses.getmouse()
        # mx, my = term.getyx()
        term.addstr(25, 0, f"{mx}, {my}")
        # term.addstr()

        # term.refresh()
        term.timeout(60)
        key = term.getch()
        term.addstr(6, 0, str(key))
        if key == ord('q'):
            break

        # when selecting/unselecting, there is a cursor artifact even
        # with curses.set_curs(0) ie. no cursor. Maybe calling it
        # again will fix
        if key == ord('s'):
            default.select()
        if key == ord('S'):
            default.unselect()
        if key == curses.KEY_MOUSE:
            # probably need to write a mouse handler
            # ex curses_mouse_handler as mouse
            mouse_down = True
            a, px, py, _, mask = curses.getmouse()

            # probably only want to make sure that the mouse was
            # only 'LEFT CLICKED' before choosing clicked method()
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