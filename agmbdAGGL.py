import itertools
import sys

#
# AGM to PDDL
#
class AGMBD:
	@staticmethod
	def toAGMBehaviorDescription(agm, name):
		writeString = ''

		#print 'Agents:', agm.agentList
		for r in agm.agm.agentList:
			writeString += 'A '+ r
			try:
				a = agm.agm.agents[r]
			except KeyError as e:
				print "There's no", r, "agent"
				print "Agents:", agm.agm.agents
				print '-------'
				print e
				sys.exit(1)
			for ass in a.statesList:
				writeString += ' ' + ass.name
			writeString += '\n'

		writeString += 'C'
		for r in agm.agm.configurationList:
			writeString += ' '+ r
		writeString += '\n'
		
		for r in agm.agm.rules:
			writeString += 'R' + ' ' + r.name + ' ' + r.configuration.toString() + '\n' 

		table = agm.listToTable(agm.parsedTable, len(agm.parsedAgents))
		for i in range(len(table)):
			for j in range(len(table[i])):
				writeString += 'S ' + agm.agm.agentList[j] + ' ' + agm.agm.configurationList[i] + ' ' + table[i][j] + '\n'
		return writeString