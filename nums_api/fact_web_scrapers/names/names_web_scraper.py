import requests
from bs4 import BeautifulSoup

URL = "https://www.behindthename.com/names/sort/alpha/display/details"
name_fact_dict = {}


def parse_a_page(url):
    """Scrapes a page and creates key/value pairs in dictionary:
    {'Name':'This is a fact', 'Name2':'Another fact.', ...}

    Returns False when a page has no name information on the page
    otherwise returns True
    """
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    # Strip unwanted data fields from html page
    for span in soup.find_all(class_="listgender"):
        span.decompose()
    for span in soup.find_all(class_="listusage"):
        span.decompose()

    results = soup.find_all(class_="browsename")
    if not results:
        return False

    # Grab key name, then delete containing tag so only fact text remains.
    # Write key/value pair to dictionary:
    for name in results:
        key = name.find(class_="listname").get_text()
        name.find(class_="listname").decompose()
        name_fact_dict[key] = name.get_text().strip()

    return True

def parse_multiple_pages(base_url=URL):
    """Loops over all pages in source website until reaching an empty page:"""
    pagenumber = 1
    
    while True:
        results = parse_a_page(f"{base_url}/{pagenumber}")
        if results == False:
            break
        pagenumber += 1
        
    return

def write_to_file(source='scraped_names_facts.txt', data=name_fact_dict):
    """Writes completed dictionary to text file:"""
    with open(source, 'w') as file:
        file.write(str(data))

def main():
    """Conductor function"""
    parse_multiple_pages()
    write_to_file()
    
    
if __name__ == '__main__':
    main()
