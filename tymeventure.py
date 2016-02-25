# TYMEVENTURE v0.0.0
# Status: Basically nothing is here
# A simple curses-based game running i Python 3.4.3.
# Help would be appreciated if you know how.
#
# TODO:
# - Actually set up more than just 2 places
# - Make inventory more than just an empty list

import curses # Curses! You've foiled my plan!

inventory = list()

# The location class
class Location():
    def __init__(self, printName, desc):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see

        self.connections = list() # A list of all the places you can go to from this place
                                  # All elements in this are other Location() classes.
        self.itemsHere = list() # For another time

    def canGoTo(self, dest):
        ''' Can we go to the destination from here? '''
        return dest in self.connections

# Make a connection between two points.
def makeConnection(pointA, pointB):
    if not pointB in pointA.connections:
        pointA.connections.append(pointB)
        
    if not pointA in pointB.connections:
        pointB.connections.append(pointA)

# Small script I wrote a while back to get keypresses
def getKey(screen):
    return chr(screen.getch())

# Convienience function to quickly make menus like the intro
def nextMenu(screen):
    key = getKey(screen)
    screen.clear()
    screen.refresh()
    return key

yourHouse = Location("Your House", "Your house, the place you live in.")
outside = Location("Outside", "Outside your house. It sure looks scary. Perhaps you should stay on the internet.")

makeConnection(yourHouse, outside)

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 0, 'Welcome to Tymeventure! Press any key to continue.', curses.color_pair(0) | curses.A_BOLD)
    nextMenu(stdscr)
    stdscr.addstr(0, 0, 'This is a simple example to test curses.', curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, 'Look, blue text!', curses.color_pair(1) | curses.A_BOLD)
    nextMenu(stdscr)
            
if __name__=='__main__':
    try:
        stdscr = curses.initscr()
        curses.cbreak() # ; curses.noecho() # Uncomment if desired/needed
        curses.start_color()
        stdscr.keypad(1)
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
        main(stdscr)                    # Enter the main loop
    except KeyboardInterrupt:
        pass # I may need something here later
    finally:
        stdscr.erase()
        stdscr.refresh()
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()                 # Terminate curses
