from operator import *
import collections, sys

sys.path.append('/opt/robocomp/share')

from AGGL import *
from xmlModelParser import *


debug = True

def constantHeader():
	return """import copy, sys
sys.path.append('/opt/robocomp/share')
from AGGL import *
from agglplanner import *

def getNewIdForSymbol(node):
	m = 1
	for k in node.graph.nodes:
			if int(node.graph.nodes[k].name) >= m:
				m = int(node.graph.nodes[k].name)+1
	return m

lastNodeId = 0

class RuleSet(object):
	def __init__(self):
		object.__init__(self)

"""

def ruleDeclaration(agm):
	ret = """\tdef getRules(self):
		mapping = dict()"""
	for r in agm.rules:
		if not r.passive:
			ret += "\n		mapping['"+ r.name + "'] = self." + r.name
	ret += "\n		return mapping\n\n"
	return ret

def ruleTriggerDeclaration(agm):
	ret = """\tdef getTriggers(self):
		mapping = dict()"""
	for r in agm.rules:
		if not r.passive:
			ret += "\n		mapping['"+ r.name + "'] = self." + r.name + "_trigger"
	ret += "\n		return mapping\n\n"
	return ret


def extractNewLinkConditionsFromList(linkList, newSymbol, alreadyThere):
	ret = ''
	number = 0
	for link in linkList:
		if newSymbol == link.a:
			if link.b in alreadyThere:
				ret += ' and [n2id["'+link.a + '"],n2id["'+ link.b + '"],"'+link.linkType+'"] in snode.graph.links'
				number += 1
		elif newSymbol == link.b:
			if link.a in alreadyThere:
				ret += ' and [n2id["'+link.a + '"],n2id["'+ link.b + '"],"'+link.linkType+'"] in snode.graph.links'
				number += 1
	return ret, number


def ruleImplementation(rule):
	if rule.passive: return ''
	ret = ''
	indent = "\n\t"
	ret += indent+"# Rule " + rule.name

	if type(rule) == AGMRule:
		ret = normalRuleImplementation(rule, ret, indent)
	elif type(rule) == AGMComboRule:
		ret = comboRuleImplementation(rule, ret, indent)
	else:
		print 'Unknown rule type'
		sys.exit(-2346)
	return ret

def comboRuleImplementation(rule, r, indent):
	ret = ''
	ret += indent+"def " + rule.name + "(self, snode, stack=[], equivalences=[]):"
	indent += "\t"
	if debug:
		ret += indent+"print 'min:"+str(rule.mindepth)+" i_am:',snode.depth"
	if rule.mindepth > 0:
		ret += indent+"if snode.depth < "+ str(rule.mindepth) + ":"
		indent += '\t'
		ret += indent + "return []"
		indent = indent[:-1]
	ret += indent+"return self." + rule.name + "_trigger(snode, dict(), stack, equivalences)"
	ret += indent
	ret += "\n"

	indent = "\n\t"
	ret += indent+"# Rule " + rule.name
	ret += indent+"def " + rule.name + "_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True):"
	indent += "\t"
	ret += indent+"aliasDict = dict()"
	ret += indent+"sid = str(len(stack)+"+str(len(rule.atoms))+")"
	#ret += indent+"stack = copy.deepcopy(stack)"
	#ret += indent+"equivalences = copy.deepcopy(equivalences)"
	ret += indent+"for atom in ["
	a_n = 0
	for a in reversed(rule.atoms):
		if a_n == 0:
			ret += "['"+a[0]+"','"+a[1]+"', '"+"#ENDS COMBO:"+rule.name+"_'+sid], "
		else:
			ret += "['"+a[0]+"','"+a[1]+"'], "
		a_n += 1
	ret = ret[:-2]
	ret += ']:'
	indent += "\t"
	ret += indent+'idInStack = len(stack)'
	ret += indent+'if len(atom)<3:'
	ret += indent+'\tstack.append((idInStack, atom[0]))'
	ret += indent+'else:'
	ret += indent+'\tstack.append((idInStack, atom[0], atom[2]))'
	ret += indent+'aliasDict[atom[1]] = idInStack'
	indent = indent[:-1]
	ret += indent+'for equivalence in ' + str(rule.equivalences) + ':'
	indent += "\t"
	ret += indent+'equivList = []'
	ret += indent+'for similar in equivalence:'
	indent += "\t"
	ret += indent+'equivList.append([aliasDict[similar[0]], similar[1]])'
	indent = indent[:-1]
	ret += indent+'equivalences.append([equivList, None])'
	indent = indent[:-1]
	#ret += indent+'print "Current stack:", stack'
	#ret += indent+'print stack[-1]'
	#ret += indent+'print stack[-1][0]'

	ret += indent+"newNode = WorldStateHistory(snode)"
	ret += indent+"global lastNodeId"
	ret += indent+"lastNodeId += 1"
	ret += indent+"newNode.nodeId = lastNodeId"
	ret += indent+"newNode.parentId = snode.nodeId"
	if debug:
		ret += indent+"print ' ------- Created', newNode.nodeId, 'from', newNode.parentId, 'rule', '" + rule.name + "'"
	ret += indent+"newNode.history.append('#STARTS COMBO:"+rule.name+"_' + sid)"
	#ret += indent+"print 'Calling ', stack[-1][1]"
	ret += indent+'ret = self.getRules()[stack[-1][1]](newNode, stack, equivalences)'
	ret += indent+"return ret"

	ret += "\n"
	ret += "\n"
	return r + ret
	

