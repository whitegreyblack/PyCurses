# test colors in init curses settings function

if __name__ == "__main__":
    import curses
    from source.utils import initialize_curses_settings

    def main(term):
        initialize_curses_settings()
        term.addstr(0, 0, "Default", curses.color_pair(2))
        term.addstr(1, 0, "Default", curses.color_pair(8))
        term.addstr(2, 0, "Info", curses.color_pair(3))
        term.addstr(3, 0, "Info", curses.color_pair(9))
        term.addstr(4, 0, "Success", curses.color_pair(4))
        term.addstr(5, 0, "Success", curses.color_pair(10))
        term.addstr(6, 0, "Warning", curses.color_pair(5))
        term.addstr(7, 0, "Warning", curses.color_pair(11))
        term.addstr(8, 0, "Danger", curses.color_pair(6))
        term.addstr(9, 0, "Danger", curses.color_pair(12))
        term.getch()
    curses.wrapper(main)