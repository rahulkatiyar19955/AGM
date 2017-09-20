import copy
import pickle
import numpy as np

from parseAGGL import AGMFileDataParsing

from genericprediction import *


class LinearRegressionPredictor3(object):
	def __init__(self, pickleFile):
		try:
			f = open(pickleFile, 'r')
		except IOError:
			print 'agglplanner error: Could not open', pickleFile
		# print str.split(' ', 1 )
		self.coeff, self.intercept, self.xHeaders, self.yHeaders = pickle.load(f)
		self.coeff = np.array(self.coeff)
		self.intercept = np.array(self.intercept)
		print '--------------------------------------------------------------------'
		self.prdDictionary = setInverseDictionaryFromList(self.xHeaders)
		self.actDictionary = setInverseDictionaryFromList(self.yHeaders)


	def get_distrb(self, init_types, init_binary, init_unary, initModel, targetVariables_types, targetVariables_binary, targetVariables_unary, target): # returns data size time
		inputv = inputVectorFromTargetAndInit(self.domainParsed, self.prdDictionary, self.actDictionary, target, initModel)
		print inputv.shape, '*', self.coeff.shape, '+', self.intercept.shape
		outputv = np.dot(inputv, self.coeff)+self.intercept

		result = copy.deepcopy(self.actDictionary)
		for key in self.actDictionary:
			value = self.actDictionary[key]
			result[key] = outputv[0][value]

		from operator import itemgetter
		kk = sorted([ [x, result[x] ] for x in result ], reverse=True, key=itemgetter(1))
		indexes = []
		thresholds = [0.5, 0.1, 0.0]
		for idx, action in enumerate(sorted([ [x, result[x] ] for x in result ], reverse=True, key=itemgetter(1))):
			#print idx, type(idx), action, type(action)
			if action[1] < thresholds[0]:
				if idx != 0:
					indexes.append(idx)
				thresholds = thresholds[1:]
				if len(thresholds) == 0:
					break
		#print 'indexes', indexes
		chunkSize = []
		for idx in reversed(indexes):
			#print 'idx', idx
			if len(chunkSize) > 0:
				#print 'hay cosas ya', chunkSize[-1], idx
				if abs(chunkSize[-1]-idx)>1:
					#print 'condicion'
					chunkSize.append(idx)
			else:
				#print 'no habia nada'
				chunkSize.append(idx)

		chunkSize = [ float(x)/(len(self.actDictionary)-1) for x in reversed(chunkSize)]
		if chunkSize[-1] < 0.999999:
			chunkSize.append(1)

		chunkTime = []
		timeSplitter = 10.
		for x in chunkSize:
			chunkTime.append(timeSplitter)
			timeSplitter *= 0.05
		print chunkSize
		return result, chunkSize, chunkTime

#
