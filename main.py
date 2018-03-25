
print("RUNNING SMASH SCRAPER")

from lib import logging
from lib import admin

from scrapers import smashggScraper

import constants

import os
import sys


CURRENT_DIR = os.getcwd()
ARCHIVE_DIR = CURRENT_DIR + "/archive"

def main():

    # Loop through args
    doGetUrls = True

    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "-c":
                admin.clear(ARCHIVE_DIR)
                print("")
            elif arg == "-v":
                constants.verbose = True
            elif arg == "-s":
                constants.stopShort = True
            elif arg == "-x":
                doGetUrls = False
            

    try:
        logger = logging.Logger(ARCHIVE_DIR)
        logger.initialLog()
        logger.printLastLog()

        ggScraper = smashggScraper.Scraper(logger)
        if(doGetUrls):
            print("Getting URLs...")
            ggScraper.getURLs()

        print("Getting Matches...")
        ggScraper.getMatches()

    except Exception as error:
        print(error)
        return

main()