from pyparsing import Word, alphas, alphanums, nums, OneOrMore, Optional, Suppress, ZeroOrMore, Group, StringEnd
import math

def distance(x1, y1, x2, y2):
	return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))

class AGMSymbol(object):
	def __init__(self, name, sType, pos):
		object.__init__(self)
		self.name = name
		self.sType = sType
		self.pos = pos
	def toString(self):
		return str(self.name)+':'+str(self.sType)+'('+str(self.pos[0])+','+str(self.pos[1])+');'

class AGMLink(object):
	def __init__(self, a, b, linkType, enabled):
		object.__init__(self)
		self.a = a
		self.b = b
		self.linkType = linkType
		self.enabled = enabled
	def toString(self):
		v = ''
		if not self.enabled: v = 'q '
		return '\t\t'+str(self.a)+'->'+str(self.b)+'('+v+str(self.linkType)+')'

class AGMGraph(object):
	def __init__(self, nodes, links, side='n'):
		object.__init__(self)
		self.nodes = nodes
		self.links = links
		self.side = side
	def getName(self, xa, ya, diameter):
		minDist = -1
		minName = None
		for name in self.nodes.keys():
			dist = distance(xa, ya, self.nodes[name].pos[0], self.nodes[name].pos[1])
			if dist < diameter/2:
				if dist < minDist or minDist < 0:
					minDist = dist
					minName = name
		if minDist > -1:
			return minName, True
		else:
			return '', False
	def getNameRelaxed(self, xa, ya, diameter):
		minDist = -1
		minName = None
		for name in self.nodes.keys():
			dist = distance(xa, ya, self.nodes[name].pos[0], self.nodes[name].pos[1])
			if dist < minDist or minDist < 0:
				minDist = dist
				minName = name
		if minDist > -1:
			return minName, True
		else:
			return '', False
	def getCenter(self, xa, ya, diameter):
		name, found = self.getName(xa, ya, diameter)
		if found:
			return self.nodes[name].pos[0], self.nodes[name].pos[1]
		else:
			return -1, -1

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

	def addNode(self, x, y, name, stype):
		if not name in self.nodes.keys():
			self.nodes[name] = AGMSymbol(name, stype, [x,y])
	def removeNode(self, x, y, diameter):
		name, found = self.getName(x, y, diameter)
		if found:
			del self.nodes[name]
		else:
			print 'no ndoe'
	def moveNode(self, name, x, y, diameter):
		name, found = self.getNameRelaxed(x, y, diameter)
		if found:
			self.nodes[name].pos = [x, y]
		else:
			print 'no ndoe'
	def addEdge(self, a, b):
		print 'Add edge', a, b
		self.links.append(AGMLink(a, b, 'link', True))

	def toString(self):
		ret = '\t{\n'
		for v in self.nodes.keys():
			ret += '\t\t' +str(self.nodes[v].name) + ':'+self.nodes[v].sType + '(' + str(self.nodes[v].pos[0]) + ','+ str(self.nodes[v].pos[1]) + ');\n'
		for l in self.links:
			ret += l.toString() + ';\n'
		return ret+'\t}'

	def nodeTypes(self):
		ret = set()
		for k in self.nodes.keys():
			ret.add(self.nodes[k].sType)
		return ret

	def nodeNames(self):
		ret = set()
		for k in self.nodes.keys():
			ret.add(self.nodes[k].name)
		return ret

	def linkTypes(self):
		ret = set()
		for l in self.links:
			ret.add(l.linkType)
		return ret

