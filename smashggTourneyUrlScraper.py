
print("Scraping Tournaments from smash.gg")

from selenium import webdriver

driver = webdriver.Firefox()


tourneyLinkList = []

# Loop through all the pages
for i in range(1,864):

    ggLink = "https://smash.gg/tournaments?per_page=5&filter=%7B%22upcoming%22%3Afalse%2C%22past%22%3Atrue%2C%22videogameIds%22%3A1%7D&page="

    driver.get(ggLink + str(i))

    cards = driver.find_elements_by_class_name("TournamentCardHeading")

    for card in cards:
        a = card.find_elements_by_class_name("Link")
        link = a[0].get_attribute("href")
        tourneyLinkList.append(link)


with open("output.txt", "a") as file:
    for link in tourneyLinkList:
        file.write(link + "\n")