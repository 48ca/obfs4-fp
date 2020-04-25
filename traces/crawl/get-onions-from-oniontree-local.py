#!/usr/bin/env python3

import yaml
import pickle

from os import listdir
from os.path import isfile, join

path = "oniontree/unsorted"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

potential_onions = []

for f in onlyfiles:
    with open("oniontree/unsorted/{}".format(f), 'r') as of:
        data = of.read()
    o = yaml.safe_load(data)
    us = o['urls']
    # if len(us) > 5:
    #     print("!!! too many onions for {}".format(o['name']))
    # for u in us:
    #     print(u)
    #     potential_onions.append(u)
    potential_onions.append(us[0])

with open("onions.sav", "wb") as of:
    pickle.dump(potential_onions, of)
