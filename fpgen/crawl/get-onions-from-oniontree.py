#!/usr/bin/env python3
from tbselenium.tbdriver import TorBrowserDriver
import pickle
from bs4 import BeautifulSoup

tbpath = "tor-browser_en-US"

with open("oniontree-source.html", 'r') as f:
    data = f.read().replace('\n','')

driver = TorBrowserDriver(tbpath)
# driver.load_url(website)


soup = BeautifulSoup(data, 'html.parser')

anchors = soup.find_all('a')
l = map(lambda x : x.get("href"), anchors)

potential_onions = []


for url in l:
    driver.load_url(url)
    e = driver.find_element_by_class_name("urls")
    onions = e.find_elements_by_tag_name("a")
    if len(onions) > 5:
        print("too many onions for {}. skipping".format(url))
    for o in onions:
        print(o.get_attribute('href'))
        potential_onions.append(o.get_attribute('href'))

pickle.save(potential_onions, 'onions.sav')
