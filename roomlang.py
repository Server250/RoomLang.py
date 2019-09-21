"""

author: Cameron Gemmell
github: BearShark

description: Contains all barebones RoomLang functionality and data structures

"""

# The data structure for holding a room.
class Room:
    
    def __init__(self, roomId,wid,hei,n=None,e=None,s=None,w=None):
        """
        Initialise the "Room" class.

        roomId - How the room shall be referenced (one char, a-zA-Z0-9)
        w - width
        h - height
        n,e,s,w - north, east, south and west doors respectively
        """
        self.id = roomId
        self.width = int(wid)
        self.height = int(hei)
        self.north = n
        self.east = e
        self.south = s
        self.west = w

    def log(self):
        """Print out helpful information about  a room to the console."""

        ljustsize = 15
        rjustsize = 6
        # Print the room's ID
        print("Room ID:".ljust(ljustsize)+self.id.rjust(rjustsize))
        # Print dimensions of the room
        print("Dimensions:".ljust(ljustsize)+(str(self.width)+"x"+str(self.height)).rjust(rjustsize))
        # Print the locations doors lead to
        print("Doors:")
        if (self.north): print("N -".rjust(8).ljust(ljustsize)+str(self.north).rjust(rjustsize))
        if (self.east):  print("E -".rjust(8).ljust(ljustsize)+str(self.east).rjust(rjustsize))
        if (self.south):  print("S -".rjust(8).ljust(ljustsize)+str(self.south).rjust(rjustsize))
        if (self.west):  print("W -".rjust(8).ljust(ljustsize)+str(self.west).rjust(rjustsize))

    def move(self,d,source=None):
        """
        Return the room that will be visited by moving in direction d (n,e,s,w), using source as the room list
        """
        if (source==None): raise ValueError("No room set was supplied to 'move' function.")
        if (str(d).lower()[0] in [str("n"),"e","s","w"]):
            # if d is n,e,s,w
            if (d.lower()[0]=="n") and (self.north!=None):
                if(self.north in source):
                    print("MOVING NORTH\n")
                    return source.get(self.north)
            if (d.lower()[0]=="e") and (self.east!=None):
                if(self.east in source):
                    print("MOVING EAST\n")
                    return source.get(self.east)
            if (d.lower()[0]=="s") and (self.south!=None):
                if(self.south in source):
                    print("MOVING SOUTH\n")
                    return source.get(self.south)
            if (d.lower()[0]=="w") and (self.west!=None):
                if(self.west in source):
                    print("MOVING WEST\n")
                    return source.get(self.west)
            # If a door hasn't activated, door doesn't exist. Return current room
            return self
        # If reaches this point, an incorrect direction was passed through
        else: raise ValueError("A direction should be 'n', 'e', 's' or 'w'!")
            
def RoomLoader(fp):
    """Load a set of rooms from file fp"""
    print("Loaded rooms")

# Program Entry Point
if __name__=="__main__":
    print("This module is intended to be imported by your project, not run itself.")
    
    roomList = {'a':Room('a',12,16,'b',None,'3',None), 'b':Room('b',4,5,None,None,'a',None)}
    
    currentRoom = roomList.get('a')

    currentRoom.log()

    currentRoom = currentRoom.move("n",roomList)

    currentRoom.log()

    currentRoom = currentRoom.move("s",roomList)

    currentRoom.log()

