import requests
from bs4 import BeautifulSoup

# URL = "https://www.babycenter.com/baby-names/details/liam-2820"
#TODO: make number larger after tests
URL = "https://www.babycenter.com/babyNamerSearch.htm?batchSize=1000"
page = requests.get(URL)

#CONSOLE PRINT FOR TESTING:
#print(page.text)

soup = BeautifulSoup(page.content, "html.parser")

# print(soup.prettify())

# # scrape list page for URLs to specific names
# # loop over name URLs and scrape facts, if present (default if no description is present?)
# # write fact dictionary to text file

results = soup.find_all(class_="nameCell")

for link in results:
    print(link.find("a").get("href"))
    
# print(results)