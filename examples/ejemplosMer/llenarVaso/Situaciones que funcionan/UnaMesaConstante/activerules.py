import copy, sys, cPickle
sys.path.append('/usr/local/share/agm/')
from AGGL import *
from agglplanner import *

def getNewIdForSymbol(node):
	m = 1
	for k in node.graph.nodes:
			if int(node.graph.nodes[k].name) >= m:
				m = int(node.graph.nodes[k].name)+1
	return m

lastNodeId = 0

class RuleSet(object):
	def __init__(self):
		object.__init__(self)

# Up to this point, all the code has been generated by the generateAGGLPlanerCode.py file

	def getRules(self):
		mapping = dict()
		mapping['ServirAgua'] = self.ServirAgua
		mapping['MoverVaso'] = self.MoverVaso
		return mapping

	def getTriggers(self):
		mapping = dict()
		mapping['ServirAgua'] = self.ServirAgua_trigger
		mapping['MoverVaso'] = self.MoverVaso_trigger
		return mapping


	# Rule ServirAgua
	def ServirAgua(self, snode, stackP=None, equivalencesP=None):
		if stackP == None: stackP=[]
		if equivalencesP == None: equivalencesP=[]
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		symbol_nodes_copy = copy.deepcopy(snode.graph.nodes)
		finishesCombo = ''
		if len(stack) > 0:
			inCombo = True
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for a
			symbol_a_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'a'] in equiv[0] and equiv[1] != None:
					symbol_a_nodes = [equiv[1]]
			# Find equivalence for j
			symbol_j_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'j'] in equiv[0] and equiv[1] != None:
					symbol_j_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'm'] in equiv[0] and equiv[1] != None:
					symbol_m_nodes = [equiv[1]]
			# Find equivalence for v
			symbol_v_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'v'] in equiv[0] and equiv[1] != None:
					symbol_v_nodes = [equiv[1]]
		else:
			inCombo = False
			symbol_a_nodes = symbol_nodes_copy
			symbol_j_nodes = symbol_nodes_copy
			symbol_m_nodes = symbol_nodes_copy
			symbol_v_nodes = symbol_nodes_copy
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_j_name in symbol_j_nodes:
			symbol_j = nodes[symbol_j_name]
			n2id['j'] = symbol_j_name
			if symbol_j.sType == 'Jarra':
				for symbol_v_name in symbol_v_nodes:
					symbol_v = nodes[symbol_v_name]
					n2id['v'] = symbol_v_name
					if symbol_v.sType == 'Vaso' and symbol_v.name!=symbol_j.name:
						for symbol_m_name in symbol_m_nodes:
							symbol_m = nodes[symbol_m_name]
							n2id['m'] = symbol_m_name
							if symbol_m.sType == 'Mesa' and symbol_m.name!=symbol_j.name and symbol_m.name!=symbol_v.name and [n2id["j"],n2id["m"],"en"] in snode.graph.links and [n2id["j"],n2id["m"],"lleno"] in snode.graph.links and [n2id["v"],n2id["m"],"en"] in snode.graph.links and [n2id["v"],n2id["m"],"vacio"] in snode.graph.links:
								for symbol_a_name in symbol_a_nodes:
									symbol_a = nodes[symbol_a_name]
									n2id['a'] = symbol_a_name
									if symbol_a.sType == 'Agua' and symbol_a.name!=symbol_j.name and symbol_a.name!=symbol_v.name and symbol_a.name!=symbol_m.name and [n2id["a"],n2id["j"],"en"] in snode.graph.links:
										# At this point we meet all the conditions.
										stack2        = copy.deepcopy(stack)
										equivalences2 = copy.deepcopy(equivalences)
										r1 = self.ServirAgua_trigger(snode, n2id, stack2, inCombo, equivalences2, copy.deepcopy(finishesCombo))
										c = copy.deepcopy(r1)
										if 'fina' in locals():
											c.history.append(finishesCombo)
										if len(stack2) > 0: c.stop = True
										ret.append(c)
										if len(stack2) > 0:
											# Set symbol for j...
											for equiv in equivalences2:
												if [me, 'j'] in equiv[0]:
													equiv[1] = symbol_j_name
											# Set symbol for v...
											for equiv in equivalences2:
												if [me, 'v'] in equiv[0]:
													equiv[1] = symbol_v_name
											# Set symbol for m...
											for equiv in equivalences2:
												if [me, 'm'] in equiv[0]:
													equiv[1] = symbol_m_name
											# Set symbol for a...
											for equiv in equivalences2:
												if [me, 'a'] in equiv[0]:
													equiv[1] = symbol_a_name
											newNode = WorldStateHistory(r1)
											global lastNodeId
											lastNodeId += 1
											newNode.nodeId = lastNodeId
											derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
											if 'fina' in locals():
												for n in derivsx: n.history.append(finishesCombo)
												for n in derivsx: n.history.append(fina)
											ret.extend(derivsx)
		return ret
		
		

	# Rule ServirAgua
	def ServirAgua_trigger(self, snode, n2id, stack=None, inCombo=False, equivalences=None, checked=True, finish=''):
		if stack == None: stack=[]
		if equivalences == None: equivalences=[]
		if not checked:
			test_symbol_j = snode.graph.nodes[n2id['j']]
			if not (test_symbol_j.sType == 'Jarra'):
				print 'test_symbol_j.sType == Jarra' , test_symbol_j.sType == 'Jarra'
				raise WrongRuleExecution('ServirAgua_trigger1')
			test_symbol_v = snode.graph.nodes[n2id['v']]
			if not (test_symbol_v.sType == 'Vaso' and test_symbol_v.name!=test_symbol_j.name):
				print 'test_symbol_v.sType == Vaso' , test_symbol_v.sType == 'Vaso'
				raise WrongRuleExecution('ServirAgua_trigger2')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'Mesa' and test_symbol_m.name!=test_symbol_j.name and test_symbol_m.name!=test_symbol_v.name and [n2id["j"],n2id["m"],"en"] in snode.graph.links and [n2id["j"],n2id["m"],"lleno"] in snode.graph.links and [n2id["v"],n2id["m"],"en"] in snode.graph.links and [n2id["v"],n2id["m"],"vacio"] in snode.graph.links):
				print 'test_symbol_m.sType == Mesa' , test_symbol_m.sType == 'Mesa'
				raise WrongRuleExecution('ServirAgua_trigger3')
			test_symbol_a = snode.graph.nodes[n2id['a']]
			if not (test_symbol_a.sType == 'Agua' and test_symbol_a.name!=test_symbol_j.name and test_symbol_a.name!=test_symbol_v.name and test_symbol_a.name!=test_symbol_m.name and [n2id["a"],n2id["j"],"en"] in snode.graph.links):
				print 'test_symbol_a.sType == Agua' , test_symbol_a.sType == 'Agua'
				raise WrongRuleExecution('ServirAgua_trigger4')
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		# Create nodes
		# Retype nodes
		# Remove nodes
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [n2id['a'], n2id['j'], 'en'], [n2id['j'], n2id['m'], 'lleno'], [n2id['v'], n2id['m'], 'vacio'] ]]
		# Create links
		l = AGMLink(n2id['j'], n2id['m'], 'vacio')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(n2id['a'], n2id['v'], 'en')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(n2id['v'], n2id['m'], 'lleno')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		if not inCombo:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('ServirAgua@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule MoverVaso
	def MoverVaso(self, snode, stackP=None, equivalencesP=None):
		if stackP == None: stackP=[]
		if equivalencesP == None: equivalencesP=[]
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		symbol_nodes_copy = copy.deepcopy(snode.graph.nodes)
		finishesCombo = ''
		if len(stack) > 0:
			inCombo = True
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for v
			symbol_v_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'v'] in equiv[0] and equiv[1] != None:
					symbol_v_nodes = [equiv[1]]
			# Find equivalence for m1
			symbol_m1_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'm1'] in equiv[0] and equiv[1] != None:
					symbol_m1_nodes = [equiv[1]]
			# Find equivalence for m2
			symbol_m2_nodes = symbol_nodes_copy
			for equiv in equivalences:
				if [me, 'm2'] in equiv[0] and equiv[1] != None:
					symbol_m2_nodes = [equiv[1]]
		else:
			inCombo = False
			symbol_v_nodes = symbol_nodes_copy
			symbol_m1_nodes = symbol_nodes_copy
			symbol_m2_nodes = symbol_nodes_copy
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_v_name in symbol_v_nodes:
			symbol_v = nodes[symbol_v_name]
			n2id['v'] = symbol_v_name
			if symbol_v.sType == 'Vaso':
				for symbol_m1_name in symbol_m1_nodes:
					symbol_m1 = nodes[symbol_m1_name]
					n2id['m1'] = symbol_m1_name
					if symbol_m1.sType == 'Mesa' and symbol_m1.name!=symbol_v.name and [n2id["v"],n2id["m1"],"en"] in snode.graph.links and [n2id["v"],n2id["m1"],"lleno"] in snode.graph.links:
						for symbol_m2_name in symbol_m2_nodes:
							symbol_m2 = nodes[symbol_m2_name]
							n2id['m2'] = symbol_m2_name
							if symbol_m2.sType == 'Mesa' and symbol_m2.name!=symbol_v.name and symbol_m2.name!=symbol_m1.name:
								# At this point we meet all the conditions.
								stack2        = copy.deepcopy(stack)
								equivalences2 = copy.deepcopy(equivalences)
								r1 = self.MoverVaso_trigger(snode, n2id, stack2, inCombo, equivalences2, copy.deepcopy(finishesCombo))
								c = copy.deepcopy(r1)
								if 'fina' in locals():
									c.history.append(finishesCombo)
								if len(stack2) > 0: c.stop = True
								ret.append(c)
								if len(stack2) > 0:
									# Set symbol for v...
									for equiv in equivalences2:
										if [me, 'v'] in equiv[0]:
											equiv[1] = symbol_v_name
									# Set symbol for m1...
									for equiv in equivalences2:
										if [me, 'm1'] in equiv[0]:
											equiv[1] = symbol_m1_name
									# Set symbol for m2...
									for equiv in equivalences2:
										if [me, 'm2'] in equiv[0]:
											equiv[1] = symbol_m2_name
									newNode = WorldStateHistory(r1)
									global lastNodeId
									lastNodeId += 1
									newNode.nodeId = lastNodeId
									derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
									if 'fina' in locals():
										for n in derivsx: n.history.append(finishesCombo)
										for n in derivsx: n.history.append(fina)
									ret.extend(derivsx)
		return ret
		
		

	# Rule MoverVaso
	def MoverVaso_trigger(self, snode, n2id, stack=None, inCombo=False, equivalences=None, checked=True, finish=''):
		if stack == None: stack=[]
		if equivalences == None: equivalences=[]
		if not checked:
			test_symbol_v = snode.graph.nodes[n2id['v']]
			if not (test_symbol_v.sType == 'Vaso'):
				print 'test_symbol_v.sType == Vaso' , test_symbol_v.sType == 'Vaso'
				raise WrongRuleExecution('MoverVaso_trigger1')
			test_symbol_m1 = snode.graph.nodes[n2id['m1']]
			if not (test_symbol_m1.sType == 'Mesa' and test_symbol_m1.name!=test_symbol_v.name and [n2id["v"],n2id["m1"],"en"] in snode.graph.links and [n2id["v"],n2id["m1"],"lleno"] in snode.graph.links):
				print 'test_symbol_m1.sType == Mesa' , test_symbol_m1.sType == 'Mesa'
				raise WrongRuleExecution('MoverVaso_trigger2')
			test_symbol_m2 = snode.graph.nodes[n2id['m2']]
			if not (test_symbol_m2.sType == 'Mesa' and test_symbol_m2.name!=test_symbol_v.name and test_symbol_m2.name!=test_symbol_m1.name):
				print 'test_symbol_m2.sType == Mesa' , test_symbol_m2.sType == 'Mesa'
				raise WrongRuleExecution('MoverVaso_trigger3')
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		# Create nodes
		# Retype nodes
		# Remove nodes
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [n2id['v'], n2id['m1'], 'en'], [n2id['v'], n2id['m1'], 'lleno'] ]]
		# Create links
		l = AGMLink(n2id['v'], n2id['m2'], 'en')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(n2id['v'], n2id['m2'], 'lleno')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		if not inCombo:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('MoverVaso@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		