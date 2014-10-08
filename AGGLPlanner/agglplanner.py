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




#---------------------------------------------------------------------------------------------------------------------------------------------------#
"""@package agglplanner
    @ingroup PyAPI
    This file loads the grammar, the initial state of the world and the GOAL status without changing the files extensions of the grammar and the goal.
    
    MODE USE:	agglplanner gramatica.aggl init.xml target.py
    
    Also, we can keep the results in a file with: agglplanner gramatica.aggl init.xml target.py result.plan
"""


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
number_of_threads = 0
maxWorldIncrement = 14
maxCost = 200
stopWithFirstPlan = False
verbose = 1
maxTimeWaitAchieved = 10.
maxTimeWaitLimit = 3000.

## @brief Method heapsort. This method receives as input parameter:
# @param iterable
def heapsort(iterable):
	h = []
	for value in iterable:
		heapq.heappush(h, value)
	return [heapq.heappop(h) for i in range(len(h))]

##@brief This class stored the status and a lock.
class EndCondition(object):
	##@brief Constructor Method. This method saves the status and the lock of the class.
	# @param status it is an optional parameter and, by default, his value is None.
	def __init__(self, status=None):
		## Status of the class --> the status of the final condition
		self.status = status
		## The lock for read and write the status
		self.lock = thread.allocate_lock()
	
	##@brief Get Method. This method returns the status of the class. To do this, the method needs
	# to lock the other threads. This method reads a critical variable.
	# @retval ret is the status of the class.
	def get(self):
		self.lock.acquire()
		ret = self.status
		self.lock.release()
		return ret
	      
	##@brief Set method. This method changes the value of the status attribute. To do this, the
	# method needs to write in a critical memory zone, so it is necesary to lock it.
	# @param value is the new status
	def set(self, value):
		self.lock.acquire()
		self.status = value
		self.lock.release()

##@brief This class manages the exception of a wrong rule execution.
class WrongRuleExecution(Exception):
	##@brief Constructor method. It saves the data of the Exception
	# @param data
	def __init__(self, data):
		## Data of the exception 
		self.data = data
	
	##@brief This method returns the data of the exception.
	# @retval data.
	def __str__(self):
		return self.data

##@brief This class get the name and the parameters of an action that belongs to a plan.
class AGGLPlannerAction(object):
	##@brief Constructor method. It receives (optionally) the contructor method of the object, but, by default, it is empty.
	# @param init is an optional initialization variable
	# If anything is wrong, this method throws an exception.
	def __init__(self, init=''):
		object.__init__(self)
		## Name of the action
		self.name = ''
		## Name of the action parameters
		self.parameters = dict()
		if len(init)>0:
			parts = init.split('@')
			self.name = parts[0]
			self.parameters = eval(parts[1])
		else:
			raise IndexError
		      
	##@brief This method returns the name and the parameters of the action in a string.
	# @retval string with the name of the action and the parameters
	def __str__(self):
		return self.name+'@'+str(self.parameters)

