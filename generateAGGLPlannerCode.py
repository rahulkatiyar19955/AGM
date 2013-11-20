from AGGL import *
from operator import *
import collections, sys

sys.path.append('/opt/robocomp/share')

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
				ret += ' and [n2id["'+link.a + '"], n2id["'+ link.b + '"], "'+link.linkType+'"] in snode.graph.links'
		elif newSymbol == link.b:
			if link.a in alreadyThere:
				ret += ' and [n2id["'+link.a + '"], n2id["'+ link.b + '"], "'+link.linkType+'"] in snode.graph.links'
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

	# Generate the loop that perform the instantiation
	symbols_in_stack = []
	for n in rule.lhs.nodes:
		ret += indent+"for symbol_"+n+"_name in nodes:"
		indent += "\t"
		ret += indent+"symbol_"+n+" = nodes[symbol_"+n+"_name]"
		ret += indent+"n2id['"+n+"'] = symbol_"+n+"_name"
		ret += indent+"if symbol_"+n+".sType == '"+rule.lhs.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		ret += extractNewLinkConditionsFromList(rule.lhs.links, n, symbols_in_stack)
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
	# Code for rule execution
	ret += indent+"smap = copy.deepcopy(n2id)"
	ret += indent+"newNode = WorldStateHistory(snode)"

	newNodes, deleteNodes, retypeNodes = rule.lhs.getNodeChanges(rule.rhs)
	ret += indent+"# Create nodes"
	for newNode in newNodes:
		ret += indent+"newName = str(getNewIdForSymbol(newNode))"
		ret += indent+"n2id['"+newNode.name+"'] = newName"
		ret += indent+"newNode.graph.nodes[newName] = AGMSymbol(newName, '"+newNode.sType+"')"
	ret += indent+"# Retype nodes"
	for retypeNode in retypeNodes:
		ret += indent+"newNode.graph.[n2id['"+retypeNode.name+"']].sType = '"+rule.rhs.nodes[retypeNode.name].sType + "'"
	ret += indent+"# Remove nodes"
	for deleteNode in deleteNodes:
		ret += indent+"del newNode.graph.nodes[n2id['"+deleteNode.name+"']]"

	newLinks, deleteLinks = rule.lhs.getLinkChanges(rule.rhs)
	ret += indent+"# Remove links"
	deleteLinks_str = ''
	for l in range(len(deleteLinks)):
		if l > 0: deleteLinks_str += ", "
		deleteLinks_str += "['" + deleteLinks[l].a + "', '" + deleteLinks[l].b + "', '" + deleteLinks[l].linkType + "']"
	ret += indent+"newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ "+deleteLinks_str+" ]]"
	ret += indent+"# Create links"
	for newLink in newLinks:
		ret += indent+"l = AGMLink(n2id['"+newLink.a+"'], n2id['"+newLink.b+"'], '"+newLink.linkType+"')"
		ret += indent+"if not l in newNode.graph.links:"
		ret += indent+"\tnewNode.graph.links.append(l)"

	ret += indent+"# Misc stuff"
	ret += indent+"newNode.probability *= 1."
	ret += indent+"newNode.cost += 1"
	ret += indent+"newNode.history += '" + rule.name + "(' + str(smap) + ')  ' "
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




def generateTarget(graph):
	ret = "def CheckTarget(graph):"
	indent = "\n\t"
	# Make a copy of the current graph node list
	ret += indent+"nodes = copy.deepcopy(snode.graph.nodes)"
	ret += indent+"n2id = dict()"
	## Generate Link list
	linkList = []
	for link_i in range(len(rule.lhs.links)):
		link = rule.lhs.links[link_i]
		linkList.append([link.a, link.b, link.linkType])
	linkList = sorted(linkList, key=itemgetter(0, 1, 2))

	# Generate the loop that perform the instantiation
	symbols_in_stack = []
	for n in rule.lhs.nodes:
		ret += indent+"for symbol_"+n+"_name in nodes:"
		indent += "\t"
		ret += indent+"symbol_"+n+" = nodes[symbol_"+n+"_name]"
		ret += indent+"n2id['"+n+"'] = symbol_"+n+"_name"
		ret += indent+"if symbol_"+n+".sType == '"+rule.lhs.nodes[n].sType+"'"
		for other in symbols_in_stack:
			ret += " and symbol_"+n+".name!=symbol_" + other + ".name"
		ret += extractNewLinkConditionsFromList(rule.lhs.links, n, symbols_in_stack)
		ret += ":"
		symbols_in_stack.append(n)
		indent += "\t"
	# Code for rule execution
	ret += indent+"smap = copy.deepcopy(n2id)"
	ret += indent+"newNode = WorldStateHistory(snode)"


	# Rule ending
	indent = "\n\t\t"
	ret += indent+"return ret"
	ret += indent+""
	ret += indent+""
	ret += "\n"
	return ret

