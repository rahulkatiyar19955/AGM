import itertools

AGMStackLastUsedName = 'stackAGMInternal'

#
# AGM to PDDL
#
class AGMPDDL:
	@staticmethod
	def toPDDL(agm, name):
		writeString  = '(define (domain '+name+')\n\n'
		writeString += '\t(:predicates\n'
		writeString += '\t\t(firstunknown ?u)\n'
		writeString += '\t\t(unknownorder ?ua ?ub)\n\n'
		writeString += AGMPDDL.typePredicatesPDDL(agm)
		writeString += AGMPDDL.linkPredicatesPDDL(agm)
		writeString += '\t)\n\n'
		writeString += '\t(:functions\n\t\t(total-cost)\n\t)\n\n'
		for r in agm.rules:
			writeString += AGMRulePDDL.toPDDL(r) + '\n'
		writeString += ')\n'
		return writeString
	@staticmethod
	def typePredicatesPDDL(agm):
		writeString = ''
		typeSet = set()
		for r in agm.rules:
			typeSet = typeSet.union(r.nodeTypes())
		for t in typeSet:
			writeString += '\t\t(IS'+t+' ?n)\n'
		return writeString
	@staticmethod
	def linkPredicatesPDDL(agm):
		writeString = ''
		linkSet = set()
		for r in agm.rules:
			linkSet = linkSet.union(r.linkTypes())
		writeString += '\n'
		for t in linkSet:
			writeString += '\t\t('+t+' ?u)\n'
		return writeString
	@staticmethod
	def typePredicatesPDDL(agm):
		writeString = ''
		typeSet = set()
		for r in agm.rules:
			typeSet = typeSet.union(r.nodeTypes())
		for t in typeSet:
			writeString += '\t\t(IS'+t+' ?n)\n'
		return writeString

