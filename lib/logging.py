
# __init__
# if main_log.txt doesn't exist, create it

import datetime
import os.path
import constants

class Logger(object):

    def __init__(self, archiveDir):
        print("Initializing Logger")
        
        self.mainLog = archiveDir + "/main_log.txt"
        self.urlLog = archiveDir + "/tourneyUrls.txt"

        lastLog = False
        if not os.path.exists(self.mainLog):
            with open(self.mainLog, 'w') as file:
                file.write("Main Log \n")
        else:
            with open(self.mainLog, 'r') as file:
                lines = file.readlines()
                for index, line in enumerate(reversed(lines)):
                    if line[0] == "-":
                        lastLog = lines[(index * -1):]
                        print(lastLog)
                        for i in range(0, len(lastLog)):
                            lastLog[i] = lastLog[i][:-1]
                        break
    
        self.info = LogInfo(lastLog)


    def initialLog(self):
        with open(self.mainLog, "a") as file:
            file.write("----------------------------------------\n")
            now = datetime.datetime.now()
            file.write(constants.logLabelDate + " - " + now.strftime("%Y-%m-%d %H:%M") + "\n")

    def addTourneysToFile(self, tourneys):
        with open(self.urlLog, "a") as file:
            for tourney in tourneys:
                print(tourney.stringify())
                file.write(tourney.stringify() + "\n")

        with open(self.mainLog, "a") as file:
            file.write(constants.logLabelTourneysGrabbed + " - " + str(len(tourneys)) + "\n")
            if len(tourneys) > 0:
                file.write(constants.logLabelLastTourney + " - " + tourneys[0].title + "\n")
                file.write(constants.logLabelLastUrl + " - " + tourneys[0].url + "\n")
            else:
                file.write(constants.logLabelLastTourney + " - " + self.info.lastTourney)
                file.write(constants.logLabelLastUrl + " - " + self.info.lastUrl)

    def addSetstoFile(self, se)

    def getTourneys(self):
        with open(self.urlLog, "r") as file:
            urls = []
            for line in file.readlines():
                urls.append( line[line.index(","):-1])
            return urls


    def printLastLog(self):
        self.info.nicePrint()

    def getLastUrl(self):
        return self.info.lastUrl




# Log Info
class LogInfo(object):

    def __init__(self, lastLog):
        
        self.lastDate = False
        self.lastUrl = False
        self.lastTourney = False
        self.lastNumTourneysGrabbed = False

        if lastLog:
            # Interpret Log
            for line in lastLog:
                s = line.split()
                if s[0] == constants.logLabelDate:
                    self.lastDate = s[2]
                elif s[0] == constants.logLabelLastUrl:
                    self.lastUrl = s[2]
                elif s[0] == constants.logLabelLastTourney:
                    self.lastTourney
                    for t in s[:2]:
                        self.lastTourney += t
                elif s[0] == constants.logLabelTourneysGrabbed:
                    self.logLabelTourneysGrabbed = s[2]
                else:
                    raise Exception("Error in Logger. Unknown value type in last log.")     


    def getLastUrl(self):
        return self.lastUrl

    def setLastUrl(self, lastUrl):
        self.lastUrl = lastUrl

    def nicePrint(self):
        print(("{0:20}{1:35s}").format(constants.logLabelDate, str(self.lastDate)))
        print(("{0:20}{1:35s}").format(constants.logLabelLastUrl, str(self.lastUrl)))
        print(("{0:20}{1:35s}").format(constants.logLabelLastTourney, str(self.lastTourney)))
        print(("{0:20}{1:35s}").format(constants.logLabelTourneysGrabbed, str(self.lastNumTourneysGrabbed)))

