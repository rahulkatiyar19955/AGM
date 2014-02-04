import itertools

global useDiff
useDiff = False
AGMListLastUsedName = 'ListAGMInternal'

def translateList(alist, dictionary):
	return [dictionary[x] for x in alist]

#
# AGM to PDDL
#
class AGMPDDL:
	@staticmethod
	def toPDDL(agm, name, skipPassive):
		writeString  = '(define (domain AGGL)\n\n'
		#writeString += '\t(:requirements :strips :typing :fluents)\n'
		#writeString += '\t(:types unknown)\n'
		writeString += '\t(:predicates\n'
		global useDiff
		if useDiff:
			writeString += '\t\t(diff ?a ?b)\n'
		writeString += '\t\t(firstunknown ?u)\n'
		writeString += '\t\t(unknownorder ?ua ?ub)\n\n'
		writeString += AGMPDDL.typePredicatesPDDL(agm)
		writeString += AGMPDDL.linkPredicatesPDDL(agm)
		writeString += '\t)\n\n'
		writeString += '\t(:functions\n\t\t(total-cost)\n\t)\n\n'
		for r in agm.rules:
			if hasattr(r, 'newNodesList'):
				writeString += AGMRulePDDL.toPDDL(r, skipPassive=skipPassive) + '\n'
		writeString += ')\n'
		return writeString
	@staticmethod
	def linkPredicatesPDDL(agm):
		writeString = ''
		linkSet = set()
		for r in agm.rules:
			if hasattr(r, 'nodeTypes'):
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
			if hasattr(r, 'nodeTypes'):
				typeSet = typeSet.union(r.nodeTypes())
			#else:
				#raise Exception("Combo rule")
		for t in typeSet:
			writeString += '\t\t(IS'+t+' ?n)\n'
		return writeString