#
# AGM rule to PDDL
#
class AGMRulePDDL:
	@staticmethod
	def computePDDLMemoryStackAndDictionary(rule, newList, forgetList):
		stack = [AGMStackLastUsedName]
		reused = []
		stackSize = max(len(forgetList), len(newList))
		for n in range(stackSize):
			stack.append('stack'+str(n))
		print 'Stack', stackSize, stack
		nodeDict = dict()
		for i in range(len(forgetList)):
			nodeDict[forgetList[i]] = stack[-1-i]
		for i in range(len(newList)):
			nodeDict[newList[i]] = stack[-1-i]
		for n in rule.stayingNodeList():
			nodeDict[n] = n
		print 'C', stack
		print 'Quitar', len(forgetList)
		for i in range(len(forgetList)):
			reused.append(stack.pop())
		print 'C', stack

		return stack, reused, nodeDict
	@staticmethod
	def toPDDL(rule, pddlVerbose=False):
		print '-----------------------------'
		print rule.name
		newList = rule.newNodesList()
		print 'New:   ', newList
		forgetList = rule.forgetNodesList()
		print 'Forget:', forgetList
		stack, reused, nodeDict = AGMRulePDDL.computePDDLMemoryStackAndDictionary(rule, newList, forgetList)
		print 'Stack:    ', stack
		print 'Reused:    ', stack
		print 'Node dict:', nodeDict

		if pddlVerbose: print '--((', rule.name, '))--'
		string  = '\t(:action ' + rule.name + '\n'
		string += '\t\t:parameters ('
		for n in rule.stayingNodeList()+stack+reused:
			string += ' ?' + n
		string += ' )\n'
		string += '\t\t:precondition (and'
		string += AGMRulePDDL.existingNodesPDDLTypes(rule, nodeDict) # TYPE preconditions
		string += AGMRulePDDL.stackPDDLPreconditions(rule, stack, forgetList, newList, nodeDict) # Include precondition for nodes to be created
		string += AGMRulePDDL.differentNodesPDDLPreconditions(rule, nodeDict) # Avoid using the same node more than once "!="
		string += ' )\n'


		string += '\t\t:effect (and'
		string += AGMRulePDDL.typeChangesPDDLEffects(rule, nodeDict) # TYPE changes for staying nodes
		string += AGMRulePDDL.stackHandlingPDDLEffects(rule, forgetList, stack, nodeDict) # Stack handling
		string += AGMRulePDDL.newAndForgetNodesTypesPDDLEffects(rule, newList, forgetList, nodeDict) # TYPE assignment for created nod
		string += AGMRulePDDL.linkPatternsPDDLEffects(rule, nodeDict)
		string += ' (increase (total-cost) 1) )\n'
		string += '\t)\n'
		return string

	#
	# P  R  E  C  O  N  D  I  T  I  O  N  S
	#
	@staticmethod
	def existingNodesPDDLTypes(rule, nodeDict, pddlVerbose=False):
		ret  = ''
		for name,node in rule.lhs.nodes.items():
			ret += ' (IS'+node.sType+' ?'+nodeDict[name]+')'
		return ret
	@staticmethod
	def stackPDDLPreconditions(rule, stack, forgetList, newList, nodeDict, pddlVerbose=False):
		ret = ''
		stackCopy = stack[:]
		first = stackCopy.pop()
		print 'Prime', first
		if pddlVerbose: print 'PRECONDITIONS firstunknown in newList', first
		ret += ' (firstunknown' + ' ?' + first + ')'
		last = first
		while len(stackCopy)>0:
			top = stackCopy.pop()
			if pddlVerbose: print 'PRECONDITIONS unknownorder', last, top
			ret += ' (unknownorder ?' + last + ' ?' + top + ')'
			last = top
		return ret
	@staticmethod
	def differentNodesPDDLPreconditions(rule, nodeDict):
		ret = ''
		for i in itertools.combinations(rule.nodeNames(), 2):
			ret += ' (not(= ?' + nodeDict[i[0]] + ' ?' + nodeDict[i[1]] + '))'
		return ret

	#
	# E  F  F  E  C  T  S
	#
	@staticmethod
	def stackHandlingPDDLEffects(rule, forgetList, stack_, nodeDict, pddlVerbose=False):
		ret = ''
		stack = stack_[:]
		last = ''
		if len(stack)>1:
			last = stack.pop()
			ret += ' (not (firstunknown ?' + last + '))'
		while len(stack)>0:
			nextn = stack.pop()
			ret += ' (not (unknownorder ?' + last + ' ?' + nextn + '))'
			last = nextn
		ret += ' (firstunknown ?' + last + ')'
		return ret
	@staticmethod
	def newAndForgetNodesTypesPDDLEffects(rule, newList, forgetList, nodeDict, pddlVerbose=False):
		ret = ''
		# Handle new nodes
		for node in newList:
			ret += ' (IS' + rule.rhs.nodes[node].sType + ' ?' + nodeDict[node] + ')'
		# Handle forget nodes
		for node in forgetList:
			ret += ' (not (IS' + rule.lhs.nodes[node].sType + ' ?' + nodeDict[node] + '))'
		return ret
	@staticmethod
	def linkPatternsPDDLEffects(rule, nodeDict, pddlVerbose=False):
		ret = ''
		initialLinkSet   = set(rule.lhs.links)
		posteriorLinkSet = set(rule.rhs.links)
		createLinks =  posteriorLinkSet.difference(initialLinkSet)
		for link in createLinks:
			if pddlVerbose: print 'NEWLINK', str(link)
			ret += ' ('+link.linkType + ' ?'+ nodeDict[link.a] +' ?'+ nodeDict[link.b] + ')'
		deleteLinks =  initialLinkSet.difference(posteriorLinkSet)
		for link in deleteLinks:
			if pddlVerbose: print 'REMOVELINK', str(link)
			ret += ' (not ('+link.linkType + ' ?'+ nodeDict[link.a] +' ?'+ nodeDict[link.b] + '))'
		return ret
	@staticmethod
	def typeChangesPDDLEffects(rule, nodeDict, pddlVerbose=False):
		ret = ''
		stay = rule.stayingNodeList()
		for n in stay:
			typeL = rule.lhs.nodes[n].sType
			typeR = rule.rhs.nodes[n].sType
			if typeL != typeR:
				if pddlVerbose: print 'EFFECTS modify', n
				ret += ' (not(IS'+typeL + ' ?' + nodeDict[n] +')) (IS'+typeR + ' ?' + nodeDict[n] +')'
		return ret

