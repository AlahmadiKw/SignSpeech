import json
import numpy as np
import scipy
import setuptools
import matplotlib
import sklearn.datasets as datasets
import sklearn.cross_validation as cross_validation
import sklearn.svm as svm
import sklearn.externals.joblib as joblib
import pickle
from library import trainingSet

trainingSets = []

# load training data
A_B = trainingSet('Data/A_B.bin')
D_K = trainingSet('Data/D_K.bin')
A1 = trainingSet('Data/A1.bin')
B1 = trainingSet('Data/B1.bin')
B2 = trainingSet('DAta/B2.bin')
B3 = trainingSet('DAta/B3.bin')
C1 = trainingSet('Data/C1.bin')
C2 = trainingSet('Data/C2.bin')
C3 = trainingSet('DAta/C3.bin')
D1 = trainingSet('Data/D1.bin')
E1 = trainingSet('Data/E1.bin')
E2 = trainingSet('Data/E2.bin')
F1 = trainingSet('Data/F1.bin')
G1 = trainingSet('Data/G1.bin')
H1 = trainingSet('Data/H1.bin')
I1 = trainingSet('Data/I1.bin')
I2 = trainingSet('Data/I2.bin')
K1 = trainingSet('Data/K1.bin')
neg1 = trainingSet('Data/negative1.bin')
neg2 = trainingSet('Data/negative2.bin')
neg3 = trainingSet('Data/negative3.bin')

trainingSets.append(A_B)
# trainingSets.append(D_K)
trainingSets.append(A1)
trainingSets.append(B1)
#trainingSets.append(B2) # bad data
trainingSets.append(B3)
trainingSets.append(C1)
#trainingSets.append(C2) # bad data
trainingSets.append(C3)
trainingSets.append(D1)
trainingSets.append(E1)
trainingSets.append(E2)
trainingSets.append(F1)
trainingSets.append(G1)
trainingSets.append(H1)
trainingSets.append(I1)
trainingSets.append(I2)
trainingSets.append(K1)
trainingSets.append(neg1)
trainingSets.append(neg2)
trainingSets.append(neg3)

# initialize
completeData = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])
completeTargets = np.array([0])

# append all data into one array
for tset in trainingSets:
	completeData = np.append(completeData, tset.data, axis = 0)
	completeTargets = np.append(completeTargets, tset.target)

print completeData
print completeTargets

# create a estimator (dumb method)
#clf = svm.SVC(gamma = 0.0006,  C = 40.)

# use cross validation to create an optimal estimator
trainData, testData, trainTarget, testTarget = cross_validation.train_test_split(completeData, completeTargets, test_size=0.4, random_state=0)

clf = svm.SVC(kernel='linear', C=1)

# fit the data
clf.fit(trainData, trainTarget)

print "Cross Validation Score:"
print clf.score(testData, testTarget)

testSet1 = trainingSet('Data/test1.bin')
testSet2 = trainingSet('Data/test2.bin')
testSet3 = trainingSet('Data/test3.bin')
testSet4 = trainingSet('Data/test4.bin')

print "Test Data Scores:"
print clf.score(testSet1.data, testSet1.target)
print clf.score(testSet2.data, testSet2.target)
print clf.score(testSet3.data, testSet3.target)
print clf.score(testSet4.data, testSet4.target)

print "Results:"
for data in testSet4.data:
	print clf.predict(data)

# save classifier
joblib.dump(clf, 'Classifiers/signspeech_svm.pkl') 