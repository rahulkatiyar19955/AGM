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
	#No hierarchical Rule
	starting_point = time.time()

	n2id = dict()
	available = copy.deepcopy(graph.nodes)

	maxScore = 0

	# Hard score
	scoreNodes = []
	scoreLinks = []
	del available['11']
	del available['13']
	del available['12']
	del available['15']
	del available['14']
	# 11
	symbol_11 = graph.nodes['11']
	n2id['11'] = '11'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_11.sType == 'Agua':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# 13
		symbol_13 = graph.nodes['13']
		n2id['13'] = '13'
		linksVal = 0
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_13.sType == 'Mesa' and symbol_13.name!=symbol_11.name:
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# 12
			symbol_12 = graph.nodes['12']
			n2id['12'] = '12'
			linksVal = 0
			if [n2id["12"],n2id["13"],"en"]  in graph.links: linksVal += 100
			if [n2id["12"],n2id["13"],"vacio"]  in graph.links: linksVal += 100
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			if symbol_12.sType == 'Jarra' and symbol_12.name!=symbol_11.name and symbol_12.name!=symbol_13.name and [n2id["12"],n2id["13"],"en"] in graph.links and [n2id["12"],n2id["13"],"vacio"] in graph.links:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				# 15
				symbol_15 = graph.nodes['15']
				n2id['15'] = '15'
				linksVal = 0
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_15.sType == 'Mesa' and symbol_15.name!=symbol_11.name and symbol_15.name!=symbol_13.name and symbol_15.name!=symbol_12.name:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# 14
					symbol_14 = graph.nodes['14']
					n2id['14'] = '14'
					linksVal = 0
					if [n2id["11"],n2id["14"],"en"]  in graph.links: linksVal += 100
					if [n2id["14"],n2id["15"],"en"]  in graph.links: linksVal += 100
					if [n2id["14"],n2id["15"],"lleno"]  in graph.links: linksVal += 100
					scoreLinks.append(linksVal)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					if symbol_14.sType == 'Vaso' and symbol_14.name!=symbol_11.name and symbol_14.name!=symbol_13.name and symbol_14.name!=symbol_12.name and symbol_14.name!=symbol_15.name and [n2id["11"],n2id["14"],"en"] in graph.links and [n2id["14"],n2id["15"],"en"] in graph.links and [n2id["14"],n2id["15"],"lleno"] in graph.links:
						scoreNodes.append(100)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if maxScore == 1000: 
							finalTime = time.time()-starting_point
							print 'Hemos llegado con: '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
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
	finalTime = time.time()-starting_point
	print 'No hemos llegado con: '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
	return maxScore, False
