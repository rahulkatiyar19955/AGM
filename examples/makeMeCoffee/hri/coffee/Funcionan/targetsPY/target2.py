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
	totalScore = 1100

	del available['20']
	del available['1']
	# Hard score
	scoreNodes = []
	scoreLinks = []
	# 20
	symbol_20 = graph.nodes['20']
	n2id['20'] = '20'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_20.sType == 'person':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# 1
		symbol_1 = graph.nodes['1']
		n2id['1'] = '1'
		linksVal = 0
		if [n2id["1"],n2id["20"],"interacting"]  in graph.links: linksVal += 100
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_1.sType == 'robot' and symbol_1.name!=symbol_20.name and [n2id["1"],n2id["20"],"interacting"] in graph.links:
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# stt1
			symbol_stt1_name = 'stt1'
			for symbol_stt1_name in available:
				symbol_stt1 = graph.nodes[symbol_stt1_name]
				n2id['stt1'] = symbol_stt1_name
				linksVal = 0
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_stt1.sType == 'objectSt' and symbol_stt1.name!=symbol_20.name and symbol_stt1.name!=symbol_1.name:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# obj1
					symbol_obj1_name = 'obj1'
					for symbol_obj1_name in available:
						symbol_obj1 = graph.nodes[symbol_obj1_name]
						n2id['obj1'] = symbol_obj1_name
						linksVal = 0
						if [n2id["obj1"],n2id["stt1"],"classifailed"]  in graph.links: linksVal += 100
						if [n2id["1"],n2id["obj1"],"know"]  in graph.links: linksVal += 100
						scoreLinks.append(linksVal)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if symbol_obj1.sType == 'object' and symbol_obj1.name!=symbol_20.name and symbol_obj1.name!=symbol_1.name and symbol_obj1.name!=symbol_stt1.name and [n2id["obj1"],n2id["stt1"],"classifailed"] in graph.links and [n2id["1"],n2id["obj1"],"know"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							# stt2
							symbol_stt2_name = 'stt2'
							for symbol_stt2_name in available:
								symbol_stt2 = graph.nodes[symbol_stt2_name]
								n2id['stt2'] = symbol_stt2_name
								linksVal = 0
								scoreLinks.append(linksVal)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								if symbol_stt2.sType == 'objectSt' and symbol_stt2.name!=symbol_20.name and symbol_stt2.name!=symbol_1.name and symbol_stt2.name!=symbol_stt1.name and symbol_stt2.name!=symbol_obj1.name:
									scoreNodes.append(100)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									# obj2
									symbol_obj2_name = 'obj2'
									for symbol_obj2_name in available:
										symbol_obj2 = graph.nodes[symbol_obj2_name]
										n2id['obj2'] = symbol_obj2_name
										linksVal = 0
										if [n2id["obj2"],n2id["stt2"],"milkpot"]  in graph.links: linksVal += 100
										if [n2id["20"],n2id["obj2"],"know"]  in graph.links: linksVal += 100
										scoreLinks.append(linksVal)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										if symbol_obj2.sType == 'object' and symbol_obj2.name!=symbol_20.name and symbol_obj2.name!=symbol_1.name and symbol_obj2.name!=symbol_stt1.name and symbol_obj2.name!=symbol_obj1.name and symbol_obj2.name!=symbol_stt2.name and [n2id["obj2"],n2id["stt2"],"milkpot"] in graph.links and [n2id["20"],n2id["obj2"],"know"] in graph.links:
											scoreNodes.append(100)
											maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
											if maxScore == 1100:
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
