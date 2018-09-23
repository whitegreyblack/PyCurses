"""Rain.py: Rain animation"""

__author__ = "Sam Whang"

import curses, random

def main(screen):
    curses.curs_set(0)
    chars = ['|', '/', '-', '\\']
    index = 0
    height, width = screen.getmaxyx()
    size = width * height

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    pixelbuffer = [0 for i in range(size + width + 1)]

    while 1:
        for i in range(width // 9):
            pixelbuffer[int((random.random() * width) + width * (height - 1))] = 65 

        for i in range(size):
            newvalue = (pixelbuffer[i] + 
                        pixelbuffer[i + 1] + 
                        pixelbuffer[i + width] + 
                        pixelbuffer[i + width + 1]) // 5
            pixelbuffer[i] = newvalue

            # b[i] = (b[i] + b[i+1] + b[i+width] + b[i+width+1]) // 4
            if i < size - 1:
                screen.addstr(i // width, 
                              i % width, 
                              "." if pixelbuffer[i] > 9 else "-",
                              curses.color_pair(1 if pixelbuffer[i] > 9 else 2))

        # screen.addstr(10, 10, chars[index % len(chars)])
        screen.refresh()
        screen.timeout(70)
        if screen.getch() != -1:
            break
        index += 1

if __name__ == "__main__":
    curses.wrapper(main)