#
# AGM rule to PDDL
#
class AGMRulePDDL:
	@staticmethod
	def computePDDLMemoryListAndDictionary(rule, newList, forgetList):
		agmlist = [AGMListLastUsedName]
		listSize = len(newList)
		if listSize==0: agmlist = []
		#listSize = max(len(forgetList), len(newList))
		for n in range(listSize):
			agmlist.append('list'+str(n))
		#print 'list', listSize, agmlist
		nodeDict = dict()
		for i in range(len(forgetList)):
			nodeDict[forgetList[i]] = forgetList[i]
		for i in range(len(newList)):
			nodeDict[newList[i]] = agmlist[-1-i]
		for n in rule.stayingNodeList():
			nodeDict[n] = n

		return agmlist, nodeDict
	@staticmethod
	def toPDDL(rule, pddlVerbose=False, skipPassive=False):
		if skipPassive==True and rule.passive == True:
			return ''
		if pddlVerbose:
			print '\n----------------------------- ----------------------------------------   ', rule.name
			print rule.name
			print 'Staying: ', rule.stayingNodeList()
		newList = rule.newNodesList()
		if pddlVerbose:
			print 'New:   ', newList
		forgetList = rule.forgetNodesList()
		if pddlVerbose:
			print 'Forget:', forgetList
		agmlist, nodeDict = AGMRulePDDL.computePDDLMemoryListAndDictionary(rule, newList, forgetList)
		if pddlVerbose:
			print 'List:    ', agmlist
			print 'Node dict:', nodeDict
		string  = '\t(:action ' + rule.name + '\n'
		string += '\t\t:parameters ('
		for n in rule.stayingNodeList()+agmlist+forgetList:
			string += ' ?v' + n
		string += ' )\n'
		string += '\t\t:precondition (and'
		string += AGMRulePDDL.existingNodesPDDLTypes(rule, nodeDict) # TYPE preconditions
		string += AGMRulePDDL.listPDDLPreconditions(rule, agmlist, forgetList, newList, nodeDict) # Include precondition for nodes to be created
		string += AGMRulePDDL.differentNodesPDDLPreconditions(rule, rule.stayingNodeList()+agmlist+forgetList) # Avoid using the same node more than once "!=". NOT INCLUDING THOSE IN THE LIST
		string += AGMRulePDDL.linkPatternsPDDLPreconditions(rule, nodeDict)
		string += ' )\n'

		string += '\t\t:effect (and'
		string += AGMRulePDDL.typeChangesPDDLEffects(rule, nodeDict) # TYPE changes for staying nodes
		string += AGMRulePDDL.listHandlingPDDLEffects(rule, forgetList, newList, agmlist, nodeDict) # List handling
		string += AGMRulePDDL.newAndForgetNodesTypesPDDLEffects(rule, newList, forgetList, nodeDict) # TYPE assignment for created nod
		string += AGMRulePDDL.linkPatternsPDDLEffects(rule, nodeDict)
		string += ' (increase (total-cost) '
		string += rule.cost
		string += ') )\n'
		string += '\t)\n'
		
		return string

	#
	# P  R  E  C  O  N  D  I  T  I  O  N  S
	#
	@staticmethod
	def existingNodesPDDLTypes(rule, nodeDict, pddlVerbose=False):
		ret  = ''
		for name,node in rule.lhs.nodes.items():
			ret += ' (IS'+node.sType+' ?v'+nodeDict[name]+')'
		return ret
	@staticmethod
	def listPDDLPreconditions(rule, agmlist, forgetList, newList, nodeDict, pddlVerbose=False):
		ret = ''
		listCopy = agmlist[:]
		if len(listCopy) > 0:
			first = listCopy.pop()
			#print 'Prime', first
			#if pddlVerbose: print 'PRECONDITIONS firstunknown in newList', first
			ret += ' (firstunknown' + ' ?v' + first + ')'
			last = first
			while len(listCopy)>0:
				top = listCopy.pop()
				#if pddlVerbose: print 'PRECONDITIONS unknownorder', last, top
				ret += ' (unknownorder ?v' + last + ' ?v' + top + ')'
				last = top
		return ret
	@staticmethod
	def differentNodesPDDLPreconditions(rule, nodesToUse):
		ret = ''
		global useDiff
		for i in itertools.combinations(nodesToUse, 2):
			if i[0] != i[1]:
				avoid = False
				if i[0] in rule.lhs.nodes.keys() and not i[1] in rule.lhs.nodes.keys():
					avoid = True
				if i[1] in rule.lhs.nodes.keys() and not i[0] in rule.lhs.nodes.keys():
					avoid = True
				if i[0] in rule.lhs.nodes.keys() and i[1] in rule.lhs.nodes.keys():
					if rule.lhs.nodes[i[0]].sType != rule.lhs.nodes[i[1]].sType:
						avoid = True
				#if avoid:
					#print 'Avoiding diff ', i[0], i[1]
				if not avoid:
					if useDiff:
						ret += ' (diff ?v' + i[0] + ' ?v' + i[1] + ')'
					else:
						ret += ' (not(= ?v' + i[0] + ' ?v' + i[1] + '))'
		return ret

	#
	# E  F  F  E  C  T  S
	#
	@staticmethod
	def listHandlingPDDLEffects(rule, forgetList_, newList_, agmlist_, nodeDict, pddlVerbose=False):
		ret = ''
		if len(agmlist_) == 0: return ret
		agmlist = agmlist_[:]
		forgetList = translateList(forgetList_, nodeDict)
		newList = translateList(newList_, nodeDict)
		if pddlVerbose:
			print '- listHandlingPDDLEffects ----------------------------------------------'
			print 'Forget list', forgetList
			print 'New list   ', newList
			print 'List      ', agmlist
			print '------------------------------------------------------------------------'
		# Same old, same old
		if len(forgetList)==0 and len(newList)==0:
			return ret

		# NEW NODES: we must pop some symbols from the list
		if len(newList)>0:
			if len(agmlist)>1:
				last = agmlist.pop()
				ret += ' (not (firstunknown ?v' + last + '))'
			else:
				raise Exception(":->")
			while len(agmlist)>0:
				nextn = agmlist.pop()
				ret += ' (not (unknownorder ?v' + last + ' ?v' + nextn + '))'
				last = nextn
			ret += ' (firstunknown ?v' + last + ')'

		# FORGET NODES: we must push some symbols from the list
		elif len(forgetList)>0:
			typeSet = set().union(rule.nodeTypes())
			while len(forgetList)>0:
				nextn = forgetList.pop()
				for tip in typeSet:
					ret += ' (not (IS' + tip + ' ' + nextn + '))'
		# Internal error :-D
		else:
			raise Exception(":-)")
		return ret
	@staticmethod
	def newAndForgetNodesTypesPDDLEffects(rule, newList, forgetList, nodeDict, pddlVerbose=False):
		ret = ''
		# Handle new nodes
		for node in newList:
			ret += ' (IS' + rule.rhs.nodes[node].sType + ' ?v' + nodeDict[node] + ')'
		# Handle forget nodes
		for node in forgetList:
			ret += ' (not (IS' + rule.lhs.nodes[node].sType + ' ?v' + nodeDict[node] + '))'
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
			if link.enabled:
				ret += ' ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + ')'
			else:
				ret += ' (not ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + '))'
		deleteLinks = initialLinkSet.difference(posteriorLinkSet)
		#print 'delete', deleteLinks
		for link in deleteLinks:
			#print 'REMOVELINK', str(link)
			if link.enabled:
				ret += ' (not ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + '))'
			else:
				ret += ' ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + ')'
		return ret
	@staticmethod
	def linkPatternsPDDLPreconditions(rule, nodeDict, pddlVerbose=False):
		ret = ''
		for link in rule.lhs.links:
			#if pddlVerbose: print 'LINK', str(link)
			if link.enabled:
				ret += ' ('+link.linkType + ' ?v'+ nodeDict[link.a] +' ?v'+ nodeDict[link.b] + ')'
			else:
				ret += ' (not ('+link.linkType + ' ?v'+ nodeDict[link.a] +' ?v'+ nodeDict[link.b] + '))'
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
				ret += ' (not(IS'+typeL + ' ?v' + nodeDict[n] +')) (IS'+typeR + ' ?v' + nodeDict[n] +')'
		return ret

