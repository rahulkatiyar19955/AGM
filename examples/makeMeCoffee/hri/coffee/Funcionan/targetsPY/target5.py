import copy, sys
sys.path.append('/usr/local/share/agm/')
from AGGL import *
from agglplanner import *

def computeMaxScore(a, b, maxScore):
	s = 0
	for i in a: s+=i
	for i in b: s+=i
	if s > maxScore: return s
	return maxScore

def CheckTarget(graph):

	n2id = dict()                             # diccionario
	available = copy.deepcopy(graph.nodes)    # lista de nodos del grafo inicial.

	maxScore = 0
	totalScore = 400

	del available['1']
	# Hard score
	scoreNodes = []
	scoreLinks = []
	# 1
	symbol_1 = graph.nodes['1']
	n2id['1'] = '1'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_1.sType == 'robot':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# stt1r
		symbol_stt1r_name = 'stt1r'
		for symbol_stt1r_name in available:
			symbol_stt1r = graph.nodes[symbol_stt1r_name]
			n2id['stt1r'] = symbol_stt1r_name
			linksVal = 0
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			if symbol_stt1r.sType == 'objectSt' and symbol_stt1r.name!=symbol_1.name:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				# obj1r
				symbol_obj1r_name = 'obj1r'
				for symbol_obj1r_name in available:
					symbol_obj1r = graph.nodes[symbol_obj1r_name]
					n2id['obj1r'] = symbol_obj1r_name
					linksVal = 0
					if [n2id["obj1r"],n2id["stt1r"],"milkpot"]  in graph.links: linksVal += 100
					scoreLinks.append(linksVal)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					if symbol_obj1r.sType == 'object' and symbol_obj1r.name!=symbol_1.name and symbol_obj1r.name!=symbol_stt1r.name and [n2id["obj1r"],n2id["stt1r"],"milkpot"] in graph.links:
						scoreNodes.append(100)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if maxScore == 400:
							print 'Correcto: score ='+str(maxScore)
							return maxScore, True
						scoreNodes.pop()
					scoreLinks.pop()
				scoreNodes.pop()
			scoreLinks.pop()
		scoreNodes.pop()
	scoreLinks.pop()
	return maxScore, False
