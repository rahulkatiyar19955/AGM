#!/usr/bin/env pypy

# -*- coding: utf-8 -*-
#
#  -------------------------
#  -----  AGGLPlanner  -----
#  -------------------------
#
#  Almost a free/libre AI planner.
#
#  Copyright (C) 2013 by Luis J. Manso
#
#  AGGLPlanner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AGGLPlanner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AGGLPlanner. If not, see <http://www.gnu.org/licenses/>.

# Python distribution imports
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import sys, traceback, os, re, threading, time, string, math, copy
import collections, imp, heapq
import datetime
sys.path.append('/usr/local/share/agm/')

import xmlModelParser
from AGGL import *
import inspect

# C O N F I G U R A T I O N
# C O N F I G U R A T I O N
# C O N F I G U R A T I O N
maxWorldIncrement = 40
maxCost = 200
stopWithFirstPlan = True
verbose = 1
maxTimeWait = 4.


class GoalAchieved(Exception):
	pass
class MaxCostReached(Exception):
	def __init__(self, cost):
		self.cost = cost
class BestSolutionFound(Exception):
	pass
class WrongRuleExecution(Exception):
	def __init__(self, data):
		self.data = data
	def __str__(self):
		return self.data

class AGGLPlannerAction(object):
	def __init__(self, init=''):
		object.__init__(self)
		self.name = ''
		self.parameters = dict()
		if len(init)>0:
			parts = init.split('@')
			self.name = parts[0]
			self.parameters = eval(parts[1])
		else:
			raise IndexError
	def __str__(self):
		return self.name+'@'+str(self.parameters)

class AGGLPlannerPlan(object):
	def __init__(self, init=''):
		object.__init__(self)
		self.data = []
		if len(init)>0:
			lines = open(init, 'r').readlines()
			for line_i in range(len(lines)):
				line = lines[line_i].strip()
				while len(line)>0:
					if line[-1]=='\n': line = line[:-1]
					else: break
				if len(line)>0:
					if line[0] != '#':
						try:
							self.data.append(AGGLPlannerAction(line))
						except:
							if len(line)>0:
								print 'Error reading plan file', init+". Line", str(line_i)+": <<"+line+">>"
	def __iter__(self):
		self.current = -1
		return self
	def next(self):
		self.current += 1
		if self.current >= len(self.data):
			raise StopIteration
		else:
			return self.data[self.current]
	
class WorldStateHistory(object):
	def __init__(self, init):
		object.__init__(self)
		if isinstance(init, AGMGraph):
			self.graph = copy.deepcopy(init)
			#self.parent = None
			self.parentId = 0
			self.probability = 1
			self.cost = 0
			self.history = []
			self.nodeId = -1
			self.depth = 0
			self.stop = False
			self.score = 0
		elif isinstance(type(init), type(WorldStateHistory)):
			self.graph = copy.deepcopy(init.graph)
			#self.parent = copy.deepcopy(init)
			self.probability = copy.deepcopy(init.probability)
			self.cost = copy.deepcopy(init.cost)
			self.history = copy.deepcopy(init.history)
			self.depth = copy.deepcopy(init.depth)
			self.stop = False
			self.score = 0
		else:
			print 'Human... wat r u doing... stahp... please, stahp'
			print type(init)
			print type(self)
			sys.exit(1)
	def __cmp__(self, other):
		return self.graph.__cmp__(other.graph)
	def __hash__(self):
		return self.graph.__hash__()
	def __eq__(self, other):
		return self.graph == other.graph
	def __repr__(self):
		return self.graph.__repr__()
	def __str__(self):
		return self.graph.__str__()

def printResult(result):
	print '-----  R  E  S  U  L  T  S  -----'
	if verbose > 0:
		print 'Cost', result.cost
		print 'Score', result.score
		print 'Probability', result.probability
		#print 'NodeID', result.nodeId
		print 'Actions\n----------------'
	for action in result.history:
		print action

