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
				writeString += ' ' + ass.name
			writeString += '\n'

		print 'B'
		writeString += 'C'
		for r in agm.configurationList:
			writeString += ' '+ r
		writeString += '\n'

		print 'C'
		for i in range(len(agm.table)):
			for j in range(len(agm.table[i])):
				writeString += 'S ' + agm.agentList[j] + ' ' + agm.configurationList[i] + ' ' + agm.table[i][j] + '\n'
		print '------------------------------------------------------------'
		return writeString