import itertools

AGMStackLastUsedName = 'stackAGMInternal'

def translateList(alist, dictionary):
	return [dictionary[x] for x in alist]

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
			writeString += '\t\t('+t+' ?u ?v)\n'
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
		#print 'Stack', stackSize, stack
		nodeDict = dict()
		for i in range(len(forgetList)):
			nodeDict[forgetList[i]] = stack[-1-i]
		for i in range(len(newList)):
			nodeDict[newList[i]] = stack[-1-i]
		for n in rule.stayingNodeList():
			nodeDict[n] = n
		for i in range(len(forgetList)):
			reused.append(stack.pop())

		return stack, reused, nodeDict
	@staticmethod
	def toPDDL(rule, pddlVerbose=False):
		#print '-----------------------------'
		#print rule.name
		newList = rule.newNodesList()
		#print 'New:   ', newList
		forgetList = rule.forgetNodesList()
		#print 'Forget:', forgetList
		stack, reused, nodeDict = AGMRulePDDL.computePDDLMemoryStackAndDictionary(rule, newList, forgetList)
		#print 'Stack:    ', stack
		#print 'Reused:    ', stack
		#print 'Node dict:', nodeDict

		#if pddlVerbose: print '--((', rule.name, '))--'
		string  = '\t(:action ' + rule.name + '\n'
		string += '\t\t:parameters ('
		for n in rule.stayingNodeList()+stack+reused:
			string += ' ?' + n
		string += ' )\n'
		string += '\t\t:precondition (and'
		string += AGMRulePDDL.existingNodesPDDLTypes(rule, nodeDict) # TYPE preconditions
		string += AGMRulePDDL.stackPDDLPreconditions(rule, stack, forgetList, newList, nodeDict) # Include precondition for nodes to be created
		string += AGMRulePDDL.differentNodesPDDLPreconditions(rule.stayingNodeList()+reused) # Avoid using the same node more than once "!=". NOT INCLUDING THOSE IN THE STACK
		string += AGMRulePDDL.linkPatternsPDDLPreconditions(rule, nodeDict)
		string += ' )\n'


		string += '\t\t:effect (and'
		string += AGMRulePDDL.typeChangesPDDLEffects(rule, nodeDict) # TYPE changes for staying nodes
		string += AGMRulePDDL.stackHandlingPDDLEffects(rule, forgetList, newList, stack, reused, nodeDict) # Stack handling
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
		#print 'Prime', first
		#if pddlVerbose: print 'PRECONDITIONS firstunknown in newList', first
		ret += ' (firstunknown' + ' ?' + first + ')'
		last = first
		while len(stackCopy)>0:
			top = stackCopy.pop()
			#if pddlVerbose: print 'PRECONDITIONS unknownorder', last, top
			ret += ' (unknownorder ?' + last + ' ?' + top + ')'
			last = top
		return ret
	@staticmethod
	def differentNodesPDDLPreconditions(nodesToUse):
		ret = ''
		for i in itertools.combinations(nodesToUse, 2):
			if i[0] != i[1]:
				ret += ' (not(= ?' + i[0] + ' ?' + i[1] + '))'
		return ret

	#
	# E  F  F  E  C  T  S
	#
	@staticmethod
	def stackHandlingPDDLEffects(rule, forgetList_, newList_, stack_, reused, nodeDict, pddlVerbose=False):
		ret = ''
		stack = stack_[:]
		forgetList = translateList(forgetList_, nodeDict)
		newList = translateList(newList_, nodeDict)
		last = ''
		#print '------------------------------------------------------------------------'
		#print 'Forget list', forgetList
		#print 'New list   ', newList
		#print 'Stack      ', stack
		#print 'Reused     ', reused
		#print '--- ignoring reused...  ---'
		forgetList2 = [x for x in forgetList if not x in newList]
		#print 'Forget list 2', forgetList2
		newList2 = [x for x in newList if not x in forgetList]
		#print 'New list 2   ', newList2
		#print '------------------------------------------------------------------------'
		# Same old, same old
		if len(forgetList2)==0 and len(newList2)==0:
			pass
		# NEW NODES: we must pop some symbols from the stack
		elif len(forgetList2)==0 and len(newList2)>0:
			if len(stack)>1:
				last = stack.pop()
				ret += ' (not (firstunknown ?' + last + '))'
			else:
				raise Exception(":->")
			while len(stack)>0:
				nextn = stack.pop()
				ret += ' (not (unknownorder ?' + last + ' ?' + nextn + '))'
				last = nextn
			ret += ' (firstunknown ?' + last + ')'
		# FORGET NODES: we must push some symbols from the stack
		elif len(forgetList2)>0 and len(newList2)==0:
			last = forgetList2.pop()
			ret += ' (firstunknown ?' + last + ')'
			while len(forgetList2)>0:
				nextn = forgetList2.pop()
				ret += ' (unknownorder ?' + last + ' ?' + nextn + ')'
				last = nextn
			ret += ' (unknownorder ?' + last + ' ?' + stack[-1] + ')'
			ret += ' (not (firstunknown ?' + stack[-1] + '))'
			
		# Internal error :-D
		else:
			raise Exception(":-)")
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
		# Substitute links names in a copy of the links
		Llinks = rule.lhs.links[:]
		initialLinkSet = set()
		for link in Llinks:
			link.a = nodeDict[link.a]
			link.b = nodeDict[link.b]
			initialLinkSet.add(link)
		Rlinks = rule.rhs.links[:]
		posteriorLinkSet = set()
		for link in Rlinks:
			link.a = nodeDict[link.a]
			link.b = nodeDict[link.b]
			posteriorLinkSet.add(link)
		#print 'L', initialLinkSet
		#print 'R', posteriorLinkSet
		createLinks =  posteriorLinkSet.difference(initialLinkSet)
		#print 'create', createLinks
		for link in createLinks:
			#print 'NEWLINK', str(link)
			ret += ' ('+link.linkType + ' ?'+ link.a +' ?'+ link.b + ')'
		deleteLinks = initialLinkSet.difference(posteriorLinkSet)
		#print 'delete', deleteLinks
		for link in deleteLinks:
			#print 'REMOVELINK', str(link)
			ret += ' (not ('+link.linkType + ' ?'+ link.a +' ?'+ link.b + '))'
		return ret
	@staticmethod
	def linkPatternsPDDLPreconditions(rule, nodeDict, pddlVerbose=False):
		ret = ''
		for link in rule.lhs.links:
			#if pddlVerbose: print 'LINK', str(link)
			ret += ' ('+link.linkType + ' ?'+ nodeDict[link.a] +' ?'+ nodeDict[link.b] + ')'
		return ret
	@staticmethod
	def typeChangesPDDLEffects(rule, nodeDict, pddlVerbose=False):
		ret = ''
		stay = rule.stayingNodeList()
		for n in stay:
			typeL = rule.lhs.nodes[n].sType
			typeR = rule.rhs.nodes[n].sType
			if typeL != typeR:
				#if pddlVerbose: print 'EFFECTS modify', n
				ret += ' (not(IS'+typeL + ' ?' + nodeDict[n] +')) (IS'+typeR + ' ?' + nodeDict[n] +')'
		return ret