class PyPlan(object):
	def __init__(self, domainPath, init, targetPath, resultFile):
		object.__init__(self)
		# Get initial world mdoel
		self.initWorld = WorldStateHistory(xmlModelParser.graphFromXML(init))
		self.initWorld.nodeId = 0
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath)
		self.domain     = domain.RuleSet()
		# Get goal-checking code
		target = imp.load_source('target', targetPath)
		self.targetCode = target.CheckTarget


		# Some little initialization
		maxWorldSize = maxWorldIncrement+len(self.initWorld.graph.nodes.keys())
		mincostOnList = 0
		self.ruleMap = self.domain.getRules()
		openNodes = []
		heapq.heappush(openNodes, (0, copy.deepcopy(self.initWorld)))
		if verbose>1: print 'INIT'.ljust(20), self.initWorld
		knownNodes = []
		results = []
		explored = 0

		cheapsetSolutionCost = -1



		timeA = datetime.datetime.now()
		# Main loop
		try:
			self.initWorld.score, achieved = self.targetCode(self.initWorld.graph)
			if achieved:
				results.append(self.initWorld)
				cheapsetSolutionCost = results[0].cost
				for s in results:
					if s.cost < cheapsetSolutionCost: cheapsetSolutionCost = s.cost
				# Check if we should stop because we are looking for the first solution
				if stopWithFirstPlan:
					raise GoalAchieved
				
			while True:
				# Check if we should finish by time
				timeB = datetime.datetime.now()
				timeElapsed = (timeB-timeA).seconds + (timeB-timeA).microseconds/1e6
				if timeElapsed > maxTimeWait:
					if len(results)>0:
						raise GoalAchieved
				# Proceed
				head = heapq.heappop(openNodes)[1]
				if head.cost <= mincostOnList:
					if len(openNodes)==0:
						mincostOnList = 0
					else:
						mincostOnList = openNodes[0][1].cost
						for n in openNodes:
							if n[1].cost < mincostOnList:
								mincostOnList = n[1].cost
				
				if (len(results)>0 and head.cost>3*cheapsetSolutionCost) or (head.cost > maxCost):
					raise MaxCostReached(head.cost)
				# Small test
				if verbose>5: print 'Expanding'.ljust(5), head
				for k in self.ruleMap:
					prtd = False
					# Iterate over rules and generate derivates
					for deriv in self.ruleMap[k](head):
						if not prtd:
							if verbose>5: print '  ',k
							prtd = True
						explored += 1
						if verbose > 0:
							if explored % 100 == 0:
								print 'Explored nodes:', explored,
								print "(last cost:"+str(head.cost)+"  depth:"+str(head.depth)+"  score:"+str(head.score)+")"
								#print head
								print 'First(cost:'+str(openNodes[0][1].cost) +', score:'+str(openNodes[0][1].score) +', depth:'+str(openNodes[0][1].depth)+')'
								print  'Last(cost:'+str(openNodes[-1][1].cost)+', score:'+str(openNodes[-1][1].score)+', depth:'+str(openNodes[-1][1].depth)+')'
						deriv.score, achieved = self.targetCode(deriv.graph)
						if verbose>4: print deriv.score, achieved, deriv
						if achieved:
							#print 'Found solution', deriv.cost
							results.append(deriv)
							# Should we stop with the first plan?
							if stopWithFirstPlan:
								raise GoalAchieved
							# Compute cheapest solution
							cheapsetSolutionCost = results[0].cost
							for s in results:
								if s.cost < cheapsetSolutionCost:
									cheapsetSolutionCost = s.cost
							# Check if ws should stop because there are no cheaper possibilities
							stopBecauseAllOpenNodesAreMoreExpensive = True
							for c in openNodes:
								if c[0] < cheapsetSolutionCost:
									stopBecauseAllOpenNodesAreMoreExpensive = False
									break
							if stopBecauseAllOpenNodesAreMoreExpensive:
								raise BestSolutionFound
							else:
								print '+('+str(deriv.cost)+')'
						if not deriv in knownNodes and deriv.stop == False:
							if len(deriv.graph.nodes.keys()) <= maxWorldSize:
								knownNodes.append(head)
								#heapq.heappush(openNodes, (-deriv.score, deriv)) # score... the more the better
								#heapq.heappush(openNodes, ( deriv.cost, deriv)) # cost...  the less the better
								heapq.heappush(openNodes, ( (float(100.*deriv.cost)/(float(1.+deriv.score)), deriv)) ) # The more the better TAKES INTO ACCOUND COST AND SCORE
								#heapq.heappush(openNodes, ( (float(100.+deriv.cost)/(float(1.+deriv.score)), deriv)) ) # The more the better TAKES INTO ACCOUND COST AND SCORE
		#except IndexError, e:
			#if verbose > 0: print 'End: state space exhausted'
			#pass
		except MaxCostReached, e:
			if verbose > 0: print 'End: max cost reached:', e.cost
			pass
		except BestSolutionFound, e:
			if verbose > 0: print 'End: best solution found'
			pass
		except GoalAchieved, e:
			if verbose > 0: print 'End: goal achieved'
			pass
		except target.GoalAchieved, e:
			if verbose > 0: print 'End: goal achieved'
			pass

		if len(results)==0:
			if verbose > 0: print 'No plan found.'
		else:
			if verbose > 0: print 'Got', len(results),' plans!'
			min_idx = 0
			for i in range(len(results)):
				if results[i].cost < results[min_idx].cost:
					min_idx = i
			i = min_idx
			printResult(results[i])
			for action in results[i].history:
				if resultFile != None:
					resultFile.write(str(action)+'\n')
			if verbose > 0: print "----------------\nExplored", explored, "nodes"

if __name__ == '__main__': # program domain problem result
	#from pycallgraph import *
	#from pycallgraph.output import GraphvizOutput
	#graphviz = GraphvizOutput()
	#graphviz.output_file = 'basic.png'
	if True:
	#with PyCallGraph(output=graphviz):
		if len(sys.argv)<4:
			print 'Usage\n\t', sys.argv[0], ' domain.aggl.py init.xml target.xml.py [result.plan]'
		elif len(sys.argv)<5:
			p = PyPlan(sys.argv[1], sys.argv[2], sys.argv[3], None)
		else:
			p = PyPlan(sys.argv[1], sys.argv[2], sys.argv[3], open(sys.argv[4], 'w'))


