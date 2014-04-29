import json
import numpy as np
import scipy
import setuptools
import matplotlib
import sklearn.datasets as datasets
import sklearn.svm as svm
import pickle
from library import trainingSet


tset = trainingSet('Data/A1.bin')

print tset.data[0]
print tset.data[10]
print tset.data[20]
print tset.data[30]
print tset.data[40]
print tset.data[50]
print tset.target


