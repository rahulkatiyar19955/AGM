#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ---------------------------
#  -----  Mojon Planner  -----
#  ---------------------------
#
#  Almost a free/libre AI planner.
#
#  Copyright (C) 2013 by Luis J. Manso
#
#  Mojon Planner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Mojon Planner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MojonPlanner. If not, see <http://www.gnu.org/licenses/>.

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

class WorldStateHistory(object):
	def __init__(self, init):
		object.__init__(self)
		if isinstance(init, AGMGraph):
			self.graph = copy.deepcopy(init)
			self.parent = None
			self.probability = 1
			self.cost = 0
			self.history = ''
			self.score = 0
		elif isinstance(type(init), type(WorldStateHistory)):
			self.graph = copy.deepcopy(init.graph)
			self.parent = init
			self.probability = init.probability
			self.cost = init.cost
			self.history = init.history
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
	def __init__(self, domainPath, init, targetPath):
		object.__init__(self)
		# Get initial world mdoel
		self.initWorld  = WorldStateHistory(xmlModelParser.graphFromXML(init))
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath)
		self.domain     = domain.RuleSet()
		# Get goal-checking code
		target = imp.load_source('target', targetPath)
		self.targetCode = target.CheckTarget


		# Some little initialization
		self.ruleMap = self.domain.getRules()
		openNodes = []
		heapq.heappush(openNodes, (0, copy.deepcopy(self.initWorld)))
		verbose = False
		if verbose: print 'INIT'.ljust(20), self.initWorld
		knownNodes = []
		results = []
		explored = 0

		# Main loop
		try:
			while True:
				head = heapq.heappop(openNodes)[1]
				#print head.cost, head.score
				if head.cost > 30: break
				# Small test
				if verbose: print 'Expanding'.ljust(5), head
				for k in self.ruleMap:
					prtd = False
					for deriv in self.ruleMap[k](head):
						if not prtd:
							if verbose: print '  ',k
							prtd = True
						explored += 1
						if verbose:
							if explored % 100 == 0:
								print 'Explored nodes:', explored, "(last cost:"+str(head.cost)+")"
						deriv.score, achieved = self.targetCode(deriv.graph)
						if verbose: print deriv.score, achieved, deriv
						if achieved:
							results.append(deriv)
						if not deriv in knownNodes:
							knownNodes.append(head)
							heapq.heappush(openNodes, (deriv.score, deriv))
		except IndexError, e:
			pass
		except GoalAchieved, e:
			pass
		except target.GoalAchieved, e:
			pass

		if len(results)==0:
			print 'Empty search space: no plan found.'
		else:
			print 'Got plans!'
			mincost = results[0].cost
			min_idx = 0
			for i in range(len(results)):
				if results[i].cost < mincost:
					mincost = results[i].cost
					min_idx = i
			print '-------------------------------------------'
			print 'Cost', results[i].cost
			print 'Score', results[i].score
			print 'Probability', results[i].probability
			print 'Actions', results[i].history
			print i
			print "\nExplored", explored, "nodes"

if __name__ == '__main__': # program domain problem result
	if len(sys.argv)<4:
		print 'Usage\n\t', sys.argv[0], ' domain.py init.xml target.xml'
	else:
		p = PyPlan(sys.argv[1], sys.argv[2], sys.argv[3])


