from AGGL import *
from operator import *
import collections

def constantHeader():
	return """import copy
from AGGL import *
from mojonplanner import *

def getNewIdForSymbol(node):
	m = 1
	for k in node.graph.nodes:
			if int(node.graph.nodes[k].name) >= m:
				m = int(node.graph.nodes[k].name)+1
	return m

class RuleSet(object):
	def __init__(self):
		object.__init__(self)
		def getRules(self):
		mapping = dict()

"""

def ruleDeclaration(agm):
	ret = ''
	for r in agm.rules:
		ret += "		mapping['"+ r.name + "'] = self." + r.name + "\n"
	ret += "		return mapping\n"
	return ret


def extractNewLinkConditionsFromList(linkList, newSymbol, alreadyThere):
	ret = ''
	for link in linkList:
		if newSymbol == link.a:
			if link.b in alreadyThere:
				ret += ' and ['+link.a + ', '+ link.b + ', '+ "'"+link.linkType+"'"+'] in links'
		elif newSymbol == link.b:
			if link.a in alreadyThere:
				ret += ' and ['+link.a + ', '+ link.b + ', '+ "'"+link.linkType+"'"+'] in links'
	return ret


def newNodes(rule):
	return [ ['name1', 'type1'], ['name2', 'type2'] ]
def deleteNodes(rule):
	return [ ['ooooh', 'toDelete'] ]
def newLinks(rule):
	return [ ['a', 'b', 'in'], ['anode', 'another', 'near'] ]
def deleteLinks(rule):
	return [ ['a', 'b', 'remove'] ]

def ruleImplementation(rule):
	indent = "\n\t"
	ret = ''
	ret += indent+"# Rule " + rule.name
	ret += indent+"def " + rule.name + "(self, graph):"
	indent += "\t"
	ret += indent+"ret = []"
	# Generate Link list
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


	# Make a copy of the current graph node list
	ret += indent+"nodes = copy.deep_copy(graph.nodes)"

	# Generate the loop that perform the instantiation
	symbols_in_stack = []
	for n in rule.lhs.nodes:
		ret += indent+"for symbol_"+n+"_name in nodes:"
		indent += "\t"
		ret += indent+"symbol_"+n+" = nodes[symbol_"+n+"_name]"
		ret += indent+"if symbol_"+n+".sType == '"+rule.lhs.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		ret += extractNewLinkConditionsFromList(rule.lhs.links, n, symbols_in_stack)
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
	# Code for rule execution
	ret += indent+"newNode = WorldStateHistory(node)"
	ret += indent+"name2id = dict()"
	ret += indent+"# Create nodes"
	for newNode in newNodes(rule):
		ret += indent+"newName = str(getNewIdForSymbol(newNode))"
		ret += indent+"name2id['"+newNode[0]+"'] = newName"
		ret += indent+"newNode.graph.nodes[newName] = AGMSymbol(newName, '"+newNode[1]+"')"
	ret += indent+"# Remove nodes"
	for deleteNode in deleteNodes(rule):
		ret += indent+"delete_node AGMSymbol('"+rule.lhs.nodes[deleteNode[0]].name+"', '"+deleteNode[1]+"')"
	ret += indent+"# Create links"
	for newLink in newLinks(rule):
		ret += indent+"newNode.graph.links.append(AGMLink(name2id['"+newLink[0]+"'], name2id['"+newLink[1]+"'], '"+newLink[2]+"'))"
	ret += indent+"# Remove links"
	for deleteLink in deleteLinks(rule):
		ret += indent+"something that removes AGMLink(name2id['"+deleteLink[0]+"'], name2id['"+deleteLink[1]+"'], '"+deleteLink[2]+"'))"

	ret += indent+"newNode.probability *= 1."
	ret += indent+"newNode.cost += 1"
	ret += indent+"newNode.history += ' "+rule.name+"'"
	ret += indent+"ret.append(newNode)"

	# Rule ending
	indent = "\n\t\t"
	ret += indent+"return ret"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	return ret

def generate(agm, skipPassiveRules):
	text = ''
	text += constantHeader()
	text += ruleDeclaration(agm)
	for rule in agm.rules:
		text+= ruleImplementation(rule)

	return text




