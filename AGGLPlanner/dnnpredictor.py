import copy
import pickle, tempfile
import numpy as np

from parseAGGL import AGMFileDataParsing
from zipfile import ZipFile

from genericprediction import *

try:
	import keras.models
	from keras.models import Sequential
	from keras.layers import Dense
except:
	pass


def zipFiles(files_paths, output_path):
	print 'output_path', output_path
	with ZipFile(output_path, 'w') as zip_out:
		for f in files_paths:
			print f
			print zip_out.write(f)


def getModel(input_path):
	zip_base = tempfile.mkdtemp(prefix='agmDNN')
	print 'zip_base', zip_base
	with ZipFile(input_path, 'r') as zip:
		zip.extractall(zip_base)
	return zip_base+'/model.h5', zip_base+'/xHeaders.pckl', zip_base+'/yHeaders.pckl'



def generateDNNMatricesFromDomainAndPlansDirectory(domain, data, outX, outY):
	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Reading domain'
	domainAGM = AGMFileDataParsing.fromFile(domain)

	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generating prdsHeader'
	prdDictionary = getPredicateDictionary(domainAGM)
	prdsHeader=range(len(prdDictionary))
	for x in prdDictionary:
		prdsHeader[prdDictionary[x]] = x
	print prdsHeader


	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generating actsHeader'
	actDictionary = getActionDictionary(domainAGM)
	actsHeader=range(len(actDictionary))
	for x in actDictionary:
		actsHeader[actDictionary[x]] = x
	print actsHeader


	print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Gathering data from stored files'
	lim = -1
	n = 0
	for (dirpath, dirnames, filenames) in os.walk(data):
		for x in filenames:
			target = dirpath  +   '/'   + x
			plan   = target   + '.plan'
			if x.endswith('.aggt'):
				if os.path.exists(plan) and os.path.exists(target) and os.path.getsize(plan)>15:
					planLines = [x.strip().strip('*') for x in open(plan, 'r').readlines() if (not x.startswith('#')) and len(x) > 3 ]
					try:
						yi = outputVectorFromPlan(planLines, actDictionary)
					except KeyError:
						print 'Non existent action in', plan
						continue
					try:
						data_y = np.concatenate( (data_y, yi), axis=0)
					except NameError:
						data_y = yi # traceback.print_exc()
					xi = np.zeros( (1, 2*len(prdDictionary)) )
					initWorld = plan.split('/')[:-1]
					initWorld.append(initWorld[-1]+'.xml')
					initWorld = '/'.join(initWorld)
					# print initWorld
					# sys.exit(-1)
					xi = inputVectorFromTargetAndInit(domainAGM, prdDictionary, actDictionary, target, initWorld)
					try:
						try:
							data_x = np.concatenate( (data_x, xi), axis=0)
						except NameError:
							data_x = xi # traceback.print_exc()
						n += 1
						if n%100 == 0:
							print n, 'generateLinearRegressionMatricesFromDomainAndPlansDirectory2'
						if n == lim:
							print 'wiiiiiiiiiii'
							break
					except KeyError:
						print 'KeyError _ ', plan
						traceback.print_exc()
			if n == lim:
				break
		if n == lim:
			break

	print 'x', np.sum(data_x)
	print data_x.shape
	# print data_x

	print 'y', np.sum(data_y)
	print data_y.shape
	# print data_y


	with open(outY, 'wb') as f:
		f.write(';'.join(actsHeader)+'\n')
		np.savetxt(f, data_y, delimiter=";")

	with open(outX, 'wb') as f:
		f.write(';'.join(prdsHeader)+'\n')
		np.savetxt(f, data_x, delimiter=";")










class DNNPredictor(object):
	def __init__(self, inputFile):
		try:
			model_path, xHeaders_path, yHeaders_path = getModel(inputFile)
			self.model = keras.models.load_model(model_path)
			self.xHeaders = pickle.load(xHeaders_path, 'r')
			self.yHeaders = pickle.load(yHeaders_path, 'r')
		except IOError:
			print 'agglplanner error: Could not open', pickleFile
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		print self.xHeaders
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		print '--------------------------------------------------------------------'
		self.prdDictionary = setInverseDictionaryFromList(self.xHeaders)
		self.actDictionary = setInverseDictionaryFromList(self.yHeaders)


	def get_distrb(self, init_types, init_binary, init_unary, initModel, targetVariables_types, targetVariables_binary, targetVariables_unary): # returns data size time
		# yr2 = np.dot(values, self.coeff)+self.intercept
		#inputv = inputVectorFromTarget(self.domainParsed, self.prdDictionary, self.actDictionary, "ex.aggt")
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print targetVariables_types
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print targetVariables_unary
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		print targetVariables_binary
		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		inputv = inputVectorFromSets(self.domainParsed, self.prdDictionary, self.actDictionary, init_types, init_binary, init_unary, initModel, targetVariables_types, targetVariables_binary, targetVariables_unary)
		#print 'INPUT V', inputv
		print inputv.shape, '*', self.coeff.shape, '+', self.intercept.shape
		outputv = np.dot(inputv, self.coeff)+self.intercept
		#print '---------------------'
		#print outputv
		#print '<--------------------'

		result = copy.deepcopy(self.actDictionary)
		for key in self.actDictionary:
			value = self.actDictionary[key]
			result[key] = outputv[0][value]
		#print result
		#print '<--------------------'


		from operator import itemgetter
		kk = sorted([ [x, result[x] ] for x in result ], reverse=True, key=itemgetter(1))
		indexes = []
		thresholds = [0.5, 0.125, 0.0]
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
		chunkTime = [ 2 for x in chunkSize ]
		print chunkSize
		return result, chunkSize, chunkTime



#
