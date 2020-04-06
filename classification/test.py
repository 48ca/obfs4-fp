#!/usr/bin/env python3

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import pandas as pd

import pickle

from sys import argv

if len(argv) != 2:
    print("please specify fp")
    exit(1)

name = argv[1]
data = pd.read_csv("fingerprints/{}.csv".format(name))
print(data.sort_values('name'))

X=data.loc[:, data.columns != 'name']
y=data['name']  # Labels

clf = pickle.load(open("auto-good-models/{}-randomforest.sav".format(name), 'rb'))

y_pred=clf.predict(X)

# Model Accuracy, how often is the classifier correct?
acc = 1 - metrics.accuracy_score(y, y_pred)
real = 10/3 * acc
print("Test Accuracy:", 1 - real)
print("Full Accuracy:", 1 - acc)
