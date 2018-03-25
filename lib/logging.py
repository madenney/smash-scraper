
import datetime
import os.path
import constants
from lib import tournament as t

class Logger(object):

    def __init__(self, archiveDir):
        print("Initializing Logger")
        
        self.mainLog = archiveDir + "/" + constants.mainLog
        self.unscrapedTourneyLog = archiveDir + "/" + constants.unscrapedTourneysFile
        self.matchesLog = archiveDir + "/" + constants.matchesFile
        self.scrapedTourneyLog = archiveDir + "/" + constants.scrapedTourneysFile
        self.errorLog = archiveDir + "/" + constants.errorLog

        # get list of scraped tournaments to use for checking for duplicates
        self.scrapedTournaments = []
        if os.path.exists(self.scrapedTourneyLog):
            with open(self.scrapedTourneyLog, "r") as file:
                for line in file.readlines():
                    self.scrapedTournaments.append(t.Tournament().parse(line[:-1]))

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
        with open(self.unscrapedTourneyLog, "a") as file:
            for tourney in tourneys:
                add = True
                for s in self.scrapedTournaments:
                    if tourney.url == s.url:
                        self.logError("Duplicate Tournament Error. Url: " + s.url)
                        add = False
                        break
                if add:
                    print(tourney.stringify())
                    file.write(tourney.stringify() + "\n")
                else:
                    print("Skipping Duplicated Tournament")

        with open(self.mainLog, "a") as file:
            file.write(constants.logLabelTourneysGrabbed + " - " + str(len(tourneys)) + "\n")
            if len(tourneys) > 0:
                file.write(constants.logLabelLastTourney + " - " + tourneys[0].title + "\n")
                file.write(constants.logLabelLastUrl + " - " + tourneys[0].url + "\n")
            else:
                file.write(constants.logLabelLastTourney + " - " + self.info.lastTourney)
                file.write(constants.logLabelLastUrl + " - " + self.info.lastUrl)


    # I'm fully aware of how cpu intensive this can be
    def addSetsToFile(self, sets, tournament):

        # Make array of unscraped
        unscraped = []
        with open(self.unscrapedTourneyLog, "r") as file:
            for line in file.readlines():
                unscraped.append( t.Tournament().parse(line[:-1]) )

        # Find new tournament in unscraped and remove it
        for u in unscraped:
            if u.url == tournament.url:
                unscraped.remove(u)
                break

        # Rewrite unscraped file with new array
        with open(self.unscrapedTourneyLog, "w") as file:
            for u in unscraped:
                file.write(u.stringify() + "\n")

        # Write new matches to matches file
        with open(self.matchesLog, "a") as file:
            for set in sets:
                file.write(set + "\n")

        # Add new tournament to scraped list
        tournament.setEntrants(str(len(sets)))
        with open(self.scrapedTourneyLog, "a") as file:
            file.write(tournament.stringify() + "\n")


    def logError(self, error):
        with open(self.errorLog, "a") as file:
            file.write(error + "\n")

    def getTourneys(self):
        with open(self.unscrapedTourneyLog, "r") as file:
            tourneys = []
            for line in file.readlines():
                tourneys.append( t.Tournament().parse(line[:-1]) )
            return tourneys


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

