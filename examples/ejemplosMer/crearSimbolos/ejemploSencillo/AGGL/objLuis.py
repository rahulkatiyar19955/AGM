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
	t0 = time.time()			  # tiempo inicial
	n2id = dict()
	available = copy.deepcopy(graph.nodes)

	maxScore = 0

	# Hard score
	scoreNodes = []
	scoreLinks = []
	# e
	symbol_e_name = 'e'
	for symbol_e_name in available:
		symbol_e = graph.nodes[symbol_e_name]
		n2id['e'] = symbol_e_name
		linksVal = 0
		scoreLinks.append(linksVal)
		maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
		if symbol_e.sType == 'E':
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
				if symbol_d.sType == 'D' and symbol_d.name!=symbol_e.name and [n2id["d"],n2id["e"],"unido"] in graph.links:
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
						if symbol_c.sType == 'C' and symbol_c.name!=symbol_e.name and symbol_c.name!=symbol_d.name and [n2id["c"],n2id["d"],"unido"] in graph.links:
							scoreNodes.append(100)
							maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
							# b
							symbol_b_name = 'b'
							for symbol_b_name in available:
								symbol_b = graph.nodes[symbol_b_name]
								n2id['b'] = symbol_b_name
								linksVal = 0
								if [n2id["b"],n2id["c"],"unido"]  in graph.links: linksVal += 100
								scoreLinks.append(linksVal)
								maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
								if symbol_b.sType == 'B' and symbol_b.name!=symbol_e.name and symbol_b.name!=symbol_d.name and symbol_b.name!=symbol_c.name and [n2id["b"],n2id["c"],"unido"] in graph.links:
									scoreNodes.append(100)
									maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
									# a
									symbol_a_name = 'a'
									for symbol_a_name in available:
										symbol_a = graph.nodes[symbol_a_name]
										n2id['a'] = symbol_a_name
										linksVal = 0
										if [n2id["a"],n2id["b"],"unido"]  in graph.links: linksVal += 100
										if [n2id["e"],n2id["a"],"unido"]  in graph.links: linksVal += 100
										scoreLinks.append(linksVal)
										maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
										if symbol_a.sType == 'A' and symbol_a.name!=symbol_e.name and symbol_a.name!=symbol_d.name and symbol_a.name!=symbol_c.name and symbol_a.name!=symbol_b.name and [n2id["a"],n2id["b"],"unido"] in graph.links and [n2id["e"],n2id["a"],"unido"] in graph.links:
											scoreNodes.append(100)
											maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
											if maxScore == 1000:
												t1=time.time()
												print 'Tiempo en llegar: ', (t1-t0).__str__()
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
		t1=time.time()
		print '...', (t1-t0).__str__()
	return maxScore, False
