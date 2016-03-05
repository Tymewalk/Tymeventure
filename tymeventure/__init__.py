# TYMEVENTURE v0.1.0
# Status: Stable
# A simple curses-based game running in Python 3.4.3.
# Help would be appreciated if you know how.
#
# TODO:
# - Develop some story
# - Better use of colors
# - MUCH bigger world
# - Make some items that can actually be used together
# - Savegames (working in this branch)

# I'll have to use something like UniCurses if I want to have people use this on Windows
import curses
import pickle # For savegames later on
from world import * # The world
from commandline import * # This just executes the code and allow us to keep the code neat
from misc import * # Misc functions
import os, sys # I just generally import both at once

inventory = list() # The player's inventory

version = "0.1.0+"

def gameLoop(stdscr):  
    currentLocation = yourComputer
    stdscr.clear()
    stdscr.refresh()
    if not args.nointro:
        stdscr.addstr(0, 0, 'TYMEVENTURE', curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(0, 4, 'V', curses.color_pair(0) | curses.A_BOLD)
        versionBar = "You have version " + version + "."
        stdscr.addstr(1, 0, versionBar, curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(2, 0, '-- Press any key to advance --', curses.color_pair(1) | curses.A_BOLD)
        nextMenu(stdscr)
        
    if not args.name: # If we didn't set a name already, prompt the user now
        stdscr.addstr(0, 0, "May I ask what your name is? (max 30 characters)", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(1, 0, 'Name: ', curses.color_pair(0) | curses.A_BOLD)
        playerName = stdscr.getstr(1, 6, 30).decode('utf8')
        stdscr.clear()
        stdscr.refresh()
    else:
        playerName = args.name
        
    if not args.nointro:
        adventureAnnounce = "OK " + playerName + ", get ready to play..."
        stdscr.addstr(0, 0, adventureAnnounce, curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(2, 0, "It's a sunny day outside and you wake up. Yawn.", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(3, 0, "Once again, like every morning, you log onto the internet and check for new messages.", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(4, 0, "A couple of forum posts, a new follower, a friend request. Slow day.", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(5, 0, "But today feels... different.", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(6, 0, "Something compels you to go outside today, as if you know something's about to happen.", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(7, 0, "You decide to close the computer, and head outside, ready to explore the world...", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(8, 0, "-- Press any key to begin --", curses.color_pair(1) | curses.A_BOLD)
        nextMenu(stdscr)

    continueGame = True
    while continueGame:
        topbar = playerName # May be expanded in the future
        stdscr.addstr(0, 0, topbar, curses.color_pair(0) | curses.A_BOLD)
        location = "Current Location: " + currentLocation.printName
        stdscr.addstr(1, 0, location, curses.color_pair(0) | curses.A_BOLD)
        description = currentLocation.desc
        stdscr.addstr(2, 0, description, curses.color_pair(0) | curses.A_BOLD)
        # Detect how many items are here
        if currentLocation.itemsHere == []:
            itemsHereBar = "There are no items here."
        elif len(currentLocation.itemsHere) == 1:
            itemsHereBar = "There is one item here."
        else:
            itemsHereBar = "There are " + str(len(currentLocation.itemsHere)) + " items here."
        stdscr.addstr(3, 0, itemsHereBar, curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(4, 0, "(Q)uit", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(5, 0, "(M)ove", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(6, 0, "(T)hings here", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(7, 0, "(I)nventory", curses.color_pair(0) | curses.A_BOLD)
        choice = nextMenu(stdscr).lower() # Case doesn't matter, and we clear anyway, so nextMenu is OK here
        if choice == "q":
            saveGame( playerName )
            continueGame = False
        elif choice == "m":
            ypos = 1
            stdscr.addstr(0, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keyCounter = 1
            for place in currentLocation.connections:
                label = "|(" + str(keyCounter) + ")" + place.printName
                stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                ypos += 1
                keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "Press the key next to where you want to move.", curses.color_pair(0) | curses.A_BOLD)
            choice = nextMenu(stdscr)
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                if int(choice) - 1 < len(currentLocation.connections):
                    moveTo = currentLocation.connections[int(choice) - 1]
                    currentLocation = moveTo # Move us
        elif choice == "t":
            ypos = 1
            stdscr.addstr(0, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keyCounter = 1
            if currentLocation.itemsHere == []:
                stdscr.addstr(ypos, 0, "|There is nothing here.                |", curses.color_pair(0) | curses.A_BOLD)
                ypos += 1
            else:
                for item in currentLocation.itemsHere:
                    label = "|(" + str(keyCounter) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                    ypos += 1
                    keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                if int(choice) - 1 < len(currentLocation.itemsHere):
                    checkItem = True
                    itemInQuestion = currentLocation.itemsHere[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                stdscr.addstr(0, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                option = "(1)Take Item"
                stdscr.addstr(1, 0, option + " " * (40 - len(option)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(1, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                stdscr.addstr(2, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                choice = nextMenu(stdscr)
                # Number doesn't matter here, I'm not converting it to int or anything
                if choice == "1":
                    currentLocation.itemsHere.remove(itemInQuestion)
                    inventory.append(itemInQuestion)
                
            
        elif choice == "i":
            ypos = 1
            stdscr.addstr(ypos - 1, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keyCounter = 1
            if inventory == []:
                stdscr.addstr(ypos, 0, "|You have nothing in your inventory.   |", curses.color_pair(0) | curses.A_BOLD)
                ypos += 1
            else:
                for item in inventory:
                    label = "|(" + str(keyCounter) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                    ypos += 1
                    keyCounter += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "-- Press an item's key to do something with it, or anything else to exit --", curses.color_pair(1) | curses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789":
                if int(choice) - 1 < len(inventory):
                    checkItem = True
                    itemInQuestion = inventory[int(choice) - 1]
                else:
                    checkItem = False

            if checkItem:
                stdscr.addstr(0, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                option = "(1)Look At Item"
                stdscr.addstr(1, 0, option + " " * (40 - len(option)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(1, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                option = "(2)Drop Item"
                stdscr.addstr(2, 0, option + " " * (40 - len(option)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(2, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                option = "(3)Use Item"
                stdscr.addstr(3, 0, option + " " * (40 - len(option)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(3, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(4, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                choice = nextMenu(stdscr)
                # Number doesn't matter here, I'm not converting it to int or anything
                if choice == "1":
                    stdscr.addstr(0, 0, itemInQuestion.printName, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(1, 0, itemInQuestion.desc, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(2, 0, '-- Press any key to exit --', curses.color_pair(1) | curses.A_BOLD)
                    nextMenu(stdscr)
                elif choice == "2":
                    currentLocation.itemsHere.append(itemInQuestion)
                    inventory.remove(itemInQuestion)
                elif choice == "3":
                    ypos = 1
                    stdscr.addstr(0, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                    for item in inventory:
                        if not item == itemInQuestion:
                            label = "|(" + str(keyCounter) + ")" + item.printName
                            stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                            stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                            ypos += 1
                            keyCounter += 1
                            
                    label = "|(0) Yourself"
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD)
                    ypos += 1
                    stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos + 1, 0, "-- Press an item's key to use it, or anything else to exit --", curses.color_pair(1) | curses.A_BOLD)
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

def saveGame( name ):
        allData = [currentLocation, inventory, locations] # Clone locations so we can keep the positions of items
        # Temp file for safety
        savename = "".join([name.rstrip().lstrip(), "_tymeventuresave"])
        tmpname = "".join([name.rstrip().lstrip(), "_tymeventuretmp"])
        savefile_out = open(tmpname, "wb")
        pickle.dump(allData, savefile_out)
        os.rename(tmpname, savename)

def main():
    try:
        stdscr = curses.initscr()
        curses.cbreak() # ; curses.noecho()
        curses.start_color()
        stdscr.keypad(1)
        if args.nocolor:            
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        else:            
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        gameLoop(stdscr)
    except KeyboardInterrupt:
        saveGame( playerName ) # Save game code goes here in the future, this way if they Ctrl-C by accident, they can still save
    finally:
        stdscr.erase()
        stdscr.refresh()
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
