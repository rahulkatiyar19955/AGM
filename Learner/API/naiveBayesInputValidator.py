import sys

class naiveBayesInputValidator():

	def __init__(self, target_list, attr_freq):

		if len(target_list) == 0:
			print("Empty Target List Error: Nothing to predict")
			sys.exit(-1)

		if len(target_list) != len(attr_freq):
			print("Error: Attribute Frequency dictionary must be of form:\n\t number of targets (x) number of attributes")
			sys.exit(-1)

		for target1 in target_list:
			
			if len(attr_freq[target1]) == 0:
				print("Error: No Attributes")
				sys.exit(-1)

			for attr in attr_freq:
				if type(attr_freq[target1][attr]) != type(int) or attr_freq[target1][attr] < 0:
					print("Invalid Value Error: Attribute Frequencies take non-negative integer value")


			for target2 in target_list:
				if attr_freq[target1] != attr_freq[target2]:
					print("Attribute Inconsitency Error: Number of attributes must remain consistent across targets")
					sys.exit(-1)


	def checkZeroDivisionError(instance_count, target_count, laplace_constant):
		
		if instance_count == 0:
			print("ZeroDivisionError: Attribute frequency for each attribute is zero for all targets")

		if laplace_constant == 0:
			for target in target_count:
				if target_count[target] == 0:
					print("Warning: One or more target variable are not trained on any instance, setting laplace constant to 1 to avoid ZeroDivisionError")
					return 1

