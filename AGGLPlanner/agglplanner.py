#!/usr/bin/env pypy

# -*- coding: utf-8 -*-
#
#  -------------------------
#  -----  AGGLPlanner  -----
#  -------------------------
#
#  A free/libre open source AI planner.
#
#  Copyright (C) 2013 - 2014 by Luis J. Manso
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
import thread
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
number_of_threads = 3
maxWorldIncrement = 6
maxCost = 200
stopWithFirstPlan = True
verbose = 1
maxTimeWaitAchieved = 10.
maxTimeWaitLimit = 1000.

maxCostRatioToBestSolution = 1.00001

class EndCondition(object):
	def __init__(self, status=None):
		self.status = status
		self.lock = thread.allocate_lock()
	def get(self):
		self.lock.acquire()
		ret = self.status
		self.lock.release()
		return ret
	def set(self, value):
		self.lock.acquire()
		self.status = value
		self.lock.release()

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
	def __init__(self, init='', direct=False):
		object.__init__(self)
		self.data = []

		if type(init) == type(''): # Read plan from file (assuming we've got a file path)
				if len(init)>0:
					if direct:
						lines = init.split("\n")
					else:
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
				else:
					pass
		elif type(init) == type([]):
			for action in init:
				self.data.append(AGGLPlannerAction(action[0]+'@'+str(action[1])))
		elif type(init) == type(AGGLPlannerPlan()):
			#print 'AGGLPlannerPlan("COPY class")'
			self.data = copy.deepcopy(init.data)
		else:
			print 'Unknown plan type ('+str(type(init))+')! (internal error)'
			sys.exit(-321)
	def removeFirstAction(self, init):
		actionToRemove = self.data[0]
		symbolsInAction = set(actionToRemove.parameters.values())
		nodesInWorld = set(init.nodes.keys())
		created = symbolsInAction.difference(nodesInWorld)
		c = AGGLPlannerPlan()
		for action in self.data[1:]:
			c.data.append(copy.deepcopy(action))
		if len(created) > 0:
			minCreated = min([int(x) for x in created])
			for action in c.data:
				for parameter in action.parameters:
					if int(action.parameters[parameter]) >= minCreated:
						n = str(int(action.parameters[parameter])-len(created))
						action.parameters[parameter] = n
		return c
	def __iter__(self):
		self.current = -1
		return self
	def next(self):
		self.current += 1
		if self.current >= len(self.data):
			raise StopIteration
		else:
			return self.data[self.current]
	def __repr__(self):
		return self.graph.__str__()
	def __str__(self):
		ret = ''
		for a in self.data:
			ret += a.__str__() + '\n'
		return ret
	def __len__(self):
		return len(self.data)

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
		#print '__cmp__'
		return self.graph.__cmp__(other.graph)
	def __hash__(self):
		return self.graph.__hash__()
	def __eq__(self, other):
		return self.graph.__eq__(other.graph)
	def __repr__(self):
		return self.graph.__repr__()
	def __str__(self):
		return self.graph.__str__()

def printResult(result):
	print '-----  R  E  S  U  L  T  S  -----'
	if verbose > 0:
		print 'Cost', result.cost
		print 'Score', result.score
		l = 0
		for action in result.history:
			if action[0] != '#':
				l += 1
		print 'Length', l
		print 'Probability', result.probability
		#print 'NodeID', result.nodeId
		print 'Actions\n----------------'
	for action in result.history:
		print action


def CheckSymbolInGraph(graph, symbol):
	for cacho_n in graph.nodes:
		cacho = graph.nodes[cacho_n]
		if cacho.sType == symbol:
			return True
	return False

