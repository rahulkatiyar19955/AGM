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

sys.path.append('/opt/robocomp/share')

import xmlModelParser
from AGGL import *
import inspect

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
				line = lines[line_i]
				while len(line)>0:
					if line[-1]=='\n': line = line[:-1]
					else: break
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
			self.parent = None
			self.probability = 1
			self.cost = 0
			self.history = []
			self.depth = 0
			self.score = 0
		elif isinstance(type(init), type(WorldStateHistory)):
			self.graph = copy.deepcopy(init.graph)
			self.parent = copy.deepcopy(init)
			self.probability = copy.deepcopy(init.probability)
			self.cost = copy.deepcopy(init.cost)
			self.history = copy.deepcopy(init.history)
			self.depth = copy.deepcopy(init.depth)
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

class PyPlan(object):
	def __init__(self, domainPath, init, targetPath, resultFile):
		object.__init__(self)
		# Get initial world mdoel
		self.initWorld  = WorldStateHistory(xmlModelParser.graphFromXML(init))
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath)
		self.domain     = domain.RuleSet()
		# Get goal-checking code
		target = imp.load_source('target', targetPath)
		self.targetCode = target.CheckTarget

		# C O N F I G U R A T I O N
		# C O N F I G U R A T I O N
		# C O N F I G U R A T I O N
		maxWorldSize = len(self.initWorld.graph.nodes.keys())+40
		breadthFirst = False
		#breadthFirst = True
		stopWithFirstPlan = True


		# Some little initialization
		mincostOnList = 0
		self.ruleMap = self.domain.getRules()
		openNodes = []
		if breadthFirst:
			openNodes = collections.deque()
			openNodes.appendleft(copy.deepcopy(self.initWorld))
		else:
			heapq.heappush(openNodes, (0, copy.deepcopy(self.initWorld)))
		verbose = 0
		if verbose>0: print 'INIT'.ljust(20), self.initWorld
		knownNodes = []
		results = []
		explored = 0

		cheaperSolutionCost = -1

		# Main loop
		try:
			while True:
				if breadthFirst:
					head = openNodes.pop()
				else:
					head = heapq.heappop(openNodes)[1]
				if head.cost <= mincostOnList:
					if len(openNodes)==0:
						mincostOnList = 0
					else:
						mincostOnList = openNodes[0].cost
						for n in openNodes:
							if n.cost < mincostOnList:
								mincostOnList = n.cost
				#print head.cost, head.score
				
				if (len(results)>0 and head.cost>3*cheaperSolutionCost) or (head.cost > 20):
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
								if breadthFirst: print 'Using breadth-first search'
								print 'Explored nodes:', explored,
								print "(last cost:"+str(head.cost)+"  depth:"+str(head.depth)+"  score:"+str(head.score)+")"
								print head
						deriv.score, achieved = self.targetCode(deriv.graph)
						if verbose>4: print deriv.score, achieved, deriv
						if achieved:
							results.append(deriv)
							cheaperSolutionCost = results[0].cost
							for s in results:
								if s.cost < cheaperSolutionCost: cheaperSolutionCost = s.cost
							if stopWithFirstPlan:
								raise GoalAchieved
						if not deriv in knownNodes:
							if len(deriv.graph.nodes.keys()) <= maxWorldSize:
								knownNodes.append(head)
								#print -deriv.score
								if breadthFirst:
									openNodes.appendleft(deriv)
								else:
									#heapq.heappush(openNodes, (-deriv.score, deriv)) # The more the better
									#heapq.heappush(openNodes, ( deriv.cost , deriv)) # The less the better
									heapq.heappush(openNodes, ( (float(deriv.cost)/(float(deriv.score)+1.), deriv)) ) # The more the better
		except IndexError, e:
			if verbose > 0: print 'End: state space exhausted'
			pass
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
			if verbose > 0:
				print '-------------------------------------------'
				print 'Cost', results[i].cost
				print 'Score', results[i].score
				print 'Probability', results[i].probability
				print 'Actions\n----------------'
			for action in results[i].history:
				print action
				if resultFile != None:
					resultFile.write(str(action)+'\n')
			if verbose > 0: print "----------------\nExplored", explored, "nodes"

if __name__ == '__main__': # program domain problem result
	if len(sys.argv)<4:
		print 'Usage\n\t', sys.argv[0], ' domain.aggl.py init.xml target.xml.py [result.plan]'
	elif len(sys.argv)<5:
		p = PyPlan(sys.argv[1], sys.argv[2], sys.argv[3], None)
	else:
		p = PyPlan(sys.argv[1], sys.argv[2], sys.argv[3], open(sys.argv[4], 'w'))


