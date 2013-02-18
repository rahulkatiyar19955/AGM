from AGM import *

class AGMGraphParsing:
	@staticmethod
	def parseGraphFromAST(i, verbose=False):
		if verbose: print '\t{'
		nodes = dict()
		for t in i.nodes:
			if verbose: print '\tT: \'' + str(t.symbol) + '\' is a \'' + t.symbolType + '\' (' + t.x, ',', t.y + ')'
			pos = [0,0]
			try:
				pos = [int(t.x), int(t.y)]
			except:
				pass
			nodes[t.symbol] = AGMSymbol(t.symbol, t.symbolType, pos)
		links = []
		for l in i.links:
			if verbose: print '\t\tL:', l.lhs, '->', l.rhs, '('+l.no, l.linkType+')'
			lV = True
			if len(l.no)>0: lV = False
			links.append(AGMLink(l.lhs, l.rhs, l.linkType, lV))
		if verbose: print '\t}'
		return AGMGraph(nodes, links)


class AGMRuleParsing:
	@staticmethod
	def parseRuleFromAST(i, verbose=False):
		if verbose: print '\nRule:', i.name
		LHS = AGMGraphParsing.parseGraphFromAST(i.lhs, verbose)
		if verbose: print '\t===>'
		RHS = AGMGraphParsing.parseGraphFromAST(i.rhs, verbose)
		return AGMRule(i.name, LHS, RHS)


class AGMFileDataParsing:
	@staticmethod
	def fromFile(filename, verbose=False):
		# Clear previous data
		agmFD = AGMFileData()
		agmFD.properties = dict()
		agmFD.agm.symbols = []
		agmFD.agm.rules = []

		# Define AGM's DSL meta-model
		an = Word(alphanums)
		nu = Word(nums)
		eq = Suppress("=")
		cn = Suppress(":") 
		lk = Suppress("->")
		ar = Suppress("=>")
		op = Suppress("{") 
		cl = Suppress("}") 
		po = Suppress("(")
		co = Suppress(",")
		pc = Suppress(")") 
		no = Suppress("!") 

		link  = Group(an.setResultsName("lhs") + lk + an.setResultsName("rhs") + po + Optional(no).setResultsName("no") + an.setResultsName("linkType") + pc)
		node  = Group(an.setResultsName("symbol") + cn + an.setResultsName("symbolType") + Optional(po + nu.setResultsName("x") + co + nu.setResultsName("y") + pc))
		graph = Group(op + ZeroOrMore(node).setResultsName("nodes") + ZeroOrMore(link).setResultsName("links") + cl)
		rule  = Group(an.setResultsName("name") + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + cl)
		prop  = Group(an.setResultsName("prop") + eq + an.setResultsName("value"))
		agm   = OneOrMore(prop).setResultsName("props") + OneOrMore(rule).setResultsName("rules") + StringEnd()

		verbose = False

		# Parse input file
		result = agm.parseString(open(filename, 'r').read())
		if verbose: print "Result:\n",result

		# Fill AGMFileData and AGM data		
		if verbose: print '\nProperties:', len(result.props)
		number = 0
		gotName = False
		strings = ['name']
		for i in result.props:
			if verbose: print '\t('+str(number)+') \''+str(i.prop)+'\' = \''+i.value+'\''
			if i.prop in strings:
				agmFD.properties[i.prop] = str(i.value)
				if i.prop == 'name': gotName = True
			else:
				try:
					agmFD.properties[i.prop] = float(i.value)
				except:
					print 'This is not a valid float:', i.value
			number += 1
		if not gotName:
			print 'SHIIIIIIIT no name'

		if verbose: print '\nRules:', len(result.rules)
		number = 0
		for i in result.rules:
			if verbose: print '\nRule:('+str(number)+')'
			agmFD.addRule(AGMRuleParsing.parseRuleFromAST(i, verbose))
			number += 1
		return agmFD