def normalRuleImplementation(rule, ret, indent):
	ret += indent+"def " + rule.name + "(self, snode, stack=[], equivalences=[]):"
	indent += "\t"
	ret += indent + "finishesCombo = False"
	#ret += indent+"print 'min:"+str(rule.mindepth)+" i_am:',snode.depth"
	if rule.mindepth > 0:
		ret += indent+"if snode.depth < "+ str(rule.mindepth) + ":"
		indent += '\t'
		ret += indent + "return []"
		indent = indent[:-1]
	#ret += indent+"stack = copy.deepcopy(stack)"
	#ret += indent+"equivalences = copy.deepcopy(equivalences)"
	ret += indent+"if len(stack) > 0:"
	indent += "\t"
	ret += indent+"pop = stack.pop()"
	ret += indent+"me = pop[0]"
	ret += indent+"print 'COMO?', pop"
	ret += indent+"if len(pop)>2:"
	ret += indent+"\tfinishesCombo = pop[2]"

	if debug:
		ret += indent+"print snode.nodeId, 'from', snode.parentId"
		ret += indent+"print snode.nodeId, 'from', snode.parentId"
		ret += indent+"print snode.nodeId, 'from', snode.parentId"
		ret += indent+"print 'Depth: ', snode.depth"
		ret += indent+"print '"+rule.name+"', me"
		ret += indent+"print '"+rule.name+"', me"
		ret += indent+"print stack"
		ret += indent+"print equivalences"
		ret += indent+"print '"+rule.name+"', me"
		ret += indent+"print '"+rule.name+"', me"
	for n in rule.lhs.nodes:
		ret += indent+"# Find equivalence for "+n
		ret += indent+"symbol_"+n+"_nodes = copy.deepcopy(snode.graph.nodes)"
		ret += indent+"for equiv in equivalences:"
		indent += "\t"
		ret += indent+"if [me, '"+n+"'] in equiv[0]:"
		indent += "\t"
		ret += indent+"if equiv[1] != None:"
		indent += "\t"
		#ret += indent+"print 'got "+n+" from equivalences!!'"
		ret += indent+"symbol_"+n+"_nodes = [equiv[1]]"
		indent = indent[:-3]
	indent = indent[:-1]
	ret += indent+"else:"
	indent += "\t"
	for n in rule.lhs.nodes:
		ret += indent+"symbol_"+n+"_nodes = copy.deepcopy(snode.graph.nodes)"
	indent = indent[:-1]
	ret += indent+"ret = []"
	# Make a copy of the current graph node list
	ret += indent+"nodes = copy.deepcopy(snode.graph.nodes)"
	ret += indent+"n2id = dict()"
	## Generate Link list
	linkList = []
	for link_i in range(len(rule.lhs.links)):
		link = rule.lhs.links[link_i]
		linkList.append([link.a, link.b, link.linkType])
	linkList = sorted(linkList, key=itemgetter(0, 1, 2))
	ret += indent+"links = [ "
	for link_i in range(len(linkList)):
		link = linkList[link_i]
		if link_i > 0:
			ret += ", "
		ret += "['" + link[0] + "', '" + link[1] + "', '" + link[2] + "']"
	ret += " ]"
	# Compute the not-actually-optimal order TODO improve this!
	counter = dict()
	for n in rule.lhs.nodes:
		counter[n] = 0
	for n in rule.lhs.nodes:
		for link in linkList:
			if n == link[0]:
				counter[n] = counter[n] + 2
			if n == link[1]:
				counter[n] = counter[n] + 1
	optimal_node_list_t = []
	for n in counter.keys():
		optimal_node_list_t.append((counter[n], n))
	optimal_node_list_t = sorted(optimal_node_list_t, reverse=True)
	optimal_node_list = []
	for o in optimal_node_list_t:
		optimal_node_list.append(o[1])
	# Generate the loop that perform the instantiation
	symbols_in_stack = []
	for n in optimal_node_list:
		ret += indent+"for symbol_"+n+"_name in symbol_"+n+"_nodes:"
		indent += "\t"
		ret += indent+"symbol_"+n+" = nodes[symbol_"+n+"_name]"
		ret += indent+"n2id['"+n+"'] = symbol_"+n+"_name"
		ret += indent+"if symbol_"+n+".sType == '"+rule.lhs.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		conditions, number = extractNewLinkConditionsFromList(rule.lhs.links, n, symbols_in_stack)
		ret += conditions
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
	# Code to call rule execution
	ret += indent+"# At this point we meet all the conditions."
	ret += indent+"# Insert additional conditions manually here if you want."
	ret += indent+"# (beware that the code could be regenerated and you might lose your changes)."
	#ret += indent+"print 'Running rule "+rule.name+"'"
	ret += indent+"stack2        = copy.deepcopy(stack)"
	ret += indent+"equivalences2 = copy.deepcopy(equivalences)"
	ret += indent+"r1 = self."+rule.name+"_trigger(snode, n2id, stack2, equivalences2)"
	ret += indent+"if finishesCombo:"
	ret += indent+"\tr1.history.append(finishesCombo)"
	ret += indent+"\tprint 'COMBU', finishesCombo"
	ret += indent+"ret.append(r1)"
	ret += indent+"if len(stack2) > 0:"
	indent += "\t"
	#ret += indent+"print '"+rule.name+" with stack'"
	#ret += indent+"equiv_deriv = copy.deepcopy(equivalences)"

	for n in optimal_node_list:
		ret += indent+"# Set symbol for "+n+"..."
		ret += indent+"for equiv in equivalences2:"
		indent += "\t"
		ret += indent+"if [me, '"+n+"'] in equiv[0]:"
		indent += "\t"
		ret += indent+"equiv[1] = symbol_"+n+"_name"
		#ret += indent+"print 'setting equivalence for " + n + "'"
		indent = indent[:-2]

	#ret += indent+"print 'Current stack2:', stack2"
	#ret += indent+"print 'Current equivs2:', equivalences2"
	#ret += indent+"print stack2[-1]"
	#ret += indent+"print stack2[-1][0]"
	ret += indent+"newNode = WorldStateHistory(r1)"
	ret += indent+"global lastNodeId"
	ret += indent+"lastNodeId += 1"
	ret += indent+"newNode.nodeId = lastNodeId"
	ret += indent+"newNode.parentId = snode.nodeId"
	if debug:
		ret += indent+"print ' ------- Created', newNode.nodeId, 'from', newNode.parentId, 'rule', '"+rule.name+"'"
	ret += indent+"ret.extend(self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2))"
	indent = indent[:-2]

	# Rule ending
	indent = "\n\t\t"
	ret += indent+"return ret"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	indent = "\n\t"
	ret += indent+"# Rule " + rule.name
	ret += indent+"def " + rule.name + "_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True):"
	indent += "\t"
	ret += indent+"if not checked:"
	indent += "\t"
	lelele = 0
	symbols_in_stack = []
	for n in optimal_node_list:
		lelele += 1
		ret += indent+"test_symbol_"+n+" = snode.graph.nodes[n2id['"+n+"']]"
		ret += indent+"if not (test_symbol_"+n+".sType == '"+rule.lhs.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and test_symbol_"+n+".name!=test_symbol_" + other + ".name"
		conditions, number = extractNewLinkConditionsFromList(rule.lhs.links, n, symbols_in_stack)
		ret += conditions
		ret += "):"
		symbols_in_stack.append(n)
		indent += "\t"
		ret += indent+"raise WrongRuleExecution('"+rule.name+"_trigger"+str(lelele)+" ')"
		indent = indent[:-1]
	indent = indent[:-1]
	ret += indent+"smap = copy.deepcopy(n2id)"
	ret += indent+"newNode = WorldStateHistory(snode)"
	ret += indent+"global lastNodeId"
	ret += indent+"lastNodeId += 1"
	ret += indent+"newNode.nodeId = lastNodeId"
	ret += indent+"newNode.parentId = snode.nodeId"
	if debug:
		ret += indent+"print ' ------- Created', newNode.nodeId, 'from', newNode.parentId, 'rule', '"+rule.name+"'"
	# Create nodes
	newNodes, deleteNodes, retypeNodes = rule.lhs.getNodeChanges(rule.rhs)
	ret += indent+"# Create nodes"
	for newNode in newNodes:
		ret += indent+"newName = str(getNewIdForSymbol(newNode))"
		ret += indent+"smap['"+newNode.name+"'] = newName"
		ret += indent+"newNode.graph.nodes[newName] = AGMSymbol(newName, '"+newNode.sType+"')"
	ret += indent+"# Retype nodes"
	# Retype nodes
	for retypeNode in retypeNodes:
		ret += indent+"newNode.graph.nodes[n2id['"+retypeNode.name+"']].sType = '"+rule.rhs.nodes[retypeNode.name].sType + "'"
	ret += indent+"# Remove nodes"
	# Remove nodes
	for deleteNode in deleteNodes:
		ret += indent+"del newNode.graph.nodes[smap['"+deleteNode.name+"']]"
	ret += indent+"newNode.graph.removeDanglingEdges()"
	# Remove links
	newLinks, deleteLinks = rule.lhs.getLinkChanges(rule.rhs)
	ret += indent+"# Remove links"
	deleteLinks_str = ''
	for l in range(len(deleteLinks)):
		if l > 0: deleteLinks_str += ", "
		deleteLinks_str += "[smap['" + deleteLinks[l].a + "'], smap['" + deleteLinks[l].b + "'], '" + deleteLinks[l].linkType + "']"
	ret += indent+"newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ "+deleteLinks_str+" ]]"
	# Create links
	ret += indent+"# Create links"
	for newLink in newLinks:
		ret += indent+"l = AGMLink(smap['"+newLink.a+"'], smap['"+newLink.b+"'], '"+newLink.linkType+"')"
		ret += indent+"if not l in newNode.graph.links:"
		ret += indent+"\tnewNode.graph.links.append(l)"
	ret += indent+"# Misc stuff"
	ret += indent+"newNode.probability *= 1."
	ret += indent+"newNode.cost += "+str(rule.cost)
	ret += indent+"newNode.depth += 1"
	ret += indent+"newNode.history.append('" + rule.name + "@' + str(n2id) )"
	ret += indent+"return newNode"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	return ret



