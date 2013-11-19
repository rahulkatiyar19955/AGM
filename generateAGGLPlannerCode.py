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
		ret += "		mapping['rompeLlaveEnMano'] = self.rompeLlaveEnMano"
	ret += "		return mapping"


def generate(agm, skipPassiveRules):
	text = ''
	text += constantHeader()
	text += ruleDeclaration(agm)
	return text