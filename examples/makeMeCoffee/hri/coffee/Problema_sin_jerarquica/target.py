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
	totalScore = 2200

	del available['3']
	del available['1']
	del available['2']
	del available['22']
	# Hard score
	scoreNodes = []
	scoreLinks = []
	# 3
	symbol_3 = graph.nodes['3']
	n2id['3'] = '3'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_3.sType == 'object':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# 1
		symbol_1 = graph.nodes['1']
		n2id['1'] = '1'
		linksVal = 0
		if [n2id["1"],n2id["3"],"in"]  in graph.links: linksVal += 100
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_1.sType == 'robot' and symbol_1.name!=symbol_3.name and [n2id["1"],n2id["3"],"in"] in graph.links:
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# 2
			symbol_2 = graph.nodes['2']
			n2id['2'] = '2'
			linksVal = 0
			if [n2id["2"],n2id["3"],"in"]  in graph.links: linksVal += 100
			if [n2id["1"],n2id["2"],"know"]  in graph.links: linksVal += 100
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			if symbol_2.sType == 'object' and symbol_2.name!=symbol_3.name and symbol_2.name!=symbol_1.name and [n2id["2"],n2id["3"],"in"] in graph.links and [n2id["1"],n2id["2"],"know"] in graph.links:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				# 22
				symbol_22 = graph.nodes['22']
				n2id['22'] = '22'
				linksVal = 0
				if [n2id["2"],n2id["22"],"table"]  in graph.links: linksVal += 100
				if [n2id["2"],n2id["22"],"noExplored"]  in graph.links: linksVal += 100
				if [n2id["2"],n2id["22"],"reach"]  in graph.links: linksVal += 100
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_22.sType == 'objectSt' and symbol_22.name!=symbol_3.name and symbol_22.name!=symbol_1.name and symbol_22.name!=symbol_2.name and [n2id["2"],n2id["22"],"table"] in graph.links and [n2id["2"],n2id["22"],"noExplored"] in graph.links and [n2id["2"],n2id["22"],"reach"] in graph.links:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# AA335
					symbol_AA335_name = 'AA335'
					for symbol_AA335_name in available:
						symbol_AA335 = graph.nodes[symbol_AA335_name]
						n2id['AA335'] = symbol_AA335_name
						linksVal = 0
						if [n2id["1"],n2id["AA335"],"know"]  in graph.links: linksVal += 100
						if [n2id["AA335"],n2id["2"],"in"]  in graph.links: linksVal += 100
						if [n2id["AA335"],n2id["3"],"in"]  in graph.links: linksVal += 100
						scoreLinks.append(linksVal)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if symbol_AA335.sType == 'object' and symbol_AA335.name!=symbol_3.name and symbol_AA335.name!=symbol_1.name and symbol_AA335.name!=symbol_2.name and symbol_AA335.name!=symbol_22.name and [n2id["1"],n2id["AA335"],"know"] in graph.links and [n2id["AA335"],n2id["2"],"in"] in graph.links and [n2id["AA335"],n2id["3"],"in"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							# AA334
							symbol_AA334_name = 'AA334'
							for symbol_AA334_name in available:
								symbol_AA334 = graph.nodes[symbol_AA334_name]
								n2id['AA334'] = symbol_AA334_name
								linksVal = 0
								if [n2id["AA335"],n2id["AA334"],"see"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"classified"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"mug"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"reach"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"position"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"reachable"]  in graph.links: linksVal += 100
								if [n2id["AA335"],n2id["AA334"],"hasStatus"]  in graph.links: linksVal += 100
								scoreLinks.append(linksVal)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								if symbol_AA334.sType == 'objectSt' and symbol_AA334.name!=symbol_3.name and symbol_AA334.name!=symbol_1.name and symbol_AA334.name!=symbol_2.name and symbol_AA334.name!=symbol_22.name and symbol_AA334.name!=symbol_AA335.name and [n2id["AA335"],n2id["AA334"],"see"] in graph.links and [n2id["AA335"],n2id["AA334"],"classified"] in graph.links and [n2id["AA335"],n2id["AA334"],"mug"] in graph.links and [n2id["AA335"],n2id["AA334"],"reach"] in graph.links and [n2id["AA335"],n2id["AA334"],"position"] in graph.links and [n2id["AA335"],n2id["AA334"],"reachable"] in graph.links and [n2id["AA335"],n2id["AA334"],"hasStatus"] in graph.links:
									scoreNodes.append(100)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									if maxScore == 2200:
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
			scoreNodes.pop()
		scoreLinks.pop()
		scoreNodes.pop()
	scoreLinks.pop()
	return maxScore, False
