from misc import nextMenu
import curses

# The location class
class Location():
    def __init__(self, printName, desc):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see
        self.connections = list() # A list of all the places you can go to from this place
                                  # All elements in this are other Location() classes.
        self.itemsHere = list() # The items at this location on the ground

    def canGoTo(self, dest):
        ''' Can we go to the destination from here? '''
        return dest in self.connections
    
# The item class
class Item():
    def __init__(self, printName, desc, canTake):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see
        self.canTake = canTake # Can this item be taken and picked up?


    def useWith(self, stdscr, item, location, inv):
        '''Use the item with another item.'''
        # stdscr is the screen
        # item is the item to use it with
        # location is where we are
        # inv is the player's inventory, in case we consume something
        return True # Placeholder
    
# Make a connection between two points.
def makeConnection(pointA, pointB):
    if not pointB in pointA.connections:
        pointA.connections.append(pointB)
        
    if not pointA in pointB.connections:
        pointB.connections.append(pointA)


# Set up locations
yourComputer = Location("Your Computer", "Your wonderful computer, where you use the internet. You feel like you shouldn't be here.")
yourDoorstep = Location("Your Doorstep", "Your doorstep. You can go outside from here.")
outside = Location("Outside", "Outside your house. You feel as if you should explore here.")
yourLawn = Location("Your Lawn", "Your lawn. It's surrounded by fences, behind which are your neighbors' houses.")
yourShed = Location("Your Shed", "Your shed. You've dumped a lot of stuff here. You keep saying you'll clean it out, but you never do.")
yourBlock = Location("Your Block", "Your block. You see your neighbors' houses around you.")
blockRoad = Location("Block Road", "The road for your block. You can see the town square up ahead.")
townSquare = Location("Town Square", "The town square. There's a lot of people. Must be a busy day.")

# Set up items
memoComputer = Item("Memo", "A memo you found taped to your computer. It reads \"Clean Out Shed\".", True)
hedgeclippers = Item("Hedgeclippers", "A pair of hedgeclippers. They look almost brand-new.", True)

# The player is a special item
playerItem = Item("Player", "A player item never used in game. It's meant to work with Item.useWith().", False)

# Item use code

# Memo
def use(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "You mess around with the note. It's just paper. You stick it back in your pocket.", curses.color_pair(0) | curses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", curses.color_pair(0) | curses.A_BOLD)
    nextMenu(stdscr)

memoComputer.useWith = use # It's the function itself, not the function being called

# Hedgeclippers
def use(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "They look sharp. It's probably best not to do that.", curses.color_pair(0) | curses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", curses.color_pair(0) | curses.A_BOLD)
    nextMenu(stdscr)

hedgeclippers.useWith = use

    
# Set up items in the world
yourComputer.itemsHere = [memoComputer]
yourShed.itemsHere = [hedgeclippers]

# Make connections
makeConnection(yourComputer, yourDoorstep)
makeConnection(yourDoorstep, outside)
makeConnection(outside, yourLawn)
makeConnection(yourLawn, yourShed)
makeConnection(outside, yourBlock)
makeConnection(yourBlock, blockRoad)
makeConnection(blockRoad, townSquare)
