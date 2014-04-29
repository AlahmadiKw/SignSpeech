import json
import numpy as np
import scipy
import setuptools
import matplotlib
import sklearn.datasets as datasets
import sklearn.svm as svm
import pickle
from library import trainingSet

testSet = trainingSet('Data/test1.bin')

clf = pickle.load(model1)

print(clf2.predict(np.array([73, 20, 14, 13, 7, 100, 0, 0, 0]))) # A
print(clf2.predict(np.array([17, 72, 96, 96, 97, 0, 0, 0, 0]))) # B

#for data in testSet.data:




