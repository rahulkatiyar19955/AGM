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
	del available['333']
	# 333
	symbol_333 = graph.nodes['333']
	n2id['333'] = '333'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_333.sType == 'Mesa':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# vvv
		symbol_vvv_name = 'vvv'
		for symbol_vvv_name in available:
			symbol_vvv = graph.nodes[symbol_vvv_name]
			n2id['vvv'] = symbol_vvv_name
			linksVal = 0
			if [n2id["vvv"],n2id["333"],"en"]  in graph.links: linksVal += 100
			if [n2id["vvv"],n2id["333"],"lleno"]  in graph.links: linksVal += 100
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			if symbol_vvv.sType == 'Vaso' and symbol_vvv.name!=symbol_333.name and [n2id["vvv"],n2id["333"],"en"] in graph.links and [n2id["vvv"],n2id["333"],"lleno"] in graph.links:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				# vv
				symbol_vv_name = 'vv'
				for symbol_vv_name in available:
					symbol_vv = graph.nodes[symbol_vv_name]
					n2id['vv'] = symbol_vv_name
					linksVal = 0
					if [n2id["vv"],n2id["333"],"en"]  in graph.links: linksVal += 100
					if [n2id["vv"],n2id["333"],"lleno"]  in graph.links: linksVal += 100
					scoreLinks.append(linksVal)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					if symbol_vv.sType == 'Vaso' and symbol_vv.name!=symbol_333.name and symbol_vv.name!=symbol_vvv.name and [n2id["vv"],n2id["333"],"en"] in graph.links and [n2id["vv"],n2id["333"],"lleno"] in graph.links:
						scoreNodes.append(100)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						# aaa
						symbol_aaa_name = 'aaa'
						for symbol_aaa_name in available:
							symbol_aaa = graph.nodes[symbol_aaa_name]
							n2id['aaa'] = symbol_aaa_name
							linksVal = 0
							if [n2id["aaa"],n2id["vvv"],"en"]  in graph.links: linksVal += 100
							scoreLinks.append(linksVal)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							if symbol_aaa.sType == 'Agua' and symbol_aaa.name!=symbol_333.name and symbol_aaa.name!=symbol_vvv.name and symbol_aaa.name!=symbol_vv.name and [n2id["aaa"],n2id["vvv"],"en"] in graph.links:
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
									if symbol_aa.sType == 'Agua' and symbol_aa.name!=symbol_333.name and symbol_aa.name!=symbol_vvv.name and symbol_aa.name!=symbol_vv.name and symbol_aa.name!=symbol_aaa.name and [n2id["aa"],n2id["vv"],"en"] in graph.links:
										scoreNodes.append(100)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										if maxScore == 1100:
											finalTime = time.time()-starting_point
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
	return maxScore, False
