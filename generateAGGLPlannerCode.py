from AGGL import *

def constantHeader():
	return """import copy
from AGGL import *
from mojonplanner import *


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

def ruleImplementation(rule):
	indent = "\n\t"
	ret = ''
	ret += indent+"# Rule " + rule.name
	ret += indent+"def " + rule.name + "(self, graph):"
	indent += "\t"
	ret += indent+"ret = []"
	ret += indent+"mapping = dict()"
	ret += indent+"symbols = [ "
	for sym_i in range(len(rule.lhs.nodes.keys())):
		sym_k = rule.lhs.nodes.keys()[sym_i]
		sym = rule.lhs.nodes[sym_k]
		if sym_i > 0:
			ret += ", "
		ret += "['" + sym.name + "', '" + sym.sType + "']"
	ret += " ]"
	ret += indent+"links = [ "
	for link_i in range(len(rule.lhs.links)):
		link = rule.lhs.links[link_i]
		if link_i > 0:
			ret += ", "
		ret += "['" + link.a + "', '" + link.linkType + "', '" + link.b + "']"
	ret += " ]"
	ret += indent+"for s in rule.lhs.nodes:"
	indent += "\t"
	ret += indent+"if de de dw:"
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