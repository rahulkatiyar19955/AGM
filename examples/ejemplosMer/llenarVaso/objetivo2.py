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
	maxScore1= 0
	maxScore2= 0
	totalScore = 1100

	# Hard score
	scoreNodes = []
	scoreLinks = []
	
	del available['333']
	
	# 333
	symbol_333 = graph.nodes['333']
	n2id['333'] = '333'
	
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore) #Vale 0
	
	if symbol_333.sType == 'Mesa':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		
		# PRIMER ORDEN: VV, AA, VVV, AAA
		# VV
		symbol_vv_name = 'vv'
		for symbol_vv_name in available:
			symbol_vv = graph.nodes[symbol_vv_name]
			n2id['vv'] = symbol_vv_name
			linksVal = 0
			
			if [n2id["vv"],n2id["333"],"en"]  in graph.links: linksVal += 100
			if [n2id["vv"],n2id["333"],"lleno"]  in graph.links: linksVal += 100
			scoreLinks.append(linksVal)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			
			if symbol_vv.sType == 'Vaso' and symbol_vv.name!=symbol_333.name and [n2id["vv"],n2id["333"],"en"] in graph.links and [n2id["vv"],n2id["333"],"lleno"] in graph.links:
				scoreNodes.append(100)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				
				# AA
				symbol_aa_name = 'aa'
				for symbol_aa_name in available:
					symbol_aa = graph.nodes[symbol_aa_name]
					n2id['aa'] = symbol_aa_name
					linksVal = 0
					
					if [n2id["aa"],n2id["vv"],"en"]  in graph.links: linksVal += 100
					scoreLinks.append(linksVal)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					
					if symbol_aa.sType == 'Agua' and symbol_aa.name!=symbol_333.name and symbol_aa.name!=symbol_vv.name and [n2id["aa"],n2id["vv"],"en"] in graph.links:
						scoreNodes.append(100)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)

						# VVV
						symbol_vvv_name = 'vvv'
						for symbol_vvv_name in available:
							symbol_vvv = graph.nodes[symbol_vvv_name]
							n2id['vvv'] = symbol_vvv_name
							linksVal = 0
							
							if [n2id["vvv"],n2id["333"],"en"]  in graph.links: linksVal += 100
							if [n2id["vvv"],n2id["333"],"lleno"]  in graph.links: linksVal += 100
							scoreLinks.append(linksVal)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							
							if symbol_vvv.sType == 'Vaso' and symbol_vvv.name!=symbol_333.name and symbol_vvv.name!=symbol_vv.name and symbol_vvv.name!=symbol_aa.name and [n2id["vvv"],n2id["333"],"en"] in graph.links and [n2id["vvv"],n2id["333"],"lleno"] in graph.links:
								scoreNodes.append(100)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								
								# AAA
								symbol_aaa_name = 'aaa'
								for symbol_aaa_name in available:
									symbol_aaa = graph.nodes[symbol_aaa_name]
									n2id['aaa'] = symbol_aaa_name
									linksVal = 0
									
									if [n2id["aaa"],n2id["vvv"],"en"]  in graph.links: linksVal += 100
									scoreLinks.append(linksVal)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									
									if symbol_aaa.sType == 'Agua' and symbol_aaa.name!=symbol_333.name and symbol_aaa.name!=symbol_vvv.name and symbol_aaa.name!=symbol_vv.name and symbol_aaa.name!=symbol_aa.name and [n2id["aaa"],n2id["vvv"],"en"] in graph.links:
										scoreNodes.append(100)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										print 'maxScore 1: '+maxScore.__str__()
										if maxScore == 1100:
											maxScore1 = maxScore
											maxScore = 100
										scoreNodes.pop()
									scoreLinks.pop()
								scoreNodes.pop()
							scoreLinks.pop()
						scoreNodes.pop()
					scoreLinks.pop()
				scoreNodes.pop()
			scoreLinks.pop()
		
		# SEGUNDO ORDEN: VVV, AAA, VV, AA
		# VVV
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
				
				# AAA
				symbol_aaa_name = 'aaa'
				for symbol_aaa_name in available:
					symbol_aaa = graph.nodes[symbol_aaa_name]
					n2id['aaa'] = symbol_aaa_name
					linksVal = 0
					
					if [n2id["aaa"],n2id["vvv"],"en"]  in graph.links: linksVal += 100
					scoreLinks.append(linksVal)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					
					if symbol_aaa.sType == 'Agua' and symbol_aaa.name!=symbol_333.name and symbol_aaa.name!=symbol_vvv.name and [n2id["aaa"],n2id["vvv"],"en"] in graph.links:
						scoreNodes.append(100)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						
						# VV
						symbol_vv_name = 'vv'
						for symbol_vv_name in available:
							symbol_vv = graph.nodes[symbol_vv_name]
							n2id['vv'] = symbol_vv_name
							linksVal = 0
							
							if [n2id["vv"],n2id["333"],"en"]  in graph.links: linksVal += 100
							if [n2id["vv"],n2id["333"],"lleno"]  in graph.links: linksVal += 100
							scoreLinks.append(linksVal)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							
							if symbol_vv.sType == 'Vaso' and symbol_vv.name!=symbol_333.name and symbol_vv.name!=symbol_vvv.name and symbol_vv.name!=symbol_aaa.name and [n2id["vv"],n2id["333"],"en"] in graph.links and [n2id["vv"],n2id["333"],"lleno"] in graph.links:
								scoreNodes.append(100)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								
								# AA
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
										print 'maxScore 2: '+maxScore.__str__()
										if maxScore == 1100:
											maxScore2 = maxScore
											maxScore = 100
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
	
	if maxScore1 == 1100 or maxScore2==1100:
		finalTime = time.time()-starting_point
		print '\n SI hemos llegado con: '+maxScore1.__str__()+' o con '+maxScore2.__str__()+' con tiempo '+finalTime.__str__()+'\n'
		return maxScore, True
	
										
	finalTime = time.time()-starting_point
	print '\n NO hemos llegado: '+maxScore1.__str__()+' o con '+maxScore2.__str__()+' con tiempo '+finalTime.__str__()+'\n'
	return maxScore, False
