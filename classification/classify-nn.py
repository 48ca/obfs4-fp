#!/usr/bin/env python3

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
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

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test


# clf=MLPClassifier(hidden_layer_sizes=(5000, 2500, 500, 50), solver='lbfgs')
clf=MLPClassifier(hidden_layer_sizes=(100,), solver='lbfgs')

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,y_train)

y_pred=clf.predict(X_test)
print(y_pred)
print(y_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

filename = 'models/{}-nn.sav'.format(name)
pickle.dump(clf, open(filename, 'wb'))