class AGMRule(object):
	def __init__(self, name='', lhs=None, rhs=None):
		object.__init__(self)
		self.name = name
		#print 'AGMRule::AGMRule', type(nodes)
		self.lhs = lhs
		self.rhs = rhs
		if lhs == None or rhs == None:
			self.lhs = AGMGraph(self, dict(), [])
			self.rhs = AGMGraph(self, dict(), [])
	@staticmethod
	def parseRuleFromAST(i, verbose=False):
		if verbose: print '\nRule:', i.name
		LHS = AGMGraph.parseGraphFromAST(i.lhs, verbose)
		if verbose: print '\t===>'
		RHS = AGMGraph.parseGraphFromAST(i.rhs, verbose)
		return AGMRule(i.name, LHS, RHS)
	def toString(self):
		ret = self.name + '\n{\n'
		ret += self.lhs.toString() + '\n'
		ret += '\t=>\n'
		ret += self.rhs.toString() + '\n'
		ret += '}'
		return ret
	def existingNodesPDDLPreconditions(self):
		ret  = ''
		for name,node in self.lhs.nodes.items():
			ret += ' (IS'+node.sType+' ?'+name+')'
		return ret
	def unknownNodesPDDLPreconditions(self):
		ret  = ''
		return ret
	def toPDDL(self):
		string  = '\t(:action ' + self.name + '\n'
		string += '\t\t:parameters ('
		for n in self.nodeNames():
			string += ' ?' + n
		string += ' )\n'
		string += '\t\t:precondition (and '
		string += self.existingNodesPDDLPreconditions() + ' '
		string += self.unknownNodesPDDLPreconditions()
		string += ' )\n'
		string += '\t\t:effect (and '
		string += '  (increase (total-cost) 1) )\n'
		string += '\t)\n'
		return string
	def nodeTypes(self):
		return self.lhs.nodeTypes().union(self.rhs.nodeTypes())
	def nodeNames(self):
		return self.lhs.nodeNames().union(self.rhs.nodeNames())
	def linkTypes(self):
		return self.lhs.linkTypes().union(self.rhs.linkTypes())


class AGM(object):
	def __init__(self, filename=''):
		object.__init__(self)
		if len(filename) == 0:
			self.rules = []
		else:
			self = AGMFileData.fromFile(filename).agm
	def addRule(self, rule):
		self.rules.append(rule)
	def toPDDL(self, name):
		writeString  = '(define (domain '+name+')\n\n'
		writeString += '\t(:predicates\n'
		writeString += '\t\t(firstunknown ?u)\n'
		writeString += '\t\t(unknownorder ?ua ?ub)\n\n'
		writeString += self.typePredicatesPDDL()
		writeString += self.linkPredicatesPDDL()
		writeString += '\t)\n\n'
		writeString += '\t(:functions\n\t\t(total-cost)\n\t)\n\n'
		for r in self.rules:
			writeString += r.toPDDL() + '\n'
		writeString += ')\n'
		return writeString
	def typePredicatesPDDL(self):
		writeString = ''
		typeSet = set()
		for r in self.rules:
			typeSet = typeSet.union(r.nodeTypes())
		for t in typeSet:
			writeString += '\t\t(IS'+t+' ?n)\n'
		return writeString
	def linkPredicatesPDDL(self):
		writeString = ''
		linkSet = set()
		for r in self.rules:
			linkSet = linkSet.union(r.linkTypes())
		writeString += '\n'
		for t in linkSet:
			writeString += '\t\t('+t+' ?u)\n'
		return writeString

class AGMFileData(object):
	def __init__(self, filename=''):
		object.__init__(self)
		if len(filename) == 0:
			self.properties = dict()
			self.agm = AGM()
		else:
			self = AGMFileData.fromFile(filename)

	def addRule(self, rule):
		self.agm.addRule(rule)

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
		sc = Suppress(";") 
		lk = Suppress("->")
		ar = Suppress("=>")
		op = Suppress("{") 
		cl = Suppress("}") 
		po = Suppress("(")
		co = Suppress(",")
		pc = Suppress(")") 
		no = Suppress("!") 

		# A link has a lhs node and a rhs node
		# lhs->rhs;
		link  = Group(an.setResultsName("lhs") + lk + an.setResultsName("rhs") + po + Optional(no).setResultsName("no") + an.setResultsName("linkType") + pc + sc)
		node  = Group(an.setResultsName("symbol") + cn + an.setResultsName("symbolType") + Optional(po + nu.setResultsName("x") + co + nu.setResultsName("y") + pc) + sc)
		graph = Group(op + ZeroOrMore(node).setResultsName("nodes") + ZeroOrMore(link).setResultsName("links") + cl)
		rule  = Group(an.setResultsName("name") + op + graph.setResultsName("lhs") + ar + graph.setResultsName("rhs") + cl + sc)
		prop  = Group(an.setResultsName("prop") + eq + an.setResultsName("value") + sc)
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
			agmFD.addRule(AGMRule.parseRuleFromAST(i, verbose))
			number += 1
		return agmFD

	def toFile(self, filename):
		writeString = ''
		for k,v in self.properties.items():
			writeString += str(k) + '=' + str(v) + ';\n'
		writeString += '\n'
		for r in self.agm.rules:
			writeString = writeString + r.toString() + ';\n\n'
		w = open(filename, 'w')
		w.write(writeString)
		w.close()

	def generatePDDL(self, filename):
		w = open(filename, 'w')
		w.write(self.agm.toPDDL(self.properties["name"]))
		w.close()
				