class PyPlan(object):
	def __init__(self, domainPath, init, targetPath, resultFile):
		object.__init__(self)
		# Get initial world mdoel
		self.initWorld = WorldStateHistory(xmlModelParser.graphFromXML(init))
		self.initWorld.nodeId = 0
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath)
		self.domain     = domain.RuleSet()

		#
		# These should be secured
		#

		# Get goal-checking code
		target = imp.load_source('target', targetPath)
		self.targetCode = target.CheckTarget
		# Some little initialization
		self.maxWorldSize = maxWorldIncrement+len(self.initWorld.graph.nodes.keys())
		self.mincostOnList = 0
		self.ruleMap = self.domain.getRules()
		self.openNodes = []
		heapq.heappush(self.openNodes, (0, copy.deepcopy(self.initWorld)))
		if verbose>1: print 'INIT'.ljust(20), self.initWorld
		self.knownNodes = []
		self.results = []
		self.explored = 0
		self.cheapestSolutionCost = -1
		self.timeA = datetime.datetime.now()

		# These are thread-safe
		self.end_condition = EndCondition()



		# Run threads
		self.initWorld.score, achieved = self.targetCode(self.initWorld.graph)
		if achieved:
			self.results.append(self.initWorld)
			self.cheapestSolutionCost = self.results[0].cost
			for s in self.results:
				if s.cost < self.cheapestSolutionCost: self.cheapestSolutionCost = s.cost
			# Check if we should stop because we are looking for the first solution
			if stopWithFirstPlan:
				self.end_condition.set("GoalAchieved")
		else:
			# Run working threads
			self.thread_locks = []
			for i in xrange(number_of_threads):
				lock = thread.allocate_lock()
				lock.acquire()
				self.thread_locks.append(lock)
				thread.start_new_thread(self.startThreadedWork, (lock, i))
			print 'Main thread waits'
			# Wait for the threads to stop
			for lock in self.thread_locks:
				lock.acquire()
			print 'workers finished'
		if self.end_condition.get() == "IndexError":
			if verbose > 0: print 'End: state space exhausted'
		elif self.end_condition.get() == "MaxCostReached":
			if verbose > 0: print 'End: max cost reached:', e.cost
		elif self.end_condition.get() == "BestSolutionFound":
			if verbose > 0: print 'End: best solution found'
		elif self.end_condition.get() == "GoalAchieved":
			if verbose > 0: print 'End: goal achieved'
		elif self.end_condition.get() == None:
			if verbose > 0: print 'NDD:DD:D:EWJRI'
		else:
			print 'UNKNOWN ERROR r3oite43kiohnx+439'

		if len(self.results)==0:
			if verbose > 0: print 'No plan found.'
		else:
			if verbose > 0: print 'Got', len(self.results),' plans!'
			min_idx = 0
			for i in range(len(self.results)):
				if self.results[i].cost < self.results[min_idx].cost:
					min_idx = i
			i = min_idx
			printResult(self.results[i])
			for action in self.results[i].history:
				if resultFile != None:
					resultFile.write(str(action)+'\n')
			if verbose > 0: print "----------------\nExplored", self.explored, "nodes"
			for e in domain.dddd:
				print e, domain.dddd[e]

	def startThreadedWork(self, lock, i):
		print 'Start thead worker'+str(i)
		while True:
			#print str(i)+'a'
			timeB = datetime.datetime.now()
			timeElapsed = (timeB-self.timeA).seconds + (timeB-self.timeA).microseconds/1e6
			# Check if we should give up because it already took too much time
			if timeElapsed > maxTimeWaitLimit:
				if len(self.results)>0:
					self.end_condition.set("GoalAchieved")
					lock.release()
					return
				else:
					self.end_condition.set("TimeLimit")
					lock.release()
					return
			# Check if we should stop looking because it's taking quite a long time and we already have a solution
			elif timeElapsed > maxTimeWaitAchieved and len(self.results)>0:
				self.end_condition.set("GoalAchieved")
				lock.release()
				return
			#print str(i)+'b'
			# Else, proceed...
			if len(self.openNodes) == 0:
				time.sleep(0.001)
				continue
			# Pop a node from the queue
			head = heapq.heappop(self.openNodes)[1] # P O P   POP   p o p   pop
			# Update 'mincostOnList', so we can stop when the minimum cost in the queue is bigger than one in the results
			if head.cost <= self.mincostOnList:
				if len(self.openNodes)==0:
					self.mincostOnList = 0
				else:
					self.mincostOnList = self.openNodes[0][1].cost
					for n in self.openNodes:
						if n[1].cost < self.mincostOnList:
							self.mincostOnList = n[1].cost
			# Check if we got to the maximum cost or the minimum solution
			#if head.cost > maxCost:
				#self.end_condition.set("MaxCostReached")
				#lock.release()
				#return
			#elif len(results)>0 and head.cost>self.cheapestSolutionCost:
				#self.end_condition.set("GoalAchieved")
				#lock.release()
				#return
			# Small test
			#print str(i)+'c'
			if verbose>5: print 'Expanding'.ljust(5), head
			for k in self.ruleMap:
				prtd = False
				# Iterate over rules and generate derivates
				for deriv in self.ruleMap[k](head):
					if not prtd:
						if verbose>5: print '  ', k
						prtd = True
					self.explored += 1
					if verbose > 0:
						if self.explored % 300 == 0:
							print 'Explored nodes:', self.explored,
							print "(last cost:"+str(head.cost)+"  depth:"+str(head.depth)+"  score:"+str(head.score)+")"
							print 'First(cost:'+str(self.openNodes[ 0][1].cost)+', score:'+str(self.openNodes[ 0][1].score)+', depth:'+str(self.openNodes[ 0][1].depth)+')'
							print  'Last(cost:'+str(self.openNodes[-1][1].cost)+', score:'+str(self.openNodes[-1][1].score)+', depth:'+str(self.openNodes[-1][1].depth)+')'
					deriv.score, achieved = self.targetCode(deriv.graph)
					if verbose>4: print deriv.score, achieved, deriv
					if achieved:
						#print 'Found solution', deriv.cost
						self.results.append(deriv)
						# Should we stop with the first plan?
						if stopWithFirstPlan:
							self.end_condition.set("GoalAchieved")
							lock.release()
							return
						# Compute cheapest solution
						self.cheapestSolutionCost = self.results[0].cost
						for s in self.results:
							if s.cost < self.cheapestSolutionCost:
								self.cheapestSolutionCost = s.cost
						# Check if ws should stop because there are no cheaper possibilities
						stopBecauseAllOpenNodesAreMoreExpensive = True
						for c in self.openNodes:
							if c[0] < self.cheapestSolutionCost:
								stopBecauseAllOpenNodesAreMoreExpensive = False
								break
						if stopBecauseAllOpenNodesAreMoreExpensive:
							self.end_condition.set("BestSolutionFound")
							lock.release()
							return
						#else:
							#print '+('+str(deriv.cost)+')'
					if not deriv in self.knownNodes:
						if deriv.stop == False:
							if self.cheapestSolutionCost < 1:
								ratio = 0.
							else:
								ratio = float(deriv.cost) / float(self.cheapestSolutionCost)
							#print cheapestSolutionCost, deriv.cost
							#print ratio
							if len(deriv.graph.nodes.keys()) <= self.maxWorldSize and ratio < maxCostRatioToBestSolution:
								self.knownNodes.append(head)
								#heapq.heappush(self.openNodes, (-deriv.score, deriv)) # score... the more the better
								#heapq.heappush(self.openNodes, ( deriv.cost, deriv)) # cost...  the less the better
								heapq.heappush(self.openNodes, ( (float(100.*deriv.cost)/(float(1.+deriv.score)), deriv)) ) # The more the better TAKES INTO ACCOUNT COST AND SCORE
								#heapq.heappush(self.openNodes, ( (float(100.+deriv.cost)/(float(1.+deriv.score)), deriv)) ) # The more the better TAKES INTO ACCOUNT COST AND SCORE

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


