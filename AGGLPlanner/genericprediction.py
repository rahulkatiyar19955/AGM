import sys, random, os, traceback
from subprocess import call
import numpy as np
import imp

sys.path.append('/usr/local/share/agm/')
from parseAGGL import AGMFileDataParsing
from generateAGGLPlannerCode import generateTarget_AGGT


def getActionDictionary(domain):
	ret = {}
	count = 0
	#print '<<getActionDictionary'
	for rule in domain.agm.rules:
		#print rule.name
		ret[rule.name] = count
		count += 1
	#print '>>getActionDictionary'
	return ret


def outputVectorFromPlan(planLines, actionDictionary):
	ret = np.zeros( (1, len(actionDictionary)) )
	#try:
	for line in planLines:
		actionName  = line.split('@')[0]
		actionIndex = actionDictionary[actionName]
		ret[0][actionIndex] = 1.
	#except KeyError:
		#print planLines
	return ret


def getPredicateDictionary(domain):
	predicates = set()
	for rule in domain.agm.rules:
		for link in rule.rhs.links:
			if not link in rule.lhs.links:
				lt = link.linkType
				if not link.enabled: lt += '*'
				binary =  link.a == link.b
				typeA = rule.rhs.nodes[link.a].sType
				for tA in domain.agm.inverseTypes[typeA]:
					typeB = rule.rhs.nodes[link.b].sType
					for tB in domain.agm.inverseTypes[typeB]:
						if not (binary and tA!=tB):
							predicates.add((lt, tA, tB))
	ret = {}
	count = 0
	for p in predicates:
		s = '#'.join(p)
		ret[s] = count
		count += 1
	return ret

def setInverseDictionaryFromList(lst):
	ret = {}
	for i, item in enumerate(lst):
		ret[item] = i
	return ret

def inputVectorFromTarget(domain, prdDictionary, actDictionary, target):
	if type(target) == type(''):
		if target.endswith('.aggt'):
 			code = generateTarget_AGGT(domain, AGMFileDataParsing.targetFromFile(target))
			m = imp.new_module('targetModule')
			exec code in m.__dict__
			a, b, c = m.getTargetVariables()
			print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
			print a
			print b
			print c
			print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
			print prdDictionary
			print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
			ret = np.zeros( (1, len(prdDictionary)) )
			for r in b|c:
				if len(r) == 2:
					x = (r[0], r[1], r[2])
				elif len(r) == 3:
					x = r
				else:
					print 'inputVectorFromTarget: unexpected predicate size', r
					sys.exit(-1)
				k = '#'.join(x)
				if k in prdDictionary.keys():
					print prdDictionary[k], ret.shape 
					ret[0][prdDictionary[k]] = 1
			return ret
		else:
			print 'to implement (maybe here would just be an error)'
			sys.exit(-1)
	else:
		print 'to implement (maybe we are in a hierarchical target which is given directly by code)'
		sys.exit(-1)

	