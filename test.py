# just a testing file

import requests
from bs4 import BeautifulSoup

page = 1
url = f"http://milionchvilek.cz/podepsali/{page}"
req = requests.get(url)

soup = BeautifulSoup(req.text, "lxml")

div = soup.select("div.pagination")[0]

number_of_pages = list(div.children)[-2]  # selects the second to last element in the list
# since \n is the last one.

# last_page = int(number_of_pages.attrs["href"][-3::]) # very clunky, could be done easier
# if the site is changed, really easily broken


while page <= 3:
    url = f"http://milionchvilek.cz/podepsali/{page}"
    req = requests.get(url)
    print(req.url)

    page += 1
