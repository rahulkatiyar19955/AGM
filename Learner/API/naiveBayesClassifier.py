import sys
import pickle

class NaiveBayesClassifier:

	def __init__(attr_freq=None, target_list=None, laplace_constant=0, fileName=None):
		'''
		2D Dictionary refernced by target value, attribute value
		returns number of instance a given attribute value was found given
		the target value while training.
		'''
		self.attr_freq = attr_freq
		# 1D array target variables
		self.target_list = target_list
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



	def loadFromPickle(fileName):
		'''Load pickled data
		For information about variables read class constructor
		The pickled data should return two valie 
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
			self.attr_freq, self.target_list = pickle.load(f)
		except ValueError:
			print("Error: Expected a tuple of form :(<dict>, <list>)")


	def getParams():

		vld = naiveBayesInputValidator(self.target_list, self.attr_freq)


		self.instance_count = 0
		self.target_count = [0 * len(self.target_list)]

		for target in self.target_list:
			for attr in self.attr_freq[target]:
				self.instance_count += self.attr_freq[target][attr]
				self.target_count[target] += self.attr_freq[target][attr]

		self.laplace_constant = vld.checkZeroDivisionError(self.instance_count, self.target_count, self.laplace_constant)
	
	def predict(self, attr_list):
		'''Provides a probability distribution over target values'''

		getParams()
		target_prob = {}
		
		for target in self.target_list:
			
			target_prob[target] = self.target_count[target]/self.instance_count
			
			for attr in self.attr_freq[target]:
				
				prob_term = 1 / (self.target_count[target] + 2 * self.laplace_constant)
				
				if attr in self.attr_freq[target]:
					prob_term *= (self.target_count[target][attr] + self.laplace_constant)
					if attr in attr_list:
						target_prob[target] *= prob_term
					else:
						target_prob[target] *= 1 - prob_term
				else:
					prob_term *= self.laplace_constant
					if attr in attr_list:
						target_prob[target] *= prob_term
					else:
						target_prob[target] *= 1 - prob_term 
		
		return target_prob
