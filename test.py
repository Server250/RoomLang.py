import re
import os

def start():
    """Load a set of rooms from file fp and return it as a dict"""
    fp = "rooms.txt"
    
    if (os.path.isfile(fp)):
        print("there is a file named that")
        rf = open(fp, "r") # Open the room file in readonly mode
        if (rf.mode == "r"): # If successfully opened
            lines = rf.read().split("\n")
            numLines = len(lines) # Store number of lines in file
            start = 0 # Start of room assumed to be beginning of file
            end = numLines # End of room assumed to be end of file
            outputDict = dict()

            allowedIdRegex = re.compile(r"[a-zA-Z0-9]")
            allowedLineStarts = re.compile(r"#") # Allowed file starts that don't constitute a new room
        
            while True: # Start of do-while loop to find multiple rooms
                
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
                                    break
                            break

                print("room height is " + str(end-start) + ", width is " + str(len(lines[start])))
                
                if (end>=numLines): # End of do-while loop to detect eof
                    break
                else: # If another room should be found, reset 'start' to after end line and 'end' to numLines to assume this is final room
                    start = end
                    end = numLines


if __name__=="__main__":
	start()