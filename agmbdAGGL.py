import itertools

#
# AGM to PDDL
#
class AGMBD:
	@staticmethod
	def toAGMBehaviorDescription(agm, name):
		for r in agm.agents:
			writeString += 'agent '+ r + '\n'
		for r in agm.configurations:
			writeString += 'configuration '+ r + '\n'
		for 
		return writeString