## @brief AGGLPlannerPlan is used as a plan container.
class AGGLPlannerPlan(object):
	## @brief Parametrized constructor.
	# @param init Optional initialization variable. It can be a) string containing a plan; b) a filename where such string is to be found,
	# or c) a list of tuples where each tuple contains the name of a rule and a dictionary with the variable mapping of the rule.
	# @param direct optional. By default his value is FALSE
	def __init__(self, init='', direct=False):
		object.__init__(self)
		
		## Data of the plan file
		self.data = []

		if type(init) == type(''): # Read plan from file (assuming we've got a file path)
			if len(init)>0:
				if direct:
					lines = init.split("\n") #newline
				else:
					lines = open(init, 'r').readlines() # take the content of a file
				for line_i in range(len(lines)):
					line = lines[line_i].strip() # take a line of the file content 
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
			self.data = copy.deepcopy(init.data)
		else:
			print 'Unknown plan type ('+str(type(init))+')! (internal error)'
			sys.exit(-321)

	## @brief Returns a copy of the plan without the first action assuming the action was executed. It's used for monitorization purposes.
	# @param currentModel Model associated to the current state of the world
	# @retval The resulting version of the plan
	def removeFirstAction(self, currentModel):
		## @internal Create the copy without the first actions.
		c = AGGLPlannerPlan()
		for action in self.data[1:]:
			c.data.append(copy.deepcopy(action))
		## @internal Modify the rest of the actions assuming the first action was executed.
		actionToRemove = self.data[0]
		symbolsInAction = set(actionToRemove.parameters.values())
		nodesInWorld = set(currentModel.nodes.keys())
		created = symbolsInAction.difference(nodesInWorld)
		if len(created) > 0:
			minCreated = min([int(x) for x in created])
			for action in c.data:
				for parameter in action.parameters:
					if int(action.parameters[parameter]) >= minCreated:
						n = str(int(action.parameters[parameter])-len(created))
						action.parameters[parameter] = n
		return c
	      
	## @brief This method This method subtracts a unit to counter the class.
	# @retval the class with the diferent value of the counter
	def __iter__(self):
		## counter of the data 
		self.current = -1
		return self
	      
	## @brief This method counts +1 on the current variable. If the counter overcome the
	# length of the data attribute, it raises an exception. If not, the method returns the
	# data with the index==current+1.
	# @retval the data with the index current+1
	def next(self):
		self.current += 1
		if self.current >= len(self.data):
			raise StopIteration
		else:
			return self.data[self.current]
	
	##@brief This method returns the information of the graph as a string.
	# @retval a string with the information of the plan graph.
	def __repr__(self):
		## The plan graph
		return self.graph.__str__()
	      
	##@brief this method returns a string with the data array information.
	# @retval ret is the string with all the data
	def __str__(self):
		ret = ''
		for a in self.data:
			ret += a.__str__() + '\n'
		return ret
	
	##@brief this method returns the length of the data array.
	# @retval an integer that is the length of the data array.
	def __len__(self):
		return len(self.data)

##@brief This class saves all the information of the current graph
class WorldStateHistory(object):
	##@brief Constructor method.
	# @param init initialization variable
	def __init__(self, init):
		object.__init__(self)
		# If
		if isinstance(init, AGMGraph):
			# Graph with the current world status.
			self.graph = copy.deepcopy(init)
			# The identifier of the graph that the current graph comes from
			self.parentId = 0
			# ???
			self.probability = 1
			# The cost of the new graph (as result of execute the heuristic?)
			self.cost = 0
			# The string with all the changes made from the original graph.
			self.history = []
			# The identifier of the current graph
			self.nodeId = -1
			# The depth of the current graph.
			self.depth = 0
			# A flag to stop.
			self.stop = False
			# The heuristic score of the current graph
			self.score = 0
		elif isinstance(type(init), type(WorldStateHistory)):
			self.graph = copy.deepcopy(init.graph)
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
			
	##@brief
	def __cmp__(self, other):
		#print '__cmp__'
		return self.graph.__cmp__(other.graph)
	def __hash__(self):
		return self.graph.__hash__()
	
	##@brief This method returns the result of comparing two graphs
	# @param other the other graph.
	# @retval a boolean wit the result of the comparison
	def __eq__(self, other):
		return self.graph.__eq__(other.graph)
	      
	
	def __repr__(self):
		return self.graph.__repr__()
	      
	##@brief This method returns a string with the information of the current graph.
	def __str__(self):
		return self.graph.__str__()

##@brief This method prints on the screen all the information of the new graph: the cost, 
# the score, the number of actions and the names of the actions.
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
		print 'Actions\n----------------'
	for action in result.history:
		#if action[0] != '#':
		print action

