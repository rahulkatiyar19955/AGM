def CheckTarget(graph):
	for cacho_n in graph.nodes:
		cacho = graph.nodes[cacho_n]
		if cacho.sType == 'cacho':
			return True
	return False