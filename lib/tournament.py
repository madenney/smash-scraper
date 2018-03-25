
from lib import helper

class Tournament(object):

    def __init__(self, title = False, url = False, date = False, location = False, entrants = False):

        if(title != False):
            title = helper.removeCommas(title)

        if(date != False):
            date = helper.removeCommas(date)

        if(location != False):
            location = helper.removeCommas(location)
        
        self.title = title
        self.url = url
        self.date = date
        self.location = location
        self.entrants = entrants

    def stringify(self):
        
        if not self.title or not self.url:
            raise Exception("Error in tournament stringify. No title or url is set.")

        if self.location == False:
            self.location = "earth"

        string = self.title + "," + self.url + "," + self.date + "," + self.location

        if(self.entrants != False):
            string += "," + self.entrants
        
        return string

    def parse(self, string):
        s = string.split()
        self.title = s[0]
        self.url = s[1]
        self.date = s[2]
        self.location = s[3]
        if len(s) >= 5:
            self.entrants = s[4]

    def setEntrants(self, entrants):
        self.entrants = entrants