##@brief
class LockableList():
	##@brief Constructor Method. It initializes the list and the mutex.
	def __init__(self):
		## The lockable list.
		self.thelist = []
		## The mutex associated to the list.
		self.mutex = threading.RLock()
		
	##@brief This method return the length of the lockable list.
	# @retval an integer that is the length of the list.
	def __len__(self):
		return len(self.thelist)
	      
	##@brief This method returns the item with the index or keyword a in the list.
	# @param a is the index or the keyword  of the item.
	# @retval the item that corresponds to the index a.
	def __getitem__(self, a):
		return self.thelist.__getitem__(a)
	     
	##@brief This method changes the item for the item b. Is necessary to lock the
	# the method, it changes a critical memory zone.-
	# @param a first item
	# @param b second item.
	def __setitem__(self, a, b):
		self.mutex.acquire()
		self.thelist.__setitem__(a, b)
		self.mutex.release()
		
	##@brief This method return the iterator of the list.
	# @retval the iterator of the lockable list.
	def __iter__(self):
		return self.thelist.__iter__()
	      
	##@brief This method returns the size (the length) of the list.
	# This method needs acces to a critical memory zone, so it is necessary to
	# lock all the process.
	# @retval ret is an integer that is the size of the list.
	def size(self):
		self.mutex.acquire()
		ret = len(self.thelist)
		self.mutex.release()
		return ret
	
	##@brief this method 
	def heapqPop(self):
		self.mutex.acquire()
		try:
			ret = heapq.heappop(self.thelist)
		finally:
			self.mutex.release()
		return ret
	
	def heapqPush(self, value):
		self.mutex.acquire()
		heapq.heappush(self.thelist, value)
		self.mutex.release()
	def getFirstElement(self):
		self.mutex.acquire()
		ret = self.thelist[0]
		self.mutex.release()
		return ret
	def append(self, v):
		self.mutex.acquire()
		self.thelist.append(v)
		self.mutex.release()
	def lock(self):
		self.mutex.acquire()
	def unlock(self):
		self.mutex.release()

class LockableInteger(object):
	def __init__(self, val=0):
		self.value = val
		self.mutex = threading.RLock()
	def set(self, val):
		self.mutex.acquire()
		self.value = val
		self.mutex.release()
	def get(self):
		self.mutex.acquire()
		ret = self.value
		self.mutex.release()
		return ret
	def lock(self):
		self.mutex.acquire()
	def unlock(self):
		self.mutex.release()
	def increase(self):
		self.mutex.acquire()
		self.value += 1
		self.mutex.release()

