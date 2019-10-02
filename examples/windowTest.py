# windowTest.py

""" Example showing vertical divder bar """

import curses
from dataclasses import dataclass, field


@dataclass
class Card:
    description: str

@dataclass
class CardList:
    cards: list = field(default_factory=list)
    def add_cards(self, *cards):
        self.cards += cards
    @property
    def descriptions(self):
        for c in self.cards: yield c.description

cards = CardList()
cards.add_cards(Card('a'), Card('b'))

def main(screen): 
    # turn off blinking cursor
    curses.curs_set(0)

    # calculate space inside divided panel
    vertical_divider = max(16, (curses.COLS - 2) // 4) 

    screen.border()
    # add separator
    screen.vline(1, vertical_divider, curses.ACS_VLINE, curses.LINES - 2)
    # add title
    screen.addstr(0, 2, '[receipt Viewer]')

    # get bounds of main panel to add string
    card_length = vertical_divider - 2
    for height, description in enumerate(cards.descriptions):
        screen.addstr(height + 1, 1, f"{chr(97+height)}. {description}")
    
    # exit on keypress
    print(repr(screen.getkey()))
    # screen.getch()

if __name__ == "__main__":
    curses.wrapper(main)
    print(curses.LINES, curses.COLS)
