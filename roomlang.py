import os # Used for loading and saving room files
import re # Used for loading room files

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
    """Load a set of rooms from file fp and return it as a dict"""
    if (os.path.isfile(fp)):
        #print("there is a file named that") # DEBUGGING CODE
        rf = open(fp, "r") # Open the room file in readonly mode
        if (rf.mode == "r"): # If successfully opened
            lines = rf.read().split("\n")
            lines.extend("\n") # Artificially add a blank line to the end, this means the end of the last room is found correctly
            
            numLines = len(lines) # Store number of lines in file
            start = 0 # Start of room assumed to be beginning of file
            end = numLines # End of room assumed to be end of file
            outputDict = dict()

            allowedIdRegex = re.compile(r"[a-zA-Z0-9]")
            allowedLineStarts = re.compile(r"!") # Special line starts that mean something
        
            while True: # Start of do-while loop to find multiple rooms
            
                # Variables for tracking properties of read room
                newId = ""
                newWid, newHei = 0,0
                newN, newE, newS, newW = None,None,None,None
                
                # Loop from the assumed start to the assumed end of the room
                for i in range(start,end):
                    
                    # Find the actual start of the next room (whitespace and comments should be allowed)
                    if (lines[i]): # Find out if there is a line there
                        if (re.match(allowedIdRegex,lines[i][0])): # If first char of a line is an id
                            start=i # The start of the next room is here
                            
                            # Find the actual end of the room, always assumes the end is eof for limiting
                            for j in range(start+1, numLines):    
                                # If the first char of a line isn't a '#' or there isn't a line, this signals the end of the room
                                if (not(lines[j])) or (not(lines[j][0]=="#")): # Find the end of the room
                                    end = j
                                    
                                    # DO SIZE WORK HERE
                                    print("room height is " + str(end-start) + ", width is " + str(len(lines[start])))
                                    
                                    # Check for any extra information included in the room
                                    for k in range (end, numLines):
                                        if lines[k] and (re.match(allowedLineStarts,lines[k][0])): # If not a newline and is a special line start
                                            print("DEALING WITH EXTRA INFO - " + lines[k])
                                            end=k
                                    break
                            break
                
                if (end>=numLines): # End of do-while loop to detect eof
                    break
                else: # If another room should be found, reset 'start' to after end line and 'end' to numLines to assume this is final room
                    start = end
                    end = numLines


    else: raise ValueError("The file supplied to RoomLoader() does not exist. Make sure you include the file extension!")

    #print("Loaded rooms") # DEBUGGING CODE

# Program Entry Point
if __name__=="__main__":
    print("This module is intended to be imported by your project, not run itself.")
    
    roomList = {'a':Room('a',12,16,'b',None,'3',None), 'b':Room('b',4,5,None,None,'a',None)}
    
    currentRoom = roomList.get('a')

    currentRoom.log()

    currentRoom = currentRoom.move("n",roomList)

    currentRoom.log()

    currentRoom = currentRoom.move("south",roomList)

    currentRoom.log()

    testList = RoomLoader("rooms.txt")

