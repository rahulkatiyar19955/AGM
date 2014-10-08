from pyparsing import Word, alphas, alphanums, nums, OneOrMore, CharsNotIn, Literal, Combine, Optional, Suppress, ZeroOrMore, Group, StringEnd, srange
from AGGL import *
#from PySide.QtCore import *
#from PySide.QtGui import *
import sys
from parseQuantifiers import *

debug = False
#debug = True

## AGM Graph parsing
# @ingroup PyAPI
#
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
			links.append(AGMLink(l.lhs, l.rhs, l.linkType, enabled=lV))
		if verbose: print '\t}'
		return AGMGraph(nodes, links)


## AGM Rule parsing
# @ingroup PyAPI
#
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
		if len(i.atomss)==0: # We are dealing with a normal rule!
			#print 'Normal rule:', i.name
			# We are dealing with a normal rule!
			if verbose: print '\nRule:', i.name
			LHS = AGMGraphParsing.parseGraphFromAST(i.lhs, verbose)
			if verbose: print '\t===>'
			RHS = AGMGraphParsing.parseGraphFromAST(i.rhs, verbose)
			regular = AGMRule(i.name, LHS, RHS, passive, i.cost, parameters, precondition, effect)
			if len(i.conditions) > 0:
				regular.conditions = str(i.conditions[0])
			else:
				regular.conditions = ''
			if len(i.effects) > 0:
				regular.effects = str(i.effects[0])
			else:
				regular.effects = ''
			return regular
		elif len(i.lhs)>0: # if there are rules inside AND a left hand side graph.. we're dealing with a hierarchical rule
			LHS = AGMGraphParsing.parseGraphFromAST(i.lhs, verbose)
			RHS = AGMGraphParsing.parseGraphFromAST(i.rhs, verbose)
			hierarchical = AGMHierarchicalRule(i.name, LHS, RHS, passive, i.cost, i.atomss.asList(), i.equivalences.asList())
			return hierarchical
		else:
			#print 'Combo rule:', i.name
			combo = AGMComboRule(i.name, passive, i.cost, i.atomss.asList(), i.equivalences.asList())
			return combo


