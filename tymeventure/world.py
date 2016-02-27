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

