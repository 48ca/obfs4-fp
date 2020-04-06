#!/usr/bin/env python3
from tbselenium.tbdriver import TorBrowserDriver
import time

from sys import argv, exit

tbpath = "tor-browser_en-US"

if len(argv) == 1:
    file = "good-onions.txt"
else:
    file = argv[1]

with open(file, "r") as f:
    pages = f.read().split("\n")

driver = TorBrowserDriver(tbpath)
driver.set_page_load_timeout(90)

for page in pages:
    if len(page) == 0:
        continue
    try:
        driver.load_url("http://{}".format(page))
        driver.save_screenshot('shots/{}.png'.format(page))
    except Exception as e:
        print("Failed", page)

driver.quit()
exit(0)
