from operator import *
import collections, sys

sys.path.append('/opt/robocomp/share')

from AGGL import *
from xmlModelParser import *

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
	ret += indent+"def " + rule.name + "(self, snode):"
	indent += "\t"
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
		ret += indent+"for symbol_"+n+"_name in nodes:"
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
	ret += indent+"ret.append(self."+rule.name+"_trigger(snode, n2id))"
	# Rule ending
	indent = "\n\t\t"
	ret += indent+"return ret"
	ret += indent+""
	ret += indent+""
	ret += "\n"



	indent = "\n\t"
	ret += indent+"# Rule " + rule.name
	ret += indent+"def " + rule.name + "_trigger(self, snode, n2id):"
	indent += "\t"
	ret += indent+"ret = []"

	ret += indent+"smap = copy.deepcopy(n2id)"
	ret += indent+"newNode = WorldStateHistory(snode)"

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
	if True:
		ret += indent+"# Easy score"
		typesDict = dict()
		for n in graph.nodes:
			t = graph.nodes[n].sType
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

	# Generate the loop that checks the actual model
	symbols_in_stack = []
	score = 0
	ret += indent+"# Hard score"
	for n in graph.nodes:
		ret += indent+"# "+n
		ret += indent+"for symbol_"+n+"_name in graph.nodes:"
		indent += "\t"
		ret += indent+"symbol_"+n+" = graph.nodes[symbol_"+n+"_name]"
		ret += indent+"n2id['"+n+"'] = symbol_"+n+"_name"
		ret += indent+"if symbol_"+n+".sType == '"+graph.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		conditions, number = extractNewLinkConditionsFromList(graph.links, n, symbols_in_stack)
		conditions = conditions.replace("snode.graph", "graph")
		ret += conditions
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
		score += 3*(1+number)
		ret += indent + "if "+str(score)+" > score: score = " + str(score)
	ret += indent+"return score, True"
	# Rule ending
	indent = "\n\t"
	ret += indent+"return score+scoreA, False"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	return ret

