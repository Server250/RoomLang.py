import os # Used for loading and saving room files
import re # Used for loading room files

"""

author: Cameron Gemmell
github: www.github.com/Server250/

description: Contains Room data structure, as well as a loader and a saver for the RoomLang standard. Documentation available at:

"""

# The data structure for holding a room.
class Room:
    
    def __init__(self, roomId,wid,hei,n=None,e=None,s=None,w=None,addDeets=dict()):
        """
        Initialise the "Room" class.

        roomId - How the room shall be referenced (one char, a-zA-Z0-9)
        w - width
        h - height
        n,e,s,w - north, east, south and west doors respectively
        addDeets - additional room information the user wants to add
        """
        
        self.id = roomId
        self.width = int(wid)
        self.height = int(hei)
        self.north = n
        self.east = e
        self.south = s
        self.west = w
        self.details=addDeets

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
    print("RoomLang loading rooms...\t",end="") # Print success or error on same line
    
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
            allowedLineStarts = re.compile(r":") # Special line starts that mean something
            extraInfoRegex = re.compile(r":([a-zA-Z ]+):([a-zA-Z ]+)") # Info for deconstructing additional room info
            
            while True: # Start of do-while loop to find multiple rooms
            
                # Variables for tracking properties of read room
                newId = "" # Hold the id of the loaded room
                newWid, newHei = 0,0 # Hold the height and width of the loaded room
                newN, newE, newS, newW = None,None,None,None # Hold directions for doors loaded
                addDict = dict() # Dictionary to hold loaded additional details
                
                # Loop from the assumed start to the assumed end of the room
                for i in range(start,end):
                    
                    # Find the actual start of the next room (whitespace and comments should be allowed)
                    if (lines[i]): # Find out if there is a line there
                        if (re.match(allowedIdRegex,lines[i][0])): # If first char of a line is an id
                            
                            start=i # The start of the next room is here
                            newId=lines[i][0] # The ID for the room has been found
                            
                            # Find the actual end of the room, always assumes the end is eof for limiting
                            for j in range(start+1, numLines-1):    
                                # If the first char of a line isn't a '#' or there isn't a line, this signals the end of the room
                                if (not(lines[j])) or (j==numLines-2) or ((not(lines[j][0]=="#")) and not(lines[j+1])): # Find the end of the room
                                    end = j
                                    
                                    # DO SIZE WORK HERE before end is repositioned
                                    newHei, newWid = end-start, len(lines[start])
                                    
                                    # Find the doors in the room
                                    #print("FIRST LINE EXC OWN ID: " + lines[start][1:])
                                    #print("DID MATCH? " + str(re.match(allowedIdRegex, lines[start][1:])))
                                    newN=re.search(allowedIdRegex, lines[start][1:]) # Find an ID on the first line of the room, missing the first char 
                                    if newN:
                                        newN=newN[0]                   
                                    # TODO - MAKE "end-1" into "end-additionalDetails"
                                    newS=re.search(allowedIdRegex, lines[end-1]) # Find an ID on the last line of the room
                                    if newS:
                                        newS=newS[0]
                                    # Loop through the lines of the room to find side doors
                                    for x in range(start+1,end):
                                        if (newW==None): # If not found a western door yet
                                            newW=re.search(allowedIdRegex, lines[x][0]) # Should always be a character at left side, so if it is a id it is the door
                                            if newW:
                                                newW=newW[0]
                                        if (len(lines[x])==newWid) and (newE==None): # If the line has characters all the way to the right (East) side and not found east door yet
                                            newE=re.search(allowedIdRegex, lines[x][newWid-1])
                                            if newE:
                                                newE=newE[0]
                                                
                                    # Check for any extra information included in the room
                                    for k in range (end, numLines):
                                        if lines[k] and (re.match(allowedLineStarts,lines[k][0])): # If not a newline and is a special line start
                                            #print("DEALING WITH EXTRA INFO - " + lines[k]) # DEBUGGING
                                            loadedDetail=re.search(extraInfoRegex,lines[k])
                                            #print("LOADED: " + str(loadedDetail)) # DEBUGGING
                                            addDict[loadedDetail[1]] = loadedDetail[2] # Load the new detail into the dictionary

                                            end=k # Update end to after the additional details (as this is used as next start point)
                                        else:
                                            break
                                    break
                            break
                
                # Create the room object to be added to the Room List
                loadedRoom = Room(newId, newWid, newHei, newN,newE,newS,newW, addDict)
                outputDict[newId]=loadedRoom
                
                if (end>=numLines-2): # End of do-while loop to detect eof (-2 to excuse whitespace used as allowances for other algorithms)
                    break
                else: # If another room should be found, reset 'start' to after end line and 'end' to numLines to assume this is final room                
                    start = end
                    end = numLines
            
            print("Rooms loaded successfully.")
            # RETURN HERE
            return outputDict

    else: raise ValueError("The file supplied to RoomLoader() does not exist. Make sure you include the file extension!")

