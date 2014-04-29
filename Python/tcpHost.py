from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import sklearn.externals.joblib as joblib
import numpy as np
 
class IphoneChat(Protocol):
    # connection handler

    gestureDict = {0: '', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 
                   5: 'E', 6: 'F', 7: 'G', 8: 'H', 9:'I', 
                   10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 
                   15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 
                   20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 
                   25: 'Y', 26: 'Z'}

    maxVals = [763, 350, 809, 680, 733]
    minVals = [305, 385, 390, 391, 322]

    def __init__(self):
        # load the classifier
        self.clf = joblib.load('Classifiers/signspeech_svm.pkl')

    def connectionMade(self):
        self.factory.clients.append(self)
        print "connected"

    # lost connection handler
    def connectionLost(self, reason):
        print "connection lost"
        self.factory.clients.remove(self)

    # receive data handler
    def dataReceived(self, data):
        print "received data: ", data       
        # convert data into np array
        dataArrStr = data.split(' ')
        dataArr = [] # declare array

        # convert and append
        for i in range(0, len(dataArrStr)):
            dataArr.append(int(dataArrStr[i]))

        # convert to numpy array
        npDataArr = np.array(dataArr)

        # need to convert raw data into range(0, 100)
        # for i in range(0, 5):
        #    npDataArr[i] = self.convert(npDataArr[i], i)

        # catch errors
        try:
            # predict
            guess = self.clf.predict(npDataArr)
            # map to string using dictionary
            letter = self.gestureDict[guess[0]]

            # echo back data to the iphone
            for c in self.factory.clients:
                c.message(letter)

        except ValueError:
            print "Data received has incorrect number of values"

    def convert(self, val, dataNum):
        newVal = ((100-0)*(val-self.minVals[dataNum]))/(self.maxVals[dataNum]-self.minVals[dataNum]) + 0 
        if newVal > 100:
            newVal = 100
        if newVal < 0:
            newVal = 0
        return newVal 
        
    def message(self, message):
        self.transport.write(message)
 
factory = Factory()
factory.protocol = IphoneChat
factory.clients = []
reactor.listenTCP(80, factory)
print "Iphone Chat server started"
reactor.run()