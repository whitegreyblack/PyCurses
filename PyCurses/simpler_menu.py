import curses
import sys

class TabsManager(object):
    ''' 
    Descriptions:    
        holds all tab headers and dynamically resizes and positions all tabs
        each tab should be connected to a single windows which should dissapear when window is exited
    '''
    def __init__(self):
        pass

class Window(object):
    def __init__(self, title):
        self.tab = Tab(title)

class Tab(object):
    def __init__(self, title):
        self.title = title

def main(mainscreen):
    mainscreen.addch(5,5,'o')
    mainscreen.addch(5,6,'O')


if __name__ == "__main__":
    curses.Wrapper(main)
