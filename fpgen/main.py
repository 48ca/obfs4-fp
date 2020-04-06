#!/usr/bin/env python3
from tbselenium.tbdriver import TorBrowserDriver
import time

from sys import argv, exit

tbpath = "tor-browser_en-US"

if len(argv) == 1:
    website = "about:blank"
else:
    website = argv[1]

driver = TorBrowserDriver(tbpath)
driver.set_page_load_timeout(90)
try:
    driver.load_url(website)
except Exception as e:
    print(e)
    driver.quit()
    exit(1)

time.sleep(1)

driver.quit()
exit(0)
