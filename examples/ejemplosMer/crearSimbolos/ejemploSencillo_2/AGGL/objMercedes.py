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
	totalScore = 2400

	del available['1']
	del available['2']
	# Hard score
	scoreNodes = []
	scoreLinks = []
	# 1
	symbol_1 = graph.nodes['1']
	n2id['1'] = '1'
	linksVal = 0
	scoreLinks.append(linksVal)
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	if symbol_1.sType == 'A':
		scoreNodes.append(100)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		# 2
		symbol_2 = graph.nodes['2']
		n2id['2'] = '2'
		linksVal = 0
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_2.sType == 'A' and symbol_2.name!=symbol_1.name:
			scoreNodes.append(100)
			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
			# e
			symbol_e_name = 'e'
			for symbol_e_name in available:
				symbol_e = graph.nodes[symbol_e_name]
				n2id['e'] = symbol_e_name
				linksVal = 0
				scoreLinks.append(linksVal)
				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
				if symbol_e.sType == 'E' and symbol_e.name!=symbol_1.name and symbol_e.name!=symbol_2.name:
					scoreNodes.append(100)
					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
					# d
					symbol_d_name = 'd'
					for symbol_d_name in available:
						symbol_d = graph.nodes[symbol_d_name]
						n2id['d'] = symbol_d_name
						linksVal = 0
						if [n2id["d"],n2id["e"],"unido"]  in graph.links: linksVal += 100
						scoreLinks.append(linksVal)
						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
						if symbol_d.sType == 'D' and symbol_d.name!=symbol_1.name and symbol_d.name!=symbol_2.name and symbol_d.name!=symbol_e.name and [n2id["d"],n2id["e"],"unido"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							# c
							symbol_c_name = 'c'
							for symbol_c_name in available:
								symbol_c = graph.nodes[symbol_c_name]
								n2id['c'] = symbol_c_name
								linksVal = 0
								if [n2id["c"],n2id["d"],"unido"]  in graph.links: linksVal += 100
								scoreLinks.append(linksVal)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								if symbol_c.sType == 'C' and symbol_c.name!=symbol_1.name and symbol_c.name!=symbol_2.name and symbol_c.name!=symbol_e.name and symbol_c.name!=symbol_d.name and [n2id["c"],n2id["d"],"unido"] in graph.links:
									scoreNodes.append(100)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									# f
									symbol_f_name = 'f'
									for symbol_f_name in available:
										symbol_f = graph.nodes[symbol_f_name]
										n2id['f'] = symbol_f_name
										linksVal = 0
										if [n2id["e"],n2id["f"],"unido"]  in graph.links: linksVal += 100
										if [n2id["f"],n2id["1"],"unido"]  in graph.links: linksVal += 100
										scoreLinks.append(linksVal)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										if symbol_f.sType == 'F' and symbol_f.name!=symbol_1.name and symbol_f.name!=symbol_2.name and symbol_f.name!=symbol_e.name and symbol_f.name!=symbol_d.name and symbol_f.name!=symbol_c.name and [n2id["e"],n2id["f"],"unido"] in graph.links and [n2id["f"],n2id["1"],"unido"] in graph.links:
											scoreNodes.append(100)
											maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
											# b
											symbol_b_name = 'b'
											for symbol_b_name in available:
												symbol_b = graph.nodes[symbol_b_name]
												n2id['b'] = symbol_b_name
												linksVal = 0
												if [n2id["1"],n2id["b"],"unido"]  in graph.links: linksVal += 100
												if [n2id["b"],n2id["c"],"unido"]  in graph.links: linksVal += 100
												scoreLinks.append(linksVal)
												maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
												if symbol_b.sType == 'B' and symbol_b.name!=symbol_1.name and symbol_b.name!=symbol_2.name and symbol_b.name!=symbol_e.name and symbol_b.name!=symbol_d.name and symbol_b.name!=symbol_c.name and symbol_b.name!=symbol_f.name and [n2id["1"],n2id["b"],"unido"] in graph.links and [n2id["b"],n2id["c"],"unido"] in graph.links:
													scoreNodes.append(100)
													maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
													# k
													symbol_k_name = 'k'
													for symbol_k_name in available:
														symbol_k = graph.nodes[symbol_k_name]
														n2id['k'] = symbol_k_name
														linksVal = 0
														scoreLinks.append(linksVal)
														maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
														if symbol_k.sType == 'E' and symbol_k.name!=symbol_1.name and symbol_k.name!=symbol_2.name and symbol_k.name!=symbol_e.name and symbol_k.name!=symbol_d.name and symbol_k.name!=symbol_c.name and symbol_k.name!=symbol_f.name and symbol_k.name!=symbol_b.name:
															scoreNodes.append(100)
															maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
															# j
															symbol_j_name = 'j'
															for symbol_j_name in available:
																symbol_j = graph.nodes[symbol_j_name]
																n2id['j'] = symbol_j_name
																linksVal = 0
																if [n2id["j"],n2id["k"],"unido"]  in graph.links: linksVal += 100
																scoreLinks.append(linksVal)
																maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																if symbol_j.sType == 'D' and symbol_j.name!=symbol_1.name and symbol_j.name!=symbol_2.name and symbol_j.name!=symbol_e.name and symbol_j.name!=symbol_d.name and symbol_j.name!=symbol_c.name and symbol_j.name!=symbol_f.name and symbol_j.name!=symbol_b.name and symbol_j.name!=symbol_k.name and [n2id["j"],n2id["k"],"unido"] in graph.links:
																	scoreNodes.append(100)
																	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																	# i
																	symbol_i_name = 'i'
																	for symbol_i_name in available:
																		symbol_i = graph.nodes[symbol_i_name]
																		n2id['i'] = symbol_i_name
																		linksVal = 0
																		if [n2id["i"],n2id["j"],"unido"]  in graph.links: linksVal += 100
																		scoreLinks.append(linksVal)
																		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																		if symbol_i.sType == 'C' and symbol_i.name!=symbol_1.name and symbol_i.name!=symbol_2.name and symbol_i.name!=symbol_e.name and symbol_i.name!=symbol_d.name and symbol_i.name!=symbol_c.name and symbol_i.name!=symbol_f.name and symbol_i.name!=symbol_b.name and symbol_i.name!=symbol_k.name and symbol_i.name!=symbol_j.name and [n2id["i"],n2id["j"],"unido"] in graph.links:
																			scoreNodes.append(100)
																			maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																			# l
																			symbol_l_name = 'l'
																			for symbol_l_name in available:
																				symbol_l = graph.nodes[symbol_l_name]
																				n2id['l'] = symbol_l_name
																				linksVal = 0
																				if [n2id["k"],n2id["l"],"unido"]  in graph.links: linksVal += 100
																				if [n2id["l"],n2id["2"],"unido"]  in graph.links: linksVal += 100
																				scoreLinks.append(linksVal)
																				maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																				if symbol_l.sType == 'F' and symbol_l.name!=symbol_1.name and symbol_l.name!=symbol_2.name and symbol_l.name!=symbol_e.name and symbol_l.name!=symbol_d.name and symbol_l.name!=symbol_c.name and symbol_l.name!=symbol_f.name and symbol_l.name!=symbol_b.name and symbol_l.name!=symbol_k.name and symbol_l.name!=symbol_j.name and symbol_l.name!=symbol_i.name and [n2id["k"],n2id["l"],"unido"] in graph.links and [n2id["l"],n2id["2"],"unido"] in graph.links:
																					scoreNodes.append(100)
																					maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																					# h
																					symbol_h_name = 'h'
																					for symbol_h_name in available:
																						symbol_h = graph.nodes[symbol_h_name]
																						n2id['h'] = symbol_h_name
																						linksVal = 0
																						if [n2id["2"],n2id["h"],"unido"]  in graph.links: linksVal += 100
																						if [n2id["h"],n2id["i"],"unido"]  in graph.links: linksVal += 100
																						scoreLinks.append(linksVal)
																						maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																						if symbol_h.sType == 'B' and symbol_h.name!=symbol_1.name and symbol_h.name!=symbol_2.name and symbol_h.name!=symbol_e.name and symbol_h.name!=symbol_d.name and symbol_h.name!=symbol_c.name and symbol_h.name!=symbol_f.name and symbol_h.name!=symbol_b.name and symbol_h.name!=symbol_k.name and symbol_h.name!=symbol_j.name and symbol_h.name!=symbol_i.name and symbol_h.name!=symbol_l.name and [n2id["2"],n2id["h"],"unido"] in graph.links and [n2id["h"],n2id["i"],"unido"] in graph.links:
																							scoreNodes.append(100)
																							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
																							if maxScore == 2400:
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
	return maxScore, False
