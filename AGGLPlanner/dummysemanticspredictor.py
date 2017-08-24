from parseAGGL import AGMFileDataParsing


class DummySemanticsPredictor(object):
	def __init__(self, parsed):
		print parsed.agm.types
		print
		# self.all = []
		# for rule in parsed.agm.rules:
			# self.all.append(rule.name)

	def get_distrb(self, init_types, init_binary, init_unary, initModel, targetVariables_types, targetVariables_binary, targetVariables_unary): # returns data size time
		chunkSize = [0.3, 0.7, 0.8, 1.0]
		chunkTime = [10., 0.05, 0.075, 0.05]
		return self.all, [1.0], [1000.]
