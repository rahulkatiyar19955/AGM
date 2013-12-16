import copy, sys
sys.path.append('/opt/robocomp/share')
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

	def getRules(self):
		mapping = dict()
		mapping['findObjectVisually'] = self.findObjectVisually
		mapping['findObjectTold'] = self.findObjectTold
		mapping['recognizeObjMug'] = self.recognizeObjMug
		mapping['recognizeObjBox'] = self.recognizeObjBox
		mapping['recognizeObjTable'] = self.recognizeObjTable
		mapping['recognizeObjFails'] = self.recognizeObjFails
		mapping['setObjectReach'] = self.setObjectReach
		mapping['setObjectSee'] = self.setObjectSee
		mapping['setObjectPosition'] = self.setObjectPosition
		mapping['tellHumanAboutMug'] = self.tellHumanAboutMug
		mapping['tellHumanAboutBox'] = self.tellHumanAboutBox
		mapping['tellHumanAboutTable'] = self.tellHumanAboutTable
		mapping['tellHumanAboutUnknownObject'] = self.tellHumanAboutUnknownObject
		mapping['makeHumanLook'] = self.makeHumanLook
		mapping['humanClassifiesMug'] = self.humanClassifiesMug
		mapping['humanClassifiesBox'] = self.humanClassifiesBox
		mapping['humanClassifiesTable'] = self.humanClassifiesTable
		mapping['humanTellsUsAboutMug'] = self.humanTellsUsAboutMug
		mapping['humanTellsUsAboutBox'] = self.humanTellsUsAboutBox
		mapping['humanTellsUsAboutTable'] = self.humanTellsUsAboutTable
		mapping['robotMovesMugFromTableToBox'] = self.robotMovesMugFromTableToBox
		mapping['humanMovesMugFromTableToBox'] = self.humanMovesMugFromTableToBox
		mapping['setTableClean'] = self.setTableClean
		mapping['MOVEtoCLEAN'] = self.MOVEtoCLEAN
		return mapping

	def getTriggers(self):
		mapping = dict()
		mapping['findObjectVisually'] = self.findObjectVisually_trigger
		mapping['findObjectTold'] = self.findObjectTold_trigger
		mapping['recognizeObjMug'] = self.recognizeObjMug_trigger
		mapping['recognizeObjBox'] = self.recognizeObjBox_trigger
		mapping['recognizeObjTable'] = self.recognizeObjTable_trigger
		mapping['recognizeObjFails'] = self.recognizeObjFails_trigger
		mapping['setObjectReach'] = self.setObjectReach_trigger
		mapping['setObjectSee'] = self.setObjectSee_trigger
		mapping['setObjectPosition'] = self.setObjectPosition_trigger
		mapping['tellHumanAboutMug'] = self.tellHumanAboutMug_trigger
		mapping['tellHumanAboutBox'] = self.tellHumanAboutBox_trigger
		mapping['tellHumanAboutTable'] = self.tellHumanAboutTable_trigger
		mapping['tellHumanAboutUnknownObject'] = self.tellHumanAboutUnknownObject_trigger
		mapping['makeHumanLook'] = self.makeHumanLook_trigger
		mapping['humanClassifiesMug'] = self.humanClassifiesMug_trigger
		mapping['humanClassifiesBox'] = self.humanClassifiesBox_trigger
		mapping['humanClassifiesTable'] = self.humanClassifiesTable_trigger
		mapping['humanTellsUsAboutMug'] = self.humanTellsUsAboutMug_trigger
		mapping['humanTellsUsAboutBox'] = self.humanTellsUsAboutBox_trigger
		mapping['humanTellsUsAboutTable'] = self.humanTellsUsAboutTable_trigger
		mapping['robotMovesMugFromTableToBox'] = self.robotMovesMugFromTableToBox_trigger
		mapping['humanMovesMugFromTableToBox'] = self.humanMovesMugFromTableToBox_trigger
		mapping['setTableClean'] = self.setTableClean_trigger
		mapping['MOVEtoCLEAN'] = self.MOVEtoCLEAN_trigger
		return mapping


	# Rule findObjectVisually
	def findObjectVisually(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
		else:
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_r_name in symbol_r_nodes:
			symbol_r = nodes[symbol_r_name]
			n2id['r'] = symbol_r_name
			if symbol_r.sType == 'robot':
				# At this point we meet all the conditions.
				# Insert additional conditions manually here if you want.
				# (beware that the code could be regenerated and you might lose your changes).
				stack2        = copy.deepcopy(stack)
				equivalences2 = copy.deepcopy(equivalences)
				r1 = self.findObjectVisually_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
				c = copy.deepcopy(r1)
				if 'fina' in locals():
					c.history.append(finishesCombo)
				if len(stack2) > 0: c.stop = True
				ret.append(c)
				if len(stack2) > 0:
					# Set symbol for r...
					for equiv in equivalences2:
						if [me, 'r'] in equiv[0]:
							equiv[1] = symbol_r_name
					newNode = WorldStateHistory(r1)
					global lastNodeId
					lastNodeId += 1
					newNode.nodeId = lastNodeId
					newNode.parentId = snode.nodeId
					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
					if 'fina' in locals():
						for n in derivsx: n.history.append(finishesCombo)
						for n in derivsx: n.history.append(fina)
					ret.extend(derivsx)
		return ret
		
		

	# Rule findObjectVisually
	def findObjectVisually_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot'):
				raise WrongRuleExecution('findObjectVisually_trigger1 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['cl'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'unclassified')
		newName = str(getNewIdForSymbol(newNode))
		smap['o'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['re'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'notReach')
		newName = str(getNewIdForSymbol(newNode))
		smap['t'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['po'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'position')
		newName = str(getNewIdForSymbol(newNode))
		smap['se'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'see')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['o'], smap['t'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['po'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['re'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['se'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['cl'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['r'], smap['o'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('findObjectVisually@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule findObjectTold
	def findObjectTold(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
		else:
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_r_name in symbol_r_nodes:
			symbol_r = nodes[symbol_r_name]
			n2id['r'] = symbol_r_name
			if symbol_r.sType == 'robot':
				# At this point we meet all the conditions.
				# Insert additional conditions manually here if you want.
				# (beware that the code could be regenerated and you might lose your changes).
				stack2        = copy.deepcopy(stack)
				equivalences2 = copy.deepcopy(equivalences)
				r1 = self.findObjectTold_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
				c = copy.deepcopy(r1)
				if 'fina' in locals():
					c.history.append(finishesCombo)
				if len(stack2) > 0: c.stop = True
				ret.append(c)
				if len(stack2) > 0:
					# Set symbol for r...
					for equiv in equivalences2:
						if [me, 'r'] in equiv[0]:
							equiv[1] = symbol_r_name
					newNode = WorldStateHistory(r1)
					global lastNodeId
					lastNodeId += 1
					newNode.nodeId = lastNodeId
					newNode.parentId = snode.nodeId
					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
					if 'fina' in locals():
						for n in derivsx: n.history.append(finishesCombo)
						for n in derivsx: n.history.append(fina)
					ret.extend(derivsx)
		return ret
		
		

	# Rule findObjectTold
	def findObjectTold_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot'):
				raise WrongRuleExecution('findObjectTold_trigger1 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['cl'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'unclassified')
		newName = str(getNewIdForSymbol(newNode))
		smap['o'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['re'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'notReach')
		newName = str(getNewIdForSymbol(newNode))
		smap['t'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['po'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'notPosition')
		newName = str(getNewIdForSymbol(newNode))
		smap['se'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'notSee')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['o'], smap['t'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['po'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['re'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['se'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['cl'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['r'], smap['o'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['t'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 4
			newNode.depth += 1
		newNode.history.append('findObjectTold@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule recognizeObjMug
	def recognizeObjMug(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for other
			symbol_other_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'other'] in equiv[0]:
					if equiv[1] != None:
						symbol_other_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for po
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'po'] in equiv[0]:
					if equiv[1] != None:
						symbol_po_nodes = [equiv[1]]
			# Find equivalence for se
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'se'] in equiv[0]:
					if equiv[1] != None:
						symbol_se_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_other_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in symbol_se_nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in symbol_po_nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in symbol_c_nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														for symbol_other_name in symbol_other_nodes:
															symbol_other = nodes[symbol_other_name]
															n2id['other'] = symbol_other_name
															if symbol_other.sType == 'object' and symbol_other.name!=symbol_s.name and symbol_other.name!=symbol_o.name and symbol_other.name!=symbol_r.name and symbol_other.name!=symbol_se.name and symbol_other.name!=symbol_po.name and symbol_other.name!=symbol_c.name:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																stack2        = copy.deepcopy(stack)
																equivalences2 = copy.deepcopy(equivalences)
																r1 = self.recognizeObjMug_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																c = copy.deepcopy(r1)
																if 'fina' in locals():
																	c.history.append(finishesCombo)
																if len(stack2) > 0: c.stop = True
																ret.append(c)
																if len(stack2) > 0:
																	# Set symbol for s...
																	for equiv in equivalences2:
																		if [me, 's'] in equiv[0]:
																			equiv[1] = symbol_s_name
																	# Set symbol for o...
																	for equiv in equivalences2:
																		if [me, 'o'] in equiv[0]:
																			equiv[1] = symbol_o_name
																	# Set symbol for r...
																	for equiv in equivalences2:
																		if [me, 'r'] in equiv[0]:
																			equiv[1] = symbol_r_name
																	# Set symbol for se...
																	for equiv in equivalences2:
																		if [me, 'se'] in equiv[0]:
																			equiv[1] = symbol_se_name
																	# Set symbol for po...
																	for equiv in equivalences2:
																		if [me, 'po'] in equiv[0]:
																			equiv[1] = symbol_po_name
																	# Set symbol for c...
																	for equiv in equivalences2:
																		if [me, 'c'] in equiv[0]:
																			equiv[1] = symbol_c_name
																	# Set symbol for other...
																	for equiv in equivalences2:
																		if [me, 'other'] in equiv[0]:
																			equiv[1] = symbol_other_name
																	newNode = WorldStateHistory(r1)
																	global lastNodeId
																	lastNodeId += 1
																	newNode.nodeId = lastNodeId
																	newNode.parentId = snode.nodeId
																	derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																	if 'fina' in locals():
																		for n in derivsx: n.history.append(finishesCombo)
																		for n in derivsx: n.history.append(fina)
																	ret.extend(derivsx)
		return ret
		
		

	# Rule recognizeObjMug
	def recognizeObjMug_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjMug_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger3 ')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger4 ')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger5 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger6 ')
			test_symbol_other = snode.graph.nodes[n2id['other']]
			if not (test_symbol_other.sType == 'object' and test_symbol_other.name!=test_symbol_s.name and test_symbol_other.name!=test_symbol_o.name and test_symbol_other.name!=test_symbol_r.name and test_symbol_other.name!=test_symbol_se.name and test_symbol_other.name!=test_symbol_po.name and test_symbol_other.name!=test_symbol_c.name):
				raise WrongRuleExecution('recognizeObjMug_trigger7 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['m'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'mug')
		# Retype nodes
		newNode.graph.nodes[n2id['c']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['m'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['s'], smap['other'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('recognizeObjMug@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule recognizeObjBox
	def recognizeObjBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for other
			symbol_other_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'other'] in equiv[0]:
					if equiv[1] != None:
						symbol_other_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for po
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'po'] in equiv[0]:
					if equiv[1] != None:
						symbol_po_nodes = [equiv[1]]
			# Find equivalence for se
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'se'] in equiv[0]:
					if equiv[1] != None:
						symbol_se_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_other_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in symbol_se_nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in symbol_po_nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in symbol_c_nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														for symbol_other_name in symbol_other_nodes:
															symbol_other = nodes[symbol_other_name]
															n2id['other'] = symbol_other_name
															if symbol_other.sType == 'object' and symbol_other.name!=symbol_s.name and symbol_other.name!=symbol_o.name and symbol_other.name!=symbol_r.name and symbol_other.name!=symbol_se.name and symbol_other.name!=symbol_po.name and symbol_other.name!=symbol_c.name:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																stack2        = copy.deepcopy(stack)
																equivalences2 = copy.deepcopy(equivalences)
																r1 = self.recognizeObjBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																c = copy.deepcopy(r1)
																if 'fina' in locals():
																	c.history.append(finishesCombo)
																if len(stack2) > 0: c.stop = True
																ret.append(c)
																if len(stack2) > 0:
																	# Set symbol for s...
																	for equiv in equivalences2:
																		if [me, 's'] in equiv[0]:
																			equiv[1] = symbol_s_name
																	# Set symbol for o...
																	for equiv in equivalences2:
																		if [me, 'o'] in equiv[0]:
																			equiv[1] = symbol_o_name
																	# Set symbol for r...
																	for equiv in equivalences2:
																		if [me, 'r'] in equiv[0]:
																			equiv[1] = symbol_r_name
																	# Set symbol for se...
																	for equiv in equivalences2:
																		if [me, 'se'] in equiv[0]:
																			equiv[1] = symbol_se_name
																	# Set symbol for po...
																	for equiv in equivalences2:
																		if [me, 'po'] in equiv[0]:
																			equiv[1] = symbol_po_name
																	# Set symbol for c...
																	for equiv in equivalences2:
																		if [me, 'c'] in equiv[0]:
																			equiv[1] = symbol_c_name
																	# Set symbol for other...
																	for equiv in equivalences2:
																		if [me, 'other'] in equiv[0]:
																			equiv[1] = symbol_other_name
																	newNode = WorldStateHistory(r1)
																	global lastNodeId
																	lastNodeId += 1
																	newNode.nodeId = lastNodeId
																	newNode.parentId = snode.nodeId
																	derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																	if 'fina' in locals():
																		for n in derivsx: n.history.append(finishesCombo)
																		for n in derivsx: n.history.append(fina)
																	ret.extend(derivsx)
		return ret
		
		

	# Rule recognizeObjBox
	def recognizeObjBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjBox_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger3 ')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger4 ')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger5 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger6 ')
			test_symbol_other = snode.graph.nodes[n2id['other']]
			if not (test_symbol_other.sType == 'object' and test_symbol_other.name!=test_symbol_s.name and test_symbol_other.name!=test_symbol_o.name and test_symbol_other.name!=test_symbol_r.name and test_symbol_other.name!=test_symbol_se.name and test_symbol_other.name!=test_symbol_po.name and test_symbol_other.name!=test_symbol_c.name):
				raise WrongRuleExecution('recognizeObjBox_trigger7 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['m'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'box')
		# Retype nodes
		newNode.graph.nodes[n2id['c']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['m'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['s'], smap['other'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('recognizeObjBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule recognizeObjTable
	def recognizeObjTable(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for po
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'po'] in equiv[0]:
					if equiv[1] != None:
						symbol_po_nodes = [equiv[1]]
			# Find equivalence for se
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'se'] in equiv[0]:
					if equiv[1] != None:
						symbol_se_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in symbol_se_nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in symbol_po_nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in symbol_c_nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														stack2        = copy.deepcopy(stack)
														equivalences2 = copy.deepcopy(equivalences)
														r1 = self.recognizeObjTable_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
														c = copy.deepcopy(r1)
														if 'fina' in locals():
															c.history.append(finishesCombo)
														if len(stack2) > 0: c.stop = True
														ret.append(c)
														if len(stack2) > 0:
															# Set symbol for s...
															for equiv in equivalences2:
																if [me, 's'] in equiv[0]:
																	equiv[1] = symbol_s_name
															# Set symbol for o...
															for equiv in equivalences2:
																if [me, 'o'] in equiv[0]:
																	equiv[1] = symbol_o_name
															# Set symbol for r...
															for equiv in equivalences2:
																if [me, 'r'] in equiv[0]:
																	equiv[1] = symbol_r_name
															# Set symbol for se...
															for equiv in equivalences2:
																if [me, 'se'] in equiv[0]:
																	equiv[1] = symbol_se_name
															# Set symbol for po...
															for equiv in equivalences2:
																if [me, 'po'] in equiv[0]:
																	equiv[1] = symbol_po_name
															# Set symbol for c...
															for equiv in equivalences2:
																if [me, 'c'] in equiv[0]:
																	equiv[1] = symbol_c_name
															newNode = WorldStateHistory(r1)
															global lastNodeId
															lastNodeId += 1
															newNode.nodeId = lastNodeId
															newNode.parentId = snode.nodeId
															derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
															if 'fina' in locals():
																for n in derivsx: n.history.append(finishesCombo)
																for n in derivsx: n.history.append(fina)
															ret.extend(derivsx)
		return ret
		
		

	# Rule recognizeObjTable
	def recognizeObjTable_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjTable_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger3 ')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger4 ')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger5 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger6 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['m'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'table')
		# Retype nodes
		newNode.graph.nodes[n2id['c']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['m'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('recognizeObjTable@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule recognizeObjFails
	def recognizeObjFails(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for po
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'po'] in equiv[0]:
					if equiv[1] != None:
						symbol_po_nodes = [equiv[1]]
			# Find equivalence for se
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'se'] in equiv[0]:
					if equiv[1] != None:
						symbol_se_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_po_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_se_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in symbol_se_nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in symbol_po_nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in symbol_c_nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														stack2        = copy.deepcopy(stack)
														equivalences2 = copy.deepcopy(equivalences)
														r1 = self.recognizeObjFails_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
														c = copy.deepcopy(r1)
														if 'fina' in locals():
															c.history.append(finishesCombo)
														if len(stack2) > 0: c.stop = True
														ret.append(c)
														if len(stack2) > 0:
															# Set symbol for s...
															for equiv in equivalences2:
																if [me, 's'] in equiv[0]:
																	equiv[1] = symbol_s_name
															# Set symbol for o...
															for equiv in equivalences2:
																if [me, 'o'] in equiv[0]:
																	equiv[1] = symbol_o_name
															# Set symbol for r...
															for equiv in equivalences2:
																if [me, 'r'] in equiv[0]:
																	equiv[1] = symbol_r_name
															# Set symbol for se...
															for equiv in equivalences2:
																if [me, 'se'] in equiv[0]:
																	equiv[1] = symbol_se_name
															# Set symbol for po...
															for equiv in equivalences2:
																if [me, 'po'] in equiv[0]:
																	equiv[1] = symbol_po_name
															# Set symbol for c...
															for equiv in equivalences2:
																if [me, 'c'] in equiv[0]:
																	equiv[1] = symbol_c_name
															newNode = WorldStateHistory(r1)
															global lastNodeId
															lastNodeId += 1
															newNode.nodeId = lastNodeId
															newNode.parentId = snode.nodeId
															derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
															if 'fina' in locals():
																for n in derivsx: n.history.append(finishesCombo)
																for n in derivsx: n.history.append(fina)
															ret.extend(derivsx)
		return ret
		
		

	# Rule recognizeObjFails
	def recognizeObjFails_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjFails_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger3 ')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger4 ')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger5 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger6 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['c']].sType = 'classifailed'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('recognizeObjFails@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule setObjectReach
	def setObjectReach(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for rb
			symbol_rb_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'rb'] in equiv[0]:
					if equiv[1] != None:
						symbol_rb_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
		else:
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_rb_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_rb_name in symbol_rb_nodes:
							symbol_rb = nodes[symbol_rb_name]
							n2id['rb'] = symbol_rb_name
							if symbol_rb.sType == 'reachable' and symbol_rb.name!=symbol_s.name and symbol_rb.name!=symbol_o.name and [n2id["s"],n2id["rb"],"link"] in snode.graph.links:
								for symbol_r_name in symbol_r_nodes:
									symbol_r = nodes[symbol_r_name]
									n2id['r'] = symbol_r_name
									if symbol_r.sType == 'notReach' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and symbol_r.name!=symbol_rb.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
										# At this point we meet all the conditions.
										# Insert additional conditions manually here if you want.
										# (beware that the code could be regenerated and you might lose your changes).
										stack2        = copy.deepcopy(stack)
										equivalences2 = copy.deepcopy(equivalences)
										r1 = self.setObjectReach_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
										c = copy.deepcopy(r1)
										if 'fina' in locals():
											c.history.append(finishesCombo)
										if len(stack2) > 0: c.stop = True
										ret.append(c)
										if len(stack2) > 0:
											# Set symbol for s...
											for equiv in equivalences2:
												if [me, 's'] in equiv[0]:
													equiv[1] = symbol_s_name
											# Set symbol for o...
											for equiv in equivalences2:
												if [me, 'o'] in equiv[0]:
													equiv[1] = symbol_o_name
											# Set symbol for rb...
											for equiv in equivalences2:
												if [me, 'rb'] in equiv[0]:
													equiv[1] = symbol_rb_name
											# Set symbol for r...
											for equiv in equivalences2:
												if [me, 'r'] in equiv[0]:
													equiv[1] = symbol_r_name
											newNode = WorldStateHistory(r1)
											global lastNodeId
											lastNodeId += 1
											newNode.nodeId = lastNodeId
											newNode.parentId = snode.nodeId
											derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
											if 'fina' in locals():
												for n in derivsx: n.history.append(finishesCombo)
												for n in derivsx: n.history.append(fina)
											ret.extend(derivsx)
		return ret
		
		

	# Rule setObjectReach
	def setObjectReach_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectReach_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger2 ')
			test_symbol_rb = snode.graph.nodes[n2id['rb']]
			if not (test_symbol_rb.sType == 'reachable' and test_symbol_rb.name!=test_symbol_s.name and test_symbol_rb.name!=test_symbol_o.name and [n2id["s"],n2id["rb"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger3 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notReach' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and test_symbol_r.name!=test_symbol_rb.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger4 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['r']].sType = 'reach'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('setObjectReach@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule setObjectSee
	def setObjectSee(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
		else:
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'notSee' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
								# At this point we meet all the conditions.
								# Insert additional conditions manually here if you want.
								# (beware that the code could be regenerated and you might lose your changes).
								stack2        = copy.deepcopy(stack)
								equivalences2 = copy.deepcopy(equivalences)
								r1 = self.setObjectSee_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
								c = copy.deepcopy(r1)
								if 'fina' in locals():
									c.history.append(finishesCombo)
								if len(stack2) > 0: c.stop = True
								ret.append(c)
								if len(stack2) > 0:
									# Set symbol for s...
									for equiv in equivalences2:
										if [me, 's'] in equiv[0]:
											equiv[1] = symbol_s_name
									# Set symbol for o...
									for equiv in equivalences2:
										if [me, 'o'] in equiv[0]:
											equiv[1] = symbol_o_name
									# Set symbol for r...
									for equiv in equivalences2:
										if [me, 'r'] in equiv[0]:
											equiv[1] = symbol_r_name
									newNode = WorldStateHistory(r1)
									global lastNodeId
									lastNodeId += 1
									newNode.nodeId = lastNodeId
									newNode.parentId = snode.nodeId
									derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
									if 'fina' in locals():
										for n in derivsx: n.history.append(finishesCombo)
										for n in derivsx: n.history.append(fina)
									ret.extend(derivsx)
		return ret
		
		

	# Rule setObjectSee
	def setObjectSee_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectSee_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectSee_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notSee' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectSee_trigger3 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['r']].sType = 'see'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('setObjectSee@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule setObjectPosition
	def setObjectPosition(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
		else:
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'notPosition' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
								# At this point we meet all the conditions.
								# Insert additional conditions manually here if you want.
								# (beware that the code could be regenerated and you might lose your changes).
								stack2        = copy.deepcopy(stack)
								equivalences2 = copy.deepcopy(equivalences)
								r1 = self.setObjectPosition_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
								c = copy.deepcopy(r1)
								if 'fina' in locals():
									c.history.append(finishesCombo)
								if len(stack2) > 0: c.stop = True
								ret.append(c)
								if len(stack2) > 0:
									# Set symbol for s...
									for equiv in equivalences2:
										if [me, 's'] in equiv[0]:
											equiv[1] = symbol_s_name
									# Set symbol for o...
									for equiv in equivalences2:
										if [me, 'o'] in equiv[0]:
											equiv[1] = symbol_o_name
									# Set symbol for r...
									for equiv in equivalences2:
										if [me, 'r'] in equiv[0]:
											equiv[1] = symbol_r_name
									newNode = WorldStateHistory(r1)
									global lastNodeId
									lastNodeId += 1
									newNode.nodeId = lastNodeId
									newNode.parentId = snode.nodeId
									derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
									if 'fina' in locals():
										for n in derivsx: n.history.append(finishesCombo)
										for n in derivsx: n.history.append(fina)
									ret.extend(derivsx)
		return ret
		
		

	# Rule setObjectPosition
	def setObjectPosition_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectPosition_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectPosition_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notPosition' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectPosition_trigger3 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['r']].sType = 'position'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('setObjectPosition@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule tellHumanAboutMug
	def tellHumanAboutMug(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for sr
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'sr'] in equiv[0]:
					if equiv[1] != None:
						symbol_sr_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont1
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont1_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_sr_name in symbol_sr_nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in symbol_o_nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_cont1_name in symbol_cont1_nodes:
									symbol_cont1 = nodes[symbol_cont1_name]
									n2id['cont1'] = symbol_cont1_name
									if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_sr.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links:
										for symbol_p_name in symbol_p_nodes:
											symbol_p = nodes[symbol_p_name]
											n2id['p'] = symbol_p_name
											if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
												for symbol_m_name in symbol_m_nodes:
													symbol_m = nodes[symbol_m_name]
													n2id['m'] = symbol_m_name
													if symbol_m.sType == 'mug' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_cont1.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
														for symbol_h_name in symbol_h_nodes:
															symbol_h = nodes[symbol_h_name]
															n2id['h'] = symbol_h_name
															if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_cont1.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
																for symbol_cont2_name in symbol_cont2_nodes:
																	symbol_cont2 = nodes[symbol_cont2_name]
																	n2id['cont2'] = symbol_cont2_name
																	if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_sr.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_cont1.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_m.name and symbol_cont2.name!=symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_c_name in symbol_c_nodes:
																			symbol_c = nodes[symbol_c_name]
																			n2id['c'] = symbol_c_name
																			if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_cont1.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and symbol_c.name!=symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				stack2        = copy.deepcopy(stack)
																				equivalences2 = copy.deepcopy(equivalences)
																				r1 = self.tellHumanAboutMug_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																				c = copy.deepcopy(r1)
																				if 'fina' in locals():
																					c.history.append(finishesCombo)
																				if len(stack2) > 0: c.stop = True
																				ret.append(c)
																				if len(stack2) > 0:
																					# Set symbol for sr...
																					for equiv in equivalences2:
																						if [me, 'sr'] in equiv[0]:
																							equiv[1] = symbol_sr_name
																					# Set symbol for r...
																					for equiv in equivalences2:
																						if [me, 'r'] in equiv[0]:
																							equiv[1] = symbol_r_name
																					# Set symbol for o...
																					for equiv in equivalences2:
																						if [me, 'o'] in equiv[0]:
																							equiv[1] = symbol_o_name
																					# Set symbol for cont1...
																					for equiv in equivalences2:
																						if [me, 'cont1'] in equiv[0]:
																							equiv[1] = symbol_cont1_name
																					# Set symbol for p...
																					for equiv in equivalences2:
																						if [me, 'p'] in equiv[0]:
																							equiv[1] = symbol_p_name
																					# Set symbol for m...
																					for equiv in equivalences2:
																						if [me, 'm'] in equiv[0]:
																							equiv[1] = symbol_m_name
																					# Set symbol for h...
																					for equiv in equivalences2:
																						if [me, 'h'] in equiv[0]:
																							equiv[1] = symbol_h_name
																					# Set symbol for cont2...
																					for equiv in equivalences2:
																						if [me, 'cont2'] in equiv[0]:
																							equiv[1] = symbol_cont2_name
																					# Set symbol for c...
																					for equiv in equivalences2:
																						if [me, 'c'] in equiv[0]:
																							equiv[1] = symbol_c_name
																					newNode = WorldStateHistory(r1)
																					global lastNodeId
																					lastNodeId += 1
																					newNode.nodeId = lastNodeId
																					newNode.parentId = snode.nodeId
																					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																					if 'fina' in locals():
																						for n in derivsx: n.history.append(finishesCombo)
																						for n in derivsx: n.history.append(fina)
																					ret.extend(derivsx)
		return ret
		
		

	# Rule tellHumanAboutMug
	def tellHumanAboutMug_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutMug_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutMug_trigger2 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger3 ')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_sr.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger4 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger5 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_cont1.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger6 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_cont1.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger7 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_sr.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_cont1.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_m.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger8 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_cont1.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and test_symbol_c.name!=test_symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger9 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['ch'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'classified')
		newName = str(getNewIdForSymbol(newNode))
		smap['oh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['hr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reach')
		newName = str(getNewIdForSymbol(newNode))
		smap['mh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'mug')
		newName = str(getNewIdForSymbol(newNode))
		smap['sh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['ph'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'position')
		newName = str(getNewIdForSymbol(newNode))
		smap['hs'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'see')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['h'], smap['oh'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['oh'], smap['sh'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ch'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ph'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['mh'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['o'], smap['oh'], 'eq')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['cont2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hs'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('tellHumanAboutMug@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule tellHumanAboutBox
	def tellHumanAboutBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for sr
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'sr'] in equiv[0]:
					if equiv[1] != None:
						symbol_sr_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont1
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont1_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_sr_name in symbol_sr_nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in symbol_o_nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_cont1_name in symbol_cont1_nodes:
									symbol_cont1 = nodes[symbol_cont1_name]
									n2id['cont1'] = symbol_cont1_name
									if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_sr.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links:
										for symbol_p_name in symbol_p_nodes:
											symbol_p = nodes[symbol_p_name]
											n2id['p'] = symbol_p_name
											if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
												for symbol_m_name in symbol_m_nodes:
													symbol_m = nodes[symbol_m_name]
													n2id['m'] = symbol_m_name
													if symbol_m.sType == 'box' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_cont1.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
														for symbol_h_name in symbol_h_nodes:
															symbol_h = nodes[symbol_h_name]
															n2id['h'] = symbol_h_name
															if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_cont1.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
																for symbol_cont2_name in symbol_cont2_nodes:
																	symbol_cont2 = nodes[symbol_cont2_name]
																	n2id['cont2'] = symbol_cont2_name
																	if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_sr.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_cont1.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_m.name and symbol_cont2.name!=symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_c_name in symbol_c_nodes:
																			symbol_c = nodes[symbol_c_name]
																			n2id['c'] = symbol_c_name
																			if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_cont1.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and symbol_c.name!=symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				stack2        = copy.deepcopy(stack)
																				equivalences2 = copy.deepcopy(equivalences)
																				r1 = self.tellHumanAboutBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																				c = copy.deepcopy(r1)
																				if 'fina' in locals():
																					c.history.append(finishesCombo)
																				if len(stack2) > 0: c.stop = True
																				ret.append(c)
																				if len(stack2) > 0:
																					# Set symbol for sr...
																					for equiv in equivalences2:
																						if [me, 'sr'] in equiv[0]:
																							equiv[1] = symbol_sr_name
																					# Set symbol for r...
																					for equiv in equivalences2:
																						if [me, 'r'] in equiv[0]:
																							equiv[1] = symbol_r_name
																					# Set symbol for o...
																					for equiv in equivalences2:
																						if [me, 'o'] in equiv[0]:
																							equiv[1] = symbol_o_name
																					# Set symbol for cont1...
																					for equiv in equivalences2:
																						if [me, 'cont1'] in equiv[0]:
																							equiv[1] = symbol_cont1_name
																					# Set symbol for p...
																					for equiv in equivalences2:
																						if [me, 'p'] in equiv[0]:
																							equiv[1] = symbol_p_name
																					# Set symbol for m...
																					for equiv in equivalences2:
																						if [me, 'm'] in equiv[0]:
																							equiv[1] = symbol_m_name
																					# Set symbol for h...
																					for equiv in equivalences2:
																						if [me, 'h'] in equiv[0]:
																							equiv[1] = symbol_h_name
																					# Set symbol for cont2...
																					for equiv in equivalences2:
																						if [me, 'cont2'] in equiv[0]:
																							equiv[1] = symbol_cont2_name
																					# Set symbol for c...
																					for equiv in equivalences2:
																						if [me, 'c'] in equiv[0]:
																							equiv[1] = symbol_c_name
																					newNode = WorldStateHistory(r1)
																					global lastNodeId
																					lastNodeId += 1
																					newNode.nodeId = lastNodeId
																					newNode.parentId = snode.nodeId
																					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																					if 'fina' in locals():
																						for n in derivsx: n.history.append(finishesCombo)
																						for n in derivsx: n.history.append(fina)
																					ret.extend(derivsx)
		return ret
		
		

	# Rule tellHumanAboutBox
	def tellHumanAboutBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutBox_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutBox_trigger2 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger3 ')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_sr.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger4 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger5 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'box' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_cont1.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger6 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_cont1.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger7 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_sr.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_cont1.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_m.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger8 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_cont1.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and test_symbol_c.name!=test_symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger9 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['ch'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'classified')
		newName = str(getNewIdForSymbol(newNode))
		smap['oh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['hr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reach')
		newName = str(getNewIdForSymbol(newNode))
		smap['mh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'box')
		newName = str(getNewIdForSymbol(newNode))
		smap['sh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['ph'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'position')
		newName = str(getNewIdForSymbol(newNode))
		smap['hs'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'see')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['h'], smap['oh'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['oh'], smap['sh'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ch'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ph'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['mh'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['o'], smap['oh'], 'eq')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['cont2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hs'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('tellHumanAboutBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule tellHumanAboutTable
	def tellHumanAboutTable(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for sr
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'sr'] in equiv[0]:
					if equiv[1] != None:
						symbol_sr_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_sr_name in symbol_sr_nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in symbol_o_nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_p_name in symbol_p_nodes:
									symbol_p = nodes[symbol_p_name]
									n2id['p'] = symbol_p_name
									if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
										for symbol_m_name in symbol_m_nodes:
											symbol_m = nodes[symbol_m_name]
											n2id['m'] = symbol_m_name
											if symbol_m.sType == 'table' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
												for symbol_h_name in symbol_h_nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
														for symbol_c_name in symbol_c_nodes:
															symbol_c = nodes[symbol_c_name]
															n2id['c'] = symbol_c_name
															if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																stack2        = copy.deepcopy(stack)
																equivalences2 = copy.deepcopy(equivalences)
																r1 = self.tellHumanAboutTable_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																c = copy.deepcopy(r1)
																if 'fina' in locals():
																	c.history.append(finishesCombo)
																if len(stack2) > 0: c.stop = True
																ret.append(c)
																if len(stack2) > 0:
																	# Set symbol for sr...
																	for equiv in equivalences2:
																		if [me, 'sr'] in equiv[0]:
																			equiv[1] = symbol_sr_name
																	# Set symbol for r...
																	for equiv in equivalences2:
																		if [me, 'r'] in equiv[0]:
																			equiv[1] = symbol_r_name
																	# Set symbol for o...
																	for equiv in equivalences2:
																		if [me, 'o'] in equiv[0]:
																			equiv[1] = symbol_o_name
																	# Set symbol for p...
																	for equiv in equivalences2:
																		if [me, 'p'] in equiv[0]:
																			equiv[1] = symbol_p_name
																	# Set symbol for m...
																	for equiv in equivalences2:
																		if [me, 'm'] in equiv[0]:
																			equiv[1] = symbol_m_name
																	# Set symbol for h...
																	for equiv in equivalences2:
																		if [me, 'h'] in equiv[0]:
																			equiv[1] = symbol_h_name
																	# Set symbol for c...
																	for equiv in equivalences2:
																		if [me, 'c'] in equiv[0]:
																			equiv[1] = symbol_c_name
																	newNode = WorldStateHistory(r1)
																	global lastNodeId
																	lastNodeId += 1
																	newNode.nodeId = lastNodeId
																	newNode.parentId = snode.nodeId
																	derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																	if 'fina' in locals():
																		for n in derivsx: n.history.append(finishesCombo)
																		for n in derivsx: n.history.append(fina)
																	ret.extend(derivsx)
		return ret
		
		

	# Rule tellHumanAboutTable
	def tellHumanAboutTable_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutTable_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutTable_trigger2 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger3 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger4 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'table' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger5 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger6 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger7 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['ch'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'classified')
		newName = str(getNewIdForSymbol(newNode))
		smap['oh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['hr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reach')
		newName = str(getNewIdForSymbol(newNode))
		smap['mh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'table')
		newName = str(getNewIdForSymbol(newNode))
		smap['sh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['hs'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'see')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['ph'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'position')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['h'], smap['oh'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['oh'], smap['sh'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ch'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ph'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['mh'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['o'], smap['oh'], 'eq')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['hs'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('tellHumanAboutTable@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule tellHumanAboutUnknownObject
	def tellHumanAboutUnknownObject(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for c
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c'] in equiv[0]:
					if equiv[1] != None:
						symbol_c_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for sr
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'sr'] in equiv[0]:
					if equiv[1] != None:
						symbol_sr_nodes = [equiv[1]]
		else:
			symbol_c_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_sr_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_sr_name in symbol_sr_nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in symbol_o_nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_p_name in symbol_p_nodes:
									symbol_p = nodes[symbol_p_name]
									n2id['p'] = symbol_p_name
									if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
										for symbol_h_name in symbol_h_nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_p.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
												for symbol_c_name in symbol_c_nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'classifailed' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														stack2        = copy.deepcopy(stack)
														equivalences2 = copy.deepcopy(equivalences)
														r1 = self.tellHumanAboutUnknownObject_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
														c = copy.deepcopy(r1)
														if 'fina' in locals():
															c.history.append(finishesCombo)
														if len(stack2) > 0: c.stop = True
														ret.append(c)
														if len(stack2) > 0:
															# Set symbol for sr...
															for equiv in equivalences2:
																if [me, 'sr'] in equiv[0]:
																	equiv[1] = symbol_sr_name
															# Set symbol for r...
															for equiv in equivalences2:
																if [me, 'r'] in equiv[0]:
																	equiv[1] = symbol_r_name
															# Set symbol for o...
															for equiv in equivalences2:
																if [me, 'o'] in equiv[0]:
																	equiv[1] = symbol_o_name
															# Set symbol for p...
															for equiv in equivalences2:
																if [me, 'p'] in equiv[0]:
																	equiv[1] = symbol_p_name
															# Set symbol for h...
															for equiv in equivalences2:
																if [me, 'h'] in equiv[0]:
																	equiv[1] = symbol_h_name
															# Set symbol for c...
															for equiv in equivalences2:
																if [me, 'c'] in equiv[0]:
																	equiv[1] = symbol_c_name
															newNode = WorldStateHistory(r1)
															global lastNodeId
															lastNodeId += 1
															newNode.nodeId = lastNodeId
															newNode.parentId = snode.nodeId
															derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
															if 'fina' in locals():
																for n in derivsx: n.history.append(finishesCombo)
																for n in derivsx: n.history.append(fina)
															ret.extend(derivsx)
		return ret
		
		

	# Rule tellHumanAboutUnknownObject
	def tellHumanAboutUnknownObject_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger2 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger3 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger4 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_p.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger5 ')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classifailed' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger6 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['ch'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'unclassified')
		newName = str(getNewIdForSymbol(newNode))
		smap['oh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'object')
		newName = str(getNewIdForSymbol(newNode))
		smap['sh'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'status')
		newName = str(getNewIdForSymbol(newNode))
		smap['rb'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'reachable')
		newName = str(getNewIdForSymbol(newNode))
		smap['ph'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'position')
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['h'], smap['oh'], 'know')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['oh'], smap['sh'], 'has')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ch'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['ph'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['o'], smap['oh'], 'eq')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['sh'], smap['rb'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 3
			newNode.depth += 1
		newNode.history.append('tellHumanAboutUnknownObject@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule makeHumanLook
	def makeHumanLook(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for nS
			symbol_nS_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'nS'] in equiv[0]:
					if equiv[1] != None:
						symbol_nS_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_nS_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in symbol_o_h_nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in symbol_o_nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in symbol_h_nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_p_name in symbol_p_nodes:
													symbol_p = nodes[symbol_p_name]
													n2id['p'] = symbol_p_name
													if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
														for symbol_nS_name in symbol_nS_nodes:
															symbol_nS = nodes[symbol_nS_name]
															n2id['nS'] = symbol_nS_name
															if symbol_nS.sType == 'notSee' and symbol_nS.name!=symbol_s.name and symbol_nS.name!=symbol_r.name and symbol_nS.name!=symbol_o_h.name and symbol_nS.name!=symbol_o.name and symbol_nS.name!=symbol_h.name and symbol_nS.name!=symbol_p.name and [n2id["s"],n2id["nS"],"link"] in snode.graph.links:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																stack2        = copy.deepcopy(stack)
																equivalences2 = copy.deepcopy(equivalences)
																r1 = self.makeHumanLook_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																c = copy.deepcopy(r1)
																if 'fina' in locals():
																	c.history.append(finishesCombo)
																if len(stack2) > 0: c.stop = True
																ret.append(c)
																if len(stack2) > 0:
																	# Set symbol for s...
																	for equiv in equivalences2:
																		if [me, 's'] in equiv[0]:
																			equiv[1] = symbol_s_name
																	# Set symbol for r...
																	for equiv in equivalences2:
																		if [me, 'r'] in equiv[0]:
																			equiv[1] = symbol_r_name
																	# Set symbol for o_h...
																	for equiv in equivalences2:
																		if [me, 'o_h'] in equiv[0]:
																			equiv[1] = symbol_o_h_name
																	# Set symbol for o...
																	for equiv in equivalences2:
																		if [me, 'o'] in equiv[0]:
																			equiv[1] = symbol_o_name
																	# Set symbol for h...
																	for equiv in equivalences2:
																		if [me, 'h'] in equiv[0]:
																			equiv[1] = symbol_h_name
																	# Set symbol for p...
																	for equiv in equivalences2:
																		if [me, 'p'] in equiv[0]:
																			equiv[1] = symbol_p_name
																	# Set symbol for nS...
																	for equiv in equivalences2:
																		if [me, 'nS'] in equiv[0]:
																			equiv[1] = symbol_nS_name
																	newNode = WorldStateHistory(r1)
																	global lastNodeId
																	lastNodeId += 1
																	newNode.nodeId = lastNodeId
																	newNode.parentId = snode.nodeId
																	derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																	if 'fina' in locals():
																		for n in derivsx: n.history.append(finishesCombo)
																		for n in derivsx: n.history.append(fina)
																	ret.extend(derivsx)
		return ret
		
		

	# Rule makeHumanLook
	def makeHumanLook_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('makeHumanLook_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('makeHumanLook_trigger2 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger3 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger4 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger5 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger6 ')
			test_symbol_nS = snode.graph.nodes[n2id['nS']]
			if not (test_symbol_nS.sType == 'notSee' and test_symbol_nS.name!=test_symbol_s.name and test_symbol_nS.name!=test_symbol_r.name and test_symbol_nS.name!=test_symbol_o_h.name and test_symbol_nS.name!=test_symbol_o.name and test_symbol_nS.name!=test_symbol_h.name and test_symbol_nS.name!=test_symbol_p.name and [n2id["s"],n2id["nS"],"link"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger7 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['nS']].sType = 'see'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 2
			newNode.depth += 1
		newNode.history.append('makeHumanLook@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanClassifiesMug
	def humanClassifiesMug(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for cl
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cl'] in equiv[0]:
					if equiv[1] != None:
						symbol_cl_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for see
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'see'] in equiv[0]:
					if equiv[1] != None:
						symbol_see_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in symbol_o_h_nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in symbol_o_nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in symbol_h_nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in symbol_see_nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in symbol_p_nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in symbol_cl_nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		for symbol_cont2_name in symbol_cont2_nodes:
																			symbol_cont2 = nodes[symbol_cont2_name]
																			n2id['cont2'] = symbol_cont2_name
																			if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_h.name and symbol_cont2.name!=symbol_see.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_cl.name:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				stack2        = copy.deepcopy(stack)
																				equivalences2 = copy.deepcopy(equivalences)
																				r1 = self.humanClassifiesMug_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																				c = copy.deepcopy(r1)
																				if 'fina' in locals():
																					c.history.append(finishesCombo)
																				if len(stack2) > 0: c.stop = True
																				ret.append(c)
																				if len(stack2) > 0:
																					# Set symbol for s...
																					for equiv in equivalences2:
																						if [me, 's'] in equiv[0]:
																							equiv[1] = symbol_s_name
																					# Set symbol for r...
																					for equiv in equivalences2:
																						if [me, 'r'] in equiv[0]:
																							equiv[1] = symbol_r_name
																					# Set symbol for o_h...
																					for equiv in equivalences2:
																						if [me, 'o_h'] in equiv[0]:
																							equiv[1] = symbol_o_h_name
																					# Set symbol for o...
																					for equiv in equivalences2:
																						if [me, 'o'] in equiv[0]:
																							equiv[1] = symbol_o_name
																					# Set symbol for h...
																					for equiv in equivalences2:
																						if [me, 'h'] in equiv[0]:
																							equiv[1] = symbol_h_name
																					# Set symbol for see...
																					for equiv in equivalences2:
																						if [me, 'see'] in equiv[0]:
																							equiv[1] = symbol_see_name
																					# Set symbol for p...
																					for equiv in equivalences2:
																						if [me, 'p'] in equiv[0]:
																							equiv[1] = symbol_p_name
																					# Set symbol for cl...
																					for equiv in equivalences2:
																						if [me, 'cl'] in equiv[0]:
																							equiv[1] = symbol_cl_name
																					# Set symbol for cont2...
																					for equiv in equivalences2:
																						if [me, 'cont2'] in equiv[0]:
																							equiv[1] = symbol_cont2_name
																					newNode = WorldStateHistory(r1)
																					global lastNodeId
																					lastNodeId += 1
																					newNode.nodeId = lastNodeId
																					newNode.parentId = snode.nodeId
																					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																					if 'fina' in locals():
																						for n in derivsx: n.history.append(finishesCombo)
																						for n in derivsx: n.history.append(fina)
																					ret.extend(derivsx)
		return ret
		
		

	# Rule humanClassifiesMug
	def humanClassifiesMug_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesMug_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesMug_trigger2 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger3 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger4 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger5 ')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger6 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger7 ')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger8 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_h.name and test_symbol_cont2.name!=test_symbol_see.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_cl.name):
				raise WrongRuleExecution('humanClassifiesMug_trigger9 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['cl']].sType = 'mug'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['cont2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 2
			newNode.depth += 1
		newNode.history.append('humanClassifiesMug@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanClassifiesBox
	def humanClassifiesBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for cl
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cl'] in equiv[0]:
					if equiv[1] != None:
						symbol_cl_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for see
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'see'] in equiv[0]:
					if equiv[1] != None:
						symbol_see_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in symbol_o_h_nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in symbol_o_nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in symbol_h_nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in symbol_see_nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in symbol_p_nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in symbol_cl_nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		for symbol_cont2_name in symbol_cont2_nodes:
																			symbol_cont2 = nodes[symbol_cont2_name]
																			n2id['cont2'] = symbol_cont2_name
																			if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_h.name and symbol_cont2.name!=symbol_see.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_cl.name:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				stack2        = copy.deepcopy(stack)
																				equivalences2 = copy.deepcopy(equivalences)
																				r1 = self.humanClassifiesBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																				c = copy.deepcopy(r1)
																				if 'fina' in locals():
																					c.history.append(finishesCombo)
																				if len(stack2) > 0: c.stop = True
																				ret.append(c)
																				if len(stack2) > 0:
																					# Set symbol for s...
																					for equiv in equivalences2:
																						if [me, 's'] in equiv[0]:
																							equiv[1] = symbol_s_name
																					# Set symbol for r...
																					for equiv in equivalences2:
																						if [me, 'r'] in equiv[0]:
																							equiv[1] = symbol_r_name
																					# Set symbol for o_h...
																					for equiv in equivalences2:
																						if [me, 'o_h'] in equiv[0]:
																							equiv[1] = symbol_o_h_name
																					# Set symbol for o...
																					for equiv in equivalences2:
																						if [me, 'o'] in equiv[0]:
																							equiv[1] = symbol_o_name
																					# Set symbol for h...
																					for equiv in equivalences2:
																						if [me, 'h'] in equiv[0]:
																							equiv[1] = symbol_h_name
																					# Set symbol for see...
																					for equiv in equivalences2:
																						if [me, 'see'] in equiv[0]:
																							equiv[1] = symbol_see_name
																					# Set symbol for p...
																					for equiv in equivalences2:
																						if [me, 'p'] in equiv[0]:
																							equiv[1] = symbol_p_name
																					# Set symbol for cl...
																					for equiv in equivalences2:
																						if [me, 'cl'] in equiv[0]:
																							equiv[1] = symbol_cl_name
																					# Set symbol for cont2...
																					for equiv in equivalences2:
																						if [me, 'cont2'] in equiv[0]:
																							equiv[1] = symbol_cont2_name
																					newNode = WorldStateHistory(r1)
																					global lastNodeId
																					lastNodeId += 1
																					newNode.nodeId = lastNodeId
																					newNode.parentId = snode.nodeId
																					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																					if 'fina' in locals():
																						for n in derivsx: n.history.append(finishesCombo)
																						for n in derivsx: n.history.append(fina)
																					ret.extend(derivsx)
		return ret
		
		

	# Rule humanClassifiesBox
	def humanClassifiesBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesBox_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesBox_trigger2 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger3 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger4 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger5 ')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger6 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger7 ')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger8 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_h.name and test_symbol_cont2.name!=test_symbol_see.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_cl.name):
				raise WrongRuleExecution('humanClassifiesBox_trigger9 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['cl']].sType = 'box'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['cont2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 2
			newNode.depth += 1
		newNode.history.append('humanClassifiesBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanClassifiesTable
	def humanClassifiesTable(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for cl
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cl'] in equiv[0]:
					if equiv[1] != None:
						symbol_cl_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for see
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'see'] in equiv[0]:
					if equiv[1] != None:
						symbol_see_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for p
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'p'] in equiv[0]:
					if equiv[1] != None:
						symbol_p_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_cl_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_see_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_p_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in symbol_o_h_nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in symbol_o_nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in symbol_h_nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in symbol_see_nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in symbol_p_nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in symbol_cl_nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		# At this point we meet all the conditions.
																		# Insert additional conditions manually here if you want.
																		# (beware that the code could be regenerated and you might lose your changes).
																		stack2        = copy.deepcopy(stack)
																		equivalences2 = copy.deepcopy(equivalences)
																		r1 = self.humanClassifiesTable_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																		c = copy.deepcopy(r1)
																		if 'fina' in locals():
																			c.history.append(finishesCombo)
																		if len(stack2) > 0: c.stop = True
																		ret.append(c)
																		if len(stack2) > 0:
																			# Set symbol for s...
																			for equiv in equivalences2:
																				if [me, 's'] in equiv[0]:
																					equiv[1] = symbol_s_name
																			# Set symbol for r...
																			for equiv in equivalences2:
																				if [me, 'r'] in equiv[0]:
																					equiv[1] = symbol_r_name
																			# Set symbol for o_h...
																			for equiv in equivalences2:
																				if [me, 'o_h'] in equiv[0]:
																					equiv[1] = symbol_o_h_name
																			# Set symbol for o...
																			for equiv in equivalences2:
																				if [me, 'o'] in equiv[0]:
																					equiv[1] = symbol_o_name
																			# Set symbol for h...
																			for equiv in equivalences2:
																				if [me, 'h'] in equiv[0]:
																					equiv[1] = symbol_h_name
																			# Set symbol for see...
																			for equiv in equivalences2:
																				if [me, 'see'] in equiv[0]:
																					equiv[1] = symbol_see_name
																			# Set symbol for p...
																			for equiv in equivalences2:
																				if [me, 'p'] in equiv[0]:
																					equiv[1] = symbol_p_name
																			# Set symbol for cl...
																			for equiv in equivalences2:
																				if [me, 'cl'] in equiv[0]:
																					equiv[1] = symbol_cl_name
																			newNode = WorldStateHistory(r1)
																			global lastNodeId
																			lastNodeId += 1
																			newNode.nodeId = lastNodeId
																			newNode.parentId = snode.nodeId
																			derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																			if 'fina' in locals():
																				for n in derivsx: n.history.append(finishesCombo)
																				for n in derivsx: n.history.append(fina)
																			ret.extend(derivsx)
		return ret
		
		

	# Rule humanClassifiesTable
	def humanClassifiesTable_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesTable_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesTable_trigger2 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger3 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger4 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger5 ')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger6 ')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger7 ')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger8 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		newNode.graph.nodes[n2id['cl']].sType = 'table'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 2
			newNode.depth += 1
		newNode.history.append('humanClassifiesTable@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanTellsUsAboutMug
	def humanTellsUsAboutMug(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for ch
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'ch'] in equiv[0]:
					if equiv[1] != None:
						symbol_ch_nodes = [equiv[1]]
			# Find equivalence for f
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'f'] in equiv[0]:
					if equiv[1] != None:
						symbol_f_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for soh
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'soh'] in equiv[0]:
					if equiv[1] != None:
						symbol_soh_nodes = [equiv[1]]
			# Find equivalence for mh
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'mh'] in equiv[0]:
					if equiv[1] != None:
						symbol_mh_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont1
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont1_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_soh_name in symbol_soh_nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in symbol_o_h_nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in symbol_s_nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in symbol_h_nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_cont2_name in symbol_cont2_nodes:
															symbol_cont2 = nodes[symbol_cont2_name]
															n2id['cont2'] = symbol_cont2_name
															if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_soh.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links:
																for symbol_cont1_name in symbol_cont1_nodes:
																	symbol_cont1 = nodes[symbol_cont1_name]
																	n2id['cont1'] = symbol_cont1_name
																	if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_soh.name and symbol_cont1.name!=symbol_o.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o_h.name and symbol_cont1.name!=symbol_s.name and symbol_cont1.name!=symbol_h.name and symbol_cont1.name!=symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_mh_name in symbol_mh_nodes:
																			symbol_mh = nodes[symbol_mh_name]
																			n2id['mh'] = symbol_mh_name
																			if symbol_mh.sType == 'mug' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and symbol_mh.name!=symbol_cont2.name and symbol_mh.name!=symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																				for symbol_f_name in symbol_f_nodes:
																					symbol_f = nodes[symbol_f_name]
																					n2id['f'] = symbol_f_name
																					if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_cont2.name and symbol_f.name!=symbol_cont1.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																						for symbol_ch_name in symbol_ch_nodes:
																							symbol_ch = nodes[symbol_ch_name]
																							n2id['ch'] = symbol_ch_name
																							if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_cont2.name and symbol_ch.name!=symbol_cont1.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																								# At this point we meet all the conditions.
																								# Insert additional conditions manually here if you want.
																								# (beware that the code could be regenerated and you might lose your changes).
																								stack2        = copy.deepcopy(stack)
																								equivalences2 = copy.deepcopy(equivalences)
																								r1 = self.humanTellsUsAboutMug_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																								c = copy.deepcopy(r1)
																								if 'fina' in locals():
																									c.history.append(finishesCombo)
																								if len(stack2) > 0: c.stop = True
																								ret.append(c)
																								if len(stack2) > 0:
																									# Set symbol for soh...
																									for equiv in equivalences2:
																										if [me, 'soh'] in equiv[0]:
																											equiv[1] = symbol_soh_name
																									# Set symbol for o...
																									for equiv in equivalences2:
																										if [me, 'o'] in equiv[0]:
																											equiv[1] = symbol_o_name
																									# Set symbol for r...
																									for equiv in equivalences2:
																										if [me, 'r'] in equiv[0]:
																											equiv[1] = symbol_r_name
																									# Set symbol for o_h...
																									for equiv in equivalences2:
																										if [me, 'o_h'] in equiv[0]:
																											equiv[1] = symbol_o_h_name
																									# Set symbol for s...
																									for equiv in equivalences2:
																										if [me, 's'] in equiv[0]:
																											equiv[1] = symbol_s_name
																									# Set symbol for h...
																									for equiv in equivalences2:
																										if [me, 'h'] in equiv[0]:
																											equiv[1] = symbol_h_name
																									# Set symbol for cont2...
																									for equiv in equivalences2:
																										if [me, 'cont2'] in equiv[0]:
																											equiv[1] = symbol_cont2_name
																									# Set symbol for cont1...
																									for equiv in equivalences2:
																										if [me, 'cont1'] in equiv[0]:
																											equiv[1] = symbol_cont1_name
																									# Set symbol for mh...
																									for equiv in equivalences2:
																										if [me, 'mh'] in equiv[0]:
																											equiv[1] = symbol_mh_name
																									# Set symbol for f...
																									for equiv in equivalences2:
																										if [me, 'f'] in equiv[0]:
																											equiv[1] = symbol_f_name
																									# Set symbol for ch...
																									for equiv in equivalences2:
																										if [me, 'ch'] in equiv[0]:
																											equiv[1] = symbol_ch_name
																									newNode = WorldStateHistory(r1)
																									global lastNodeId
																									lastNodeId += 1
																									newNode.nodeId = lastNodeId
																									newNode.parentId = snode.nodeId
																									derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																									if 'fina' in locals():
																										for n in derivsx: n.history.append(finishesCombo)
																										for n in derivsx: n.history.append(fina)
																									ret.extend(derivsx)
		return ret
		
		

	# Rule humanTellsUsAboutMug
	def humanTellsUsAboutMug_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger3 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger4 ')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger5 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger6 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_soh.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger7 ')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_soh.name and test_symbol_cont1.name!=test_symbol_o.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o_h.name and test_symbol_cont1.name!=test_symbol_s.name and test_symbol_cont1.name!=test_symbol_h.name and test_symbol_cont1.name!=test_symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger8 ')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'mug' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and test_symbol_mh.name!=test_symbol_cont2.name and test_symbol_mh.name!=test_symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger9 ')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_cont2.name and test_symbol_f.name!=test_symbol_cont1.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger10 ')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_cont2.name and test_symbol_ch.name!=test_symbol_cont1.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger11 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['mr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'mug')
		# Retype nodes
		newNode.graph.nodes[n2id['f']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['mr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['s'], smap['cont1'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 3
			newNode.depth += 1
		newNode.history.append('humanTellsUsAboutMug@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanTellsUsAboutBox
	def humanTellsUsAboutBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for ch
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'ch'] in equiv[0]:
					if equiv[1] != None:
						symbol_ch_nodes = [equiv[1]]
			# Find equivalence for f
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'f'] in equiv[0]:
					if equiv[1] != None:
						symbol_f_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for cont2
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont2_nodes = [equiv[1]]
			# Find equivalence for mh
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'mh'] in equiv[0]:
					if equiv[1] != None:
						symbol_mh_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for cont1
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cont1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cont1_nodes = [equiv[1]]
			# Find equivalence for soh
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'soh'] in equiv[0]:
					if equiv[1] != None:
						symbol_soh_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cont1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_soh_name in symbol_soh_nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in symbol_o_h_nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in symbol_s_nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in symbol_h_nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_cont2_name in symbol_cont2_nodes:
															symbol_cont2 = nodes[symbol_cont2_name]
															n2id['cont2'] = symbol_cont2_name
															if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_soh.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links:
																for symbol_cont1_name in symbol_cont1_nodes:
																	symbol_cont1 = nodes[symbol_cont1_name]
																	n2id['cont1'] = symbol_cont1_name
																	if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_soh.name and symbol_cont1.name!=symbol_o.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o_h.name and symbol_cont1.name!=symbol_s.name and symbol_cont1.name!=symbol_h.name and symbol_cont1.name!=symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_mh_name in symbol_mh_nodes:
																			symbol_mh = nodes[symbol_mh_name]
																			n2id['mh'] = symbol_mh_name
																			if symbol_mh.sType == 'box' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and symbol_mh.name!=symbol_cont2.name and symbol_mh.name!=symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																				for symbol_f_name in symbol_f_nodes:
																					symbol_f = nodes[symbol_f_name]
																					n2id['f'] = symbol_f_name
																					if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_cont2.name and symbol_f.name!=symbol_cont1.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																						for symbol_ch_name in symbol_ch_nodes:
																							symbol_ch = nodes[symbol_ch_name]
																							n2id['ch'] = symbol_ch_name
																							if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_cont2.name and symbol_ch.name!=symbol_cont1.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																								# At this point we meet all the conditions.
																								# Insert additional conditions manually here if you want.
																								# (beware that the code could be regenerated and you might lose your changes).
																								stack2        = copy.deepcopy(stack)
																								equivalences2 = copy.deepcopy(equivalences)
																								r1 = self.humanTellsUsAboutBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																								c = copy.deepcopy(r1)
																								if 'fina' in locals():
																									c.history.append(finishesCombo)
																								if len(stack2) > 0: c.stop = True
																								ret.append(c)
																								if len(stack2) > 0:
																									# Set symbol for soh...
																									for equiv in equivalences2:
																										if [me, 'soh'] in equiv[0]:
																											equiv[1] = symbol_soh_name
																									# Set symbol for o...
																									for equiv in equivalences2:
																										if [me, 'o'] in equiv[0]:
																											equiv[1] = symbol_o_name
																									# Set symbol for r...
																									for equiv in equivalences2:
																										if [me, 'r'] in equiv[0]:
																											equiv[1] = symbol_r_name
																									# Set symbol for o_h...
																									for equiv in equivalences2:
																										if [me, 'o_h'] in equiv[0]:
																											equiv[1] = symbol_o_h_name
																									# Set symbol for s...
																									for equiv in equivalences2:
																										if [me, 's'] in equiv[0]:
																											equiv[1] = symbol_s_name
																									# Set symbol for h...
																									for equiv in equivalences2:
																										if [me, 'h'] in equiv[0]:
																											equiv[1] = symbol_h_name
																									# Set symbol for cont2...
																									for equiv in equivalences2:
																										if [me, 'cont2'] in equiv[0]:
																											equiv[1] = symbol_cont2_name
																									# Set symbol for cont1...
																									for equiv in equivalences2:
																										if [me, 'cont1'] in equiv[0]:
																											equiv[1] = symbol_cont1_name
																									# Set symbol for mh...
																									for equiv in equivalences2:
																										if [me, 'mh'] in equiv[0]:
																											equiv[1] = symbol_mh_name
																									# Set symbol for f...
																									for equiv in equivalences2:
																										if [me, 'f'] in equiv[0]:
																											equiv[1] = symbol_f_name
																									# Set symbol for ch...
																									for equiv in equivalences2:
																										if [me, 'ch'] in equiv[0]:
																											equiv[1] = symbol_ch_name
																									newNode = WorldStateHistory(r1)
																									global lastNodeId
																									lastNodeId += 1
																									newNode.nodeId = lastNodeId
																									newNode.parentId = snode.nodeId
																									derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																									if 'fina' in locals():
																										for n in derivsx: n.history.append(finishesCombo)
																										for n in derivsx: n.history.append(fina)
																									ret.extend(derivsx)
		return ret
		
		

	# Rule humanTellsUsAboutBox
	def humanTellsUsAboutBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger3 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger4 ')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger5 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger6 ')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_soh.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger7 ')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_soh.name and test_symbol_cont1.name!=test_symbol_o.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o_h.name and test_symbol_cont1.name!=test_symbol_s.name and test_symbol_cont1.name!=test_symbol_h.name and test_symbol_cont1.name!=test_symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger8 ')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'box' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and test_symbol_mh.name!=test_symbol_cont2.name and test_symbol_mh.name!=test_symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger9 ')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_cont2.name and test_symbol_f.name!=test_symbol_cont1.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger10 ')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_cont2.name and test_symbol_ch.name!=test_symbol_cont1.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger11 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['mr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'box')
		# Retype nodes
		newNode.graph.nodes[n2id['f']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['mr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		l = AGMLink(smap['s'], smap['cont1'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 3
			newNode.depth += 1
		newNode.history.append('humanTellsUsAboutBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanTellsUsAboutTable
	def humanTellsUsAboutTable(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for ch
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'ch'] in equiv[0]:
					if equiv[1] != None:
						symbol_ch_nodes = [equiv[1]]
			# Find equivalence for f
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'f'] in equiv[0]:
					if equiv[1] != None:
						symbol_f_nodes = [equiv[1]]
			# Find equivalence for h
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'h'] in equiv[0]:
					if equiv[1] != None:
						symbol_h_nodes = [equiv[1]]
			# Find equivalence for mh
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'mh'] in equiv[0]:
					if equiv[1] != None:
						symbol_mh_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for soh
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'soh'] in equiv[0]:
					if equiv[1] != None:
						symbol_soh_nodes = [equiv[1]]
			# Find equivalence for o_h
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o_h'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_h_nodes = [equiv[1]]
		else:
			symbol_ch_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_f_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_h_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_mh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_soh_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_h_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_soh_name in symbol_soh_nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in symbol_o_h_nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in symbol_s_nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in symbol_h_nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_mh_name in symbol_mh_nodes:
															symbol_mh = nodes[symbol_mh_name]
															n2id['mh'] = symbol_mh_name
															if symbol_mh.sType == 'table' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																for symbol_f_name in symbol_f_nodes:
																	symbol_f = nodes[symbol_f_name]
																	n2id['f'] = symbol_f_name
																	if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																		for symbol_ch_name in symbol_ch_nodes:
																			symbol_ch = nodes[symbol_ch_name]
																			n2id['ch'] = symbol_ch_name
																			if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				stack2        = copy.deepcopy(stack)
																				equivalences2 = copy.deepcopy(equivalences)
																				r1 = self.humanTellsUsAboutTable_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																				c = copy.deepcopy(r1)
																				if 'fina' in locals():
																					c.history.append(finishesCombo)
																				if len(stack2) > 0: c.stop = True
																				ret.append(c)
																				if len(stack2) > 0:
																					# Set symbol for soh...
																					for equiv in equivalences2:
																						if [me, 'soh'] in equiv[0]:
																							equiv[1] = symbol_soh_name
																					# Set symbol for o...
																					for equiv in equivalences2:
																						if [me, 'o'] in equiv[0]:
																							equiv[1] = symbol_o_name
																					# Set symbol for r...
																					for equiv in equivalences2:
																						if [me, 'r'] in equiv[0]:
																							equiv[1] = symbol_r_name
																					# Set symbol for o_h...
																					for equiv in equivalences2:
																						if [me, 'o_h'] in equiv[0]:
																							equiv[1] = symbol_o_h_name
																					# Set symbol for s...
																					for equiv in equivalences2:
																						if [me, 's'] in equiv[0]:
																							equiv[1] = symbol_s_name
																					# Set symbol for h...
																					for equiv in equivalences2:
																						if [me, 'h'] in equiv[0]:
																							equiv[1] = symbol_h_name
																					# Set symbol for mh...
																					for equiv in equivalences2:
																						if [me, 'mh'] in equiv[0]:
																							equiv[1] = symbol_mh_name
																					# Set symbol for f...
																					for equiv in equivalences2:
																						if [me, 'f'] in equiv[0]:
																							equiv[1] = symbol_f_name
																					# Set symbol for ch...
																					for equiv in equivalences2:
																						if [me, 'ch'] in equiv[0]:
																							equiv[1] = symbol_ch_name
																					newNode = WorldStateHistory(r1)
																					global lastNodeId
																					lastNodeId += 1
																					newNode.nodeId = lastNodeId
																					newNode.parentId = snode.nodeId
																					derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																					if 'fina' in locals():
																						for n in derivsx: n.history.append(finishesCombo)
																						for n in derivsx: n.history.append(fina)
																					ret.extend(derivsx)
		return ret
		
		

	# Rule humanTellsUsAboutTable
	def humanTellsUsAboutTable_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger3 ')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger4 ')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger5 ')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger6 ')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'table' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger7 ')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger8 ')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger9 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		newName = str(getNewIdForSymbol(newNode))
		smap['mr'] = newName
		newNode.graph.nodes[newName] = AGMSymbol(newName, 'table')
		# Retype nodes
		newNode.graph.nodes[n2id['f']].sType = 'classified'
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [  ]]
		# Create links
		l = AGMLink(smap['s'], smap['mr'], 'link')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 3
			newNode.depth += 1
		newNode.history.append('humanTellsUsAboutTable@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule robotMovesMugFromTableToBox
	def robotMovesMugFromTableToBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for b
			symbol_b_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'b'] in equiv[0]:
					if equiv[1] != None:
						symbol_b_nodes = [equiv[1]]
			# Find equivalence for r1
			symbol_r1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r1'] in equiv[0]:
					if equiv[1] != None:
						symbol_r1_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for rc1
			symbol_rc1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'rc1'] in equiv[0]:
					if equiv[1] != None:
						symbol_rc1_nodes = [equiv[1]]
			# Find equivalence for rc2
			symbol_rc2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'rc2'] in equiv[0]:
					if equiv[1] != None:
						symbol_rc2_nodes = [equiv[1]]
			# Find equivalence for t
			symbol_t_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 't'] in equiv[0]:
					if equiv[1] != None:
						symbol_t_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for c2
			symbol_c2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c2'] in equiv[0]:
					if equiv[1] != None:
						symbol_c2_nodes = [equiv[1]]
			# Find equivalence for c1
			symbol_c1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c1'] in equiv[0]:
					if equiv[1] != None:
						symbol_c1_nodes = [equiv[1]]
			# Find equivalence for cs1
			symbol_cs1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cs1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cs1_nodes = [equiv[1]]
			# Find equivalence for cs2
			symbol_cs2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cs2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cs2_nodes = [equiv[1]]
		else:
			symbol_b_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_rc1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_rc2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_t_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_c2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_c1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cs1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cs2_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_cs2_name in symbol_cs2_nodes:
							symbol_cs2 = nodes[symbol_cs2_name]
							n2id['cs2'] = symbol_cs2_name
							if symbol_cs2.sType == 'status' and symbol_cs2.name!=symbol_s.name and symbol_cs2.name!=symbol_r.name:
								for symbol_cs1_name in symbol_cs1_nodes:
									symbol_cs1 = nodes[symbol_cs1_name]
									n2id['cs1'] = symbol_cs1_name
									if symbol_cs1.sType == 'status' and symbol_cs1.name!=symbol_s.name and symbol_cs1.name!=symbol_r.name and symbol_cs1.name!=symbol_cs2.name:
										for symbol_c1_name in symbol_c1_nodes:
											symbol_c1 = nodes[symbol_c1_name]
											n2id['c1'] = symbol_c1_name
											if symbol_c1.sType == 'object' and symbol_c1.name!=symbol_s.name and symbol_c1.name!=symbol_r.name and symbol_c1.name!=symbol_cs2.name and symbol_c1.name!=symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links:
												for symbol_o_name in symbol_o_nodes:
													symbol_o = nodes[symbol_o_name]
													n2id['o'] = symbol_o_name
													if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_cs2.name and symbol_o.name!=symbol_cs1.name and symbol_o.name!=symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
														for symbol_c2_name in symbol_c2_nodes:
															symbol_c2 = nodes[symbol_c2_name]
															n2id['c2'] = symbol_c2_name
															if symbol_c2.sType == 'object' and symbol_c2.name!=symbol_s.name and symbol_c2.name!=symbol_r.name and symbol_c2.name!=symbol_cs2.name and symbol_c2.name!=symbol_cs1.name and symbol_c2.name!=symbol_c1.name and symbol_c2.name!=symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links:
																for symbol_t_name in symbol_t_nodes:
																	symbol_t = nodes[symbol_t_name]
																	n2id['t'] = symbol_t_name
																	if symbol_t.sType == 'table' and symbol_t.name!=symbol_s.name and symbol_t.name!=symbol_r.name and symbol_t.name!=symbol_cs2.name and symbol_t.name!=symbol_cs1.name and symbol_t.name!=symbol_c1.name and symbol_t.name!=symbol_o.name and symbol_t.name!=symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links:
																		for symbol_rc2_name in symbol_rc2_nodes:
																			symbol_rc2 = nodes[symbol_rc2_name]
																			n2id['rc2'] = symbol_rc2_name
																			if symbol_rc2.sType == 'reach' and symbol_rc2.name!=symbol_s.name and symbol_rc2.name!=symbol_r.name and symbol_rc2.name!=symbol_cs2.name and symbol_rc2.name!=symbol_cs1.name and symbol_rc2.name!=symbol_c1.name and symbol_rc2.name!=symbol_o.name and symbol_rc2.name!=symbol_c2.name and symbol_rc2.name!=symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links:
																				for symbol_rc1_name in symbol_rc1_nodes:
																					symbol_rc1 = nodes[symbol_rc1_name]
																					n2id['rc1'] = symbol_rc1_name
																					if symbol_rc1.sType == 'reach' and symbol_rc1.name!=symbol_s.name and symbol_rc1.name!=symbol_r.name and symbol_rc1.name!=symbol_cs2.name and symbol_rc1.name!=symbol_cs1.name and symbol_rc1.name!=symbol_c1.name and symbol_rc1.name!=symbol_o.name and symbol_rc1.name!=symbol_c2.name and symbol_rc1.name!=symbol_t.name and symbol_rc1.name!=symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links:
																						for symbol_r1_name in symbol_r1_nodes:
																							symbol_r1 = nodes[symbol_r1_name]
																							n2id['r1'] = symbol_r1_name
																							if symbol_r1.sType == 'reach' and symbol_r1.name!=symbol_s.name and symbol_r1.name!=symbol_r.name and symbol_r1.name!=symbol_cs2.name and symbol_r1.name!=symbol_cs1.name and symbol_r1.name!=symbol_c1.name and symbol_r1.name!=symbol_o.name and symbol_r1.name!=symbol_c2.name and symbol_r1.name!=symbol_t.name and symbol_r1.name!=symbol_rc2.name and symbol_r1.name!=symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links:
																								for symbol_m_name in symbol_m_nodes:
																									symbol_m = nodes[symbol_m_name]
																									n2id['m'] = symbol_m_name
																									if symbol_m.sType == 'mug' and symbol_m.name!=symbol_s.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_cs2.name and symbol_m.name!=symbol_cs1.name and symbol_m.name!=symbol_c1.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_c2.name and symbol_m.name!=symbol_t.name and symbol_m.name!=symbol_rc2.name and symbol_m.name!=symbol_rc1.name and symbol_m.name!=symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links:
																										for symbol_b_name in symbol_b_nodes:
																											symbol_b = nodes[symbol_b_name]
																											n2id['b'] = symbol_b_name
																											if symbol_b.sType == 'box' and symbol_b.name!=symbol_s.name and symbol_b.name!=symbol_r.name and symbol_b.name!=symbol_cs2.name and symbol_b.name!=symbol_cs1.name and symbol_b.name!=symbol_c1.name and symbol_b.name!=symbol_o.name and symbol_b.name!=symbol_c2.name and symbol_b.name!=symbol_t.name and symbol_b.name!=symbol_rc2.name and symbol_b.name!=symbol_rc1.name and symbol_b.name!=symbol_r1.name and symbol_b.name!=symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links:
																												# At this point we meet all the conditions.
																												# Insert additional conditions manually here if you want.
																												# (beware that the code could be regenerated and you might lose your changes).
																												stack2        = copy.deepcopy(stack)
																												equivalences2 = copy.deepcopy(equivalences)
																												r1 = self.robotMovesMugFromTableToBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																												c = copy.deepcopy(r1)
																												if 'fina' in locals():
																													c.history.append(finishesCombo)
																												if len(stack2) > 0: c.stop = True
																												ret.append(c)
																												if len(stack2) > 0:
																													# Set symbol for s...
																													for equiv in equivalences2:
																														if [me, 's'] in equiv[0]:
																															equiv[1] = symbol_s_name
																													# Set symbol for r...
																													for equiv in equivalences2:
																														if [me, 'r'] in equiv[0]:
																															equiv[1] = symbol_r_name
																													# Set symbol for cs2...
																													for equiv in equivalences2:
																														if [me, 'cs2'] in equiv[0]:
																															equiv[1] = symbol_cs2_name
																													# Set symbol for cs1...
																													for equiv in equivalences2:
																														if [me, 'cs1'] in equiv[0]:
																															equiv[1] = symbol_cs1_name
																													# Set symbol for c1...
																													for equiv in equivalences2:
																														if [me, 'c1'] in equiv[0]:
																															equiv[1] = symbol_c1_name
																													# Set symbol for o...
																													for equiv in equivalences2:
																														if [me, 'o'] in equiv[0]:
																															equiv[1] = symbol_o_name
																													# Set symbol for c2...
																													for equiv in equivalences2:
																														if [me, 'c2'] in equiv[0]:
																															equiv[1] = symbol_c2_name
																													# Set symbol for t...
																													for equiv in equivalences2:
																														if [me, 't'] in equiv[0]:
																															equiv[1] = symbol_t_name
																													# Set symbol for rc2...
																													for equiv in equivalences2:
																														if [me, 'rc2'] in equiv[0]:
																															equiv[1] = symbol_rc2_name
																													# Set symbol for rc1...
																													for equiv in equivalences2:
																														if [me, 'rc1'] in equiv[0]:
																															equiv[1] = symbol_rc1_name
																													# Set symbol for r1...
																													for equiv in equivalences2:
																														if [me, 'r1'] in equiv[0]:
																															equiv[1] = symbol_r1_name
																													# Set symbol for m...
																													for equiv in equivalences2:
																														if [me, 'm'] in equiv[0]:
																															equiv[1] = symbol_m_name
																													# Set symbol for b...
																													for equiv in equivalences2:
																														if [me, 'b'] in equiv[0]:
																															equiv[1] = symbol_b_name
																													newNode = WorldStateHistory(r1)
																													global lastNodeId
																													lastNodeId += 1
																													newNode.nodeId = lastNodeId
																													newNode.parentId = snode.nodeId
																													derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																													if 'fina' in locals():
																														for n in derivsx: n.history.append(finishesCombo)
																														for n in derivsx: n.history.append(fina)
																													ret.extend(derivsx)
		return ret
		
		

	# Rule robotMovesMugFromTableToBox
	def robotMovesMugFromTableToBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger2 ')
			test_symbol_cs2 = snode.graph.nodes[n2id['cs2']]
			if not (test_symbol_cs2.sType == 'status' and test_symbol_cs2.name!=test_symbol_s.name and test_symbol_cs2.name!=test_symbol_r.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger3 ')
			test_symbol_cs1 = snode.graph.nodes[n2id['cs1']]
			if not (test_symbol_cs1.sType == 'status' and test_symbol_cs1.name!=test_symbol_s.name and test_symbol_cs1.name!=test_symbol_r.name and test_symbol_cs1.name!=test_symbol_cs2.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger4 ')
			test_symbol_c1 = snode.graph.nodes[n2id['c1']]
			if not (test_symbol_c1.sType == 'object' and test_symbol_c1.name!=test_symbol_s.name and test_symbol_c1.name!=test_symbol_r.name and test_symbol_c1.name!=test_symbol_cs2.name and test_symbol_c1.name!=test_symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger5 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_cs2.name and test_symbol_o.name!=test_symbol_cs1.name and test_symbol_o.name!=test_symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger6 ')
			test_symbol_c2 = snode.graph.nodes[n2id['c2']]
			if not (test_symbol_c2.sType == 'object' and test_symbol_c2.name!=test_symbol_s.name and test_symbol_c2.name!=test_symbol_r.name and test_symbol_c2.name!=test_symbol_cs2.name and test_symbol_c2.name!=test_symbol_cs1.name and test_symbol_c2.name!=test_symbol_c1.name and test_symbol_c2.name!=test_symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger7 ')
			test_symbol_t = snode.graph.nodes[n2id['t']]
			if not (test_symbol_t.sType == 'table' and test_symbol_t.name!=test_symbol_s.name and test_symbol_t.name!=test_symbol_r.name and test_symbol_t.name!=test_symbol_cs2.name and test_symbol_t.name!=test_symbol_cs1.name and test_symbol_t.name!=test_symbol_c1.name and test_symbol_t.name!=test_symbol_o.name and test_symbol_t.name!=test_symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger8 ')
			test_symbol_rc2 = snode.graph.nodes[n2id['rc2']]
			if not (test_symbol_rc2.sType == 'reach' and test_symbol_rc2.name!=test_symbol_s.name and test_symbol_rc2.name!=test_symbol_r.name and test_symbol_rc2.name!=test_symbol_cs2.name and test_symbol_rc2.name!=test_symbol_cs1.name and test_symbol_rc2.name!=test_symbol_c1.name and test_symbol_rc2.name!=test_symbol_o.name and test_symbol_rc2.name!=test_symbol_c2.name and test_symbol_rc2.name!=test_symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger9 ')
			test_symbol_rc1 = snode.graph.nodes[n2id['rc1']]
			if not (test_symbol_rc1.sType == 'reach' and test_symbol_rc1.name!=test_symbol_s.name and test_symbol_rc1.name!=test_symbol_r.name and test_symbol_rc1.name!=test_symbol_cs2.name and test_symbol_rc1.name!=test_symbol_cs1.name and test_symbol_rc1.name!=test_symbol_c1.name and test_symbol_rc1.name!=test_symbol_o.name and test_symbol_rc1.name!=test_symbol_c2.name and test_symbol_rc1.name!=test_symbol_t.name and test_symbol_rc1.name!=test_symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger10 ')
			test_symbol_r1 = snode.graph.nodes[n2id['r1']]
			if not (test_symbol_r1.sType == 'reach' and test_symbol_r1.name!=test_symbol_s.name and test_symbol_r1.name!=test_symbol_r.name and test_symbol_r1.name!=test_symbol_cs2.name and test_symbol_r1.name!=test_symbol_cs1.name and test_symbol_r1.name!=test_symbol_c1.name and test_symbol_r1.name!=test_symbol_o.name and test_symbol_r1.name!=test_symbol_c2.name and test_symbol_r1.name!=test_symbol_t.name and test_symbol_r1.name!=test_symbol_rc2.name and test_symbol_r1.name!=test_symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger11 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_s.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_cs2.name and test_symbol_m.name!=test_symbol_cs1.name and test_symbol_m.name!=test_symbol_c1.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_c2.name and test_symbol_m.name!=test_symbol_t.name and test_symbol_m.name!=test_symbol_rc2.name and test_symbol_m.name!=test_symbol_rc1.name and test_symbol_m.name!=test_symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger12 ')
			test_symbol_b = snode.graph.nodes[n2id['b']]
			if not (test_symbol_b.sType == 'box' and test_symbol_b.name!=test_symbol_s.name and test_symbol_b.name!=test_symbol_r.name and test_symbol_b.name!=test_symbol_cs2.name and test_symbol_b.name!=test_symbol_cs1.name and test_symbol_b.name!=test_symbol_c1.name and test_symbol_b.name!=test_symbol_o.name and test_symbol_b.name!=test_symbol_c2.name and test_symbol_b.name!=test_symbol_t.name and test_symbol_b.name!=test_symbol_rc2.name and test_symbol_b.name!=test_symbol_rc1.name and test_symbol_b.name!=test_symbol_r1.name and test_symbol_b.name!=test_symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger13 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [smap['s'], smap['c1'], 'in'] ]]
		# Create links
		l = AGMLink(smap['s'], smap['c2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('robotMovesMugFromTableToBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule humanMovesMugFromTableToBox
	def humanMovesMugFromTableToBox(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for b
			symbol_b_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'b'] in equiv[0]:
					if equiv[1] != None:
						symbol_b_nodes = [equiv[1]]
			# Find equivalence for r1
			symbol_r1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r1'] in equiv[0]:
					if equiv[1] != None:
						symbol_r1_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for rc1
			symbol_rc1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'rc1'] in equiv[0]:
					if equiv[1] != None:
						symbol_rc1_nodes = [equiv[1]]
			# Find equivalence for rc2
			symbol_rc2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'rc2'] in equiv[0]:
					if equiv[1] != None:
						symbol_rc2_nodes = [equiv[1]]
			# Find equivalence for t
			symbol_t_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 't'] in equiv[0]:
					if equiv[1] != None:
						symbol_t_nodes = [equiv[1]]
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
			# Find equivalence for c2
			symbol_c2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c2'] in equiv[0]:
					if equiv[1] != None:
						symbol_c2_nodes = [equiv[1]]
			# Find equivalence for c1
			symbol_c1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'c1'] in equiv[0]:
					if equiv[1] != None:
						symbol_c1_nodes = [equiv[1]]
			# Find equivalence for cs1
			symbol_cs1_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cs1'] in equiv[0]:
					if equiv[1] != None:
						symbol_cs1_nodes = [equiv[1]]
			# Find equivalence for cs2
			symbol_cs2_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'cs2'] in equiv[0]:
					if equiv[1] != None:
						symbol_cs2_nodes = [equiv[1]]
		else:
			symbol_b_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_rc1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_rc2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_t_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_c2_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_c1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cs1_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_cs2_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in symbol_r_nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'human' and symbol_r.name!=symbol_s.name:
						for symbol_cs2_name in symbol_cs2_nodes:
							symbol_cs2 = nodes[symbol_cs2_name]
							n2id['cs2'] = symbol_cs2_name
							if symbol_cs2.sType == 'status' and symbol_cs2.name!=symbol_s.name and symbol_cs2.name!=symbol_r.name:
								for symbol_cs1_name in symbol_cs1_nodes:
									symbol_cs1 = nodes[symbol_cs1_name]
									n2id['cs1'] = symbol_cs1_name
									if symbol_cs1.sType == 'status' and symbol_cs1.name!=symbol_s.name and symbol_cs1.name!=symbol_r.name and symbol_cs1.name!=symbol_cs2.name:
										for symbol_c1_name in symbol_c1_nodes:
											symbol_c1 = nodes[symbol_c1_name]
											n2id['c1'] = symbol_c1_name
											if symbol_c1.sType == 'object' and symbol_c1.name!=symbol_s.name and symbol_c1.name!=symbol_r.name and symbol_c1.name!=symbol_cs2.name and symbol_c1.name!=symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links:
												for symbol_o_name in symbol_o_nodes:
													symbol_o = nodes[symbol_o_name]
													n2id['o'] = symbol_o_name
													if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_cs2.name and symbol_o.name!=symbol_cs1.name and symbol_o.name!=symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
														for symbol_c2_name in symbol_c2_nodes:
															symbol_c2 = nodes[symbol_c2_name]
															n2id['c2'] = symbol_c2_name
															if symbol_c2.sType == 'object' and symbol_c2.name!=symbol_s.name and symbol_c2.name!=symbol_r.name and symbol_c2.name!=symbol_cs2.name and symbol_c2.name!=symbol_cs1.name and symbol_c2.name!=symbol_c1.name and symbol_c2.name!=symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links:
																for symbol_t_name in symbol_t_nodes:
																	symbol_t = nodes[symbol_t_name]
																	n2id['t'] = symbol_t_name
																	if symbol_t.sType == 'table' and symbol_t.name!=symbol_s.name and symbol_t.name!=symbol_r.name and symbol_t.name!=symbol_cs2.name and symbol_t.name!=symbol_cs1.name and symbol_t.name!=symbol_c1.name and symbol_t.name!=symbol_o.name and symbol_t.name!=symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links:
																		for symbol_rc2_name in symbol_rc2_nodes:
																			symbol_rc2 = nodes[symbol_rc2_name]
																			n2id['rc2'] = symbol_rc2_name
																			if symbol_rc2.sType == 'reach' and symbol_rc2.name!=symbol_s.name and symbol_rc2.name!=symbol_r.name and symbol_rc2.name!=symbol_cs2.name and symbol_rc2.name!=symbol_cs1.name and symbol_rc2.name!=symbol_c1.name and symbol_rc2.name!=symbol_o.name and symbol_rc2.name!=symbol_c2.name and symbol_rc2.name!=symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links:
																				for symbol_rc1_name in symbol_rc1_nodes:
																					symbol_rc1 = nodes[symbol_rc1_name]
																					n2id['rc1'] = symbol_rc1_name
																					if symbol_rc1.sType == 'reach' and symbol_rc1.name!=symbol_s.name and symbol_rc1.name!=symbol_r.name and symbol_rc1.name!=symbol_cs2.name and symbol_rc1.name!=symbol_cs1.name and symbol_rc1.name!=symbol_c1.name and symbol_rc1.name!=symbol_o.name and symbol_rc1.name!=symbol_c2.name and symbol_rc1.name!=symbol_t.name and symbol_rc1.name!=symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links:
																						for symbol_r1_name in symbol_r1_nodes:
																							symbol_r1 = nodes[symbol_r1_name]
																							n2id['r1'] = symbol_r1_name
																							if symbol_r1.sType == 'reach' and symbol_r1.name!=symbol_s.name and symbol_r1.name!=symbol_r.name and symbol_r1.name!=symbol_cs2.name and symbol_r1.name!=symbol_cs1.name and symbol_r1.name!=symbol_c1.name and symbol_r1.name!=symbol_o.name and symbol_r1.name!=symbol_c2.name and symbol_r1.name!=symbol_t.name and symbol_r1.name!=symbol_rc2.name and symbol_r1.name!=symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links:
																								for symbol_m_name in symbol_m_nodes:
																									symbol_m = nodes[symbol_m_name]
																									n2id['m'] = symbol_m_name
																									if symbol_m.sType == 'mug' and symbol_m.name!=symbol_s.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_cs2.name and symbol_m.name!=symbol_cs1.name and symbol_m.name!=symbol_c1.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_c2.name and symbol_m.name!=symbol_t.name and symbol_m.name!=symbol_rc2.name and symbol_m.name!=symbol_rc1.name and symbol_m.name!=symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links:
																										for symbol_b_name in symbol_b_nodes:
																											symbol_b = nodes[symbol_b_name]
																											n2id['b'] = symbol_b_name
																											if symbol_b.sType == 'box' and symbol_b.name!=symbol_s.name and symbol_b.name!=symbol_r.name and symbol_b.name!=symbol_cs2.name and symbol_b.name!=symbol_cs1.name and symbol_b.name!=symbol_c1.name and symbol_b.name!=symbol_o.name and symbol_b.name!=symbol_c2.name and symbol_b.name!=symbol_t.name and symbol_b.name!=symbol_rc2.name and symbol_b.name!=symbol_rc1.name and symbol_b.name!=symbol_r1.name and symbol_b.name!=symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links:
																												# At this point we meet all the conditions.
																												# Insert additional conditions manually here if you want.
																												# (beware that the code could be regenerated and you might lose your changes).
																												stack2        = copy.deepcopy(stack)
																												equivalences2 = copy.deepcopy(equivalences)
																												r1 = self.humanMovesMugFromTableToBox_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
																												c = copy.deepcopy(r1)
																												if 'fina' in locals():
																													c.history.append(finishesCombo)
																												if len(stack2) > 0: c.stop = True
																												ret.append(c)
																												if len(stack2) > 0:
																													# Set symbol for s...
																													for equiv in equivalences2:
																														if [me, 's'] in equiv[0]:
																															equiv[1] = symbol_s_name
																													# Set symbol for r...
																													for equiv in equivalences2:
																														if [me, 'r'] in equiv[0]:
																															equiv[1] = symbol_r_name
																													# Set symbol for cs2...
																													for equiv in equivalences2:
																														if [me, 'cs2'] in equiv[0]:
																															equiv[1] = symbol_cs2_name
																													# Set symbol for cs1...
																													for equiv in equivalences2:
																														if [me, 'cs1'] in equiv[0]:
																															equiv[1] = symbol_cs1_name
																													# Set symbol for c1...
																													for equiv in equivalences2:
																														if [me, 'c1'] in equiv[0]:
																															equiv[1] = symbol_c1_name
																													# Set symbol for o...
																													for equiv in equivalences2:
																														if [me, 'o'] in equiv[0]:
																															equiv[1] = symbol_o_name
																													# Set symbol for c2...
																													for equiv in equivalences2:
																														if [me, 'c2'] in equiv[0]:
																															equiv[1] = symbol_c2_name
																													# Set symbol for t...
																													for equiv in equivalences2:
																														if [me, 't'] in equiv[0]:
																															equiv[1] = symbol_t_name
																													# Set symbol for rc2...
																													for equiv in equivalences2:
																														if [me, 'rc2'] in equiv[0]:
																															equiv[1] = symbol_rc2_name
																													# Set symbol for rc1...
																													for equiv in equivalences2:
																														if [me, 'rc1'] in equiv[0]:
																															equiv[1] = symbol_rc1_name
																													# Set symbol for r1...
																													for equiv in equivalences2:
																														if [me, 'r1'] in equiv[0]:
																															equiv[1] = symbol_r1_name
																													# Set symbol for m...
																													for equiv in equivalences2:
																														if [me, 'm'] in equiv[0]:
																															equiv[1] = symbol_m_name
																													# Set symbol for b...
																													for equiv in equivalences2:
																														if [me, 'b'] in equiv[0]:
																															equiv[1] = symbol_b_name
																													newNode = WorldStateHistory(r1)
																													global lastNodeId
																													lastNodeId += 1
																													newNode.nodeId = lastNodeId
																													newNode.parentId = snode.nodeId
																													derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
																													if 'fina' in locals():
																														for n in derivsx: n.history.append(finishesCombo)
																														for n in derivsx: n.history.append(fina)
																													ret.extend(derivsx)
		return ret
		
		

	# Rule humanMovesMugFromTableToBox
	def humanMovesMugFromTableToBox_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger1 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'human' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger2 ')
			test_symbol_cs2 = snode.graph.nodes[n2id['cs2']]
			if not (test_symbol_cs2.sType == 'status' and test_symbol_cs2.name!=test_symbol_s.name and test_symbol_cs2.name!=test_symbol_r.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger3 ')
			test_symbol_cs1 = snode.graph.nodes[n2id['cs1']]
			if not (test_symbol_cs1.sType == 'status' and test_symbol_cs1.name!=test_symbol_s.name and test_symbol_cs1.name!=test_symbol_r.name and test_symbol_cs1.name!=test_symbol_cs2.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger4 ')
			test_symbol_c1 = snode.graph.nodes[n2id['c1']]
			if not (test_symbol_c1.sType == 'object' and test_symbol_c1.name!=test_symbol_s.name and test_symbol_c1.name!=test_symbol_r.name and test_symbol_c1.name!=test_symbol_cs2.name and test_symbol_c1.name!=test_symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger5 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_cs2.name and test_symbol_o.name!=test_symbol_cs1.name and test_symbol_o.name!=test_symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger6 ')
			test_symbol_c2 = snode.graph.nodes[n2id['c2']]
			if not (test_symbol_c2.sType == 'object' and test_symbol_c2.name!=test_symbol_s.name and test_symbol_c2.name!=test_symbol_r.name and test_symbol_c2.name!=test_symbol_cs2.name and test_symbol_c2.name!=test_symbol_cs1.name and test_symbol_c2.name!=test_symbol_c1.name and test_symbol_c2.name!=test_symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger7 ')
			test_symbol_t = snode.graph.nodes[n2id['t']]
			if not (test_symbol_t.sType == 'table' and test_symbol_t.name!=test_symbol_s.name and test_symbol_t.name!=test_symbol_r.name and test_symbol_t.name!=test_symbol_cs2.name and test_symbol_t.name!=test_symbol_cs1.name and test_symbol_t.name!=test_symbol_c1.name and test_symbol_t.name!=test_symbol_o.name and test_symbol_t.name!=test_symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger8 ')
			test_symbol_rc2 = snode.graph.nodes[n2id['rc2']]
			if not (test_symbol_rc2.sType == 'reach' and test_symbol_rc2.name!=test_symbol_s.name and test_symbol_rc2.name!=test_symbol_r.name and test_symbol_rc2.name!=test_symbol_cs2.name and test_symbol_rc2.name!=test_symbol_cs1.name and test_symbol_rc2.name!=test_symbol_c1.name and test_symbol_rc2.name!=test_symbol_o.name and test_symbol_rc2.name!=test_symbol_c2.name and test_symbol_rc2.name!=test_symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger9 ')
			test_symbol_rc1 = snode.graph.nodes[n2id['rc1']]
			if not (test_symbol_rc1.sType == 'reach' and test_symbol_rc1.name!=test_symbol_s.name and test_symbol_rc1.name!=test_symbol_r.name and test_symbol_rc1.name!=test_symbol_cs2.name and test_symbol_rc1.name!=test_symbol_cs1.name and test_symbol_rc1.name!=test_symbol_c1.name and test_symbol_rc1.name!=test_symbol_o.name and test_symbol_rc1.name!=test_symbol_c2.name and test_symbol_rc1.name!=test_symbol_t.name and test_symbol_rc1.name!=test_symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger10 ')
			test_symbol_r1 = snode.graph.nodes[n2id['r1']]
			if not (test_symbol_r1.sType == 'reach' and test_symbol_r1.name!=test_symbol_s.name and test_symbol_r1.name!=test_symbol_r.name and test_symbol_r1.name!=test_symbol_cs2.name and test_symbol_r1.name!=test_symbol_cs1.name and test_symbol_r1.name!=test_symbol_c1.name and test_symbol_r1.name!=test_symbol_o.name and test_symbol_r1.name!=test_symbol_c2.name and test_symbol_r1.name!=test_symbol_t.name and test_symbol_r1.name!=test_symbol_rc2.name and test_symbol_r1.name!=test_symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger11 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_s.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_cs2.name and test_symbol_m.name!=test_symbol_cs1.name and test_symbol_m.name!=test_symbol_c1.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_c2.name and test_symbol_m.name!=test_symbol_t.name and test_symbol_m.name!=test_symbol_rc2.name and test_symbol_m.name!=test_symbol_rc1.name and test_symbol_m.name!=test_symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger12 ')
			test_symbol_b = snode.graph.nodes[n2id['b']]
			if not (test_symbol_b.sType == 'box' and test_symbol_b.name!=test_symbol_s.name and test_symbol_b.name!=test_symbol_r.name and test_symbol_b.name!=test_symbol_cs2.name and test_symbol_b.name!=test_symbol_cs1.name and test_symbol_b.name!=test_symbol_c1.name and test_symbol_b.name!=test_symbol_o.name and test_symbol_b.name!=test_symbol_c2.name and test_symbol_b.name!=test_symbol_t.name and test_symbol_b.name!=test_symbol_rc2.name and test_symbol_b.name!=test_symbol_rc1.name and test_symbol_b.name!=test_symbol_r1.name and test_symbol_b.name!=test_symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger13 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [smap['s'], smap['c1'], 'in'] ]]
		# Create links
		l = AGMLink(smap['s'], smap['c2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('humanMovesMugFromTableToBox@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule setTableClean
	def setTableClean(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		finishesCombo = ''
		if len(stack) > 0:
			pop = stack.pop()
			me = pop[0]
			if len(pop)>2:
				finishesCombo = copy.deepcopy(pop[2])
				fina = copy.deepcopy(pop[2])
			# Find equivalence for s
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 's'] in equiv[0]:
					if equiv[1] != None:
						symbol_s_nodes = [equiv[1]]
			# Find equivalence for r
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'r'] in equiv[0]:
					if equiv[1] != None:
						symbol_r_nodes = [equiv[1]]
			# Find equivalence for m
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'm'] in equiv[0]:
					if equiv[1] != None:
						symbol_m_nodes = [equiv[1]]
			# Find equivalence for o
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
			for equiv in equivalences:
				if [me, 'o'] in equiv[0]:
					if equiv[1] != None:
						symbol_o_nodes = [equiv[1]]
		else:
			symbol_s_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_r_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_m_nodes = copy.deepcopy(snode.graph.nodes)
			symbol_o_nodes = copy.deepcopy(snode.graph.nodes)
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		for symbol_s_name in symbol_s_nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in symbol_o_nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in symbol_r_nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_m_name in symbol_m_nodes:
									symbol_m = nodes[symbol_m_name]
									n2id['m'] = symbol_m_name
									if symbol_m.sType == 'table' and symbol_m.name!=symbol_s.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_r.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links and not [n2id["s"],n2id["m"],"clean"] in snode.graph.links:
										# At this point we meet all the conditions.
										# Insert additional conditions manually here if you want.
										# (beware that the code could be regenerated and you might lose your changes).
										stack2        = copy.deepcopy(stack)
										equivalences2 = copy.deepcopy(equivalences)
										r1 = self.setTableClean_trigger(snode, n2id, stack2, equivalences2, copy.deepcopy(finishesCombo))
										c = copy.deepcopy(r1)
										if 'fina' in locals():
											c.history.append(finishesCombo)
										if len(stack2) > 0: c.stop = True
										ret.append(c)
										if len(stack2) > 0:
											# Set symbol for s...
											for equiv in equivalences2:
												if [me, 's'] in equiv[0]:
													equiv[1] = symbol_s_name
											# Set symbol for o...
											for equiv in equivalences2:
												if [me, 'o'] in equiv[0]:
													equiv[1] = symbol_o_name
											# Set symbol for r...
											for equiv in equivalences2:
												if [me, 'r'] in equiv[0]:
													equiv[1] = symbol_r_name
											# Set symbol for m...
											for equiv in equivalences2:
												if [me, 'm'] in equiv[0]:
													equiv[1] = symbol_m_name
											newNode = WorldStateHistory(r1)
											global lastNodeId
											lastNodeId += 1
											newNode.nodeId = lastNodeId
											newNode.parentId = snode.nodeId
											derivsx = self.getRules()[stack2[-1][1]](newNode, stack2, equivalences2)
											if 'fina' in locals():
												for n in derivsx: n.history.append(finishesCombo)
												for n in derivsx: n.history.append(fina)
											ret.extend(derivsx)
		return ret
		
		

	# Rule setTableClean
	def setTableClean_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setTableClean_trigger1 ')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger2 ')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger3 ')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'table' and test_symbol_m.name!=test_symbol_s.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_r.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links and not [n2id["s"],n2id["m"],"clean"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger4 ')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		# Create nodes
		# Retype nodes
		# Remove nodes
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [smap['s'], smap['m'], 'clean'] ]]
		# Create links
		l = AGMLink(smap['s'], smap['m'], 'clean')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		if len(stack) == 0:
			newNode.cost += 1
			newNode.depth += 1
		newNode.history.append('setTableClean@' + str(n2id) )
		if finish!='': newNode.history.append(finish)
		return newNode
		
		

	# Rule MOVEtoCLEAN
	def MOVEtoCLEAN(self, snode, stackP=[], equivalencesP=[]):
		stack        = copy.deepcopy(stackP)
		equivalences = copy.deepcopy(equivalencesP)
		return self.MOVEtoCLEAN_trigger(snode, dict(), stack, equivalences)
		

	# Rule MOVEtoCLEAN
	def MOVEtoCLEAN_trigger(self, snode, n2id, stack=[], equivalences=[], checked=True, finish=''):
		aliasDict = dict()
		sid = str(len(stack)+2)
		for atom in [['setTableClean','set', '# ENDS COMBO:MOVEtoCLEAN_'+sid], ['robotMovesMugFromTableToBox','move']]:
			idInStack = len(stack)
			if len(atom)<3:
				stack.append((idInStack, atom[0]))
			else:
				stack.append((idInStack, atom[0], atom[2]))
			aliasDict[atom[1]] = idInStack
		for equivalence in [[['move', 'cs1'], ['set', 'sr']], [['move', 'r'], ['set', 'r']], [['move', 't'], ['set', 'm']], [['move', 'c1'], ['set', 'o']]]:
			equivList = []
			for similar in equivalence:
				equivList.append([aliasDict[similar[0]], similar[1]])
			equivalences.append([equivList, None])
		newNode = WorldStateHistory(snode)
		global lastNodeId
		lastNodeId += 1
		newNode.cost += 1
		newNode.depth += 1
		newNode.nodeId = lastNodeId
		newNode.parentId = snode.nodeId
		newNode.history.append('# STARTS COMBO:MOVEtoCLEAN_' + sid)
		ret = self.getRules()[stack[-1][1]](newNode, stack, equivalences)
		return ret

