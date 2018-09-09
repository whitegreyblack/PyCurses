#!/usr/env/bin python3

__author__ = "Samuel Whang"

import curses

def border(screen, x, y, dx, dy):
    screen.vline(y, x, curses.ACS_SBSB, dy)
    screen.vline(y, x + dx, curses.ACS_SBSB, dy)
    screen.hline(y, x, curses.ACS_BSBS, dx)
    screen.hline(dy, x, curses.ACS_BSBS, dx)
    screen.addch(y, x, curses.ACS_BSSB)
    screen.addch(y, x + dx, curses.ACS_BBSS)
    screen.addch(dy, x, curses.ACS_SSBB)
    screen.addch(dy, x + dx, curses.ACS_SBBS)
