#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------------
#  -----  AGGLPlanChecker  -----
#  -----------------------------
#
#  Almost a free/libre AI planner.
#
#  Copyright (C) 2013-2014 by Luis J. Manso
#
#  AGGLPlanChecker is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AGGLPlanChecker is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AGGLPlanner. If not, see <http://www.gnu.org/licenses/>.




#---------------------------------------------------------------------------------------------------------------------------------------------------#
"""@package agglplanchecker
    @ingroup PyAPI
    This file contains a class that checks that the rules of a grammar are correct
"""



# Python distribution imports
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import sys, traceback, os, re, threading, time, string, math, copy
import collections, imp, heapq

sys.path.append('/usr/local/share/agm/')

import xmlModelParser
from AGGL import *
import inspect
from agglplanner import *
from parseAGGL import *
from generateAGGLPlannerCode import *


##@brief This class is responsible for checking the plan that is generated in python.
class PyPlanChecker(object):

	##@brief Constructor method: It initializes all class attributes and checks the plan
	# @param domainPath Python version of the grammar
	# @param init XML-version of the initial world state
	# @param planPath Path of the plan
	# @param targetPath Python-version of the target state
	# Also, there are two optionals parameters:
	# @param resultPath is the path of the result is stored. By default it's empty
	# @param verbose is a parameter that shows additional information
	def __init__(self, agmData, domainPath, init, planPath, targetPath, resultPath='', verbose=False):
		object.__init__(self)
		## We get the initial world model graph
		self.initWorld  = WorldStateHistory(xmlModelParser.graphFromXML(init))
		# Get graph rewriting rules
		if verbose: print 'domainPath:', domainPath
		domain = imp.load_source('domain', domainPath)
		## We save the grammar rules
		self.domain     = domain.RuleSet()
		# Get goal-checking code
		if len(targetPath) > 0:
			if verbose: print 'targetPath:', targetPath
			target = imp.load_source('target', targetPath)
			## We get the python code of the target world status
			self.targetCode = target.CheckTarget
		## We get the plan code
		self.plan = AGGLPlannerPlan(planPath)

		# Apply plan
		if verbose: print "PyPlanChecker applying plan"
		try:
			world = copy.deepcopy(self.initWorld) # we copy the initial world status.
			#if verbose: print world
			line = 0 # This is the actions lines counter. It saves the lines of actions contained in a plan
			if verbose: print '<<plan'
			if verbose: print self.plan
			if verbose: print 'plan>>'
			# We check all the actions in a plan.
			for action in self.plan:
				if verbose: print 'Executing action', line
				line += 1
				if verbose: print action
				# We check that the actions parameters are into the world.
				for p in action.parameters.keys():
					if not action.parameters[p] in world.graph.nodes.keys():
						for r in agmData.agm.rules:
							if r.name == action.name:
								rhs = r.rhs
						if not (p in rhs.nodes.keys()):
							# If the parameter doesnt exit in the world nor the RHS of the rule, we raise an exception.
							# Just to warn we're receiving useless parameters
							raise WrongRuleExecution("Parameter '"+action.parameters[p]+"' (variable '"+p+"') doesn't exist in the current world model.")
				world = self.domain.getTriggers()[action.name](world, action.parameters, checked=False)
				if verbose:
					print 'result:'
					print world
				world.graph.toXML('after_plan_step'+str(line)+".xml")

			if verbose: print 'Done executing actions. Let\'s see what we\'ve got (computing score and checking if the goal was achieved).'
			if verbose: print targetPath
			# Get result
			score, achieved = self.targetCode(world.graph)
			## We store the result to check the plan
			self.valid = achieved
			# By one hand, if we achieve the target world status, we will print all the  correct actions of the plan.
			# By the other hand, if we dont achieve the goal, we will print an error message.
			if achieved:
				print 'GOAL ACHIEVED'
				self.achieved = True
				for action in self.plan:
					if verbose: print action
			else:
				self.achieved = False
				print 'Not achieved (didn\'t get to the goal)'
				
		# If we have thrown an exception (because a parameter of an action does not exist), 
		# we handle part of the exception in this code.
		except WrongRuleExecution, e:
			if verbose: print 'Invalid rule execution', action
			if verbose: print 'Rule: ', e
			if verbose: print 'Line: ', line
			if verbose: print 'Not achieved'
			self.valid = False
			#traceback.print_exc()
		except:
			self.valid = False
			if verbose: print 'Not achieved (error)'
			#traceback.print_exc()
		# If there is a XML file where we must save the result, we store the result... 
		if resultPath!='':
			world.graph.toXML(resultPath)

## @brief This method prints the USER MODE of the PyPlanChecker class.
# " Usage
#   PROGRAM_NAME domain.[py/aggl] init.xml plan.plan target.[py/xml] [result.xml]
def printUsage():
	print 'Usage\n\t', sys.argv[0], ' domain.[py/aggl] init.xml plan.plan target.[py/xml]   [result.xml]'
	sys.exit(0)

# Procedure.
if __name__ == '__main__': # program domain problem result
	# We check the correct number of arguments
	if len(sys.argv)<5 or len(sys.argv)>6:
		printUsage()
	# If everything is correct, we save the arguments in local variables.
	## The grammar rules
	domain = sys.argv[1]
	## The initial world status
	init   = sys.argv[2]
	## The plan genetared by the planner.
	plan   = sys.argv[3]
	## The target or goal world status.
	target = sys.argv[4]
	
	if len(sys.argv)==6:
		## We save the name of the file where the result will be stored.
		result = sys.argv[5]
	else:
		result = ''
  
	# If the grammar is stored in a .aggl file, we must generate the domain python file.
	if domain.endswith('.aggl'):
		## The domain python file is stored in agmData
		agmData = AGMFileDataParsing.fromFile(domain)
		# We save the python code in the domain.py file.
		agmData.generateAGGLPlannerCode("/tmp/domain.py", skipPassiveRules=True)
		domain = "/tmp/domain.py"
	# If the domain file doesnt finish with the correct extension, we will show an error message
	elif not domain.endswith('.py'):
		printUsage()

	if target.endswith('.xml'):
		# Generate target Python file
		if False:
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
			print 'TARGET WRITING IS DISABLED WARNING!!'
		else:
			## graph contains the state of the target world become a graph 
			graph = graphFromXML(target)
			## outputText get the python code of the target world graph.
			outputText = generateTarget(graph)
			## ofile is the file where we will store the python code of the target world graph.
			ofile = open("/tmp/target.py", 'w')
			ofile.write(outputText)
			ofile.close()
		# We save the name of the file where we will store the python code of the target world graph.
		target = "/tmp/target.py"
	# If the target file doesnt end with the cirrect extension, we will show an error message.
	elif not target.endswith('.py'):
		printUsage()


	## P is the PyPlanChecker, that checks the plan generated by the planner
	p = PyPlanChecker(agmData, domain, init, plan, target, result)

