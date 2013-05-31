import itertools

#
# AGM to PDDL
#
class AGMBD:
	@staticmethod
	def toAGMBehaviorDescription(agm, name):
		writeString = ''
		print 'A'
		print agm.agentList
		for r in agm.agentList:
			writeString += 'A '+ r
			a = agm.agents[r]
			for ass in a.statesList:
				writeString += ' ' + ass
		
		print 'B'
		writeString += 'C'
		for r in agm.configurationList:
			writeString += ' '+ r
		writeString += '\n'

		print 'C'
		for i in ramge(len(agm.table)):
			for j in ramge(len(agm.table[i])):
				print i, j
		print '------------------------------------------------------------'
		return writeString