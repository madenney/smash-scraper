
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import math
import re
import constants

from lib import tournament as t
from lib import pysmash
smash = pysmash.SmashGG()

TOURNEYS_PER_PAGE = 5

class Scraper(object):


    def __init__(self, logger):
        self.logger = logger


    def getMatches(self):

        tourneys = self.logger.getTourneys()
        
        tourneySets = []
        for tourney in tourneys:

            ggtag = tourney.url[tourney.url.index('smash.gg/tournament')+20:]

            if "/" in ggtag:
                ggtag = ggtag[:ggtag.index('/')]
            
            if(constants.verbose):
                print("Getting Sets")
            sets = []

            try:
                keyword = 'melee-singles'
                try:
                    sets = smash.tournament_show_sets(ggtag, keyword)
                except pysmash.exceptions.ValidationError:
                    keyword = 'super-smash-bros-melee-singles'
                    try:
                        sets = smash.tournament_show_sets(ggtag, keyword)
                    except pysmash.exceptions.ValidationError:
                        keyword = 'melee-singles-1'
                        try:
                            sets = smash.tournament_show_sets(ggtag, keyword)
                        except pysmash.exceptions.ValidationError:
                            keyword = 'melee-singles-2'
                            try:
                                sets = smash.tournament_show_sets(ggtag, keyword)
                            except pysmash.exceptions.ValidationError:
                                keyword = 'super-smash-bros-melee'
                                sets = smash.tournament_show_sets(ggtag, keyword)

                players = smash.tournament_show_players(ggtag, keyword)

            except (KeyError, pysmash.exceptions.ResponseError) as err:
                print("ERROR WITH PYSMASH", err)
                continue

            for set in sets:

                winner = loser = score = winner_score = loser_score = None

                winner_id = int(set['winner_id'])
                loser_id = int(set['loser_id'])

                if(winner_id == int(set['entrant_1_id'])):
                    winner_score = str(set['entrant_1_score'])
                    loser_score = str(set['entrant_2_score'])
                    score = winner_score + "-" + loser_score
                else:
                    winner_score = str(set['entrant_2_score'])
                    loser_score = str(set['entrant_1_score'])
                    score = winner_score + "-" + loser_score

                # If no score was kept
                if(winner_score == 'None' and loser_score == 'None'):
                    score = 'x-x'

                # Check for DQ
                if len(score) != 3:
                    print("DQ")
                    continue

                # Get winner tag
                for player in players:
                    if winner_id == player['entrant_id']:
                        winner = player['tag']
                        break

                # Get loser tag
                for player in players:
                    if loser_id == player['entrant_id']:
                        loser = player['tag']
                        break

                try:
                    output = winner + ',' + loser + ',' + score + ',' + tourney.title
                except TypeError:
                    print("An error occured. Skipping this match.")
                    error = "smashggScraper typeError. Tournament - " + tourney.title
                    if(winner != None):
                        error += " player -" + winner
                    if(loser != None):
                        error += " player -" + loser
                    self.logger.logError(error)
                    continue

                print(output)
                tourneySets.append(output)

        
            ## before end of tourney in tourneys loop
            self.logger.addSetsToFile(tourneySets, tourney)
        # end of tourney in tourneys loop




    def getURLs(self):

        print("Initializing Web Driver")
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
        
        ggLink = "https://smash.gg/tournaments?per_page="+str(TOURNEYS_PER_PAGE)+"&filter=%7B%22upcoming%22%3Afalse%2C%22past%22%3Atrue%2C%22videogameIds%22%3A1%7D&page="

        driver.get(ggLink)

        # Get number of pages available
        pageText = "none"
        centerElements = driver.find_elements_by_class_name("text-center")
        for element in centerElements:
            pagination = element.find_elements_by_class_name("pagination")
            if len(pagination) > 0:
                pageTextElement = element.find_elements_by_class_name("text-muted")
                if len(pageTextElement) > 0:
                    pageText = pageTextElement[0].get_attribute("innerHTML")
                    break   

        if(pageText == "none"):
            raise Exception("Error in Smashgg Scraper. Number of pages not found")

        # Get number of results from the end of the string
        results = int(pageText.split()[-1])
        numberOfPages = math.ceil(results / TOURNEYS_PER_PAGE)
        
        # Loop through all pages and get links
        tourneys = []
        stop = False
        count = 0
        for i in range(2, numberOfPages + 1):
            
            cards = driver.find_elements_by_class_name("TournamentCardContainer")
            for card in cards:

                # Get title and URL
                titleElement = card.find_elements_by_class_name("TournamentCardHeading__title")
                a = titleElement[0].find_element_by_tag_name("a")
                title = a.get_attribute("innerHTML")
                url = a.get_attribute("href")

                # Get Date
                dateElement = card.find_elements_by_class_name("TournamentCardHeading__information")
                dateSpan = dateElement[0].find_elements_by_tag_name("span")
                if len(dateSpan) > 1:
                    date = dateSpan[1].get_attribute("innerHTML")
                else:
                    date = dateSpan[0].get_attribute("innerHTML")

                # Get Location
                infoList = card.find_elements_by_class_name("InfoList__title")
                spans = infoList[0].find_elements_by_tag_name("span")
                location = spans[0].get_attribute("innerHTML")
                if "react" in location: # If smashGG has a messed up date
                    location = False
                
                # Check if the end was reached yet
                if self.logger.getLastUrl() == url:
                    stop = True
                    break
                else:
                    tournament = t.Tournament(title, url, date, location)
                    tourneys.append(tournament)
                    count += 1
            
            print("Number of URLs grabbed: " + str(count))

            if(stop or constants.stopShort):
                break
            else:
                print("Getting page " + str(i) + " out of " + str(numberOfPages + 1) + "...")
                count = 0
                driver.get(ggLink + str(i))

        driver.quit()
        self.logger.addTourneysToFile(tourneys)
