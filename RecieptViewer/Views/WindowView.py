import curses
def main(screen): 
    terminal_lines = curses.LINES
    terminal_cols = curses.COLS

    if (curses.COLS <= 80):
        # accounts for border characters taking up two lines horizontally and
        # vertically each
        screen_length = terminal_cols - 2
        screen_height = terminal_lines - 2

        screen_divider = screen_height // 5 # closest int

        curses.curs_set(0)

        # Mobile view
        screen.border()
        screen.addstr(screen_height, 1, '-' * screen_length)
        screen.getch()
        
        # get bounds of header
        
        # get bounds of main panel to add string
        

    else:
        # Desktop view
        raise NotYetImplementedError()

if __name__ == "__main__":
    curses.wrapper(main)
    print(curses.LINES, curses.COLS)
