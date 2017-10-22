import sys
sys.path.append('/usr/local/share/agm/')

import itertools
import re

from AGGL import *
from parseAGGL import *
from xmlModelParser import *
import agglplanner2_utils

global useDiff
useDiff = False

global splitActionModif
#splitActionModif = False
splitActionModif = True

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
		typeStr = ''
		global splitActionModif
		if splitActionModif:
			typeStr = ' - tipo'
			writeString += '\t(:requirements :strips :typing )\n' # :fluents
			writeString += '\t(:types tipo)\n'

		writeString += '\t(:predicates\n'
		global useDiff
		if useDiff:
			writeString += '\t\t(diff ?a ?b'+typeStr+')\n'
		writeString += '\t\t(firstunknown ?u'+typeStr+')\n'
		writeString += '\t\t(unknownorder ?ua ?ub'+typeStr+')\n\n'
		writeString += AGMPDDL.typePredicatesPDDL(agm, typeStr)
		writeString += AGMPDDL.linkPredicatesPDDL(agm, typeStr)
		writeString += '\t)\n\n'
		if not splitActionModif:
			writeString += '\t(:functions\n\t\t(total-cost)\n\t)\n\n'
		for r in agm.rules:
			if hasattr(r, 'newNodesList'):
				writeString += AGMRulePDDL.toPDDL(agm, r, skipPassive=skipPassive) + '\n'
		writeString += ')\n'
		return writeString
	@staticmethod
	def linkPredicatesPDDL(agm, typeStr):
		writeString = ''
		linkSet = set()
		for r in agm.rules:
			if hasattr(r, 'nodeTypes'):
				linkSet = linkSet.union(r.linkTypes())
		writeString += '\n'
		for t in linkSet:
			writeString += '\t\t('+t+' ?u ?v'+typeStr+')\n'
		return writeString
	@staticmethod
	def typePredicatesPDDL(agm, typeStr):
		writeString = ''
		for t in agm.typesDirect:
			writeString += '\t\t(IS'+t+' ?n'+typeStr+')\n'
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
	def toPDDL(agmFD, rule, pddlVerbose=False, skipPassive=False):
		if skipPassive==True and rule.passive == True:
			return ''
		if rule.isHierarchical():
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
		global splitActionModif
		if splitActionModif:
			string += ' - tipo'
		string += ' )\n'
		string += '\t\t:precondition (and'
		string += AGMRulePDDL.existingNodesPDDLTypes(agmFD, rule, nodeDict) # TYPE preconditions
		string += AGMRulePDDL.listPDDLPreconditions(rule, agmlist, forgetList, newList, nodeDict) # Include precondition for nodes to be created
		string += AGMRulePDDL.differentNodesPDDLPreconditions(rule, rule.stayingNodeList()+agmlist+forgetList) # Avoid using the same node more than once "!=". NOT INCLUDING THOSE IN THE LIST
		string += AGMRulePDDL.linkPatternsPDDLPreconditions(rule, nodeDict)
		string += ' )\n'

		string += '\t\t:effect (and'
		string += AGMRulePDDL.typeChangesPDDLEffects(rule, nodeDict) # TYPE changes for staying nodes
		string += AGMRulePDDL.listHandlingPDDLEffects(rule, forgetList, newList, agmlist, nodeDict) # List handling
		string += AGMRulePDDL.newAndForgetNodesTypesPDDLEffects(rule, newList, forgetList, nodeDict) # TYPE assignment for created nod
		string += AGMRulePDDL.linkPatternsPDDLEffects(rule, nodeDict)
		if not splitActionModif:
			string += ' (increase (total-cost) '
			string += rule.cost
			string += ')'
			string += AGMRulePDDL.explicitEffectsPDDLEffects(rule, nodeDict)
		string += '\n\t\t)\n'
		string += '\t)\n'

		return string

	#
	# P  R  E  C  O  N  D  I  T  I  O  N  S
	#
	@staticmethod
	def existingNodesPDDLTypes(agmFD, rule, nodeDict, pddlVerbose=False):
		ret  = ''
		for name,node in rule.lhs.nodes.items():
			if len (agmFD.validTypesForType(node.sType)) > 1:
				ret += ' (or'
			first = True
			for t in agmFD.validTypesForType(node.sType):
				ret += ' (IS'+t+' ?v'+nodeDict[name]+')'
				first = False
			if len (agmFD.validTypesForType(node.sType)) > 1:
				ret += ')'
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
		createLinks =  posteriorLinkSet.difference(initialLinkSet)
		for link in createLinks:
			if link.enabled:
				ret += ' ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + ')'
			else:
				ret += ' (not ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + '))'
		deleteLinks = initialLinkSet.difference(posteriorLinkSet)
		for link in deleteLinks:
			if link.enabled:
				ret += ' (not ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + '))'
			else:
				ret += ' ('+link.linkType + ' ?v'+ link.a +' ?v'+ link.b + ')'
		return ret

	@staticmethod
	def explicitEffectsPDDLEffects(rule, nodeDict, pddlVerbose=False):
		global splitActionModif
		if splitActionModif: typeStr = ' - tipo'
		else: typeStr = ''

		if len(rule.effect) == 0: return ''
		ret = str(rule.effect)
		for i in nodeDict:
			ret = ret.replace(' '+i+' ', ' ?'+i+' ')
			ret = ret.replace(' '+i+')', ' ?'+i+')')
		pattern = "\(forall[\t\n ]+(\w+):(\w+)[\t\n ]+\(when([\t\n ]+)"
		m = re.search(pattern, ret)
		if m:
			symbol_name = m.group(1)
			symbol_type = m.group(2)
			blank_space = m.group(3)
			ret = ret[:m.end(3)] + '(IS' + symbol_type + ' ?v' + symbol_name + ')' + blank_space + ret[m.end(3):]
			ret = ret.replace(symbol_name+':'+symbol_type, '( ?v' + symbol_name + typeStr + ' )')
			ret = ret.replace(' ' + symbol_name, ' ?v' + symbol_name)
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


