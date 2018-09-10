import curses

cards = []

def main(screen): 
    terminal_lines = curses.LINES
    terminal_cols = curses.COLS

    if (curses.COLS <= 80):
        # accounts for border characters taking up two lines 
        # horizontally and vertically each
        screen_length = terminal_cols - 2
        screen_height = terminal_lines - 2

        horizontal_divider = (screen_height // 5) # closest int
        vertical_divider = max(16, screen_height // 4) 
        curses.curs_set(0)

        # Mobile view
        screen.border()
        #screen.addstr(horizontal_divider, 1, '-' * screen_length)
        for i in range(screen_height):
            screen.addch(i + 1, vertical_divider, '|')
        # get bounds of header
        screen.addstr(0, 1, 'Reciept Viewer')

        # get bounds of main panel to add string
        card_length = vertical_divider - 3
        for index, card in enumerate(cards):
            screen.addstr(index + 1, 1, card.description(card_length))

        screen.getch()
    else:
        # Desktop view
        raise NotYetImplementedError()

if __name__ == "__main__":
    curses.wrapper(main)
    print(curses.LINES, curses.COLS)
