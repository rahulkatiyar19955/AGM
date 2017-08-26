from __future__ import division
import sys

class NaiveBayesInputValidator():

	def __init__(self, target_freq, attr_freq):

		if len(target_freq) == 0:
			print("Empty Target List Error: Nothing to predict")
			sys.exit(-1)

		if len(target_freq) != len(attr_freq):
			print("Error: Attribute Frequency dictionary must be of form:\n\t number of targets (x) number of attributes")
			sys.exit(-1)

		for target1 in target_freq:
			
			if len(attr_freq[target1]) == 0:
				print("Error: No Attributes")
				sys.exit(-1)

			for attr in attr_freq[target1]:
				if not isinstance(attr_freq[target1][attr], int) or attr_freq[target1][attr] < 0:
					print("Invalid Value Error: Attribute Frequencies take non-negative integer value")


			for target2 in target_freq:
				if list(attr_freq[target1]) != list(attr_freq[target2]):
					print("Attribute Inconsitency Error: Number of attributes must remain consistent across targets")
					sys.exit(-1)


	def checkZeroDivisionError(self, instance_count, target_freq, laplace_constant):
		
		if instance_count == 0:
			print("ZeroDivisionError: Attribute frequency for each attribute is zero for all targets")
			sys.exit(-1)

		if laplace_constant == 0:
			for target in target_freq:
				if target_freq[target] == 0 and laplace_constant == 0:
					print("Warning: One or more target variable are not trained on any instance, setting laplace constant to 1 to avoid ZeroDivisionError")
					return 1

		return laplace_constant

