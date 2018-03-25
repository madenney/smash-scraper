

import os

def clear(archiveDir):
    print("CLEARING ARCHIVE")
    for filename in os.listdir(archiveDir):
        os.remove(archiveDir + "/" + filename)        
        print(" -- Deleted " + filename)

