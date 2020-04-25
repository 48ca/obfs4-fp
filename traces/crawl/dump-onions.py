#!/usr/bin/env python3

import pickle

with open('good-onions.sav', 'rb') as f:
    a = pickle.load(f)
    for o in a:
        i = o.index('/')
        j = o.index('.onion')
        po = o[i+2:j+len('onion')+1]
        print(po)
