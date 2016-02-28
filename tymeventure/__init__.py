# TYMEVENTURE v0.0.2
# Status: Stable
# A simple curses-based game running in Python 3.4.3.
# Help would be appreciated if you know how.
#
# TODO:
# - Develop some story
# - Allow players to use items, even on themselves
# - Let players know if there's an item where they are
# - Better use of colors

import curses # Curses! You've foiled my plan!
import pickle # For savegames later on
from world import *
from commandline import * # In theory this should just execute the code and allow us to keep the code neat

inventory = list() # The player's inventory

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

def main(stdscr):  
    currentLocation = yourComputer
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 0, 'Welcome to Tymeventure!', curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, '-- Press any key to advance --', curses.color_pair(1) | curses.A_BOLD)
    nextMenu(stdscr)    
    stdscr.addstr(0, 0, "What's your name? (max 30 characters)", curses.color_pair(0) | curses.A_BOLD)
    stdscr.addstr(1, 0, 'Name: ', curses.color_pair(0) | curses.A_BOLD)
    playerName = stdscr.getstr(1, 6, 30).decode('utf8')
    stdscr.clear()
    stdscr.refresh()
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
        if not currentLocation.itemsHere == []:
            if len(currentLocation.itemsHere) == 1:
                itemsHereBar = "There is one item here."
            else:

                itemsHereBar = "There are " + str(len(currentLocation.itemsHere)) + " items here."
        else:
            itemsHereBar = "There are no items here."
        stdscr.addstr(3, 0, itemsHereBar, curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(4, 0, "(Q)uit", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(5, 0, "(M)ove", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(6, 0, "(T)hings here", curses.color_pair(0) | curses.A_BOLD)
        stdscr.addstr(7, 0, "(I)nventory", curses.color_pair(0) | curses.A_BOLD)
        choice = getKey(stdscr).lower() # Case doesn't matter
        # Clear before we process so we can print other stuff
        stdscr.clear()
        stdscr.refresh()
        if choice == "q":
            continueGame = False
        elif choice == "m":
            ypos = 1
            stdscr.addstr(ypos - 1, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keycount = 1
            for place in currentLocation.connections:
                label = "|(" + str(keycount) + ")" + place.printName
                stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                ypos += 1
                keycount += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "Press the key next to where you want to move.", curses.color_pair(0) | curses.A_BOLD)
            choice = nextMenu(stdscr)
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                if int(choice) - 1 < len(currentLocation.connections):
                    moveTo = currentLocation.connections[int(choice) - 1]
                    currentLocation = moveTo # Move us
        elif choice == "t":
            ypos = 1
            stdscr.addstr(ypos - 1, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            keycount = 1
            if currentLocation.itemsHere == []:
                stdscr.addstr(ypos, 0, "|There is nothing here.                |", curses.color_pair(0) | curses.A_BOLD)
                ypos += 1
            else:
                for item in currentLocation.itemsHere:
                    label = "|(" + str(keycount) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                    ypos += 1
                    keycount += 1
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
            keycount = 1
            if inventory == []:
                stdscr.addstr(ypos, 0, "|You have nothing in your inventory.   |", curses.color_pair(0) | curses.A_BOLD)
                ypos += 1
            else:
                for item in inventory:
                    label = "|(" + str(keycount) + ")" + item.printName
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                    ypos += 1
                    keycount += 1
            stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
            stdscr.addstr(ypos + 1, 0, "Press an item's key to do something with it, or anything else to exit.", curses.color_pair(0) | curses.A_BOLD)
            choice = nextMenu(stdscr)
            checkItem = False
            if choice in "123456789": # Make sure it's a number, the game crashes otherwise
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
                stdscr.addstr(2, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                option = "(3)Use Item"
                stdscr.addstr(3, 0, option + " " * (40 - len(option)), curses.color_pair(0) | curses.A_BOLD)
                stdscr.addstr(3, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                stdscr.addstr(4, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                choice = nextMenu(stdscr)
                # Number doesn't matter here, I'm not converting it to int or anything
                if choice == "1":
                    stdscr.addstr(0, 0, itemInQuestion.printName, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(1, 0, itemInQuestion.desc, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(2, 0, '-- Press any key to exit --', curses.color_pair(0) | curses.A_BOLD)
                    nextMenu(stdscr)
                elif choice == "2":
                    currentLocation.itemsHere.append(itemInQuestion)
                    inventory.remove(itemInQuestion)
                elif choice == "3":
                    for item in inventory:
                        if not item == itemInQuestion:
                            label = "|(" + str(keycount) + ")" + item.printName
                            stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                            stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                            ypos += 1
                            keycount += 1
                            
                    label = "|(0) Yourself"
                    stdscr.addstr(ypos, 0, label + (" " * (len(label) - 40)), curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos, 40, "|", curses.color_pair(0) | curses.A_BOLD) # Make a "box"
                    ypos += 1
                    stdscr.addstr(ypos, 0, "-" * 40, curses.color_pair(0) | curses.A_BOLD)
                    stdscr.addstr(ypos + 1, 0, "Press an item's key to do use it, or anything else to exit.", curses.color_pair(0) | curses.A_BOLD)
                    choice = nextMenu(stdscr)
                    checkItem = False
                    if choice in "123456789": # Make sure it's a number, the game crashes otherwise
                        if int(choice) - 1 < len(inventory):
                            checkItem = True
                            itemToUseWith = inventory[int(choice) - 1]
                        else:
                            checkItem = False
                    elif choice == "0": # If it's the player being used...
                        itemToUseWith = playerItem
                        checkItem = True
                    else:
                        checkItem = False
                        
                    if checkItem:
                        itemInQuestion.useWith(itemToUseWith, currentLocation, inventory)
                        
                else:
                    pass
            
        else:
            pass


def runGame():
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
        main(stdscr)
    except KeyboardInterrupt:
        pass # For save games in the future
    finally:
        stdscr.erase()
        stdscr.refresh()
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
