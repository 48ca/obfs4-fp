#!/usr/bin/env python3
from tbselenium.tbdriver import TorBrowserDriver
import pickle

tbpath = "tor-browser_en-US"

with open('onions.sav', 'rb') as f:
    potential_onions = pickle.load(f)

print("Loaded {} onions".format(len(potential_onions)))

driver = TorBrowserDriver(tbpath)
driver.set_page_load_timeout(60)

good_onions = []

for onion in potential_onions:
    try:
        driver.load_url(onion)
        good_onions.append(onion)
    except Exception as e:
        print(e)

print("Good onions")
for onion in good_onions:
    print(onion)

with open('good-onions.sav', 'wb') as f:
    pickle.dump(good_onions, f)
