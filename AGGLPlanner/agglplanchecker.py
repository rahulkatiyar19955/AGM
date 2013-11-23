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

sys.path.append('/opt/robocomp/share')

import xmlModelParser
from AGGL import *
import inspect
from agglplanner import *


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
			for action in self.plan:
				print action
				for p in action.parameters.keys():
					if not action.parameters[p] in world.graph.nodes.keys():
						raise WrongRuleExecution("Parameter '"+action.parameters[p]+"' (variable '"+p+"') doesn't exists in the current world model.")
				world = self.domain.getTriggers()[action.name](world, action.parameters)
				print 'result:'
				print world
		except WrongRuleExecution, e:
			print e


		# Get result
		score, achieved = self.targetCode(world.graph)

		if achieved:
			print 'GOAL ACHIEVED'
			for action in self.plan:
				print action

		if resultPath!='':
			world.graph.toXML(resultPath)

		

if __name__ == '__main__': # program domain problem result
	if len(sys.argv)!=6 and len(sys.argv)!=5:
		print 'Usage\n\t', sys.argv[0], ' domain.py init.xml plan.plan target.aggl.py [result.xml]'
		sys.exit(0)
	elif len(sys.argv)==5:
		domain = sys.argv[1]
		init   = sys.argv[2]
		plan   = sys.argv[3]
		target = sys.argv[4]
		result = ''
	elif len(sys.argv)==6:
		domain = sys.argv[1]
		init   = sys.argv[2]
		plan   = sys.argv[3]
		target = sys.argv[4]
		result = sys.argv[5]

	p = PyPlanChecker(domain, init, plan, target, result)


