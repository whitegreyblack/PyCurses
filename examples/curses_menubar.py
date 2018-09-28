import curses
from source.controls import Window, View, OptionsBar, Label

def initialize_curses_settings(logger=None):
    """Sets settings for cursor visibility and color pairings"""
    if logger:
        logger.info('main(): initializing curses library settings')
    curses.curs_set(0)
    curses.start_color()
    for i in range(16):
        curses.init_pair(i + 1, 0, 7)
    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)

def main(screen):
    initialize_curses_settings()
    height, width = screen.getmaxyx()
    window = Window('Application', width, height)
    optbar = OptionsBar(screen,
                        options=[("File", ("long option", "shortopt")),
                                 ("Edit", ("someother", "secondopt")),])
    # v1.add_element(optbar)
    # v2 = View(screen.subwin(height-1, width, 1, 0))
    # optionsbar(
    #   options=[], 
    #   handlers=[]
    # )

    # optbar.add_option('File', file_options)
    # optbar.add_option('Edit', None)
    # optbar.add_option('Select', None)
    # optbar.add_option('Help', None)
    window.add_component(optbar)

    keymap = dict()
    keymap[49] = "File"
    keymap[50] = "Edit"
    # keymap[51] = 'Select'
    # keymap[52] = 'Help'

    #window.add_keymap(keymap)

    while 1:
        window.draw()
        # screen.refresh()
        c = screen.getch()

        # screen.addstr(10, 10, f"{c}")
        if c in keymap.keys():
            screen.addstr(10, 10, 'ff')
            optbar.show(keymap[c])
        if c == 27:
            optbar.close_option_menus()
        if c == ord('q'):
            break
    #     window.clear()
    #     window.draw(screen)


if __name__ == "__main__":
    curses.wrapper(main)