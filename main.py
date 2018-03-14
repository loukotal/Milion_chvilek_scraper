import json
import pprint
import re

import bs4
import requests


# count values of the passed in key
def count_values(input_dict, input_key):
    mydict = {}
    for nested_dict in input_dict.values():
        for key, value in nested_dict.items():
            if key == input_key:
                mydict.setdefault(value, 0)
                mydict[value] += 1

    return mydict


# pass in the dict to the count_values func with appropriate key
def count_places(input_dict):
    places = count_values(input_dict, "place")
    return places


# pass in the dict to the count_values func with appropriate key
def count_occ(input_dict):
    occ = count_values(input_dict, "occupation")
    return occ


# MAIN
page = 1
url = f"http://milionchvilek.cz/podepsali/{page}"
req = requests.get(url)

# handle other response than 200
req.raise_for_status()

# initialize BeautifulSoup
soup = bs4.BeautifulSoup(req.text, "lxml")

# get number of pages
div = soup.select("div.pagination")[0]

number_of_pages = list(div.children)[-2]  # selects the second to last element in the list
# since \n is the last one.

last_page = int(number_of_pages.attrs["href"][-3::])  # very clunky, could be done easier
# last_page = 10                                                    # if the site is changed, really easily broken

# select all tr elements
all_tr = soup.select("tr")

data = {}

# enumerate and loop through all tr on a page
while page <= last_page:

    for index, tr in enumerate(all_tr):

        # modify the index for the pages > 1;
        if page != 1:
            index = (index + 1) * page

        # find all td tags in the tr
        tds = tr.find_all("td")

        # setup a temp_dictionary just to add it to data dict.
        temp_dict = {}
        i = 0
        # loop through all td's elements inside of the tr element
        for td in tds:
            # setup None for Anonymous signatures
            if len(tds) < 4:
                temp_dict["name"] = None
                temp_dict["place"] = None
                temp_dict["occupation"] = None

            # setup the dict based on the position of the td inside of the tds list
            if i % len(tds) == 1:
                # delete/substitute the \xa0 element after every first name
                text = re.sub("\xa0", " ", td.text)
                temp_dict["name"] = text
            elif i % len(tds) == 2:
                temp_dict["place"] = td.text
            elif i % len(tds) == 3:
                temp_dict["occupation"] = td.text
            i += 1
        data[index] = temp_dict

    page += 1
    url = f"http://milionchvilek.cz/podepsali/{page}"
    req = requests.get(url)

    # parse the current page
    soup = bs4.BeautifulSoup(req.text, "lxml")

    # select all tr elements
    all_tr = soup.select("tr")

    print(req.url)

print(pprint.pformat(data))

# use of functions for further analysis (might get moved to a different file,
# which will be used only for the analysis)
# pprint.pprint(count_places(data))
# pprint.pprint(count_occ(data))

# save data to a .json file
with open("data.json", "w") as fp:
    json.dump(data, fp, indent=4, separators=(",", ":"))
