import requests
from bs4 import BeautifulSoup

URL = "https://www.babycenter.com/baby-names/details/liam-2820"
# URL = "https://www.babycenter.com/babyNamerSearch.htm?batchSize=1000"
page = requests.get(URL)

print(page.text)