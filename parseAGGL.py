from pyparsing import Word, alphas, alphanums, nums, OneOrMore, Literal, Combine, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from AGGL import *
from PySide.QtCore import *
from PySide.QtGui import *

class AGMGraphParsing:
	@staticmethod
	def parseGraphFromAST(i, verbose=False):
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
	def parseRuleFromAST(i, verbose=False):
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
		if hasattr(i, 'lhs') and (hasattr(i, 'lhs') and len(i.lhs)>0 and hasattr(i, 'lhs')): # We are dealing with a normal rule!
			# We are dealing with a normal rule!
			if verbose: print '\nRule:', i.name
			LHS = AGMGraphParsing.parseGraphFromAST(i.lhs, verbose)
			if verbose: print '\t===>'
			RHS = AGMGraphParsing.parseGraphFromAST(i.rhs, verbose)
			regular = AGMRule(i.name, LHS, RHS, passive, i.cost)
			regular.mindepth = mindepth
			#print regular.toString()
			return regular
		elif hasattr(i, 'atoms'): # We are dealing with a rule combo!
			print '  Combo'
			# We are dealing with a rule combo!
			combo = AGMComboRule(i.name, passive, i.cost, i.atoms.asList(), i.equivalences.asList())
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
		rule_seq  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + Optional(dep + po + nu.setResultsName("value") + pc).setResultsName("depth") + op + OneOrMore(atom).setResultsName("atoms") + Suppress("where:") + ZeroOrMore(equiv).setResultsName("equivalences") + cl)
		# NORMAL RULE
		rule_nrm  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + Optional(dep + po + nu.setResultsName("value") + pc).setResultsName("depth") + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + cl)
		# GENERAL RULE
		rule = rule_nrm | rule_seq
		# PROPERTY
		prop  = Group(an.setResultsName("prop") + eq + an.setResultsName("value"))
		# WHOLE FILE
		agm   = OneOrMore(prop).setResultsName("props") + sep + OneOrMore(rule).setResultsName("rules") + StringEnd()


		# Parse input file
		inputText = "\n".join([line for line in open(filename, 'r').read().split("\n") if not line.lstrip(" \t").startswith('#')])
		result = agm.parseString(inputText)
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

		verbose=True
		verbose=False
		if verbose: print '\nRules:', len(result.rules)
		number = 0
		for i in result.rules:
			if verbose: print '\nRule:('+str(number)+')'
			agmFD.addRule(AGMRuleParsing.parseRuleFromAST(i, verbose))
			number += 1

		return agmFD
		