## AGGL Parser
# @ingroup PyAPI
#
class AGMFileDataParsing:
	## This method makes the analysis of the .aggl file where is stored the grammar that we will use.
	# It returns agmFD, a variable with the grammar file, the properties, symbols and rules of the grammar.
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
		rule_seq  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + OneOrMore(atom).setResultsName("atomss") + Suppress("where:") + ZeroOrMore(equiv).setResultsName("equivalences") + cl)
		# NORMAL RULE
		Prm = Optional(parameters   + op + almostanything + cl).setResultsName("parameters")
		Cnd = Optional(precondition + op + almostanything + cl).setResultsName("precondition")
		Eft = Optional(effect       + op + almostanything + cl).setResultsName("effect")
		rule_nrm  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + OneOrMore(atom).setResultsName("atomss") + Suppress("where:") + ZeroOrMore(equiv).setResultsName("equivalences") + cl)
		# HIERARCHICAL RULE
		rule_hierarchical  = Group(an.setResultsName("name") + cn + an.setResultsName("passive") + po + nu.setResultsName("cost") + pc + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + Prm + Cnd + Eft + cl)
		# indlude
		include = Group(Suppress("include") + po + an.setResultsName("includefile") + pc)
		# GENERAL RULE
		rule = rule_nrm | rule_seq | rule_hierarchical | include
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
			if i.includefile:
				inc = AGMFileDataParsing.fromFile(i.includefile)
				for incr in inc.agm.rules:
					agmFD.addRule(incr)
					number = number + 1
			else:
				preconditionRec = None
				parametersList = None
				effectRec = None
				# Read params
				parametersStr = ''
				parametersList = []
				
				if i.parameters:
					if len(str(i.parameters[0]).strip())>0:
						#print 'Parameters: <'+str(i.parameters[0])+'>'
						parametersStr = str(i.parameters[0])
						parametersTree = AGGLCodeParsing.parseParameters(parametersStr)
						parametersList = AGMFileDataParsing.interpretParameters(parametersTree)
				# Read precond
				preconditionStr = ''
				preconditionTree = None
				preconditionRec = None
				if i.precondition:
					if len(str(i.precondition[0]).strip())>0:
						#print 'Precondition: <'+i.precondition[0]+'>'
						preconditionStr = str(i.precondition[0])
						preconditionTree = AGGLCodeParsing.parseFormula(preconditionStr)
						if len(preconditionTree)>0: preconditionTree = preconditionTree[0]
						preconditionRec = AGMFileDataParsing.interpretPrecondition(preconditionTree)
				# Read effect
				effectStr = ''
				effectTree = None
				effectRec = None
				if i.effect:
					if len(str(i.effect[0]).strip())>0:
						#print 'Effect: <', str(i.effect[0])+'>'
						effectStr = str(i.effect[0])
						effectTree = AGGLCodeParsing.parseFormula(effectStr)
						if len(effectTree)>0: effectTree = effectTree[0]
						effectRec = AGMFileDataParsing.interpretEffect(effectTree)
				# Build rule
				rule = AGMRuleParsing.parseRuleFromAST(i, parametersList, preconditionRec, effectRec, verbose)
				rule.parameters      = parametersStr
				rule.parametersAST   = parametersList
				rule.precondition    = preconditionStr
				rule.preconditionAST = preconditionRec
				rule.effect          = effectStr
				rule.effectAST       = effectRec
				#print rule.name
				#print 'PARMS', rule.parametersAST
				#print 'PRECN', rule.preconditionAST
				#print 'EFFEC', rule.effectAST
				agmFD.addRule(rule)
				#print i.parameters[0]
				#print i.precondition[0]
				#print i.effect[0]
				number = number + 1
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
			if debug: print pre+'not'
			n = AGMFileDataParsing.interpretPrecondition(tree.child, pre+"\t")
			return ["not", n]
		elif tree.type == "or":
			if debug: print pre+'or'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretPrecondition(tree.child, pre+"\t"))
			return ["or", r]
		elif tree.type == "and":
			if debug: print pre+'and'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretPrecondition(i, pre+"\t"))
			return ["and", r]
		elif tree.type == "forall":
			if debug: print pre+'forall'
			if debug: print pre+'\t',
			for i in tree.vars:
				if debug: print pre+str(i),
			if debug: print ''
			effect = AGMFileDataParsing.interpretPrecondition(tree.child, pre+"\t")
			ret = ["forall", [[str(x.var), str(x.t)] for x in tree.vars], effect]
			return ret
		elif tree.type == "when":
			if debug: print pre+'when'
			if debug: print pre+'\tif'
			iff = AGMFileDataParsing.interpretPrecondition(tree.iff, pre+"\t\t")
			if debug: print pre+'\tthen'
			then = AGMFileDataParsing.interpretPrecondition(tree.then, pre+"\t\t")
			return ["when", iff, then]
		elif tree.type == "=":
			if debug: print pre+'='
			return ["=", tree.a, tree.b]
		else:
			if debug: print pre+"link <"+tree.type+"> between <"+tree.a+"> and <"+tree.b+">"
			return [tree.type, tree.a, tree.b]


	@staticmethod
	def interpretEffect(tree, pre=''):
		if tree.type == "not":
			if debug: print pre+'not'
			n = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["not", n]
		elif tree.type == "or":
			if debug: print pre+'or'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(tree.child, pre+"\t"))
			return ["or", r]
		elif tree.type == "and":
			if debug: print pre+'and'
			r = []
			for i in tree.more:
				r.append(AGMFileDataParsing.interpretEffect(i, pre+"\t"))
			return ["and", r]
		elif tree.type == "forall":
			if debug: print pre+'forall'
			if debug: print pre+'\t',
			for i in tree.vars:
				if debug: print pre+str(i),
			if debug: print ''
			effect = AGMFileDataParsing.interpretEffect(tree.child, pre+"\t")
			return ["forall", [[str(x.var), str(x.t)] for x in tree.vars], effect]
		elif tree.type == "when":
			if debug: print pre+'when'
			if debug: print pre+'\tif'
			iff = AGMFileDataParsing.interpretEffect(tree.iff, pre+"\t\t")
			if debug: print pre+'\tthen'
			then = AGMFileDataParsing.interpretEffect(tree.then, pre+"\t\t")
			return ["when", iff, then]
		elif tree.type == "=":
			if debug: print pre+'='
			return ["=", tree.a, tree.b]
		else:
			if debug: print pre+"link <"+tree.type+"> between <"+tree.a+"> and <"+tree.b+">"
			return [tree.type, tree.a, tree.b]





