import numpy as np
import json

class trainingSet(object):
	data = np.array([])
	target = np.array([])
	def __init__(self, filename):
		f = open(filename, 'r')
		file_data = json.load(f)
		f.close()
		np_data = np.array(file_data)
		self.data = np_data[:, 0:9]
		self.target = np_data[:, 9]
		# multiple touch sensor values by 100
		self.data[:, 5:9] = self.data[:, 5:9]*100

	def getData(self):
		return self.data

	def getTarget(self):
		return self.target

