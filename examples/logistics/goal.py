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
	for n in graph.nodes:
		if graph.nodes[n].sType in typesDict:
			scoreA += 1
			typesDict[graph.nodes[n].sType] -= 1
			if typesDict[graph.nodes[n].sType] == 0:
				del typesDict[graph.nodes[n].sType]

	# Hard score
	if score == 0:
		return score+scoreA, True
	return score+scoreA, False
	
	
