#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------------
#  -----  AGGLPlanChecker  -----
#  -----------------------------
#
#  Almost a free/libre AI planner.
#
#  Copyright (C) 2013 by Luis J. Manso
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


class PyPlanChecker(object):
	def __init__(self, domainPath, init, planPath, targetPath, resultPath=''):
		object.__init__(self)
		# Get initial world mdoel
		self.initWorld  = WorldStateHistory(xmlModelParser.graphFromXML(init))
		# Get graph rewriting rules
		domain = imp.load_source('domain', domainPath)
		self.domain     = domain.RuleSet()
		# Get goal-checking code
		if len(targetPath) > 0:
			target = imp.load_source('target', targetPath)
			self.targetCode = target.CheckTarget
		# Get plan
		self.plan = AGGLPlannerPlan(planPath)
		
		# Apply plan
		try:
			world = copy.deepcopy(self.initWorld)
			print world
			line = 0
			for action in self.plan:
				print 'Executing action', line 
				line += 1
				print action
				for p in action.parameters.keys():
					if not action.parameters[p] in world.graph.nodes.keys():
						raise WrongRuleExecution("Parameter '"+action.parameters[p]+"' (variable '"+p+"') doesn't exists in the current world model.")
				world = self.domain.getTriggers()[action.name](world, action.parameters, checked=False)
				print 'result:'
				print world
				world.graph.toXML('after_plan_step'+str(line)+".xml")

			print 'Done executing actions. Let\'s see what we\'ve got (computing score and checking if the goal was achieved).'

			print targetPath
			# Get result
			score, achieved = self.targetCode(world.graph)
			

			if achieved:
				print 'GOAL ACHIEVED'
				for action in self.plan:
					print action
			else:
				print 'Not achieved (didn\'t get to the goal)'

		except WrongRuleExecution, e:
			print 'Invalid rule execution', action
			print 'Rule: ', e
			print 'Line: ', line
			print 'Not achieved'
			traceback.print_exc()
		
		except:
			print 'Not achieved (error)'
			traceback.print_exc()


		if resultPath!='':
			world.graph.toXML(resultPath)

		
def printUsage():
	print 'Usage\n\t', sys.argv[0], ' domain.[py/aggl] init.xml plan.plan target.[py/xml]   [result.xml]'
	sys.exit(0)

if __name__ == '__main__': # program domain problem result
	if len(sys.argv)<5 or len(sys.argv)>6:
		printUsage()
	domain = sys.argv[1]
	init   = sys.argv[2]
	plan   = sys.argv[3]
	target = sys.argv[4]
	if len(sys.argv)==6:
		result = sys.argv[5]
	else:
		result = ''

	if domain.endswith('.aggl'):
		# Generate domain Python file
		agmData = AGMFileDataParsing.fromFile(domain)
		agmData.generateAGGLPlannerCode("/tmp/domain.py", skipPassiveRules=True)
		domain = "/tmp/domain.py"
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
			graph = graphFromXML(target)
			outputText = generateTarget(graph)
			ofile = open("/tmp/target.py", 'w')
			ofile.write(outputText)
			ofile.close()
		target = "/tmp/target.py"
	elif not target.endswith('.py'):
		printUsage()
		


	p = PyPlanChecker(domain, init, plan, target, result)


