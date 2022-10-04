import requests
from bs4 import BeautifulSoup

URL = "https://www.behindthename.com/names/sort/alpha/display/details"
MAX_PAGE_COUNT = 84
name_fact_dict = {}

def parse_a_page(url):
    """Scrapes a page and creates key/value pairs in dictionary:
    {'Name':'This is a fact', 'Name2':'Another fact.', ...}
    """
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # Strip unwanted data fields from html page
    for span in soup.find_all(class_="listgender"):
        span.decompose()
    for span in soup.find_all(class_="listusage"):
        span.decompose()

    results = soup.find_all(class_="browsename")

    # Grab key name, then delete containing tag so only fact text remains.
    # Write key/value pair to dictionary:
    for name in results:
        key = name.find(class_="listname").get_text()
        name.find(class_="listname").decompose()
        name_fact_dict[key] = name.get_text().strip()
        
# Loops over all pages in source website:
for pagenumber in range(1,MAX_PAGE_COUNT):
    parse_a_page(f"{URL}/{pagenumber}")
    
# Writes completed dictionary to text file:
with open('scraped_names_facts.txt','w') as data: 
      data.write(str(name_fact_dict))

