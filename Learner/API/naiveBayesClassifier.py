from __future__ import division
import sys
import pickle
from naiveBayesInputValidator import *

class NaiveBayesClassifier:

	def __init__(self, attr_freq, target_freq, laplace_constant=1, fileName=None):
		'''
		Initializes following variables:

		attr_freq: 2D Dictionary refernced by (target, attribute)
		returns number of instance an (target, attribute) was trained.

		target_freq: 1D Dictionary referenced by (target) returns number of instance
		a given target was trained.

		If you want to pass variable data via a file, pickle it and store.
		Unpickling the file should return a tuple of the form: (attr_freq, target_freq)
		'''

		self.attr_freq = attr_freq
		# 1D array target variables
		self.target_freq = target_freq
		self.laplace_constant = laplace_constant
		
		if self.laplace_constant < 0:
			print("Warning: Laplace Constant cannot be negative, setting it to zero")
			self.laplace_constant = 0

		if fileName != None:
			if attr_freq != None and attr_freq != None:
				print("Warning: file data won't be considered as data is already passed to the constructor")
			elif attr_freq != None or attr_freq != None:
				print("Warning: Since one of the parameter is none, data from file will be considered")
				loadFromPickle(fileName)
			else:
				loadFromPickle(fileName)


	def normalize(self, target_prob, sort=True):
		'''
		This function normalizes the probability distribution over all actions
		'''
		total = 0

		for target in target_prob:
			total += target_prob[target]

		for target in target_prob:
			target_prob[target] = target_prob[target]/total
		
		if sort:
			return sorted(target_prob, key=target_prob.get, reverse=True)
		else:
			return target_prob



	def loadFromPickle(fileName):
		'''
		File should be pickled.
		Loading the unpickled file must return a tuple of the form: (attr_freq, target_freq) 
		For information about attr_freq and target_freq read class constructor
		'''
		try:
			f = open(fileName, "rb")
		except FileNotFoundError:
			print("Error: " + fileName + " not found")
			sys.exit(-1)
		except PermissionError:
			print("File Permission Error: Cannot read " + fileName)
			sys.exit(-1)	
		except IOError:
			print("I/O Error: while reading file " + fileName)
			sys.exit(-1)

		try:
			self.attr_freq, self.target_freq = pickle.load(f)
		except ValueError:
			print("Error: Expected a tuple of form :(<dict>, <list>)")


	def getParams(self):
		'''
		This functions validates certain matrix shape and value requirement.
		Also it sums up and adds total training instance count
		All future manipulations can be done in this function
		'''

		vld = NaiveBayesInputValidator(self.target_freq, self.attr_freq)
		
		self.instance_count = 0
		for target in self.target_freq:
			self.instance_count += self.target_freq[target]
		
		self.laplace_constant = vld.checkZeroDivisionError(self.instance_count, self.target_freq, self.laplace_constant)
	

	def predict(self, attr_list, normFlag=True):
		'''
		Provides a probability distribution over target values
		attr_list is the list of attributes which are hold true in the instance
		To normalize the distribution set normFlag to True
		'''

		self.getParams()
		target_prob = {}

		for target in self.target_freq:
			
			target_prob[target] = self.target_freq[target]/self.instance_count
			
			for attr in self.attr_freq[target]:
				
				prob_term = 1 / (self.target_freq[target] + 2 * self.laplace_constant)
				prob_term *= (self.attr_freq[target][attr] + self.laplace_constant)

				if attr in attr_list:
					target_prob[target] *= prob_term
				else:
					target_prob[target] *= 1 - prob_term

		if normFlag:
			return self.normalize(target_prob)
		else:
			return target_prob
