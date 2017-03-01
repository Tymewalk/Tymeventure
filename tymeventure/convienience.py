# convienience.py
# Convienience functions.
import unicurses

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

def drawBoxPopup(screen, text, xsize=40):
    screen.addstr(0, 0, "-" * 40, unicurses.color_pair(0) | unicurses.A_BOLD)
    ypos = 1
    for option in options:
        screen.addstr(ypos, 0, option + " " * (xsize - len(option)), unicurses.color_pair(0) | unicurses.A_BOLD)
        screen.addstr(ypos, xsize, "|", unicurses.color_pair(0) | unicurses.A_BOLD)
        ypos += 1

    screen.addstr(ypos, 0, "-" * xsize, unicurses.color_pair(0) | unicurses.A_BOLD)

def drawBoxMenu(screen, options, xsize=40):
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

    return ypos
