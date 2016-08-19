# TYMEVENTURE v0.1.2
# Status: Stable
# A simple unicurses-based game running in Python 3.
# Help would be appreciated if you know how.

import pickle, os, sys
import unicurses

version = "0.1.2-dev"
hasSave = False
currentLocation = None

# Command-line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="Set your name")
parser.add_argument("--nocolor", help="Turn off colors", action="store_true")
parser.add_argument("--nointro", help="Skip the intro, best used with -n", action="store_true")
args = parser.parse_args()

# Small function I wrote a while back to get keypresses
def getKey(screen):
    return chr(screen.getch())

# Convienience function to quickly make menus that can be skipped through like the intro
# Also returns a key if you want multi-choice menus. Nifty.
def nextMenu(screen):
    key = getKey(screen)
    screen.clear()
    screen.refresh()
    return key

def drawBoxMenu(screen, options, xsize=40):
    screen.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
    ypos = 1
    for option in options:
        screen.addstr(ypos, 0, option + " " * (xsize - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
        screen.addstr(ypos, xsize, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
        ypos += 1
        
    screen.addstr(ypos, 0, "-" * xsize, unicurses.color_pair(0) | unicurses.A_BOLD)

def drawBoxMenuNumbered(screen, options, xsize=40):
    screen.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
    ypos = 1
    numCounter = 1
    for option in options:
        option = "(" + str(numCounter) + ") " + option
        screen.addstr(ypos, 0, option + " " * (xsize - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
        screen.addstr(ypos, xsize, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
        ypos += 1
        numCounter += 1
        
    screen.addstr(ypos, 0, "-" * xsize, unicurses.color_pair(0) | unicurses.A_BOLD)

# Set up the world
locations = list()

# The location class
class Location():
    def __init__(self, printName, desc):
        self.printName = printName # The "pretty" name it uses in the game
        self.desc = desc # The description it uses, which is what the player will see
        self.connections = list() # A list of all the places you can go to from this place
                                  # All elements in this are other Location() classes.
        self.itemsHere = list() # The items at this location on the ground, in Item() classes
        locations.append(self)

    def canGoTo(self, dest):
        ''' Can we go to the destination from here? '''
        # A good example of when to use this is if we have the super detector that
        # shimmers when we're near the magic castle
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

    def onPickup(self, stdscr, item, location, inv):
        '''When the item is picked up, run the code in this function.'''
        # For example, when we pick up the magic ring, it glows and attaches itself to our hand
        return True # Placeholder
    
# Make a connection between two points.
def makeConnection(pointA, pointB):
    if not pointB in pointA.connections:
        pointA.connections.append(pointB)
        
    if not pointA in pointB.connections:
        pointB.connections.append(pointA)


# Set up locations
yourBedroom = Location("Your Bedroom", "Your bedroom, where you sleep.")
yourDoorstep = Location("Your Doorstep", "The doorstep of your house.")
outside = Location("Outside", "Outside your house. You feel as if you should explore here.")
yourLawn = Location("Your Lawn", "Your lawn. It's surrounded by fences, behind which are your neighbors' houses.")
yourShed = Location("Your Shed", "Your shed. You've dumped a lot of stuff here. You keep saying you'll clean it out, but you never do.")
yourBlock = Location("Your Block", "Your block. You see your neighbors' houses around you.")
blockRoad = Location("Block Road", "The road for your block. You can see the town square up ahead.")
townSquare = Location("Town Square", "The town square. There's a lot of people. Must be a busy day.")
townMall = Location("Town Mall", "The mall for the town. Many people come here to shop and chat with one another. Today is no exception.")
townRoad = Location("Town Road", "The road running along the center of the town. Not many people go here.")
townOutskirts = Location("Town Outskirts", "The outskirts of town. Many adventurers are afraid to go deeper into the forest.")
forestEntry = Location("Forest Entry", "The entry to the forest. Many adventurers have perished in these woods.")
thinForestA = Location("Thin Forest", "A thin area of forest. You feel a chill run down your spine.")
forestCreekA = Location("Creek", "A creek. Perhaps there is something useful on the bank.")

# Make connections
makeConnection(yourBedroom, yourDoorstep)
makeConnection(yourDoorstep, outside)
makeConnection(outside, yourLawn)
makeConnection(yourLawn, yourShed)
makeConnection(outside, yourBlock)
makeConnection(yourBlock, blockRoad)
makeConnection(blockRoad, townSquare)
makeConnection(townSquare, townMall)
makeConnection(townSquare, townRoad)
makeConnection(townRoad, townOutskirts)
makeConnection(townOutskirts, forestEntry)

# Set up items
memoBedroom = Item("Memo", "A memo you found taped to your wall. It reads \"Clean Out Shed\".", True)
hedgeclippers = Item("Hedgeclippers", "A pair of hedgeclippers. They look almost brand-new.", True)
penny = Item("Penny", "A penny you found on the ground. Must be your lucky day.", True)

# The player is a special item
playerItem = Item("Player", "A player item never used in game. It's meant to work with Item.useWith().", False)

# Code for using items

# Memo
def memoBedroomUse(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "You mess around with the note. It has some writing on it. If you looked at the note, you might be able to read it.", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

memoBedroom.useWith = memoBedroomUse # It's the function itself, not the function being called

# Hedgeclippers
def hedgeclippersUse(stdscr, item, location, inv):
    if item == playerItem:
        stdscr.addstr(0, 0, "They look sharp. It's probably best not to do that.", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

hedgeclippers.useWith = hedgeclippersUse

# Penny
def pennyUse(stdscr, item, location, inv):
    if item == playerItem:
        # The coin actually flips :o
        stdscr.addstr(0, 0, "You flip the penny. It comes up " + random.choice(["heads", "tails"]) + ".", unicurses.color_pair(0) | unicurses.A_BOLD)
    else:
        stdscr.addstr(0, 0, "That doesn't seem like it will do anything.", unicurses.color_pair(0) | unicurses.A_BOLD)
    nextMenu(stdscr)

penny.useWith = pennyUse

# Set up items in the world
yourBedroom.itemsHere = [memoBedroom]
yourShed.itemsHere = [hedgeclippers]
townMall.itemsHere = [penny]

# Main game loop
def gameLoop(stdscr):
    global locations
    stdscr.clear()
    stdscr.refresh()
    if not args.nointro:
        stdscr.addstr(0, 0, 'TYMEVENTURE', unicurses.color_pair(0) | unicurses.A_BOLD)
        versionBar = "You have version " + version + "."
        stdscr.addstr(1, 0, versionBar, unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(2, 0, '-- Press any key to advance --', unicurses.color_pair(1) | unicurses.A_BOLD)
        nextMenu(stdscr)
        
    if not args.name: # If we didn't set a name already, prompt the user now
        stdscr.addstr(0, 0, "May I ask what your name is? (max 30 characters)", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(1, 0, 'Name: ', unicurses.color_pair(0) | unicurses.A_BOLD)
        playerName = stdscr.getstr(1, 6, 30).decode('utf8')
        stdscr.clear()
        stdscr.refresh()
    else:
        playerName = args.name

    # Load the data from the player's save
    #allData = loadGame( playerName )
    hasSave = False
    savename = "".join([playerName.rstrip().lstrip(), "_tymeventuresave"])
    if os.path.exists("".join([os.getcwd(), "/", savename])):
        savefile_open = open("".join([os.getcwd(), "/", savename]), "rb")
        saveData = pickle.load(savefile_open)
        hasSave = True


    if hasSave:
        currentLocation = saveData[0]
        inventory = saveData[1]
        locations = saveData[2]
    else:
        currentLocation = yourBedroom
        inventory = list()
        
    if not args.nointro:
        adventureAnnounce = "OK " + playerName + ", get ready to play..."
        stdscr.addstr(0, 0, adventureAnnounce, unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(2, 0, "It's a sunny day outside and you wake up. Yawn.", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(3, 0, "You: I think there was something going on today, a big press conference...?", unicurses.color_pair(3) | unicurses.A_BOLD)
        stdscr.addstr(4, 0, "After getting dressed and having breakfast, you get ready to take on the day.", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(5, 0, "You: Well, better get started.", unicurses.color_pair(3) | unicurses.A_BOLD)
        stdscr.addstr(7, 0, "-- Press any key to begin --", unicurses.color_pair(1) | unicurses.A_BOLD)
        nextMenu(stdscr)

    continueGame = True
    while continueGame:
        topbar = playerName # May be expanded in the future
        stdscr.addstr(0, 0, topbar, unicurses.color_pair(0) | unicurses.A_BOLD)
        location = "Current Location: " + currentLocation.printName
        stdscr.addstr(1, 0, location, unicurses.color_pair(0) | unicurses.A_BOLD)
        description = currentLocation.desc
        stdscr.addstr(2, 0, description, unicurses.color_pair(0) | unicurses.A_BOLD)
        # Detect how many items are here
        if currentLocation.itemsHere == []:
            itemsHereBar = "There are no items here."
        elif len(currentLocation.itemsHere) == 1:
            itemsHereBar = "There is one item here."
        else:
            itemsHereBar = "There are " + str(len(currentLocation.itemsHere)) + " items here."
        stdscr.addstr(3, 0, itemsHereBar, unicurses.color_pair(0) | unicurses.A_BOLD)
        # Options
        stdscr.addstr(5, 0, "Save and (Q)uit", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(6, 0, "(M)ove", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(7, 0, "(T)hings Here", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(8, 0, "(I)nventory", unicurses.color_pair(0) | unicurses.A_BOLD)
        choice = nextMenu(stdscr).lower() # Use nextMenu for nice, easy clearing
        if choice == "q":
            # Save and Quit
            #saveGame( playerName, currentLocation, inventory, locations )
            allData = [currentLocation, inventory, locations] # Clone locations so we can keep the positions of items
            placename = currentLocation.printName
            savename = "".join([playerName.rstrip().lstrip(), "_tymeventuresave"])
            tmpname = "".join([playerName.rstrip().lstrip(), "_tymeventuretmp"]) # Use temp file to be safe
            savefile_out = open(tmpname, "wb")
            pickle.dump(allData, savefile_out)
            os.rename(tmpname, savename)
            continueGame = False
        elif choice == "m":
            ypos = 1
            stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            keyCounter = 1
            for place in currentLocation.connections:
                label = "|(" + str(keyCounter) + ") " + place.printName
                stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD) # Make a "box"
                ypos += 1
                keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "-- Press the key next to where you want to move --", unicurses.color_pair(1) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            if choice in "123456789": # Make sure it's a valid location number
                if int(choice) - 1 < len(currentLocation.connections):
                    moveTo = currentLocation.connections[int(choice) - 1]
                    for index, item in enumerate(locations):
                        if item.printName == currentLocation.printName:
                            locations[index] = currentLocation
                    
                    currentLocation = moveTo # Move us
        elif choice == "t":
            ypos = 1
            stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            keyCounter = 1
            if currentLocation.itemsHere == []:
                stdscr.addstr(ypos, 0, "|There is nothing here.                |", unicurses.color_pair(0) | unicurses.A_BOLD)
                ypos += 1
                stdscr.addstr(ypos, 0, "-- Press any key to continue --", unicurses.color_pair(1) | unicurses.A_BOLD)
            else:
                for item in currentLocation.itemsHere:
                    label = "|(" + str(keyCounter) + ") " + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD) # Make a "box"
                    ypos += 1
                    keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "-- Press the key next to the item you want to use --", unicurses.color_pair(1) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789": # Make sure it's a valid item number
                if int(choice) - 1 < len(currentLocation.itemsHere):
                    checkItem = True
                    itemInQuestion = currentLocation.itemsHere[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                drawBoxMenu(stdscr, ["(1) Take Item"])
                choice = nextMenu(stdscr)
                # Number doesn't matter here, I'm not converting it to int or anything
                if choice == "1":
                    currentLocation.itemsHere.remove(itemInQuestion)
                    inventory.append(itemInQuestion)
                
            
        elif choice == "i":
            ypos = 1
            stdscr.addstr(ypos - 1, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            keyCounter = 1
            if inventory == []:
                stdscr.addstr(ypos, 0, "|You have nothing in your inventory.   |", unicurses.color_pair(0) | unicurses.A_BOLD)
                ypos += 1
                stdscr.addstr(ypos, 0, "-- Press any key to continue --", unicurses.color_pair(1) | unicurses.A_BOLD)
            else:
                itemNames = [i.printName for i in inventory]
                drawBoxMenuNumbered(stdscr, itemNames)
            stdscr.addstr(10, 0, "-- Press an item's key to do something with it, or anything else to exit --", unicurses.color_pair(1) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789":
                if int(choice) - 1 < len(inventory):
                    checkItem = True
                    itemInQuestion = inventory[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                drawBoxMenu(stdscr, ["(1) Look At Item", "(2) Drop Item", "(3) Use Item"])
                choice = nextMenu(stdscr)
                # Number doesn't matter here, I'm not converting it to int or anything
                if choice == "1":
                    stdscr.addstr(0, 0, itemInQuestion.printName, unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(1, 0, itemInQuestion.desc, unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(2, 0, '-- Press any key to exit --', unicurses.color_pair(1) | unicurses.A_BOLD)
                    nextMenu(stdscr)
                elif choice == "2":
                    currentLocation.itemsHere.append(itemInQuestion)
                    inventory.remove(itemInQuestion)
                elif choice == "3":
                    ypos = 1
                    stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
                    for item in inventory:
                        if not item == itemInQuestion:
                            label = "|(" + str(keyCounter) + ") " + item.printName
                            stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                            stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                            ypos += 1
                            keyCounter += 1
                            
                    label = "|(0) Yourself"
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                    ypos += 1
                    stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(ypos + 1, 0, "-- Press an item's key to use it, or anything else to exit --", unicurses.color_pair(1) | unicurses.A_BOLD)
                    choice = nextMenu(stdscr)
                    checkItem = False
                    if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                        if int(choice) - 1 < len(inventory):
                            checkItem = True
                            itemToUseWith = inventory[int(choice) - 1]
                        else:
                            checkItem = False
                    elif choice == "0": # If it's the player being used...
                        itemToUseWith = playerItem # ...then use the special player item.
                        checkItem = True
                    else:
                        checkItem = False
                        
                    if checkItem:
                        itemInQuestion.useWith(stdscr, itemToUseWith, currentLocation, inventory)
                        
                else:
                    pass
            
        else:
            pass

# Broken stuff
##def saveGame( name, curLoc, inv, locs ):
##    allData = [curLoc, inv, locs] # Clone locations so we can keep the positions of items
##    # Temp file for safety
##    placename = curLoc.printName
##    savename = "".join([name.rstrip().lstrip(), "_tymeventuresave"])
##    tmpname = "".join([name.rstrip().lstrip(), "_tymeventuretmp"])
##    savefile_out = open(tmpname, "wb")
##    pickle.dump(allData, savefile_out)
##    os.rename(tmpname, savename)
##
##def loadGame( name ):
##    savename = "".join([name.rstrip().lstrip(), "_tymeventuresave"])
##    if os.path.exists("".join([os.getcwd(), "/", savename])):
##        savefile_open = open("".join([os.getcwd(), "/", savename]), "rb")
##        allData = pickle.load(savefile_open)
##        hasSave = True
##        return allData
##    else:
##        return [None, None, None]


def main():
    try:
        stdscr = unicurses.initscr()
        unicurses.cbreak() # ; unicurses.noecho()
        unicurses.start_color()
        stdscr.keypad(1)
        # Determine if we need color
        if args.nocolor:            
            unicurses.init_pair(1, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK)
            unicurses.init_pair(2, unicurses.COLOR_WHITE, unicurses.COLOR_BLACK)
        else:            
            unicurses.init_pair(1, unicurses.COLOR_BLUE, unicurses.COLOR_BLACK)
            unicurses.init_pair(2, unicurses.COLOR_RED, unicurses.COLOR_BLACK)
            unicurses.init_pair(3, unicurses.COLOR_GREEN, unicurses.COLOR_BLACK)
        # Game loop after this point
        gameLoop(stdscr)
    except KeyboardInterrupt:
        saveGame( playerName )
    finally:
        stdscr.erase()
        stdscr.refresh()
        stdscr.keypad(0)
        unicurses.echo() ; unicurses.nocbreak()
        unicurses.endwin()
