#!/usr/env/bin python3

__author__ = "Samuel Whang"

from typing import Union
import curses
import os

def format_directory_path(path: str) -> str:
    formatted_path = path.replace('\\', '/')
    if formatted_path[-1] is not '/':
        formatted_path += '/'
    return formatted_path

def check_directory_path(path: str) -> bool:
    return os.path.isdir(path)

def border(screen: object, x: int, y: int, dx: int, dy: int): -> None
    screen.vline(y, x, curses.ACS_SBSB, dy)
    screen.vline(y, x + dx, curses.ACS_SBSB, dy)
    screen.hline(y, x, curses.ACS_BSBS, dx)
    screen.hline(y + dy, x, curses.ACS_BSBS, dx)
    screen.addch(y, x, curses.ACS_BSSB)
    screen.addch(y, x + dx, curses.ACS_BBSS)
    screen.addch(y + dy, x, curses.ACS_SSBB)
    screen.addch(y + dy, x + dx, curses.ACS_SBBS)

def format_float(number: Union[int, float]) -> float:
    return f"{number:.2f}"
