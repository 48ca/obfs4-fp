#!/usr/bin/env python3
from tbselenium.tbdriver import TorBrowserDriver
import time

from sys import argv

tbpath = "tor-browser_en-US"

if len(argv) == 1:
    website = "about:support"
else:
    website = argv[1]

driver = TorBrowserDriver(tbpath)
driver.load_url(website)
