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


    def useWith(item, location):
        '''Use the item with another item.'''
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
hedgeclippers = Item("Hedgeclippers", "A pair of hedgeclippers. They look almost brand-new.", True)

# Set up items in the world
yourShed.itemsHere = [hedgeclippers]

# Make connections
makeConnection(yourComputer, yourDoorstep)
makeConnection(yourDoorstep, outside)
makeConnection(outside, yourLawn)
makeConnection(yourLawn, yourShed)
makeConnection(outside, yourBlock)
makeConnection(yourBlock, blockRoad)
makeConnection(blockRoad, townSquare)
