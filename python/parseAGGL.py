from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from AGGL import *
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from parseQuantifiers import *

class AGMGraphParsing:
	@staticmethod
	def parseGraphFromAST(i, verbose=False):
		if type(i) == str:
			return AGMGraph(dict(), [])
		if verbose: print '\t{'
		nodes = dict()
		for t in i.nodes:
			if verbose: print '\tT: \'' + str(t.symbol) + '\' is a \'' + t.symbolType + '\' (' + t.x, ',', t.y + ')'
			pos = [0,0]
			try:
				multiply = 1.
				pos = [multiply*int(t.x), multiply*int(t.y)]
			except:
				pass
			if t.symbol in nodes:
				QMessageBox.warning(None, "Invalid node name", "Two nodes can't have the same name in the same graph. Because some planners are case-insensitive, we also perform a case-insensitive comparison.\nNode name: "+t.symbol)

			nodes[t.symbol] = AGMSymbol(t.symbol, t.symbolType, pos)
		links = []
		for l in i.links:
			if verbose: print '\t\tL:', l.lhs, '->', l.rhs, '('+l.no, l.linkType+') ['+l.enabled+']'
			lV = True
			if len(l.enabled)>0: lV = False
			links.append(AGMLink(l.lhs, l.rhs, l.linkType, lV))
		if verbose: print '\t}'
		return AGMGraph(nodes, links)


class AGMRuleParsing:
	@staticmethod
	def parseRuleFromAST(i, parameters, precondition, effect, verbose=False):
		passive = False
		if i.passive == 'passive':
			passive = True
		elif i.passive == 'active':
			passive = False
		else:
			print 'Error parsing rule', i.name+':', i.passive, 'is not a valid active/passive definition only "active" or "passive".'
			sys.exit(-345)
		try:
			mindepth = int(i.depth.value)
		except:
			mindepth = 0
		if hasattr(i, 'lhs') and (hasattr(i, 'lhs') and hasattr(i, 'lhs')): # We are dealing with a normal rule!
			print 'parseRuleFromAST', parameters
			print 'parseRuleFromAST', parameters
			print 'parseRuleFromAST', parameters
			# We are dealing with a normal rule!
			if verbose: print '\nRule:', i.name
			LHS = AGMGraphParsing.parseGraphFromAST(i.lhs, verbose)
			if verbose: print '\t===>'
			RHS = AGMGraphParsing.parseGraphFromAST(i.rhs, verbose)
			regular = AGMRule(i.name, LHS, RHS, passive, i.cost, parameters, precondition, effect)
			regular.mindepth = mindepth
			if len(i.conditions) > 0:
				regular.conditions = str(i.conditions[0])
			else:
				regular.conditions = ''
			if len(i.effects) > 0:
				regular.effects = str(i.effects[0])
			else:
				regular.effects = ''
			return regular
		elif hasattr(i, 'atomss'): # We are dealing with a rule combo!
			if len(i.atomss) == 0:
				print '  Error rrrrrrrrr  32423 trgf 2  Rule('+i.name+')'
				sys.exit(-1)
			#print '  Combo'
			# We are dealing with a rule combo!
			#print i.atoms
			combo = AGMComboRule(i.name, passive, i.cost, i.atomss.asList(), i.equivalences.asList())
			combo.mindepth = mindepth
			#print combo.toString()
			return combo
		else:
			print '  Error rrrrrrrrr'
			sys.exit(-1)
		

