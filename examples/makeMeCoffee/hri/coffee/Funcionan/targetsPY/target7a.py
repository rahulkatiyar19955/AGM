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
	totalScore = 900

	del available['1']
	del available['8']
	del available['3']
	del available['7']
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
		# 8
		symbol_8 = graph.nodes['8']
		n2id['8'] = '8'
		linksVal = 0
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_8.sType == 'objectSt' and symbol_8.name!=symbol_1.name:
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# 3
			symbol_3 = graph.nodes['3']
			n2id['3'] = '3'
			linksVal = 0
			if [n2id["1"],n2id["3"],"in"]  in graph.links: linksVal += 100
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			if symbol_3.sType == 'object' and symbol_3.name!=symbol_1.name and symbol_3.name!=symbol_8.name and [n2id["1"],n2id["3"],"in"] in graph.links:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				# 7
				symbol_7 = graph.nodes['7']
				n2id['7'] = '7'
				linksVal = 0
				if [n2id["1"],n2id["7"],"know"]  in graph.links: linksVal += 100
				if [n2id["7"],n2id["3"],"in"]  in graph.links: linksVal += 100
				if [n2id["7"],n2id["8"],"table"]  in graph.links: linksVal += 100
				if [n2id["7"],n2id["8"],"explored"]  in graph.links: linksVal += 100
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_7.sType == 'object' and symbol_7.name!=symbol_1.name and symbol_7.name!=symbol_8.name and symbol_7.name!=symbol_3.name and [n2id["1"],n2id["7"],"know"] in graph.links and [n2id["7"],n2id["3"],"in"] in graph.links and [n2id["7"],n2id["8"],"table"] in graph.links and [n2id["7"],n2id["8"],"explored"] in graph.links:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					if maxScore == 900:
						print 'Correcto: score ='+str(maxScore)
						return maxScore, True
					scoreNodes.pop()
				scoreLinks.pop()
				scoreNodes.pop()
			scoreLinks.pop()
			scoreNodes.pop()
		scoreLinks.pop()
		scoreNodes.pop()
	scoreLinks.pop()
	return maxScore, False
