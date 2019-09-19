"""

author: Cameron Gemmell
github: BearShark

description: Contains all barebones RoomLang functionality and data structures

"""

# The data structure for holding a room.
# roomId - How the room shall be referenced (one char, a-zA-Z0-9)
# w - width
# h - height
# n,e,s,w - north, east, south and west doors respectively
class Room:

    def __init__(self, roomId,wid,hei,n=None,e=None,s=None,w=None):
        self.id = roomId
        self.width = int(wid)
        self.height = int(hei)
        self.north = n
        self.east = e
        self.south = s
        self.west = w

    """Print out helpful information about  a room to the console."""
    def log(self):
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
# Program Entry Point
if __name__=="__main__":
    print("This module is intended to be imported by your project, not run itself.")
    
    testRoom = Room('a',12,16,'b',None,'3',None)
    testRoom.log()
