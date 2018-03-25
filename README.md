# Smash Scraper

The purpose of this project is to gather competitive Super Smash Bros Melee tournament data, format it, and enter it into a database.

## Getting Started

This uses **selenium-webdriver** python package, which requires a tool called 'geckodriver'. This is found in the *assets* directory.

Make sure to add this directory to your PATH variables by using the following command:

' export PATH=$PATH:/path/to/directory/smash-scraper/assets '

## Command line arguments

'''
optional arguments:
  -v                Verbose Mode.
  -x                Skip the 'get urls' step
  -c                Delete all files in /archive before starting
  -s                Stop after only one page of URLs (for testing purposes)
'''

## Deployment

Notes coming soon

## Authors

* **Matt Denney** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* I must tip my hat to user [petercat12](https://github.com/petercat12) for creating the very helpful pysmash library
* Also, thanks to smash.gg for having an amazing website to grab data from

