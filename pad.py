import curses

def main(screen):
    screen.border()
    y,x=screen.getmaxyx()
    mypad=curses.newpad(y*3,9)
    mypad.addstr(1,1,"here")
    mypad.border()
    mypad.refresh(0,0,0,0,y-1,9)
    mypad.getch()
if __name__ == "__main__":
    curses.wrapper(main)