def generatePDDLProblem(domain, initXMLPath, target, outputPath):
	output = open(outputPath, 'w')

	if type(domain) == AGMFileData:
		domainParsed = domain
	elif type(domain) == str:
		domainParsed = AGMFileDataParsing.fromFile(domain)
	else:
		print 'generatePDDLProblem received a domain which is neither a path or an AGMFileData instance, exiting...'
		sys.exit(-1)
	initModel = graphFromXMLFile(initXMLPath)

	target = AGMFileDataParsing.targetFromFile(target)
	agglplanner2_utils.groundAutoTypesInTarget(target, initXMLPath)

	output.write('(define (problem PROBLEM_NAME)\n\n\t(:domain AGGL)\n\n\t(:requirements :typing :strips :adl)\n\n\t(:objects\n')

	originalObjects = []
	for n in initModel.nodes:
		originalObjects.append(n)
		nn = initModel.nodes[n].sType + '_' + n + ' - tipo'
		output.write('\t\t' + nn + '\n')
	unknowns = 8
	targetObjects = []
	for n in target['graph'].nodes:
		if not n in originalObjects:
			nn = target['graph'].nodes[n].sType + '_' + n + ' - tipo'
			targetObjects.append(nn)
	unknownObjectsVec = []
	for u in xrange(unknowns):
		nn = 'unknown_' + str(u)
		output.write('\t\t' + nn + ' - tipo \n')
		unknownObjectsVec.append(nn)


	output.write('\t)\n\n')


	#
	#  INIT MODEL
	#
	output.write('\t(:init\n')
	# 	//output.write('		(= (total-cost) 0)\n')
	# unknowns
	if unknowns>0:
		output.write('\t\t(firstunknown unknown_0)\n')
	for u in xrange(unknowns):
		output.write('\t\t(unknownorder unknown_' + str(u) + ' unknown_' + str(u+1) + ')\n')
	# Set not='s
	allObjects = originalObjects + unknownObjectsVec # + targetObjects
	useDiff = False
	# useDiff = True
	if useDiff:
		for ind1 in xrange(len(allObjects)):
			for ind2 in xrange(len(allObjects)):
				if (ind1 != ind2):
					output.write('\t\t(diff ' + allObjects[ind1] + ' ' + allObjects[ind2] + ')\n')
	# Known symbols type for the objects in the initial world
	for s in initModel.nodes:
		output.write('\t\t(IS' + initModel.nodes[s].sType + ' ' + initModel.nodes[s].sType + '_' + s + ' )\n')
	# Introduce edges themselves
	for l in initModel.links:
		a = initModel.nodes[l.a].sType + '_' + l.a
		b = initModel.nodes[l.b].sType + '_' + l.b
		output.write('\t\t(' + str(l.linkType) + ' ' + str(a) + ' ' + str(b) + ')\n')
	output.write('\t)\n')

	#
	# T A R G E T    W O R L D
	output.write('\n\t(:goal\n')
	if len(targetObjects) > 0:
		output.write('\t\t(exists (')
		for x in targetObjects:
			output.write(' ?' + x)
		output.write(' )\n')
	output.write('\t\t\t(and\n')
	# Known symbols type for the objects in the target world
	for s in target['graph'].nodes:
		sn = target['graph'].nodes[s].sType + '_' + s
		kStr = ' '
		for i in targetObjects:
			if sn == i:
				kStr = ' ?'
				break
		for t in domainParsed.validTypesForType(target['graph'].nodes[s].sType):
			output.write('\t\t\t\t(IS' + t + kStr + sn + ')\n')
	# Edges
	for e in target['graph'].links:
		a = target['graph'].nodes[e.a].sType + '_' + e.a
		b = target['graph'].nodes[e.b].sType + '_' + e.b
		label = e.linkType
		output.write('\t\t\t\t(' + label)
		kStr = ' '
		if e.a in targetObjects: kStr = ' ?'
		output.write(kStr + a)
		kStr = ' '
		if e.b in targetObjects: kStr = ' ?'
		output.write(kStr + b)
		output.write(')\n')
	output.write('\t\t\t)\n')

	if target['precondition']:
		print type(target['precondition'])
		output.write(str(target['precondition']))

	if len(targetObjects)>0:
		output.write('\t\t)\n')
	output.write('\t)\n')

	# Metric definition
	# output.write('	(:metric minimize (total-cost))\n')
	output.write('\n')
	output.write(')\n')