class AGMFileDataParsing:
	@staticmethod
	def fromFile(filename, verbose=False):
		if verbose: print 'Verbose:', verbose
		# Clear previous data
		agmFD = AGMFileData()
		agmFD.properties = dict()
		agmFD.agm.symbols = []
		agmFD.agm.rules = []

		# Define AGM's DSL meta-model
		an = Word(srange("[a-zA-Z0-9_.]"))
		ids = Word(srange("[a-zA-Z0-9_]"))
		almostanything = CharsNotIn("{}")
		parameters = Suppress("parameters")
		precondition = Suppress("precondition")
		effect = Suppress("effect")
		plusorminus = Literal('+') | Literal('-')
		number = Word(nums)
		nu = Combine( Optional(plusorminus) + number )
		neg = Optional(Literal('*'))
		sep = Suppress("===")
		dep = Suppress("mindepth")
		eq = Suppress("=")
		cn = Suppress(":")
		lk = Suppress("->")
		ar = Suppress("=>")
		op = Suppress("{")
		cl = Suppress("}")
		po = Suppress("(")
		co = Suppress(",")
		pt = Suppress(".")
		pc = Suppress(")")
		no = Suppress("!")

		# LINK
		link  = Group(an.setResultsName("lhs") + lk + an.setResultsName("rhs") + po + Optional(no).setResultsName("no") + an.setResultsName("linkType") + pc + neg.setResultsName("enabled"))
		# NODE
		node  = Group(an.setResultsName("symbol") + cn + an.setResultsName("symbolType") + Optional(po + nu.setResultsName("x") + co + nu.setResultsName("y") + pc))
		# GRAPH
		graph = Group(op + ZeroOrMore(node).setResultsName("nodes") + ZeroOrMore(link).setResultsName("links") + cl)
		# RULE SEQUENCE
		atom = Group(ids.setResultsName("name") + Suppress("as") + ids.setResultsName("alias"))
		equivElement = Group(ids.setResultsName("rule") + pt + ids.setResultsName("variable"))
		equivRhs = eq + equivElement
		equiv = Group(equivElement.setResultsName("first") + OneOrMore(equivRhs).setResultsName("more"))
		rule_seq  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + Optional(dep + po + nu.setResultsName("value") + pc).setResultsName("depth") + op + OneOrMore(atom).setResultsName("atomss") + Suppress("where:") + ZeroOrMore(equiv).setResultsName("equivalences") + cl)
		# NORMAL RULE
		Prm = Optional(parameters   + op + almostanything + cl).setResultsName("parameters")
		Cnd = Optional(precondition + op + almostanything + cl).setResultsName("precondition")
		Eft = Optional(effect       + op + almostanything + cl).setResultsName("effect")
		rule_nrm  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + Optional(dep + po + nu.setResultsName("value") + pc).setResultsName("depth") + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + Prm + Cnd + Eft + cl)
		# GENERAL RULE
		rule = rule_nrm | rule_seq
		# PROPERTY
		prop  = Group(an.setResultsName("prop") + eq + an.setResultsName("value"))
		# WHOLE FILE
		agm   = OneOrMore(prop).setResultsName("props") + sep + OneOrMore(rule).setResultsName("rules") + StringEnd()


		# Parse input file
		inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('#')])
		result = agm.parseWithTabs().parseString(inputText)
		if verbose: print "Result:\n",result

		# Fill AGMFileData and AGM data
		if verbose: print '\nProperties:', len(result.props)
		number = 0
		gotName = False
		strings = ['name', 'fontName']
		for i in result.props:
			if verbose: print '\t('+str(number)+') \''+str(i.prop)+'\' = \''+i.value+'\''
			if i.prop in strings:
				agmFD.properties[i.prop] = str(i.value)
				if i.prop == 'name': gotName = True
			else:
				try:
					agmFD.properties[i.prop] = int(i.value)
				except:
					try:
						agmFD.properties[i.prop] = int(float(i.value))
					except:
						print 'This is not a valid (or float)', i.value
			number += 1
		if not gotName:
			print 'drats! no name'

		#verbose=True
		#verbose=False
		if verbose: print '\nRules:', len(result.rules)
		number = 0
		for i in result.rules:
			if verbose: print '\nRule:('+str(number)+')'
			print 'Parameters:', i.parameters
			if len(i.parameters) > 0:
				parametersTree = AGGLCodeParsing.parseParameters(str(i.parameters[0]))
				parametersList = AGMFileDataParsing.interpretParameters(parametersTree)
			print 'Precondition:', i.precondition
			if len(i.precondition) > 0:
				preconditionTree = AGGLCodeParsing.parseFormula(str(i.precondition[0]))
				AGMFileDataParsing.interpretPrecondition(preconditionTree[0])
			print 'Effect:', i.effect
			if len(i.effect) > 0:
				effectTree = AGGLCodeParsing.parseFormula(str(i.effect[0]))
				AGMFileDataParsing.interpretEffect(effectTree[0])
			agmFD.addRule(AGMRuleParsing.parseRuleFromAST(i, parametersList, preconditionTree, effectTree, verbose))
		#sys.exit(1)
		return agmFD

	@staticmethod
	def interpretParameters(tree, pre=''):
		r = []
		for v in tree:
			v2 = v[0].split(':')
			#print v2
			r.append(v2)
		return r

	@staticmethod
	def interpretPrecondition(tree, pre=''):
		if tree.type == "not":
			print pre+'not'
			n = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["not", n]
		elif tree.type == "or":
			print pre+'or'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(tree.child, pre+"\t"))
			return ["or", r]
		elif tree.type == "and":
			print pre+'and'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(i, pre+"\t"))
			return ["and", r]
		elif tree.type == "forall":
			print pre+'forall'
			print pre+'\t',
			for i in tree.vars:
				print pre+str(i),
			print ''
			effect = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["forall", tree.vars, effect]
		elif tree.type == "when":
			print pre+'when'
			print pre+'\tif'
			iff = AGMFileDataParsing.interpretEffect(tree.iff, pre+"\t\t")
			print pre+'\tthen'
			then = AGMFileDataParsing.interpretEffect(tree.then, pre+"\t\t")
			return ["when", iff, then]
		else:
			print pre+"link <"+tree.type+"> between <"+tree.a+"> and <"+tree.b+">"
			return [tree.type, tree.a, tree.b]


	@staticmethod
	def interpretEffect(tree, pre=''):
		if tree.type == "not":
			print pre+'not'
			n = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["not", n]
		elif tree.type == "or":
			print pre+'or'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(tree.child, pre+"\t"))
			return ["or", r]
		elif tree.type == "and":
			print pre+'and'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(i, pre+"\t"))
			return ["and", r]
		elif tree.type == "forall":
			print pre+'forall'
			print pre+'\t',
			for i in tree.vars:
				print pre+str(i),
			print ''
			effect = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["forall", tree.vars, effect]
		elif tree.type == "when":
			print pre+'when'
			print pre+'\tif'
			iff = AGMFileDataParsing.interpretEffect(tree.iff, pre+"\t\t")
			print pre+'\tthen'
			then = AGMFileDataParsing.interpretEffect(tree.then, pre+"\t\t")
			return ["when", iff, then]
		else:
			print pre+"link <"+tree.type+"> between <"+tree.a+"> and <"+tree.b+">"
			return [tree.type, tree.a, tree.b]





