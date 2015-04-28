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
	totalScore = 3000

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
			# obj2r
			symbol_obj2r_name = 'obj2r'
			for symbol_obj2r_name in available:
				symbol_obj2r = graph.nodes[symbol_obj2r_name]
				n2id['obj2r'] = symbol_obj2r_name
				linksVal = 0
				if [n2id["1"],n2id["obj2r"],"know"]  in graph.links: linksVal += 100
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_obj2r.sType == 'object' and symbol_obj2r.name!=symbol_20.name and symbol_obj2r.name!=symbol_1.name and [n2id["1"],n2id["obj2r"],"know"] in graph.links:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# obj2h
					symbol_obj2h_name = 'obj2h'
					for symbol_obj2h_name in available:
						symbol_obj2h = graph.nodes[symbol_obj2h_name]
						n2id['obj2h'] = symbol_obj2h_name
						linksVal = 0
						if [n2id["20"],n2id["obj2h"],"know"]  in graph.links: linksVal += 100
						if [n2id["obj2r"],n2id["obj2h"],"eq"]  in graph.links: linksVal += 100
						scoreLinks.append(linksVal)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if symbol_obj2h.sType == 'object' and symbol_obj2h.name!=symbol_20.name and symbol_obj2h.name!=symbol_1.name and symbol_obj2h.name!=symbol_obj2r.name and [n2id["20"],n2id["obj2h"],"know"] in graph.links and [n2id["obj2r"],n2id["obj2h"],"eq"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							# stt2r
							symbol_stt2r_name = 'stt2r'
							for symbol_stt2r_name in available:
								symbol_stt2r = graph.nodes[symbol_stt2r_name]
								n2id['stt2r'] = symbol_stt2r_name
								linksVal = 0
								if [n2id["obj2r"],n2id["stt2r"],"coffeepot"]  in graph.links: linksVal += 100
								scoreLinks.append(linksVal)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								if symbol_stt2r.sType == 'objectSt' and symbol_stt2r.name!=symbol_20.name and symbol_stt2r.name!=symbol_1.name and symbol_stt2r.name!=symbol_obj2r.name and symbol_stt2r.name!=symbol_obj2h.name and [n2id["obj2r"],n2id["stt2r"],"coffeepot"] in graph.links:
									scoreNodes.append(100)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									# stt2h
									symbol_stt2h_name = 'stt2h'
									for symbol_stt2h_name in available:
										symbol_stt2h = graph.nodes[symbol_stt2h_name]
										n2id['stt2h'] = symbol_stt2h_name
										linksVal = 0
										if [n2id["obj2h"],n2id["stt2h"],"coffeepot"]  in graph.links: linksVal += 100
										scoreLinks.append(linksVal)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										if symbol_stt2h.sType == 'objectSt' and symbol_stt2h.name!=symbol_20.name and symbol_stt2h.name!=symbol_1.name and symbol_stt2h.name!=symbol_obj2r.name and symbol_stt2h.name!=symbol_obj2h.name and symbol_stt2h.name!=symbol_stt2r.name and [n2id["obj2h"],n2id["stt2h"],"coffeepot"] in graph.links:
											scoreNodes.append(100)
											maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
											# obj3r
											symbol_obj3r_name = 'obj3r'
											for symbol_obj3r_name in available:
												symbol_obj3r = graph.nodes[symbol_obj3r_name]
												n2id['obj3r'] = symbol_obj3r_name
												linksVal = 0
												if [n2id["1"],n2id["obj3r"],"know"]  in graph.links: linksVal += 100
												scoreLinks.append(linksVal)
												maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
												if symbol_obj3r.sType == 'object' and symbol_obj3r.name!=symbol_20.name and symbol_obj3r.name!=symbol_1.name and symbol_obj3r.name!=symbol_obj2r.name and symbol_obj3r.name!=symbol_obj2h.name and symbol_obj3r.name!=symbol_stt2r.name and symbol_obj3r.name!=symbol_stt2h.name and [n2id["1"],n2id["obj3r"],"know"] in graph.links:
													scoreNodes.append(100)
													maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
													# obj3h
													symbol_obj3h_name = 'obj3h'
													for symbol_obj3h_name in available:
														symbol_obj3h = graph.nodes[symbol_obj3h_name]
														n2id['obj3h'] = symbol_obj3h_name
														linksVal = 0
														if [n2id["20"],n2id["obj3h"],"know"]  in graph.links: linksVal += 100
														if [n2id["obj3r"],n2id["obj3h"],"eq"]  in graph.links: linksVal += 100
														scoreLinks.append(linksVal)
														maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
														if symbol_obj3h.sType == 'object' and symbol_obj3h.name!=symbol_20.name and symbol_obj3h.name!=symbol_1.name and symbol_obj3h.name!=symbol_obj2r.name and symbol_obj3h.name!=symbol_obj2h.name and symbol_obj3h.name!=symbol_stt2r.name and symbol_obj3h.name!=symbol_stt2h.name and symbol_obj3h.name!=symbol_obj3r.name and [n2id["20"],n2id["obj3h"],"know"] in graph.links and [n2id["obj3r"],n2id["obj3h"],"eq"] in graph.links:
															scoreNodes.append(100)
															maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
															# stt3r
															symbol_stt3r_name = 'stt3r'
															for symbol_stt3r_name in available:
																symbol_stt3r = graph.nodes[symbol_stt3r_name]
																n2id['stt3r'] = symbol_stt3r_name
																linksVal = 0
																if [n2id["obj3r"],n2id["stt3r"],"mug"]  in graph.links: linksVal += 100
																scoreLinks.append(linksVal)
																maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																if symbol_stt3r.sType == 'objectSt' and symbol_stt3r.name!=symbol_20.name and symbol_stt3r.name!=symbol_1.name and symbol_stt3r.name!=symbol_obj2r.name and symbol_stt3r.name!=symbol_obj2h.name and symbol_stt3r.name!=symbol_stt2r.name and symbol_stt3r.name!=symbol_stt2h.name and symbol_stt3r.name!=symbol_obj3r.name and symbol_stt3r.name!=symbol_obj3h.name and [n2id["obj3r"],n2id["stt3r"],"mug"] in graph.links:
																	scoreNodes.append(100)
																	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																	# stt3h
																	symbol_stt3h_name = 'stt3h'
																	for symbol_stt3h_name in available:
																		symbol_stt3h = graph.nodes[symbol_stt3h_name]
																		n2id['stt3h'] = symbol_stt3h_name
																		linksVal = 0
																		if [n2id["obj3h"],n2id["stt3h"],"mug"]  in graph.links: linksVal += 100
																		scoreLinks.append(linksVal)
																		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																		if symbol_stt3h.sType == 'objectSt' and symbol_stt3h.name!=symbol_20.name and symbol_stt3h.name!=symbol_1.name and symbol_stt3h.name!=symbol_obj2r.name and symbol_stt3h.name!=symbol_obj2h.name and symbol_stt3h.name!=symbol_stt2r.name and symbol_stt3h.name!=symbol_stt2h.name and symbol_stt3h.name!=symbol_obj3r.name and symbol_stt3h.name!=symbol_obj3h.name and symbol_stt3h.name!=symbol_stt3r.name and [n2id["obj3h"],n2id["stt3h"],"mug"] in graph.links:
																			scoreNodes.append(100)
																			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																			# obj1r
																			symbol_obj1r_name = 'obj1r'
																			for symbol_obj1r_name in available:
																				symbol_obj1r = graph.nodes[symbol_obj1r_name]
																				n2id['obj1r'] = symbol_obj1r_name
																				linksVal = 0
																				if [n2id["1"],n2id["obj1r"],"know"]  in graph.links: linksVal += 100
																				scoreLinks.append(linksVal)
																				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																				if symbol_obj1r.sType == 'object' and symbol_obj1r.name!=symbol_20.name and symbol_obj1r.name!=symbol_1.name and symbol_obj1r.name!=symbol_obj2r.name and symbol_obj1r.name!=symbol_obj2h.name and symbol_obj1r.name!=symbol_stt2r.name and symbol_obj1r.name!=symbol_stt2h.name and symbol_obj1r.name!=symbol_obj3r.name and symbol_obj1r.name!=symbol_obj3h.name and symbol_obj1r.name!=symbol_stt3r.name and symbol_obj1r.name!=symbol_stt3h.name and [n2id["1"],n2id["obj1r"],"know"] in graph.links:
																					scoreNodes.append(100)
																					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																					# obj1h
																					symbol_obj1h_name = 'obj1h'
																					for symbol_obj1h_name in available:
																						symbol_obj1h = graph.nodes[symbol_obj1h_name]
																						n2id['obj1h'] = symbol_obj1h_name
																						linksVal = 0
																						if [n2id["20"],n2id["obj1h"],"know"]  in graph.links: linksVal += 100
																						if [n2id["obj1r"],n2id["obj1h"],"eq"]  in graph.links: linksVal += 100
																						scoreLinks.append(linksVal)
																						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																						if symbol_obj1h.sType == 'object' and symbol_obj1h.name!=symbol_20.name and symbol_obj1h.name!=symbol_1.name and symbol_obj1h.name!=symbol_obj2r.name and symbol_obj1h.name!=symbol_obj2h.name and symbol_obj1h.name!=symbol_stt2r.name and symbol_obj1h.name!=symbol_stt2h.name and symbol_obj1h.name!=symbol_obj3r.name and symbol_obj1h.name!=symbol_obj3h.name and symbol_obj1h.name!=symbol_stt3r.name and symbol_obj1h.name!=symbol_stt3h.name and symbol_obj1h.name!=symbol_obj1r.name and [n2id["20"],n2id["obj1h"],"know"] in graph.links and [n2id["obj1r"],n2id["obj1h"],"eq"] in graph.links:
																							scoreNodes.append(100)
																							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																							# stt1r
																							symbol_stt1r_name = 'stt1r'
																							for symbol_stt1r_name in available:
																								symbol_stt1r = graph.nodes[symbol_stt1r_name]
																								n2id['stt1r'] = symbol_stt1r_name
																								linksVal = 0
																								if [n2id["obj1r"],n2id["stt1r"],"classifailed"]  in graph.links: linksVal += 100
																								scoreLinks.append(linksVal)
																								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																								if symbol_stt1r.sType == 'objectSt' and symbol_stt1r.name!=symbol_20.name and symbol_stt1r.name!=symbol_1.name and symbol_stt1r.name!=symbol_obj2r.name and symbol_stt1r.name!=symbol_obj2h.name and symbol_stt1r.name!=symbol_stt2r.name and symbol_stt1r.name!=symbol_stt2h.name and symbol_stt1r.name!=symbol_obj3r.name and symbol_stt1r.name!=symbol_obj3h.name and symbol_stt1r.name!=symbol_stt3r.name and symbol_stt1r.name!=symbol_stt3h.name and symbol_stt1r.name!=symbol_obj1r.name and symbol_stt1r.name!=symbol_obj1h.name and [n2id["obj1r"],n2id["stt1r"],"classifailed"] in graph.links:
																									scoreNodes.append(100)
																									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																									# stt1h
																									symbol_stt1h_name = 'stt1h'
																									for symbol_stt1h_name in available:
																										symbol_stt1h = graph.nodes[symbol_stt1h_name]
																										n2id['stt1h'] = symbol_stt1h_name
																										linksVal = 0
																										if [n2id["obj1h"],n2id["stt1h"],"unclassified"]  in graph.links: linksVal += 100
																										scoreLinks.append(linksVal)
																										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																										if symbol_stt1h.sType == 'objectSt' and symbol_stt1h.name!=symbol_20.name and symbol_stt1h.name!=symbol_1.name and symbol_stt1h.name!=symbol_obj2r.name and symbol_stt1h.name!=symbol_obj2h.name and symbol_stt1h.name!=symbol_stt2r.name and symbol_stt1h.name!=symbol_stt2h.name and symbol_stt1h.name!=symbol_obj3r.name and symbol_stt1h.name!=symbol_obj3h.name and symbol_stt1h.name!=symbol_stt3r.name and symbol_stt1h.name!=symbol_stt3h.name and symbol_stt1h.name!=symbol_obj1r.name and symbol_stt1h.name!=symbol_obj1h.name and symbol_stt1h.name!=symbol_stt1r.name and [n2id["obj1h"],n2id["stt1h"],"unclassified"] in graph.links:
																											scoreNodes.append(100)
																											maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																											if maxScore == 3000:
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
			scoreNodes.pop()
		scoreLinks.pop()
		scoreNodes.pop()
	scoreLinks.pop()
	return maxScore, False