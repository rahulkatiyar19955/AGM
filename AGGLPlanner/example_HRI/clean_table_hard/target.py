import copy, sys
sys.path.append('/opt/robocomp/share')
from AGGL import *
from agglplanner import *
def CheckTarget(graph):
	n2id = dict()

	score = 0
	scoreA = 0

	# Easy score
	typesDict = dict()
	typesDict['status'] = 1
	typesDict['table'] = 1
	typesDict['object'] = 1
	for n in graph.nodes:
		if graph.nodes[n].sType in typesDict:
			scoreA += 1
			typesDict[graph.nodes[n].sType] -= 1
			if typesDict[graph.nodes[n].sType] == 0:
				del typesDict[graph.nodes[n].sType]

	# Hard score
	# 9
	for symbol_9_name in graph.nodes:
		symbol_9 = graph.nodes[symbol_9_name]
		n2id['9'] = symbol_9_name
		if symbol_9.sType == 'status' and symbol_9.name == '9':
			if 3 > score: score = 3
			# 15
			for symbol_15_name in graph.nodes:
				symbol_15 = graph.nodes[symbol_15_name]
				n2id['15'] = symbol_15_name
				if symbol_15.sType == 'table' and symbol_15.name!=symbol_9.name and [n2id["9"],n2id["15"],"link"] in graph.links and [n2id["9"],n2id["15"],"clean"] in graph.links:
					if 12 > score: score = 12
					# 5
					for symbol_5_name in graph.nodes:
						symbol_5 = graph.nodes[symbol_5_name]
						n2id['5'] = symbol_5_name
						if symbol_5.sType == 'object' and symbol_5.name!=symbol_9.name and symbol_5.name!=symbol_15.name and [n2id["5"],n2id["9"],"has"] in graph.links:
							if 18 > score: score = 18
							return score, True
	return score+scoreA, False
	
	
