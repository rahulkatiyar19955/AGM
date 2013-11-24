import copy, sys
sys.path.append('/opt/robocomp/share')
from AGGL import *
from agglplanner import *
def CheckTarget(graph):
	n2id = dict()

	score = 0
	scoreA = 0

	# Easy score
	typesDict = dict()
	typesDict['status'] = 2
	typesDict['mug'] = 2
	typesDict['object'] = 2
	for n in graph.nodes:
		if graph.nodes[n].sType in typesDict:
			scoreA += 1
			typesDict[graph.nodes[n].sType] -= 1
			if typesDict[graph.nodes[n].sType] == 0:
				del typesDict[graph.nodes[n].sType]

	# Hard score
	# mugR
	for symbol_mugR_name in graph.nodes:
		symbol_mugR = graph.nodes[symbol_mugR_name]
		n2id['mugR'] = symbol_mugR_name
		if symbol_mugR.sType == 'mug':
			if 3 > score: score = 3
			# statusR
			for symbol_statusR_name in graph.nodes:
				symbol_statusR = graph.nodes[symbol_statusR_name]
				n2id['statusR'] = symbol_statusR_name
				if symbol_statusR.sType == 'status' and symbol_statusR.name!=symbol_mugR.name and [n2id["statusR"],n2id["mugR"],"link"] in graph.links:
					if 9 > score: score = 9
					# objectH
					for symbol_objectH_name in graph.nodes:
						symbol_objectH = graph.nodes[symbol_objectH_name]
						n2id['objectH'] = symbol_objectH_name
						if symbol_objectH.sType == 'object' and symbol_objectH.name!=symbol_mugR.name and symbol_objectH.name!=symbol_statusR.name:
							if 12 > score: score = 12
							# objectR
							for symbol_objectR_name in graph.nodes:
								symbol_objectR = graph.nodes[symbol_objectR_name]
								n2id['objectR'] = symbol_objectR_name
								if symbol_objectR.sType == 'object' and symbol_objectR.name!=symbol_mugR.name and symbol_objectR.name!=symbol_statusR.name and symbol_objectR.name!=symbol_objectH.name and [n2id["objectR"],n2id["objectH"],"eq"] in graph.links and [n2id["objectR"],n2id["statusR"],"has"] in graph.links:
									if 21 > score: score = 21
									# statusH
									for symbol_statusH_name in graph.nodes:
										symbol_statusH = graph.nodes[symbol_statusH_name]
										n2id['statusH'] = symbol_statusH_name
										if symbol_statusH.sType == 'status' and symbol_statusH.name!=symbol_mugR.name and symbol_statusH.name!=symbol_statusR.name and symbol_statusH.name!=symbol_objectH.name and symbol_statusH.name!=symbol_objectR.name and [n2id["objectH"],n2id["statusH"],"has"] in graph.links:
											if 27 > score: score = 27
											# mugH
											for symbol_mugH_name in graph.nodes:
												symbol_mugH = graph.nodes[symbol_mugH_name]
												n2id['mugH'] = symbol_mugH_name
												if symbol_mugH.sType == 'mug' and symbol_mugH.name!=symbol_mugR.name and symbol_mugH.name!=symbol_statusR.name and symbol_mugH.name!=symbol_objectH.name and symbol_mugH.name!=symbol_objectR.name and symbol_mugH.name!=symbol_statusH.name and [n2id["statusH"],n2id["mugH"],"link"] in graph.links:
													if 33 > score: score = 33
													return score, True
	return score+scoreA, False
	
	
