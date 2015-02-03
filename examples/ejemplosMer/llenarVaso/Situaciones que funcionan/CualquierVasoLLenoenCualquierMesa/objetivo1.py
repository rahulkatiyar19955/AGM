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
	starting_point = time.time()  # Guardamos tiempo inicial
	n2id = dict()
	available = copy.deepcopy(graph.nodes)

	maxScore = 0

	# Hard score
	scoreNodes = []
	scoreLinks = []
	# vv
	symbol_vv_name = 'vv'
	for symbol_vv_name in available:
		symbol_vv = graph.nodes[symbol_vv_name]
		n2id['vv'] = symbol_vv_name
		linksVal = 0
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_vv.sType == 'Vaso':
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# mm
			symbol_mm_name = 'mm'
			for symbol_mm_name in available:
				symbol_mm = graph.nodes[symbol_mm_name]
				n2id['mm'] = symbol_mm_name
				linksVal = 0
				if [n2id["vv"],n2id["mm"],"en"]  in graph.links: linksVal += 100
				if [n2id["vv"],n2id["mm"],"lleno"]  in graph.links: linksVal += 100
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_mm.sType == 'Mesa' and symbol_mm.name!=symbol_vv.name and [n2id["vv"],n2id["mm"],"en"] in graph.links and [n2id["vv"],n2id["mm"],"lleno"] in graph.links:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# aa
					symbol_aa_name = 'aa'
					for symbol_aa_name in available:
						symbol_aa = graph.nodes[symbol_aa_name]
						n2id['aa'] = symbol_aa_name
						linksVal = 0
						if [n2id["aa"],n2id["vv"],"en"]  in graph.links: linksVal += 100
						scoreLinks.append(linksVal)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if symbol_aa.sType == 'Agua' and symbol_aa.name!=symbol_vv.name and symbol_aa.name!=symbol_mm.name and [n2id["aa"],n2id["vv"],"en"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							if maxScore == 600:
								finalTime = time.time()-starting_point
								print 'SI hemos llegado: '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
								return maxScore, True
							scoreNodes.pop()
						scoreLinks.pop()
					scoreNodes.pop()
				scoreLinks.pop()
			scoreNodes.pop()
		scoreLinks.pop()
	finalTime = time.time()-starting_point
	print 'NO hemos llegado: '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
	return maxScore, False