# Function for saving rooms to disk
def RoomSaver(roomList, location, mode):
    """
    Save the rooms stored in roomList to a file at location. To overwrite an existing file, use "o"verwrite mode. To append to the end of the existing file, use "a"ppend mode. append by default
    
    """
    
    # Validate the input of the mode
    mode = str(mode)
    if not (mode == "o" or mode == "a" or mode=="O" or mode=="A"): # If a valid mode not entered
        raise ValueError("Invalid argument supplied to RoomSaver: Use either 'a' for append mode or 'o' for overwrite mode.")
    
    # Check location to see if existing file
    fileExists = os.path.isfile(location)

    if not fileExists:
       print("File not found; will be created.") 

    # Append mode will add to end so comments are intact
    if (mode=="a" or mode=="A"):
        print("APPEND MODE")
	# Load rooms, append rooms that don't exist (ie room key not in file yet)
    	# New function to just get all room IDs because no need to get all room data
	# Overwrite mode will just make a whole new file
    else: # Overwrite mode
        print("OVERWRITE MODE")
        # Open file
        f = open(location,"w+") # '+' means if file doesn't exist then it'll be created
        # Straight go down room list and save to file
        for rm in roomList:
            
            r = roomList[rm]
            
            # Used for writing doors with correct padding
            halfW = int(r.width/2)
            halfH = int(r.height/2)
            
            f.write(r.id)
            if (r.north==None):
                f.write(("#"*(r.width-1)) + "\n")
            else:
                f.write(("#"*(halfW)) + r.north + ("#"*((r.width-halfW)-2)) + "\n") # r.width - halfW used to make sure odd numbers written without being rounded twice/not at all
            
            f.write(("#"+(" "*(r.width-2))+"#\n")*(halfH-1))
            if (r.west==None):
                f.write("#")
            else:
                f.write(r.west)
                
            f.write(" "*(r.width-2))
            
            if (r.east==None):
                f.write("#")
            else:
                f.write(r.east)
            f.write("\n")
            
            f.write(("#" + " "*(r.width-2) + "#\n")*(r.height-(halfH+3)))
            
            if (r.south==None):
                f.write(("#"*(r.width)) + "\n")
            else:
                f.write(("#"*(halfW)) + r.south + ("#"*((r.width-halfW)-1)) + "\n") # r.width - halfW used to make sure odd numbers written without being rounded twice/not at all
            
            f.write("\n")
            
            print("ROOM PRINTED")	
        
        f.close() # Close the file

    print("Rooms saved successfully.")

# Program Entry Point
if __name__=="__main__":
    print("This module is intended to be imported by your project, not run itself.\n")
    
    # Load rooms from file
    testList = RoomLoader("rooms.txt")
    
    # Log all loaded rooms
    for k in testList:
        testList[k].log()
        print("\n")
	
    # Save rooms
    RoomSaver(testList, "roomsSaved.txt", "o")   
 

