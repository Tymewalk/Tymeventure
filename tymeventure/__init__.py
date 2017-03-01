# TYMEVENTURE v0.1.2
# Status: Stable
# A simple unicurses-based game running in Python 3.
# Help would be appreciated if you know how.

import pickle, os, argparse, random
import unicurses
from tymeventure.world import *
from tymeventure.convienience import *

# Some basic variables
version = "0.1.2-dev"
saveVersion = "0.1.2-r1"
hasSave = False
currentLocation = None

# Command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="Set your name")
parser.add_argument("--nocolor", help="Turn off colors", action="store_true")
parser.add_argument("--nointro", help="Skip the intro, best used with -n", action="store_true")
args = parser.parse_args()

# Main game loop
def gameLoop(stdscr):
    global locations
    stdscr.clear()
    stdscr.refresh()
    if not args.nointro:
        stdscr.addstr(0, 0, 'Tymeventure', unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(1, 0, "Version {}".format(version), unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(2, 0, '-- Press any key to begin --', unicurses.color_pair(1) | unicurses.A_BOLD)
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
        currentLocation = saveData[1]
        inventory = saveData[2]
        locations = saveData[3]
    else:
        currentLocation = yourBedroom
        inventory = list()

    if not args.nointro and not hasSave:
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
            allData = [saveVersion, currentLocation, inventory, locations] # Clone locations so we can keep the positions of items
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
                stdscr.addstr(ypos + 1, 0, "-- Press any key to continue --", unicurses.color_pair(1) | unicurses.A_BOLD)
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
                drawBoxMenu(stdscr, ["Take Item"])
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
                stdscr.addstr(ypos + 1, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(ypos + 2, 0, "-- Press any key to continue --", unicurses.color_pair(1) | unicurses.A_BOLD)
            else:
                itemNames = [i.printName for i in inventory]
                ypos = drawBoxMenu(stdscr, itemNames)
                stdscr.addstr(ypos, 0, "-- Press an item's key to do something with it, or anything else to exit --", unicurses.color_pair(1) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789":
                if int(choice) - 1 < len(inventory):
                    checkItem = True
                    itemInQuestion = inventory[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                drawBoxMenu(stdscr, ["Look At Item", "Drop Item", "Use Item"])
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
        unicurses.cbreak()
        # unicurses.noecho()
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
        unicurses.echo()
        unicurses.nocbreak()
        unicurses.endwin()
