#!/usr/bin/env python

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
#
#--------------------------------------------------------------------------
#                            DOCUMENTATION                                 
#--------------------------------------------------------------------------
# This file loads the grammar, the initial state of the world and the GOAL 
# status without changing the files extensions of the grammar and the goal.
# MODE USE:
# 		agglplan gramatica.aggl init.xml target.xml
#
# Python distribution imports
import sys, traceback, subprocess

sys.path.append('/usr/local/share/agm/')
from AGGL import *
from parseAGGL import *
from generateAGGLPlannerCode import *
from agglplanner import *

if __name__ == '__main__': # program domain problem result
	if len(sys.argv)<4:
		print 'Usage\n\t', sys.argv[0], ' domain.aggl init.xml target.xml [result.plan]'
	else:
		domainFile = sys.argv[1]
		worldFile  = sys.argv[2]
		targetFile = sys.argv[3]
		result = None
		if len(sys.argv)>4:
			result = sys.argv[4]
			
		print 'Generating search code...',

		# Generate domain Python file
		agmData = AGMFileDataParsing.fromFile(domainFile)
		agmData.generateAGGLPlannerCode("/tmp/domain.py", skipPassiveRules=True)

		# Generate target Python file
		graph = graphFromXML(targetFile)
		outputText = generateTarget(graph)
		ofile = open("/tmp/target.py", 'w')
		ofile.write(outputText)
		ofile.close()

		# Run planner
		import time
		print 'done\nRunning the planner...'
		start = time.time()
		if result:
			subprocess.call(["agglplanner", "/tmp/domain.py", worldFile, "/tmp/target.py", result])
		else:
			subprocess.call(["agglplanner", "/tmp/domain.py", worldFile, "/tmp/target.py"])
		end = time.time()
		print 'It took', end - start, 'seconds'