def generate(agm, skipPassiveRules):
	text = ''
	text += constantHeader()
	text += ruleDeclaration(agm)
	text += ruleTriggerDeclaration(agm)
	for rule in agm.rules:
		text+= ruleImplementation(rule)
	return text


def generateTarget(graph):
	scorePerContition = 20
	ret = """import copy, sys
sys.path.append('/opt/robocomp/share')\nfrom AGGL import *\nfrom agglplanner import *
def CheckTarget(graph):"""
	indent = "\n\t"
	# Make a copy of the current graph node list
	ret += indent+"n2id = dict()\n"+indent+"score = 0"
	## Generate Link list
	linkList = []
	for link_i in range(len(graph.links)):
		link = graph.links[link_i]
		linkList.append([link.a, link.b, link.linkType])
	linkList = sorted(linkList, key=itemgetter(0, 1, 2))

	ret += indent+"scoreA = 0"
	ret += '\n'
	easy = 1
	if True:
		ret += indent+"# Easy score"
		typesDict = dict()
		for n in graph.nodes:
			t = graph.nodes[n].sType
			easy += 1
			if t in typesDict:
				typesDict[t] += 1
			else:
				typesDict[t] = 1
		ret += indent+"typesDict = dict()"
		for t in typesDict:
			ret += indent+"typesDict['"+t+"'] = "+str(typesDict[t])
		ret += indent+"for n in graph.nodes:"
		ret += indent+"	if graph.nodes[n].sType in typesDict:"
		ret += indent+"		scoreA += 1"
		ret += indent+"		typesDict[graph.nodes[n].sType] -= 1"
		ret += indent+"		if typesDict[graph.nodes[n].sType] == 0:"
		ret += indent+"			del typesDict[graph.nodes[n].sType]"
		ret += '\n'

	conditionsListList = []
	# Generate the loop that checks the actual model
	symbols_in_stack = []
	score = 0
	ret += indent+"# Hard score"
	for n in graph.nodes:
		ret += indent+"# "+n
		if n[0] in "0123456789":
			ret += indent+"symbol_"+n+"_name = '" + n + "'"
		else:
			ret += indent+"for symbol_"+n+"_name in graph.nodes:"
			indent += "\t"
		ret += indent+"symbol_"+n+" = graph.nodes[symbol_"+n+"_name]"
		ret += indent+"n2id['"+n+"'] = symbol_"+n+"_name"
		ret += indent+"if symbol_"+n+".sType == '"+graph.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		conditions, number = extractNewLinkConditionsFromList(graph.links, n, symbols_in_stack)
		conditions = conditions.replace("snode.graph", "graph")
		conditionsListList.append( [conditions, number] )
		#ret += conditions
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
		score += scorePerContition
		ret += indent + "if "+str(score)+" > score: score = " + str(score)

	allConditionsStr = ''
	for c in conditionsListList:
		allConditionsStr += c[0]
	conditionsSeparated = allConditionsStr.split("and ")
	realCond = 0
	for cond in conditionsSeparated:
		if len(cond) > 1:
			realCond += 1
			ret += indent+"if " + cond + ": score += "+str(scorePerContition)+""
	ret += indent+"if score == " + str(score + realCond*scorePerContition) + ":"
	indent +="\t"
	ret += indent+"return score+scoreA, True"
	# Rule ending
	indent = "\n\t"
	ret += indent+"return score+scoreA, False"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	return ret