class PyPlan(object):
	def __init__(self, domainPath, init, targetPath, resultFile):
		object.__init__(self)
		# Get initial world mdoel
		initWorld = WorldStateHistory(xmlModelParser.graphFromXML(init))
		initWorld.nodeId = 0
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath).RuleSet()
		ruleMap = domain.getRules()
		# Get goal-checking code
		target = imp.load_source('target', targetPath)
		self.targetCode = target.CheckTarget

		# Search initialization
		self.maxWorldSize = maxWorldIncrement+len(initWorld.graph.nodes.keys())
		self.minCostOnOpenNodes = LockableInteger(0)
		self.openNodes = LockableList()
		self.knownNodes = LockableList()
		self.results = LockableList()
		self.explored = LockableInteger(0)
		self.cheapestSolutionCost = LockableInteger(-1)
		self.end_condition = EndCondition()
		self.openNodes.heapqPush((0, copy.deepcopy(initWorld)))
		if verbose>1: print 'INIT'.ljust(20), initWorld

		# Create initial state
		initWorld.score, achieved = self.targetCode(initWorld.graph)

		if achieved:
			self.results.append(initWorld)
			self.cheapestSolutionCost.set(self.results.getFirstElement().cost)
			self.end_condition.set("GoalAchieved")
		elif number_of_threads>0:
			# Run working threads
			self.thread_locks = []
			threadStatus = LockableList()
			for i in xrange(number_of_threads):
				lock = thread.allocate_lock()
				lock.acquire()
				threadStatus.append(True)
				self.thread_locks.append(lock)
				thread.start_new_thread(self.startThreadedWork, (copy.deepcopy(ruleMap), lock, i, threadStatus))
			# Wait for the threads to stop
			for lock in self.thread_locks:
				lock.acquire()
		else:
			print 'no threading'
			self.startThreadedWork(ruleMap)

		if self.end_condition.get() == "IndexError":
			if verbose > 0: print 'End: state space exhausted'
		elif self.end_condition.get() == "MaxCostReached":
			if verbose > 0: print 'End: max cost reached:', e.cost
		elif self.end_condition.get() == "BestSolutionFound":
			if verbose > 0: print 'End: best solution found'
		elif self.end_condition.get() == "GoalAchieved":
			if verbose > 0: print 'End: goal achieved'
		elif self.end_condition.get() == "TimeLimit":
			if verbose > 0: print 'End: TimeLimit'
		elif self.end_condition.get() == None:
			if verbose > 0: print 'NDD:DD:D:EWJRI'
		else:
			print 'UNKNOWN ERROR'
			print self.end_condition.get()

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
			if verbose > 0: print "----------------\nExplored", self.explored.get(), "nodes"

	def startThreadedWork(self, ruleMap, lock=None, i=0, threadPoolStatus=None):
		if lock == None:
			lock = thread.allocate_lock()
			lock.acquire()
		if threadPoolStatus != None:
			threadPoolStatus.lock()
			threadPoolStatus[i] = True
			threadPoolStatus.unlock()
		timeA = datetime.datetime.now()
		while True:
			#print 'a'
			timeB = datetime.datetime.now()
			timeElapsed = float((timeB-timeA).seconds) + float((timeB-timeA).microseconds)/1e6
			# Check if we should give up because it already took too much time
			nResults = self.results.size()
			if timeElapsed > maxTimeWaitLimit or (timeElapsed > maxTimeWaitAchieved and nResults > 0):
				if nResults>0: self.end_condition.set("GoalAchieved")
				else: self.end_condition.set("TimeLimit")
				lock.release()
				return
			# Else, proceed...
			# Try to pop a node from the queue
			try:
				#print 'b'
				head = self.openNodes.heapqPop()[1] # P O P   POP   p o p   pop
				#print 'c'
				if threadPoolStatus:
					threadPoolStatus.lock()
					threadPoolStatus[i] = True
					threadPoolStatus.unlock()
				# Handle hierarchical rules
				if hasattr(head, "parentNodeToExplore"):
					try:
						#print 'd'
						gotFromHead = head.parentNodeToExploreWith(head.parentNodeToExplore, head.stackP, head.equivalencesP)
						print 'ueeeeeee', len(gotFromHead)
						for deriv in gotFromHead:
							self.explored.increase()
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
								self.updateCheapestSolutionCostAndCutOpenNodes(self.results[0].cost)
							self.knownNodes.lock()
							notDerivInKnownNodes = not deriv in self.knownNodes
							self.knownNodes.unlock()
							if notDerivInKnownNodes:
								if deriv.stop == False:
									if len(deriv.graph.nodes.keys()) <= self.maxWorldSize:
										self.openNodes.heapqPush( (float(deriv.cost)-10.*float(deriv.score), deriv) ) # The more the better TAKES INTO ACCOUNT COST AND SCORE
						continue
						#print 'e'
					except:
						#print 'f'
						traceback.print_exc()
				else:
					#print 'g'
					self.knownNodes.append(head)
					#print 'h'
					gotFromHead = [head]
					#print 'i'
			except:
				#traceback.print_exc()
				if not threadPoolStatus:
					self.end_condition.set("IndexError")
					lock.release()
					return
				time.sleep(0.001)
				threadPoolStatus.lock()
				threadPoolStatus[i] = False
				if not True in threadPoolStatus:
					self.end_condition.set("IndexError")
					lock.release()
					return
				threadPoolStatus.unlock()
				continue

			#print 'h'
			for head in gotFromHead: # Bear in mind that if we pop an unexplored node from a hierarchical rule we usually end up fetching serveral nodes
				#print 'i'

				# Update 'minCostOnOpenNodes', so we can stop when the minimum cost in the queue is bigger than one in the results
				self.updateMinCostOnOpenNodes(head.cost)
				# Check if we got to the maximum cost or the minimum solution
				if head.cost > maxCost:
					self.end_condition.set("MaxCostReached")
					lock.release()
					return
				elif self.results.size()>0 and head.cost>self.cheapestSolutionCost.value:
					self.end_condition.set("GoalAchieved")
					lock.release()
					return
				if verbose>5: print 'Expanding'.ljust(5), head
				for k in ruleMap:
					# Iterate over rules and generate derivates
					for deriv in ruleMap[k](head):
						self.explored.increase()
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
							self.updateCheapestSolutionCostAndCutOpenNodes(self.results[0].cost)
						self.knownNodes.lock()
						notDerivInKnownNodes = not deriv in self.knownNodes
						self.knownNodes.unlock()
						if notDerivInKnownNodes:
							if deriv.stop == False:
								if len(deriv.graph.nodes.keys()) <= self.maxWorldSize:
									self.openNodes.heapqPush( (float(deriv.cost)-10.*float(deriv.score), deriv) ) # The more the better TAKES INTO ACCOUNT COST AND SCORE
				if verbose > 0:
					doIt=False
					nowNow = datetime.datetime.now()
					try:
						elap = (nowNow-self.lastTime).seconds + (nowNow-self.lastTime).microseconds/1e6
						doIt = elap > 3
					except:
						self.lastTime = datetime.datetime.now()
						doIt = True
					if doIt:
						self.lastTime = nowNow
						try:
							#print nowNow
							print str(int(timeElapsed)).zfill(10)+','+str(len(self.openNodes))+','+str(len(self.knownNodes))+','+str(head.score)
							#rrrr = heapsort(self.openNodes)
							#print 'OpenNodes', len(rrrr), "(HEAD cost:"+str(head.cost)+"  depth:"+str(head.depth)+"  score:"+str(head.score)+")"
							#if len(self.openNodes) > 0:
								#print 'First['+str(rrrr[ 0][0])+'](cost:'+str(rrrr[ 0][1].cost)+', score:'+str(rrrr[ 0][1].score)+', depth:'+str(rrrr[ 0][1].depth)+')'
								#print  'Last['+str(rrrr[-1][0])+'](cost:'+str(rrrr[-1][1].cost)+', score:'+str(rrrr[-1][1].score)+', depth:'+str(rrrr[-1][1].depth)+')'
							#else:
								#print 'no open nodes'
						except:
							traceback.print_exc()

	def updateCheapestSolutionCostAndCutOpenNodes(self, cost):
		self.cheapestSolutionCost.lock()
		if cost >= self.cheapestSolutionCost.get():
			self.cheapestSolutionCost.unlock()
		else:
			self.openNodes.lock()
			self.cheapestSolutionCost.set(cost)

			newOpenNodes = LockableList()
			for node in self.openNodes:
				if node[1].cost < cost:
					newOpenNodes.heapqPush(node)
			self.openNodes.thelist = newOpenNodes.thelist

			self.openNodes.unlock()
			self.cheapestSolutionCost.unlock()

	def updateMinCostOnOpenNodes(self, cost):
		self.minCostOnOpenNodes.lock()
		self.openNodes.lock()
		if cost < self.minCostOnOpenNodes.value:
			if self.getNumberOfOpenNodes()==0:
				self.minCostOnOpenNodes.value = 0
			else:
				self.minCostOnOpenNodes.value = self.firstOpenNode()[1].cost
				for n in self.openNodes:
					if n[1].cost < self.minCostOnOpenNodes.value:
						self.minCostOnOpenNodes.value = n[1].cost
		self.openNodes.unlock()
		self.minCostOnOpenNodes.unlock()

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
