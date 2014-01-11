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

def hasEqual(name, graph):
	for l in graph.links:
		if l.linkType == "eq":
			if l.a == name or l.b == name:
				return True
	return False

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
		return mapping

	def setTableClean(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['r', 'o', 'know'], ['o', 'sr', 'has'], ['sr', 'm', 'link'] ]
		for symbol_sr_name in nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_m_name in nodes:
									symbol_m = nodes[symbol_m_name]
									n2id['m'] = symbol_m_name
									if symbol_m.sType == 'table' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
										anyObject = False
										for link in snode.graph.links:
											if link.b == n2id['o'] and link.linkType == "in":
												# Ok, there is something... is it a mug?
												status = link.a # this is the status of the object, let's check if it's a mug
												for link2 in snode.graph.links:
													if link2.a == status:
														prop = link2.b
														if snode.graph.nodes[prop].sType == 'mug':
															anyObject = True
															break
										if not anyObject:
											ret.append(self.setTableClean_trigger(snode, n2id))
		return ret

	def setTableClean_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot'):
				raise WrongRuleExecution('setTableClean_trigger 1')

			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger 2')

			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status' and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger 3')

			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'table' and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setTableClean_trigger 4')

			anyObject = False
			for link in snode.graph.links:
				if link.b == n2id['o'] and link.linkType == "in":
					# Ok, there is something... is it a mug?
					status = link.a # this is the status of the object, let's check if it's a mug
					for link2 in snode.graph.links:
						if link2.a == status:
							prop = link2.b
							if snode.graph.nodes[prop].sType == 'mug':
								anyObject = True
								break
			if anyObject:
				raise WrongRuleExecution('setTableClean_trigger 5')

		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		# Create links
		l = AGMLink(smap['sr'], smap['m'], 'clean')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)
		# Misc stuff
		newNode.probability *= 1.
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('setTableClean@' + str(n2id) )
		return newNode



	# Rule findObjectVisually
	def findObjectVisually(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [  ]
		for symbol_r_name in nodes:
			symbol_r = nodes[symbol_r_name]
			n2id['r'] = symbol_r_name
			if symbol_r.sType == 'robot':
				# At this point we meet all the conditions.
				# Insert additional conditions manually here if you want.
				# (beware that the code could be regenerated and you might lose your changes).
				ret.append(self.findObjectVisually_trigger(snode, n2id))
		return ret



	# Rule findObjectVisually
	def findObjectVisually_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot'):
				raise WrongRuleExecution('findObjectVisually_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('findObjectVisually@' + str(n2id) )
		return newNode



	# Rule findObjectTold
	def findObjectTold(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [  ]
		for symbol_r_name in nodes:
			symbol_r = nodes[symbol_r_name]
			n2id['r'] = symbol_r_name
			if symbol_r.sType == 'robot':
				# At this point we meet all the conditions.
				# Insert additional conditions manually here if you want.
				# (beware that the code could be regenerated and you might lose your changes).
				ret.append(self.findObjectTold_trigger(snode, n2id))
		return ret



	# Rule findObjectTold
	def findObjectTold_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot'):
				raise WrongRuleExecution('findObjectTold_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 4
		newNode.depth += 1
		newNode.history.append('findObjectTold@' + str(n2id) )
		return newNode



	# Rule recognizeObjMug
	def recognizeObjMug(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['r', 'o', 'know'], ['s', 'c', 'link'], ['s', 'po', 'link'], ['s', 'se', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														for symbol_other_name in nodes:
															symbol_other = nodes[symbol_other_name]
															n2id['other'] = symbol_other_name
															if symbol_other.sType == 'object' and symbol_other.name!=symbol_s.name and symbol_other.name!=symbol_o.name and symbol_other.name!=symbol_r.name and symbol_other.name!=symbol_se.name and symbol_other.name!=symbol_po.name and symbol_other.name!=symbol_c.name:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																ret.append(self.recognizeObjMug_trigger(snode, n2id))
		return ret



	# Rule recognizeObjMug
	def recognizeObjMug_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjMug_trigger')
			test_symbol_other = snode.graph.nodes[n2id['other']]
			if not (test_symbol_other.sType == 'object' and test_symbol_other.name!=test_symbol_s.name and test_symbol_other.name!=test_symbol_o.name and test_symbol_other.name!=test_symbol_r.name and test_symbol_other.name!=test_symbol_se.name and test_symbol_other.name!=test_symbol_po.name and test_symbol_other.name!=test_symbol_c.name):
				raise WrongRuleExecution('recognizeObjMug_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('recognizeObjMug@' + str(n2id) )
		return newNode



	# Rule recognizeObjBox
	def recognizeObjBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['r', 'o', 'know'], ['s', 'c', 'link'], ['s', 'po', 'link'], ['s', 'se', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														for symbol_other_name in nodes:
															symbol_other = nodes[symbol_other_name]
															n2id['other'] = symbol_other_name
															if symbol_other.sType == 'object' and symbol_other.name!=symbol_s.name and symbol_other.name!=symbol_o.name and symbol_other.name!=symbol_r.name and symbol_other.name!=symbol_se.name and symbol_other.name!=symbol_po.name and symbol_other.name!=symbol_c.name:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																ret.append(self.recognizeObjBox_trigger(snode, n2id))
		return ret



	# Rule recognizeObjBox
	def recognizeObjBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjBox_trigger')
			test_symbol_other = snode.graph.nodes[n2id['other']]
			if not (test_symbol_other.sType == 'object' and test_symbol_other.name!=test_symbol_s.name and test_symbol_other.name!=test_symbol_o.name and test_symbol_other.name!=test_symbol_r.name and test_symbol_other.name!=test_symbol_se.name and test_symbol_other.name!=test_symbol_po.name and test_symbol_other.name!=test_symbol_c.name):
				raise WrongRuleExecution('recognizeObjBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('recognizeObjBox@' + str(n2id) )
		return newNode



	# Rule recognizeObjTable
	def recognizeObjTable(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['r', 'o', 'know'], ['s', 'c', 'link'], ['s', 'po', 'link'], ['s', 'se', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														ret.append(self.recognizeObjTable_trigger(snode, n2id))
		return ret



	# Rule recognizeObjTable
	def recognizeObjTable_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjTable_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjTable_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('recognizeObjTable@' + str(n2id) )
		return newNode



	# Rule recognizeObjFails
	def recognizeObjFails(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['r', 'o', 'know'], ['s', 'c', 'link'], ['s', 'po', 'link'], ['s', 'se', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_se_name in nodes:
									symbol_se = nodes[symbol_se_name]
									n2id['se'] = symbol_se_name
									if symbol_se.sType == 'see' and symbol_se.name!=symbol_s.name and symbol_se.name!=symbol_o.name and symbol_se.name!=symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links:
										for symbol_po_name in nodes:
											symbol_po = nodes[symbol_po_name]
											n2id['po'] = symbol_po_name
											if symbol_po.sType == 'position' and symbol_po.name!=symbol_s.name and symbol_po.name!=symbol_o.name and symbol_po.name!=symbol_r.name and symbol_po.name!=symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links:
												for symbol_c_name in nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'unclassified' and symbol_c.name!=symbol_s.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_se.name and symbol_c.name!=symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														ret.append(self.recognizeObjFails_trigger(snode, n2id))
		return ret



	# Rule recognizeObjFails
	def recognizeObjFails_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('recognizeObjFails_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger')
			test_symbol_se = snode.graph.nodes[n2id['se']]
			if not (test_symbol_se.sType == 'see' and test_symbol_se.name!=test_symbol_s.name and test_symbol_se.name!=test_symbol_o.name and test_symbol_se.name!=test_symbol_r.name and [n2id["s"],n2id["se"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger')
			test_symbol_po = snode.graph.nodes[n2id['po']]
			if not (test_symbol_po.sType == 'position' and test_symbol_po.name!=test_symbol_s.name and test_symbol_po.name!=test_symbol_o.name and test_symbol_po.name!=test_symbol_r.name and test_symbol_po.name!=test_symbol_se.name and [n2id["s"],n2id["po"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'unclassified' and test_symbol_c.name!=test_symbol_s.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_se.name and test_symbol_c.name!=test_symbol_po.name and [n2id["s"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('recognizeObjFails_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('recognizeObjFails@' + str(n2id) )
		return newNode



	# Rule setObjectReach
	def setObjectReach(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['s', 'r', 'link'], ['s', 'rb', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_rb_name in nodes:
							symbol_rb = nodes[symbol_rb_name]
							n2id['rb'] = symbol_rb_name
							if symbol_rb.sType == 'reachable' and symbol_rb.name!=symbol_s.name and symbol_rb.name!=symbol_o.name and [n2id["s"],n2id["rb"],"link"] in snode.graph.links:
								for symbol_r_name in nodes:
									symbol_r = nodes[symbol_r_name]
									n2id['r'] = symbol_r_name
									if symbol_r.sType == 'notReach' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and symbol_r.name!=symbol_rb.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
										# At this point we meet all the conditions.
										# Insert additional conditions manually here if you want.
										# (beware that the code could be regenerated and you might lose your changes).
										ret.append(self.setObjectReach_trigger(snode, n2id))
		return ret



	# Rule setObjectReach
	def setObjectReach_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectReach_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger')
			test_symbol_rb = snode.graph.nodes[n2id['rb']]
			if not (test_symbol_rb.sType == 'reachable' and test_symbol_rb.name!=test_symbol_s.name and test_symbol_rb.name!=test_symbol_o.name and [n2id["s"],n2id["rb"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notReach' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and test_symbol_r.name!=test_symbol_rb.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectReach_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('setObjectReach@' + str(n2id) )
		return newNode



	# Rule setObjectSee
	def setObjectSee(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['s', 'r', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'notSee' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
								# At this point we meet all the conditions.
								# Insert additional conditions manually here if you want.
								# (beware that the code could be regenerated and you might lose your changes).
								ret.append(self.setObjectSee_trigger(snode, n2id))
		return ret



	# Rule setObjectSee
	def setObjectSee_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectSee_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectSee_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notSee' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectSee_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('setObjectSee@' + str(n2id) )
		return newNode



	# Rule setObjectPosition
	def setObjectPosition(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 's', 'has'], ['s', 'r', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'notPosition' and symbol_r.name!=symbol_s.name and symbol_r.name!=symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links:
								# At this point we meet all the conditions.
								# Insert additional conditions manually here if you want.
								# (beware that the code could be regenerated and you might lose your changes).
								ret.append(self.setObjectPosition_trigger(snode, n2id))
		return ret



	# Rule setObjectPosition
	def setObjectPosition_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('setObjectPosition_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('setObjectPosition_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'notPosition' and test_symbol_r.name!=test_symbol_s.name and test_symbol_r.name!=test_symbol_o.name and [n2id["s"],n2id["r"],"link"] in snode.graph.links):
				raise WrongRuleExecution('setObjectPosition_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('setObjectPosition@' + str(n2id) )
		return newNode



	# Rule tellHumanAboutMug
	def tellHumanAboutMug(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['cont1', 'cont2', 'eq'], ['o', 'sr', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['sr', 'c', 'link'], ['sr', 'cont1', 'in'], ['sr', 'm', 'link'], ['sr', 'p', 'link'] ]
		for symbol_sr_name in nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_cont1_name in nodes:
									symbol_cont1 = nodes[symbol_cont1_name]
									n2id['cont1'] = symbol_cont1_name
									if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_sr.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links:
										for symbol_p_name in nodes:
											symbol_p = nodes[symbol_p_name]
											n2id['p'] = symbol_p_name
											if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
												for symbol_m_name in nodes:
													symbol_m = nodes[symbol_m_name]
													n2id['m'] = symbol_m_name
													if symbol_m.sType == 'mug' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_cont1.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
														for symbol_h_name in nodes:
															symbol_h = nodes[symbol_h_name]
															n2id['h'] = symbol_h_name
															if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_cont1.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
																for symbol_cont2_name in nodes:
																	symbol_cont2 = nodes[symbol_cont2_name]
																	n2id['cont2'] = symbol_cont2_name
																	if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_sr.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_cont1.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_m.name and symbol_cont2.name!=symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_c_name in nodes:
																			symbol_c = nodes[symbol_c_name]
																			n2id['c'] = symbol_c_name
																			if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_cont1.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and symbol_c.name!=symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				if not hasEqual(n2id["o"], snode.graph):
																					ret.append(self.tellHumanAboutMug_trigger(snode, n2id))
		return ret



	# Rule tellHumanAboutMug
	def tellHumanAboutMug_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_sr.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_cont1.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_cont1.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_sr.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_cont1.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_m.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_cont1.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and test_symbol_c.name!=test_symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutMug_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('tellHumanAboutMug@' + str(n2id) )
		return newNode



	# Rule tellHumanAboutBox
	def tellHumanAboutBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['cont1', 'cont2', 'eq'], ['o', 'sr', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['sr', 'c', 'link'], ['sr', 'cont1', 'in'], ['sr', 'm', 'link'], ['sr', 'p', 'link'] ]
		for symbol_sr_name in nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_cont1_name in nodes:
									symbol_cont1 = nodes[symbol_cont1_name]
									n2id['cont1'] = symbol_cont1_name
									if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_sr.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links:
										for symbol_p_name in nodes:
											symbol_p = nodes[symbol_p_name]
											n2id['p'] = symbol_p_name
											if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
												for symbol_m_name in nodes:
													symbol_m = nodes[symbol_m_name]
													n2id['m'] = symbol_m_name
													if symbol_m.sType == 'box' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_cont1.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
														for symbol_h_name in nodes:
															symbol_h = nodes[symbol_h_name]
															n2id['h'] = symbol_h_name
															if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_cont1.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
																for symbol_cont2_name in nodes:
																	symbol_cont2 = nodes[symbol_cont2_name]
																	n2id['cont2'] = symbol_cont2_name
																	if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_sr.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_cont1.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_m.name and symbol_cont2.name!=symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_c_name in nodes:
																			symbol_c = nodes[symbol_c_name]
																			n2id['c'] = symbol_c_name
																			if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_cont1.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and symbol_c.name!=symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				if not hasEqual(n2id["o"], snode.graph):
																					ret.append(self.tellHumanAboutBox_trigger(snode, n2id))
		return ret



	# Rule tellHumanAboutBox
	def tellHumanAboutBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_sr.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o.name and [n2id["sr"],n2id["cont1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_cont1.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'box' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_cont1.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_cont1.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_sr.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_cont1.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_m.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_cont1.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and test_symbol_c.name!=test_symbol_cont2.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('tellHumanAboutBox@' + str(n2id) )
		return newNode



	# Rule tellHumanAboutTable
	def tellHumanAboutTable(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 'sr', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['sr', 'c', 'link'], ['sr', 'm', 'link'], ['sr', 'p', 'link'] ]
		for symbol_sr_name in nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_p_name in nodes:
									symbol_p = nodes[symbol_p_name]
									n2id['p'] = symbol_p_name
									if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
										for symbol_m_name in nodes:
											symbol_m = nodes[symbol_m_name]
											n2id['m'] = symbol_m_name
											if symbol_m.sType == 'table' and symbol_m.name!=symbol_sr.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links:
												for symbol_h_name in nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_p.name and symbol_h.name!=symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
														for symbol_c_name in nodes:
															symbol_c = nodes[symbol_c_name]
															n2id['c'] = symbol_c_name
															if symbol_c.sType == 'classified' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_m.name and symbol_c.name!=symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																if not hasEqual(n2id["o"], snode.graph):
																	ret.append(self.tellHumanAboutTable_trigger(snode, n2id))
		return ret



	# Rule tellHumanAboutTable
	def tellHumanAboutTable_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'table' and test_symbol_m.name!=test_symbol_sr.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_p.name and [n2id["sr"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_p.name and test_symbol_h.name!=test_symbol_m.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classified' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_m.name and test_symbol_c.name!=test_symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutTable_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('tellHumanAboutTable@' + str(n2id) )
		return newNode



	# Rule tellHumanAboutUnknownObject
	def tellHumanAboutUnknownObject(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['o', 'sr', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['sr', 'c', 'link'], ['sr', 'p', 'link'] ]
		for symbol_sr_name in nodes:
			symbol_sr = nodes[symbol_sr_name]
			n2id['sr'] = symbol_sr_name
			if symbol_sr.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_sr.name:
						for symbol_o_name in nodes:
							symbol_o = nodes[symbol_o_name]
							n2id['o'] = symbol_o_name
							if symbol_o.sType == 'object' and symbol_o.name!=symbol_sr.name and symbol_o.name!=symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links:
								for symbol_p_name in nodes:
									symbol_p = nodes[symbol_p_name]
									n2id['p'] = symbol_p_name
									if symbol_p.sType == 'position' and symbol_p.name!=symbol_sr.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links:
										for symbol_h_name in nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_sr.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_p.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links:
												for symbol_c_name in nodes:
													symbol_c = nodes[symbol_c_name]
													n2id['c'] = symbol_c_name
													if symbol_c.sType == 'classifailed' and symbol_c.name!=symbol_sr.name and symbol_c.name!=symbol_r.name and symbol_c.name!=symbol_o.name and symbol_c.name!=symbol_p.name and symbol_c.name!=symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links:
														# At this point we meet all the conditions.
														# Insert additional conditions manually here if you want.
														# (beware that the code could be regenerated and you might lose your changes).
														if not hasEqual(n2id["o"], snode.graph):
															ret.append(self.tellHumanAboutUnknownObject_trigger(snode, n2id))
		return ret



	# Rule tellHumanAboutUnknownObject
	def tellHumanAboutUnknownObject_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_sr = snode.graph.nodes[n2id['sr']]
			if not (test_symbol_sr.sType == 'status'):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_sr.name):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_sr.name and test_symbol_o.name!=test_symbol_r.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["sr"],"has"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_sr.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o.name and [n2id["sr"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_sr.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_p.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
			test_symbol_c = snode.graph.nodes[n2id['c']]
			if not (test_symbol_c.sType == 'classifailed' and test_symbol_c.name!=test_symbol_sr.name and test_symbol_c.name!=test_symbol_r.name and test_symbol_c.name!=test_symbol_o.name and test_symbol_c.name!=test_symbol_p.name and test_symbol_c.name!=test_symbol_h.name and [n2id["sr"],n2id["c"],"link"] in snode.graph.links):
				raise WrongRuleExecution('tellHumanAboutUnknownObject_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 3
		newNode.depth += 1
		newNode.history.append('tellHumanAboutUnknownObject@' + str(n2id) )
		return newNode



	# Rule makeHumanLook
	def makeHumanLook(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o_h', 's', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'nS', 'link'], ['s', 'p', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_p_name in nodes:
													symbol_p = nodes[symbol_p_name]
													n2id['p'] = symbol_p_name
													if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
														for symbol_nS_name in nodes:
															symbol_nS = nodes[symbol_nS_name]
															n2id['nS'] = symbol_nS_name
															if symbol_nS.sType == 'notSee' and symbol_nS.name!=symbol_s.name and symbol_nS.name!=symbol_r.name and symbol_nS.name!=symbol_o_h.name and symbol_nS.name!=symbol_o.name and symbol_nS.name!=symbol_h.name and symbol_nS.name!=symbol_p.name and [n2id["s"],n2id["nS"],"link"] in snode.graph.links:
																# At this point we meet all the conditions.
																# Insert additional conditions manually here if you want.
																# (beware that the code could be regenerated and you might lose your changes).
																ret.append(self.makeHumanLook_trigger(snode, n2id))
		return ret



	# Rule makeHumanLook
	def makeHumanLook_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger')
			test_symbol_nS = snode.graph.nodes[n2id['nS']]
			if not (test_symbol_nS.sType == 'notSee' and test_symbol_nS.name!=test_symbol_s.name and test_symbol_nS.name!=test_symbol_r.name and test_symbol_nS.name!=test_symbol_o_h.name and test_symbol_nS.name!=test_symbol_o.name and test_symbol_nS.name!=test_symbol_h.name and test_symbol_nS.name!=test_symbol_p.name and [n2id["s"],n2id["nS"],"link"] in snode.graph.links):
				raise WrongRuleExecution('makeHumanLook_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 2
		newNode.depth += 1
		newNode.history.append('makeHumanLook@' + str(n2id) )
		return newNode



	# Rule humanClassifiesMug
	def humanClassifiesMug(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o_h', 's', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'cl', 'link'], ['s', 'p', 'link'], ['s', 'see', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		for symbol_cont2_name in nodes:
																			symbol_cont2 = nodes[symbol_cont2_name]
																			n2id['cont2'] = symbol_cont2_name
																			if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_h.name and symbol_cont2.name!=symbol_see.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_cl.name:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				ret.append(self.humanClassifiesMug_trigger(snode, n2id))
		return ret



	# Rule humanClassifiesMug
	def humanClassifiesMug_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_h.name and test_symbol_cont2.name!=test_symbol_see.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_cl.name):
				raise WrongRuleExecution('humanClassifiesMug_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 2
		newNode.depth += 1
		newNode.history.append('humanClassifiesMug@' + str(n2id) )
		return newNode



	# Rule humanClassifiesBox
	def humanClassifiesBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o_h', 's', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'cl', 'link'], ['s', 'p', 'link'], ['s', 'see', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		for symbol_cont2_name in nodes:
																			symbol_cont2 = nodes[symbol_cont2_name]
																			n2id['cont2'] = symbol_cont2_name
																			if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_h.name and symbol_cont2.name!=symbol_see.name and symbol_cont2.name!=symbol_p.name and symbol_cont2.name!=symbol_cl.name:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				ret.append(self.humanClassifiesBox_trigger(snode, n2id))
		return ret



	# Rule humanClassifiesBox
	def humanClassifiesBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_h.name and test_symbol_cont2.name!=test_symbol_see.name and test_symbol_cont2.name!=test_symbol_p.name and test_symbol_cont2.name!=test_symbol_cl.name):
				raise WrongRuleExecution('humanClassifiesBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 2
		newNode.depth += 1
		newNode.history.append('humanClassifiesBox@' + str(n2id) )
		return newNode



	# Rule humanClassifiesTable
	def humanClassifiesTable(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o_h', 's', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'cl', 'link'], ['s', 'p', 'link'], ['s', 'see', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_o_h_name in nodes:
							symbol_o_h = nodes[symbol_o_h_name]
							n2id['o_h'] = symbol_o_h_name
							if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_s.name and symbol_o_h.name!=symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links:
								for symbol_o_name in nodes:
									symbol_o = nodes[symbol_o_name]
									n2id['o'] = symbol_o_name
									if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
										for symbol_h_name in nodes:
											symbol_h = nodes[symbol_h_name]
											n2id['h'] = symbol_h_name
											if symbol_h.sType == 'human' and symbol_h.name!=symbol_s.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
												for symbol_see_name in nodes:
													symbol_see = nodes[symbol_see_name]
													n2id['see'] = symbol_see_name
													if symbol_see.sType == 'see' and symbol_see.name!=symbol_s.name and symbol_see.name!=symbol_r.name and symbol_see.name!=symbol_o_h.name and symbol_see.name!=symbol_o.name and symbol_see.name!=symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links:
														for symbol_p_name in nodes:
															symbol_p = nodes[symbol_p_name]
															n2id['p'] = symbol_p_name
															if symbol_p.sType == 'position' and symbol_p.name!=symbol_s.name and symbol_p.name!=symbol_r.name and symbol_p.name!=symbol_o_h.name and symbol_p.name!=symbol_o.name and symbol_p.name!=symbol_h.name and symbol_p.name!=symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links:
																for symbol_cl_name in nodes:
																	symbol_cl = nodes[symbol_cl_name]
																	n2id['cl'] = symbol_cl_name
																	if symbol_cl.sType == 'unclassified' and symbol_cl.name!=symbol_s.name and symbol_cl.name!=symbol_r.name and symbol_cl.name!=symbol_o_h.name and symbol_cl.name!=symbol_o.name and symbol_cl.name!=symbol_h.name and symbol_cl.name!=symbol_see.name and symbol_cl.name!=symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links:
																		# At this point we meet all the conditions.
																		# Insert additional conditions manually here if you want.
																		# (beware that the code could be regenerated and you might lose your changes).
																		ret.append(self.humanClassifiesTable_trigger(snode, n2id))
		return ret



	# Rule humanClassifiesTable
	def humanClassifiesTable_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_s.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o_h"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_o_h.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_s.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_o.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_see = snode.graph.nodes[n2id['see']]
			if not (test_symbol_see.sType == 'see' and test_symbol_see.name!=test_symbol_s.name and test_symbol_see.name!=test_symbol_r.name and test_symbol_see.name!=test_symbol_o_h.name and test_symbol_see.name!=test_symbol_o.name and test_symbol_see.name!=test_symbol_h.name and [n2id["s"],n2id["see"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_p = snode.graph.nodes[n2id['p']]
			if not (test_symbol_p.sType == 'position' and test_symbol_p.name!=test_symbol_s.name and test_symbol_p.name!=test_symbol_r.name and test_symbol_p.name!=test_symbol_o_h.name and test_symbol_p.name!=test_symbol_o.name and test_symbol_p.name!=test_symbol_h.name and test_symbol_p.name!=test_symbol_see.name and [n2id["s"],n2id["p"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
			test_symbol_cl = snode.graph.nodes[n2id['cl']]
			if not (test_symbol_cl.sType == 'unclassified' and test_symbol_cl.name!=test_symbol_s.name and test_symbol_cl.name!=test_symbol_r.name and test_symbol_cl.name!=test_symbol_o_h.name and test_symbol_cl.name!=test_symbol_o.name and test_symbol_cl.name!=test_symbol_h.name and test_symbol_cl.name!=test_symbol_see.name and test_symbol_cl.name!=test_symbol_p.name and [n2id["s"],n2id["cl"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanClassifiesTable_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 2
		newNode.depth += 1
		newNode.history.append('humanClassifiesTable@' + str(n2id) )
		return newNode



	# Rule humanTellsUsAboutMug
	def humanTellsUsAboutMug(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['cont1', 'cont2', 'eq'], ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o', 's', 'has'], ['o_h', 'soh', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'f', 'link'], ['soh', 'ch', 'link'], ['soh', 'cont2', 'in'], ['soh', 'mh', 'link'] ]
		for symbol_soh_name in nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_cont2_name in nodes:
															symbol_cont2 = nodes[symbol_cont2_name]
															n2id['cont2'] = symbol_cont2_name
															if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_soh.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links:
																for symbol_cont1_name in nodes:
																	symbol_cont1 = nodes[symbol_cont1_name]
																	n2id['cont1'] = symbol_cont1_name
																	if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_soh.name and symbol_cont1.name!=symbol_o.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o_h.name and symbol_cont1.name!=symbol_s.name and symbol_cont1.name!=symbol_h.name and symbol_cont1.name!=symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_mh_name in nodes:
																			symbol_mh = nodes[symbol_mh_name]
																			n2id['mh'] = symbol_mh_name
																			if symbol_mh.sType == 'mug' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and symbol_mh.name!=symbol_cont2.name and symbol_mh.name!=symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																				for symbol_f_name in nodes:
																					symbol_f = nodes[symbol_f_name]
																					n2id['f'] = symbol_f_name
																					if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_cont2.name and symbol_f.name!=symbol_cont1.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																						for symbol_ch_name in nodes:
																							symbol_ch = nodes[symbol_ch_name]
																							n2id['ch'] = symbol_ch_name
																							if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_cont2.name and symbol_ch.name!=symbol_cont1.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																								# At this point we meet all the conditions.
																								# Insert additional conditions manually here if you want.
																								# (beware that the code could be regenerated and you might lose your changes).
																								if not hasEqual(n2id["o"], snode.graph):
																									ret.append(self.humanTellsUsAboutMug_trigger(snode, n2id))
		return ret



	# Rule humanTellsUsAboutMug
	def humanTellsUsAboutMug_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_soh.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_soh.name and test_symbol_cont1.name!=test_symbol_o.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o_h.name and test_symbol_cont1.name!=test_symbol_s.name and test_symbol_cont1.name!=test_symbol_h.name and test_symbol_cont1.name!=test_symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'mug' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and test_symbol_mh.name!=test_symbol_cont2.name and test_symbol_mh.name!=test_symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_cont2.name and test_symbol_f.name!=test_symbol_cont1.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_cont2.name and test_symbol_ch.name!=test_symbol_cont1.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutMug_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 3
		newNode.depth += 1
		newNode.history.append('humanTellsUsAboutMug@' + str(n2id) )
		return newNode



	# Rule humanTellsUsAboutBox
	def humanTellsUsAboutBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['cont1', 'cont2', 'eq'], ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o', 's', 'has'], ['o_h', 'soh', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'f', 'link'], ['soh', 'ch', 'link'], ['soh', 'cont2', 'in'], ['soh', 'mh', 'link'] ]
		for symbol_soh_name in nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_cont2_name in nodes:
															symbol_cont2 = nodes[symbol_cont2_name]
															n2id['cont2'] = symbol_cont2_name
															if symbol_cont2.sType == 'object' and symbol_cont2.name!=symbol_soh.name and symbol_cont2.name!=symbol_o.name and symbol_cont2.name!=symbol_r.name and symbol_cont2.name!=symbol_o_h.name and symbol_cont2.name!=symbol_s.name and symbol_cont2.name!=symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links:
																for symbol_cont1_name in nodes:
																	symbol_cont1 = nodes[symbol_cont1_name]
																	n2id['cont1'] = symbol_cont1_name
																	if symbol_cont1.sType == 'object' and symbol_cont1.name!=symbol_soh.name and symbol_cont1.name!=symbol_o.name and symbol_cont1.name!=symbol_r.name and symbol_cont1.name!=symbol_o_h.name and symbol_cont1.name!=symbol_s.name and symbol_cont1.name!=symbol_h.name and symbol_cont1.name!=symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links:
																		for symbol_mh_name in nodes:
																			symbol_mh = nodes[symbol_mh_name]
																			n2id['mh'] = symbol_mh_name
																			if symbol_mh.sType == 'box' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and symbol_mh.name!=symbol_cont2.name and symbol_mh.name!=symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																				for symbol_f_name in nodes:
																					symbol_f = nodes[symbol_f_name]
																					n2id['f'] = symbol_f_name
																					if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_cont2.name and symbol_f.name!=symbol_cont1.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																						for symbol_ch_name in nodes:
																							symbol_ch = nodes[symbol_ch_name]
																							n2id['ch'] = symbol_ch_name
																							if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_cont2.name and symbol_ch.name!=symbol_cont1.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																								# At this point we meet all the conditions.
																								# Insert additional conditions manually here if you want.
																								# (beware that the code could be regenerated and you might lose your changes).
																								ret.append(self.humanTellsUsAboutBox_trigger(snode, n2id))
		return ret



	# Rule humanTellsUsAboutBox
	def humanTellsUsAboutBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_cont2 = snode.graph.nodes[n2id['cont2']]
			if not (test_symbol_cont2.sType == 'object' and test_symbol_cont2.name!=test_symbol_soh.name and test_symbol_cont2.name!=test_symbol_o.name and test_symbol_cont2.name!=test_symbol_r.name and test_symbol_cont2.name!=test_symbol_o_h.name and test_symbol_cont2.name!=test_symbol_s.name and test_symbol_cont2.name!=test_symbol_h.name and [n2id["soh"],n2id["cont2"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_cont1 = snode.graph.nodes[n2id['cont1']]
			if not (test_symbol_cont1.sType == 'object' and test_symbol_cont1.name!=test_symbol_soh.name and test_symbol_cont1.name!=test_symbol_o.name and test_symbol_cont1.name!=test_symbol_r.name and test_symbol_cont1.name!=test_symbol_o_h.name and test_symbol_cont1.name!=test_symbol_s.name and test_symbol_cont1.name!=test_symbol_h.name and test_symbol_cont1.name!=test_symbol_cont2.name and [n2id["cont1"],n2id["cont2"],"eq"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'box' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and test_symbol_mh.name!=test_symbol_cont2.name and test_symbol_mh.name!=test_symbol_cont1.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_cont2.name and test_symbol_f.name!=test_symbol_cont1.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_cont2.name and test_symbol_ch.name!=test_symbol_cont1.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 3
		newNode.depth += 1
		newNode.history.append('humanTellsUsAboutBox@' + str(n2id) )
		return newNode



	# Rule humanTellsUsAboutTable
	def humanTellsUsAboutTable(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['h', 'o_h', 'know'], ['o', 'o_h', 'eq'], ['o', 's', 'has'], ['o_h', 'soh', 'has'], ['r', 'h', 'interacting'], ['r', 'o', 'know'], ['s', 'f', 'link'], ['soh', 'ch', 'link'], ['soh', 'mh', 'link'] ]
		for symbol_soh_name in nodes:
			symbol_soh = nodes[symbol_soh_name]
			n2id['soh'] = symbol_soh_name
			if symbol_soh.sType == 'status':
				for symbol_o_name in nodes:
					symbol_o = nodes[symbol_o_name]
					n2id['o'] = symbol_o_name
					if symbol_o.sType == 'object' and symbol_o.name!=symbol_soh.name:
						for symbol_r_name in nodes:
							symbol_r = nodes[symbol_r_name]
							n2id['r'] = symbol_r_name
							if symbol_r.sType == 'robot' and symbol_r.name!=symbol_soh.name and symbol_r.name!=symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links:
								for symbol_o_h_name in nodes:
									symbol_o_h = nodes[symbol_o_h_name]
									n2id['o_h'] = symbol_o_h_name
									if symbol_o_h.sType == 'object' and symbol_o_h.name!=symbol_soh.name and symbol_o_h.name!=symbol_o.name and symbol_o_h.name!=symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links:
										for symbol_s_name in nodes:
											symbol_s = nodes[symbol_s_name]
											n2id['s'] = symbol_s_name
											if symbol_s.sType == 'status' and symbol_s.name!=symbol_soh.name and symbol_s.name!=symbol_o.name and symbol_s.name!=symbol_r.name and symbol_s.name!=symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
												for symbol_h_name in nodes:
													symbol_h = nodes[symbol_h_name]
													n2id['h'] = symbol_h_name
													if symbol_h.sType == 'human' and symbol_h.name!=symbol_soh.name and symbol_h.name!=symbol_o.name and symbol_h.name!=symbol_r.name and symbol_h.name!=symbol_o_h.name and symbol_h.name!=symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links:
														for symbol_mh_name in nodes:
															symbol_mh = nodes[symbol_mh_name]
															n2id['mh'] = symbol_mh_name
															if symbol_mh.sType == 'table' and symbol_mh.name!=symbol_soh.name and symbol_mh.name!=symbol_o.name and symbol_mh.name!=symbol_r.name and symbol_mh.name!=symbol_o_h.name and symbol_mh.name!=symbol_s.name and symbol_mh.name!=symbol_h.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links:
																for symbol_f_name in nodes:
																	symbol_f = nodes[symbol_f_name]
																	n2id['f'] = symbol_f_name
																	if symbol_f.sType == 'classifailed' and symbol_f.name!=symbol_soh.name and symbol_f.name!=symbol_o.name and symbol_f.name!=symbol_r.name and symbol_f.name!=symbol_o_h.name and symbol_f.name!=symbol_s.name and symbol_f.name!=symbol_h.name and symbol_f.name!=symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links:
																		for symbol_ch_name in nodes:
																			symbol_ch = nodes[symbol_ch_name]
																			n2id['ch'] = symbol_ch_name
																			if symbol_ch.sType == 'classified' and symbol_ch.name!=symbol_soh.name and symbol_ch.name!=symbol_o.name and symbol_ch.name!=symbol_r.name and symbol_ch.name!=symbol_o_h.name and symbol_ch.name!=symbol_s.name and symbol_ch.name!=symbol_h.name and symbol_ch.name!=symbol_mh.name and symbol_ch.name!=symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links:
																				# At this point we meet all the conditions.
																				# Insert additional conditions manually here if you want.
																				# (beware that the code could be regenerated and you might lose your changes).
																				ret.append(self.humanTellsUsAboutTable_trigger(snode, n2id))
		return ret



	# Rule humanTellsUsAboutTable
	def humanTellsUsAboutTable_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_soh = snode.graph.nodes[n2id['soh']]
			if not (test_symbol_soh.sType == 'status'):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_soh.name):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_soh.name and test_symbol_r.name!=test_symbol_o.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_o_h = snode.graph.nodes[n2id['o_h']]
			if not (test_symbol_o_h.sType == 'object' and test_symbol_o_h.name!=test_symbol_soh.name and test_symbol_o_h.name!=test_symbol_o.name and test_symbol_o_h.name!=test_symbol_r.name and [n2id["o"],n2id["o_h"],"eq"] in snode.graph.links and [n2id["o_h"],n2id["soh"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status' and test_symbol_s.name!=test_symbol_soh.name and test_symbol_s.name!=test_symbol_o.name and test_symbol_s.name!=test_symbol_r.name and test_symbol_s.name!=test_symbol_o_h.name and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_h = snode.graph.nodes[n2id['h']]
			if not (test_symbol_h.sType == 'human' and test_symbol_h.name!=test_symbol_soh.name and test_symbol_h.name!=test_symbol_o.name and test_symbol_h.name!=test_symbol_r.name and test_symbol_h.name!=test_symbol_o_h.name and test_symbol_h.name!=test_symbol_s.name and [n2id["r"],n2id["h"],"interacting"] in snode.graph.links and [n2id["h"],n2id["o_h"],"know"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_mh = snode.graph.nodes[n2id['mh']]
			if not (test_symbol_mh.sType == 'table' and test_symbol_mh.name!=test_symbol_soh.name and test_symbol_mh.name!=test_symbol_o.name and test_symbol_mh.name!=test_symbol_r.name and test_symbol_mh.name!=test_symbol_o_h.name and test_symbol_mh.name!=test_symbol_s.name and test_symbol_mh.name!=test_symbol_h.name and [n2id["soh"],n2id["mh"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_f = snode.graph.nodes[n2id['f']]
			if not (test_symbol_f.sType == 'classifailed' and test_symbol_f.name!=test_symbol_soh.name and test_symbol_f.name!=test_symbol_o.name and test_symbol_f.name!=test_symbol_r.name and test_symbol_f.name!=test_symbol_o_h.name and test_symbol_f.name!=test_symbol_s.name and test_symbol_f.name!=test_symbol_h.name and test_symbol_f.name!=test_symbol_mh.name and [n2id["s"],n2id["f"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
			test_symbol_ch = snode.graph.nodes[n2id['ch']]
			if not (test_symbol_ch.sType == 'classified' and test_symbol_ch.name!=test_symbol_soh.name and test_symbol_ch.name!=test_symbol_o.name and test_symbol_ch.name!=test_symbol_r.name and test_symbol_ch.name!=test_symbol_o_h.name and test_symbol_ch.name!=test_symbol_s.name and test_symbol_ch.name!=test_symbol_h.name and test_symbol_ch.name!=test_symbol_mh.name and test_symbol_ch.name!=test_symbol_f.name and [n2id["soh"],n2id["ch"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanTellsUsAboutTable_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 3
		newNode.depth += 1
		newNode.history.append('humanTellsUsAboutTable@' + str(n2id) )
		return newNode



	# Rule robotMovesMugFromTableToBox
	def robotMovesMugFromTableToBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['c1', 'cs1', 'has'], ['c2', 'cs2', 'has'], ['cs1', 'rc1', 'link'], ['cs1', 't', 'link'], ['cs2', 'b', 'link'], ['cs2', 'rc2', 'link'], ['o', 's', 'has'], ['r', 'c1', 'know'], ['r', 'c2', 'know'], ['r', 'o', 'know'], ['s', 'c1', 'in'], ['s', 'm', 'link'], ['s', 'r1', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'robot' and symbol_r.name!=symbol_s.name:
						for symbol_cs2_name in nodes:
							symbol_cs2 = nodes[symbol_cs2_name]
							n2id['cs2'] = symbol_cs2_name
							if symbol_cs2.sType == 'status' and symbol_cs2.name!=symbol_s.name and symbol_cs2.name!=symbol_r.name:
								for symbol_cs1_name in nodes:
									symbol_cs1 = nodes[symbol_cs1_name]
									n2id['cs1'] = symbol_cs1_name
									if symbol_cs1.sType == 'status' and symbol_cs1.name!=symbol_s.name and symbol_cs1.name!=symbol_r.name and symbol_cs1.name!=symbol_cs2.name:
										for symbol_c1_name in nodes:
											symbol_c1 = nodes[symbol_c1_name]
											n2id['c1'] = symbol_c1_name
											if symbol_c1.sType == 'object' and symbol_c1.name!=symbol_s.name and symbol_c1.name!=symbol_r.name and symbol_c1.name!=symbol_cs2.name and symbol_c1.name!=symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links:
												for symbol_o_name in nodes:
													symbol_o = nodes[symbol_o_name]
													n2id['o'] = symbol_o_name
													if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_cs2.name and symbol_o.name!=symbol_cs1.name and symbol_o.name!=symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
														for symbol_c2_name in nodes:
															symbol_c2 = nodes[symbol_c2_name]
															n2id['c2'] = symbol_c2_name
															if symbol_c2.sType == 'object' and symbol_c2.name!=symbol_s.name and symbol_c2.name!=symbol_r.name and symbol_c2.name!=symbol_cs2.name and symbol_c2.name!=symbol_cs1.name and symbol_c2.name!=symbol_c1.name and symbol_c2.name!=symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links:
																for symbol_t_name in nodes:
																	symbol_t = nodes[symbol_t_name]
																	n2id['t'] = symbol_t_name
																	if symbol_t.sType == 'table' and symbol_t.name!=symbol_s.name and symbol_t.name!=symbol_r.name and symbol_t.name!=symbol_cs2.name and symbol_t.name!=symbol_cs1.name and symbol_t.name!=symbol_c1.name and symbol_t.name!=symbol_o.name and symbol_t.name!=symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links:
																		for symbol_rc2_name in nodes:
																			symbol_rc2 = nodes[symbol_rc2_name]
																			n2id['rc2'] = symbol_rc2_name
																			if symbol_rc2.sType == 'reach' and symbol_rc2.name!=symbol_s.name and symbol_rc2.name!=symbol_r.name and symbol_rc2.name!=symbol_cs2.name and symbol_rc2.name!=symbol_cs1.name and symbol_rc2.name!=symbol_c1.name and symbol_rc2.name!=symbol_o.name and symbol_rc2.name!=symbol_c2.name and symbol_rc2.name!=symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links:
																				for symbol_rc1_name in nodes:
																					symbol_rc1 = nodes[symbol_rc1_name]
																					n2id['rc1'] = symbol_rc1_name
																					if symbol_rc1.sType == 'reach' and symbol_rc1.name!=symbol_s.name and symbol_rc1.name!=symbol_r.name and symbol_rc1.name!=symbol_cs2.name and symbol_rc1.name!=symbol_cs1.name and symbol_rc1.name!=symbol_c1.name and symbol_rc1.name!=symbol_o.name and symbol_rc1.name!=symbol_c2.name and symbol_rc1.name!=symbol_t.name and symbol_rc1.name!=symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links:
																						for symbol_r1_name in nodes:
																							symbol_r1 = nodes[symbol_r1_name]
																							n2id['r1'] = symbol_r1_name
																							if symbol_r1.sType == 'reach' and symbol_r1.name!=symbol_s.name and symbol_r1.name!=symbol_r.name and symbol_r1.name!=symbol_cs2.name and symbol_r1.name!=symbol_cs1.name and symbol_r1.name!=symbol_c1.name and symbol_r1.name!=symbol_o.name and symbol_r1.name!=symbol_c2.name and symbol_r1.name!=symbol_t.name and symbol_r1.name!=symbol_rc2.name and symbol_r1.name!=symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links:
																								for symbol_m_name in nodes:
																									symbol_m = nodes[symbol_m_name]
																									n2id['m'] = symbol_m_name
																									if symbol_m.sType == 'mug' and symbol_m.name!=symbol_s.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_cs2.name and symbol_m.name!=symbol_cs1.name and symbol_m.name!=symbol_c1.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_c2.name and symbol_m.name!=symbol_t.name and symbol_m.name!=symbol_rc2.name and symbol_m.name!=symbol_rc1.name and symbol_m.name!=symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links:
																										for symbol_b_name in nodes:
																											symbol_b = nodes[symbol_b_name]
																											n2id['b'] = symbol_b_name
																											if symbol_b.sType == 'box' and symbol_b.name!=symbol_s.name and symbol_b.name!=symbol_r.name and symbol_b.name!=symbol_cs2.name and symbol_b.name!=symbol_cs1.name and symbol_b.name!=symbol_c1.name and symbol_b.name!=symbol_o.name and symbol_b.name!=symbol_c2.name and symbol_b.name!=symbol_t.name and symbol_b.name!=symbol_rc2.name and symbol_b.name!=symbol_rc1.name and symbol_b.name!=symbol_r1.name and symbol_b.name!=symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links:
																												# At this point we meet all the conditions.
																												# Insert additional conditions manually here if you want.
																												# (beware that the code could be regenerated and you might lose your changes).
																												ret.append(self.robotMovesMugFromTableToBox_trigger(snode, n2id))
		return ret



	# Rule robotMovesMugFromTableToBox
	def robotMovesMugFromTableToBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'robot' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_cs2 = snode.graph.nodes[n2id['cs2']]
			if not (test_symbol_cs2.sType == 'status' and test_symbol_cs2.name!=test_symbol_s.name and test_symbol_cs2.name!=test_symbol_r.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_cs1 = snode.graph.nodes[n2id['cs1']]
			if not (test_symbol_cs1.sType == 'status' and test_symbol_cs1.name!=test_symbol_s.name and test_symbol_cs1.name!=test_symbol_r.name and test_symbol_cs1.name!=test_symbol_cs2.name):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_c1 = snode.graph.nodes[n2id['c1']]
			if not (test_symbol_c1.sType == 'object' and test_symbol_c1.name!=test_symbol_s.name and test_symbol_c1.name!=test_symbol_r.name and test_symbol_c1.name!=test_symbol_cs2.name and test_symbol_c1.name!=test_symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_cs2.name and test_symbol_o.name!=test_symbol_cs1.name and test_symbol_o.name!=test_symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_c2 = snode.graph.nodes[n2id['c2']]
			if not (test_symbol_c2.sType == 'object' and test_symbol_c2.name!=test_symbol_s.name and test_symbol_c2.name!=test_symbol_r.name and test_symbol_c2.name!=test_symbol_cs2.name and test_symbol_c2.name!=test_symbol_cs1.name and test_symbol_c2.name!=test_symbol_c1.name and test_symbol_c2.name!=test_symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_t = snode.graph.nodes[n2id['t']]
			if not (test_symbol_t.sType == 'table' and test_symbol_t.name!=test_symbol_s.name and test_symbol_t.name!=test_symbol_r.name and test_symbol_t.name!=test_symbol_cs2.name and test_symbol_t.name!=test_symbol_cs1.name and test_symbol_t.name!=test_symbol_c1.name and test_symbol_t.name!=test_symbol_o.name and test_symbol_t.name!=test_symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_rc2 = snode.graph.nodes[n2id['rc2']]
			if not (test_symbol_rc2.sType == 'reach' and test_symbol_rc2.name!=test_symbol_s.name and test_symbol_rc2.name!=test_symbol_r.name and test_symbol_rc2.name!=test_symbol_cs2.name and test_symbol_rc2.name!=test_symbol_cs1.name and test_symbol_rc2.name!=test_symbol_c1.name and test_symbol_rc2.name!=test_symbol_o.name and test_symbol_rc2.name!=test_symbol_c2.name and test_symbol_rc2.name!=test_symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_rc1 = snode.graph.nodes[n2id['rc1']]
			if not (test_symbol_rc1.sType == 'reach' and test_symbol_rc1.name!=test_symbol_s.name and test_symbol_rc1.name!=test_symbol_r.name and test_symbol_rc1.name!=test_symbol_cs2.name and test_symbol_rc1.name!=test_symbol_cs1.name and test_symbol_rc1.name!=test_symbol_c1.name and test_symbol_rc1.name!=test_symbol_o.name and test_symbol_rc1.name!=test_symbol_c2.name and test_symbol_rc1.name!=test_symbol_t.name and test_symbol_rc1.name!=test_symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_r1 = snode.graph.nodes[n2id['r1']]
			if not (test_symbol_r1.sType == 'reach' and test_symbol_r1.name!=test_symbol_s.name and test_symbol_r1.name!=test_symbol_r.name and test_symbol_r1.name!=test_symbol_cs2.name and test_symbol_r1.name!=test_symbol_cs1.name and test_symbol_r1.name!=test_symbol_c1.name and test_symbol_r1.name!=test_symbol_o.name and test_symbol_r1.name!=test_symbol_c2.name and test_symbol_r1.name!=test_symbol_t.name and test_symbol_r1.name!=test_symbol_rc2.name and test_symbol_r1.name!=test_symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_s.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_cs2.name and test_symbol_m.name!=test_symbol_cs1.name and test_symbol_m.name!=test_symbol_c1.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_c2.name and test_symbol_m.name!=test_symbol_t.name and test_symbol_m.name!=test_symbol_rc2.name and test_symbol_m.name!=test_symbol_rc1.name and test_symbol_m.name!=test_symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
			test_symbol_b = snode.graph.nodes[n2id['b']]
			if not (test_symbol_b.sType == 'box' and test_symbol_b.name!=test_symbol_s.name and test_symbol_b.name!=test_symbol_r.name and test_symbol_b.name!=test_symbol_cs2.name and test_symbol_b.name!=test_symbol_cs1.name and test_symbol_b.name!=test_symbol_c1.name and test_symbol_b.name!=test_symbol_o.name and test_symbol_b.name!=test_symbol_c2.name and test_symbol_b.name!=test_symbol_t.name and test_symbol_b.name!=test_symbol_rc2.name and test_symbol_b.name!=test_symbol_rc1.name and test_symbol_b.name!=test_symbol_r1.name and test_symbol_b.name!=test_symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links):
				raise WrongRuleExecution('robotMovesMugFromTableToBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
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
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('robotMovesMugFromTableToBox@' + str(n2id) )
		return newNode



	# Rule humanMovesMugFromTableToBox
	def humanMovesMugFromTableToBox(self, snode):
		ret = []
		nodes = copy.deepcopy(snode.graph.nodes)
		n2id = dict()
		links = [ ['c1', 'cs1', 'has'], ['c2', 'cs2', 'has'], ['cs1', 'rc1', 'link'], ['cs1', 't', 'link'], ['cs2', 'b', 'link'], ['cs2', 'rc2', 'link'], ['o', 's', 'has'], ['r', 'c1', 'know'], ['r', 'c2', 'know'], ['r', 'o', 'know'], ['s', 'c1', 'in'], ['s', 'm', 'link'], ['s', 'r1', 'link'] ]
		for symbol_s_name in nodes:
			symbol_s = nodes[symbol_s_name]
			n2id['s'] = symbol_s_name
			if symbol_s.sType == 'status':
				for symbol_r_name in nodes:
					symbol_r = nodes[symbol_r_name]
					n2id['r'] = symbol_r_name
					if symbol_r.sType == 'human' and symbol_r.name!=symbol_s.name:
						for symbol_cs2_name in nodes:
							symbol_cs2 = nodes[symbol_cs2_name]
							n2id['cs2'] = symbol_cs2_name
							if symbol_cs2.sType == 'status' and symbol_cs2.name!=symbol_s.name and symbol_cs2.name!=symbol_r.name:
								for symbol_cs1_name in nodes:
									symbol_cs1 = nodes[symbol_cs1_name]
									n2id['cs1'] = symbol_cs1_name
									if symbol_cs1.sType == 'status' and symbol_cs1.name!=symbol_s.name and symbol_cs1.name!=symbol_r.name and symbol_cs1.name!=symbol_cs2.name:
										for symbol_c1_name in nodes:
											symbol_c1 = nodes[symbol_c1_name]
											n2id['c1'] = symbol_c1_name
											if symbol_c1.sType == 'object' and symbol_c1.name!=symbol_s.name and symbol_c1.name!=symbol_r.name and symbol_c1.name!=symbol_cs2.name and symbol_c1.name!=symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links:
												for symbol_o_name in nodes:
													symbol_o = nodes[symbol_o_name]
													n2id['o'] = symbol_o_name
													if symbol_o.sType == 'object' and symbol_o.name!=symbol_s.name and symbol_o.name!=symbol_r.name and symbol_o.name!=symbol_cs2.name and symbol_o.name!=symbol_cs1.name and symbol_o.name!=symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links:
														for symbol_c2_name in nodes:
															symbol_c2 = nodes[symbol_c2_name]
															n2id['c2'] = symbol_c2_name
															if symbol_c2.sType == 'object' and symbol_c2.name!=symbol_s.name and symbol_c2.name!=symbol_r.name and symbol_c2.name!=symbol_cs2.name and symbol_c2.name!=symbol_cs1.name and symbol_c2.name!=symbol_c1.name and symbol_c2.name!=symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links:
																for symbol_t_name in nodes:
																	symbol_t = nodes[symbol_t_name]
																	n2id['t'] = symbol_t_name
																	if symbol_t.sType == 'table' and symbol_t.name!=symbol_s.name and symbol_t.name!=symbol_r.name and symbol_t.name!=symbol_cs2.name and symbol_t.name!=symbol_cs1.name and symbol_t.name!=symbol_c1.name and symbol_t.name!=symbol_o.name and symbol_t.name!=symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links:
																		for symbol_rc2_name in nodes:
																			symbol_rc2 = nodes[symbol_rc2_name]
																			n2id['rc2'] = symbol_rc2_name
																			if symbol_rc2.sType == 'reach' and symbol_rc2.name!=symbol_s.name and symbol_rc2.name!=symbol_r.name and symbol_rc2.name!=symbol_cs2.name and symbol_rc2.name!=symbol_cs1.name and symbol_rc2.name!=symbol_c1.name and symbol_rc2.name!=symbol_o.name and symbol_rc2.name!=symbol_c2.name and symbol_rc2.name!=symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links:
																				for symbol_rc1_name in nodes:
																					symbol_rc1 = nodes[symbol_rc1_name]
																					n2id['rc1'] = symbol_rc1_name
																					if symbol_rc1.sType == 'reach' and symbol_rc1.name!=symbol_s.name and symbol_rc1.name!=symbol_r.name and symbol_rc1.name!=symbol_cs2.name and symbol_rc1.name!=symbol_cs1.name and symbol_rc1.name!=symbol_c1.name and symbol_rc1.name!=symbol_o.name and symbol_rc1.name!=symbol_c2.name and symbol_rc1.name!=symbol_t.name and symbol_rc1.name!=symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links:
																						for symbol_r1_name in nodes:
																							symbol_r1 = nodes[symbol_r1_name]
																							n2id['r1'] = symbol_r1_name
																							if symbol_r1.sType == 'reach' and symbol_r1.name!=symbol_s.name and symbol_r1.name!=symbol_r.name and symbol_r1.name!=symbol_cs2.name and symbol_r1.name!=symbol_cs1.name and symbol_r1.name!=symbol_c1.name and symbol_r1.name!=symbol_o.name and symbol_r1.name!=symbol_c2.name and symbol_r1.name!=symbol_t.name and symbol_r1.name!=symbol_rc2.name and symbol_r1.name!=symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links:
																								for symbol_m_name in nodes:
																									symbol_m = nodes[symbol_m_name]
																									n2id['m'] = symbol_m_name
																									if symbol_m.sType == 'mug' and symbol_m.name!=symbol_s.name and symbol_m.name!=symbol_r.name and symbol_m.name!=symbol_cs2.name and symbol_m.name!=symbol_cs1.name and symbol_m.name!=symbol_c1.name and symbol_m.name!=symbol_o.name and symbol_m.name!=symbol_c2.name and symbol_m.name!=symbol_t.name and symbol_m.name!=symbol_rc2.name and symbol_m.name!=symbol_rc1.name and symbol_m.name!=symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links:
																										for symbol_b_name in nodes:
																											symbol_b = nodes[symbol_b_name]
																											n2id['b'] = symbol_b_name
																											if symbol_b.sType == 'box' and symbol_b.name!=symbol_s.name and symbol_b.name!=symbol_r.name and symbol_b.name!=symbol_cs2.name and symbol_b.name!=symbol_cs1.name and symbol_b.name!=symbol_c1.name and symbol_b.name!=symbol_o.name and symbol_b.name!=symbol_c2.name and symbol_b.name!=symbol_t.name and symbol_b.name!=symbol_rc2.name and symbol_b.name!=symbol_rc1.name and symbol_b.name!=symbol_r1.name and symbol_b.name!=symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links:
																												# At this point we meet all the conditions.
																												# Insert additional conditions manually here if you want.
																												# (beware that the code could be regenerated and you might lose your changes).
																												ret.append(self.humanMovesMugFromTableToBox_trigger(snode, n2id))
		return ret



	# Rule humanMovesMugFromTableToBox
	def humanMovesMugFromTableToBox_trigger(self, snode, n2id, checked=True):
		if not checked:
			test_symbol_s = snode.graph.nodes[n2id['s']]
			if not (test_symbol_s.sType == 'status'):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_r = snode.graph.nodes[n2id['r']]
			if not (test_symbol_r.sType == 'human' and test_symbol_r.name!=test_symbol_s.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_cs2 = snode.graph.nodes[n2id['cs2']]
			if not (test_symbol_cs2.sType == 'status' and test_symbol_cs2.name!=test_symbol_s.name and test_symbol_cs2.name!=test_symbol_r.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_cs1 = snode.graph.nodes[n2id['cs1']]
			if not (test_symbol_cs1.sType == 'status' and test_symbol_cs1.name!=test_symbol_s.name and test_symbol_cs1.name!=test_symbol_r.name and test_symbol_cs1.name!=test_symbol_cs2.name):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_c1 = snode.graph.nodes[n2id['c1']]
			if not (test_symbol_c1.sType == 'object' and test_symbol_c1.name!=test_symbol_s.name and test_symbol_c1.name!=test_symbol_r.name and test_symbol_c1.name!=test_symbol_cs2.name and test_symbol_c1.name!=test_symbol_cs1.name and [n2id["r"],n2id["c1"],"know"] in snode.graph.links and [n2id["c1"],n2id["cs1"],"has"] in snode.graph.links and [n2id["s"],n2id["c1"],"in"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_o = snode.graph.nodes[n2id['o']]
			if not (test_symbol_o.sType == 'object' and test_symbol_o.name!=test_symbol_s.name and test_symbol_o.name!=test_symbol_r.name and test_symbol_o.name!=test_symbol_cs2.name and test_symbol_o.name!=test_symbol_cs1.name and test_symbol_o.name!=test_symbol_c1.name and [n2id["r"],n2id["o"],"know"] in snode.graph.links and [n2id["o"],n2id["s"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_c2 = snode.graph.nodes[n2id['c2']]
			if not (test_symbol_c2.sType == 'object' and test_symbol_c2.name!=test_symbol_s.name and test_symbol_c2.name!=test_symbol_r.name and test_symbol_c2.name!=test_symbol_cs2.name and test_symbol_c2.name!=test_symbol_cs1.name and test_symbol_c2.name!=test_symbol_c1.name and test_symbol_c2.name!=test_symbol_o.name and [n2id["r"],n2id["c2"],"know"] in snode.graph.links and [n2id["c2"],n2id["cs2"],"has"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_t = snode.graph.nodes[n2id['t']]
			if not (test_symbol_t.sType == 'table' and test_symbol_t.name!=test_symbol_s.name and test_symbol_t.name!=test_symbol_r.name and test_symbol_t.name!=test_symbol_cs2.name and test_symbol_t.name!=test_symbol_cs1.name and test_symbol_t.name!=test_symbol_c1.name and test_symbol_t.name!=test_symbol_o.name and test_symbol_t.name!=test_symbol_c2.name and [n2id["cs1"],n2id["t"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_rc2 = snode.graph.nodes[n2id['rc2']]
			if not (test_symbol_rc2.sType == 'reach' and test_symbol_rc2.name!=test_symbol_s.name and test_symbol_rc2.name!=test_symbol_r.name and test_symbol_rc2.name!=test_symbol_cs2.name and test_symbol_rc2.name!=test_symbol_cs1.name and test_symbol_rc2.name!=test_symbol_c1.name and test_symbol_rc2.name!=test_symbol_o.name and test_symbol_rc2.name!=test_symbol_c2.name and test_symbol_rc2.name!=test_symbol_t.name and [n2id["cs2"],n2id["rc2"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_rc1 = snode.graph.nodes[n2id['rc1']]
			if not (test_symbol_rc1.sType == 'reach' and test_symbol_rc1.name!=test_symbol_s.name and test_symbol_rc1.name!=test_symbol_r.name and test_symbol_rc1.name!=test_symbol_cs2.name and test_symbol_rc1.name!=test_symbol_cs1.name and test_symbol_rc1.name!=test_symbol_c1.name and test_symbol_rc1.name!=test_symbol_o.name and test_symbol_rc1.name!=test_symbol_c2.name and test_symbol_rc1.name!=test_symbol_t.name and test_symbol_rc1.name!=test_symbol_rc2.name and [n2id["cs1"],n2id["rc1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_r1 = snode.graph.nodes[n2id['r1']]
			if not (test_symbol_r1.sType == 'reach' and test_symbol_r1.name!=test_symbol_s.name and test_symbol_r1.name!=test_symbol_r.name and test_symbol_r1.name!=test_symbol_cs2.name and test_symbol_r1.name!=test_symbol_cs1.name and test_symbol_r1.name!=test_symbol_c1.name and test_symbol_r1.name!=test_symbol_o.name and test_symbol_r1.name!=test_symbol_c2.name and test_symbol_r1.name!=test_symbol_t.name and test_symbol_r1.name!=test_symbol_rc2.name and test_symbol_r1.name!=test_symbol_rc1.name and [n2id["s"],n2id["r1"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_m = snode.graph.nodes[n2id['m']]
			if not (test_symbol_m.sType == 'mug' and test_symbol_m.name!=test_symbol_s.name and test_symbol_m.name!=test_symbol_r.name and test_symbol_m.name!=test_symbol_cs2.name and test_symbol_m.name!=test_symbol_cs1.name and test_symbol_m.name!=test_symbol_c1.name and test_symbol_m.name!=test_symbol_o.name and test_symbol_m.name!=test_symbol_c2.name and test_symbol_m.name!=test_symbol_t.name and test_symbol_m.name!=test_symbol_rc2.name and test_symbol_m.name!=test_symbol_rc1.name and test_symbol_m.name!=test_symbol_r1.name and [n2id["s"],n2id["m"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
			test_symbol_b = snode.graph.nodes[n2id['b']]
			if not (test_symbol_b.sType == 'box' and test_symbol_b.name!=test_symbol_s.name and test_symbol_b.name!=test_symbol_r.name and test_symbol_b.name!=test_symbol_cs2.name and test_symbol_b.name!=test_symbol_cs1.name and test_symbol_b.name!=test_symbol_c1.name and test_symbol_b.name!=test_symbol_o.name and test_symbol_b.name!=test_symbol_c2.name and test_symbol_b.name!=test_symbol_t.name and test_symbol_b.name!=test_symbol_rc2.name and test_symbol_b.name!=test_symbol_rc1.name and test_symbol_b.name!=test_symbol_r1.name and test_symbol_b.name!=test_symbol_m.name and [n2id["cs2"],n2id["b"],"link"] in snode.graph.links):
				raise WrongRuleExecution('humanMovesMugFromTableToBox_trigger')
		smap = copy.deepcopy(n2id)
		newNode = WorldStateHistory(snode)
		# <<Hardcoded stuff
		movedObject = smap['o']
		status = smap['s']
		oldContainter = smap['c1']
		newContainer = smap['c2']
		# >>Hardcoded stuff
		# Create nodes
		# Retype nodes
		# Remove nodes
		#print 'movedObject   ', movedObject
		#print 'status        ', status
		#print 'oldContainter ', oldContainter
		#print 'newContainer  ', newContainer
		newNode.graph.removeDanglingEdges()
		# Remove links
		newNode.graph.links = [x for x in newNode.graph.links if [x.a, x.b, x.linkType] not in [ [smap['s'], smap['c1'], 'in'] ]]
		# Create links
		l = AGMLink(smap['s'], smap['c2'], 'in')
		if not l in newNode.graph.links:
			newNode.graph.links.append(l)

		# <<Hardcoded stuff
		#print 'a'
		for l in newNode.graph.links:
			if l.b == movedObject and l.linkType == 'eq':
				#print 'b'
				similarObject = l.a
				#print 'similarObject', similarObject
				for l2 in newNode.graph.links:
					if l2.a == similarObject and l2.linkType == 'has':
						#print 'c'
						similarStatus = l2.b
						#print 'similarStatus', similarStatus
						for l3 in newNode.graph.links:
							if l3.a == similarStatus and l3.linkType == 'in':
								#print 'd'
								similarOldContainter = l3.b
								#print 'similarOldContainter', similarOldContainter
								for l4 in newNode.graph.links:
									if l4.b == newContainer and l4.linkType == 'eq':
										#print 'e'
										similarNewContainer = l4.a
										#print 'similarNewContainer', similarNewContainer
										for enlace in newNode.graph.links:
											if enlace.a == similarStatus and enlace.b == similarOldContainter and enlace.linkType == 'in':
												#print 'f'
												#print enlace.a, enlace.b, enlace.linkType
												enlace.b = similarNewContainer
												#print enlace.a, enlace.b, enlace.linkType
												#print 'g'

		# >>Hardcoded stuff

		# Misc stuff
		newNode.probability *= 1.
		newNode.cost += 1
		newNode.depth += 1
		newNode.history.append('humanMovesMugFromTableToBox@' + str(n2id) )
		return newNode

