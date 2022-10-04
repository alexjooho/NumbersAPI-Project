import requests
from bs4 import BeautifulSoup

URL = "https://www.behindthename.com/names/sort/alpha/display/details"


# for link in results:

#     print(f'{BASE_URL}{link.find("a").get("href")}')

# print(results)

def parse_a_page(url):
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")

    # Strip unwanted data fields from html page
    for span in soup.find_all(class_="listgender"):
        span.decompose()
    for span in soup.find_all(class_="listusage"):
        span.decompose()

    # scrape list page for URLs to specific names
    # loop over name URLs and scrape facts, if present (default if no description is present?)
    # write fact dictionary to text file

    results = soup.find_all(class_="browsename")

    for name in results:
        print(name.get_text())
        
for pagenumber in range(1,84):
    parse_a_page(f"{URL}/{pagenumber}")