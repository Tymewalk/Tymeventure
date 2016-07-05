# TYMEVENTURE v0.1.1 (Working on 0.1.2)
# Status: Stable
# A simple unicurses-based game running in Python 3.4.3.
# Help would be appreciated if you know how.
#
# TODO:
# - Develop some story
# - Better use of colors
# - MUCH bigger world
# - Make some items that can actually be used together
# - Document the game on the Wikia

import pickle, os, sys
import unicurses
from world import * # The world
from commandline import * # This just executes the code and keeps it neat
from misc import * # Misc functions

version = "0.1.2"
hasSave = False
currentLocation = None

def gameLoop(stdscr):
    locations = world.locations
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
        allData = pickle.load(savefile_open)
        hasSave = True


    if not hasSave:
        currentLocation = yourBedroom
        inventory = list()
    else:
        currentLocation = allData[0]
        inventory = allData[1]
        locations = allData[2]
        
    if not args.nointro:
        adventureAnnounce = "OK " + playerName + ", get ready to play..."
        stdscr.addstr(0, 0, adventureAnnounce, unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(2, 0, "It's a sunny day outside and you wake up. Yawn.", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(3, 0, "\"I think there was something going on today, a big press conference...?\"", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(4, 0, "After getting dressed and having breakfast, you get ready to take on the day.", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(5, 0, "\"Well, better get started.\"", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(6, 0, "-- Press any key to begin --", unicurses.color_pair(1) | unicurses.A_BOLD)
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
        stdscr.addstr(4, 0, "(Q)uit", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(5, 0, "(M)ove", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(6, 0, "(T)hings here", unicurses.color_pair(0) | unicurses.A_BOLD)
        stdscr.addstr(7, 0, "(I)nventory", unicurses.color_pair(0) | unicurses.A_BOLD)
        choice = nextMenu(stdscr).lower() # Case doesn't matter, and we clear anyway, so nextMenu is OK here
        if choice == "q":
            #saveGame( playerName, currentLocation, inventory, locations )
            allData = [currentLocation, inventory, locations] # Clone locations so we can keep the positions of items
            # Temp file for safety
            placename = currentLocation.printName
            savename = "".join([playerName.rstrip().lstrip(), "_tymeventuresave"])
            tmpname = "".join([playerName.rstrip().lstrip(), "_tymeventuretmp"])
            savefile_out = open(tmpname, "wb")
            pickle.dump(allData, savefile_out)
            os.rename(tmpname, savename)
            continueGame = False
        elif choice == "m":
            ypos = 1
            stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            keyCounter = 1
            for place in currentLocation.connections:
                label = "|(" + str(keyCounter) + ")" + place.printName
                stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD) # Make a "box"
                ypos += 1
                keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "Press the key next to where you want to move.", unicurses.color_pair(0) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
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
            else:
                for item in currentLocation.itemsHere:
                    label = "|(" + str(keyCounter) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD) # Make a "box"
                    ypos += 1
                    keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                if int(choice) - 1 < len(currentLocation.itemsHere):
                    checkItem = True
                    itemInQuestion = currentLocation.itemsHere[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
                option = "(1)Take Item"
                stdscr.addstr(1, 0, option + " " * (40 - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(1, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD) # Make a "box"
                stdscr.addstr(2, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
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
            else:
                for item in inventory:
                    label = "|(" + str(keyCounter) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), unicurses.color_pair(0) | unicurses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                    ypos += 1
                    keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "-- Press an item's key to do something with it, or anything else to exit --", unicurses.color_pair(1) | unicurses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789":
                if int(choice) - 1 < len(inventory):
                    checkItem = True
                    itemInQuestion = inventory[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                stdscr.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
                option = "(1)Look At Item"
                stdscr.addstr(1, 0, option + " " * (40 - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(1, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                option = "(2)Drop Item"
                stdscr.addstr(2, 0, option + " " * (40 - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(2, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                option = "(3)Use Item"
                stdscr.addstr(3, 0, option + " " * (40 - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(3, 40, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
                stdscr.addstr(4, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
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
                            label = "|(" + str(keyCounter) + ")" + item.printName
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
