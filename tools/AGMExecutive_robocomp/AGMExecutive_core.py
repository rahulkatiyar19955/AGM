import sys, traceback, Ice, subprocess, threading, time, Queue, os
import IceStorm

# AGM
sys.path.append('/usr/local/share/agm')

from parseAGGL import *
from generateAGGLPlannerCode import *
import xmlModelParser


# Check that RoboComp has been correctly detected
ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	pass
if len(ROBOCOMP)<1:
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()
preStr = "-I"+ROBOCOMP+"/Interfaces/ --all "+ROBOCOMP+"/Interfaces/"
Ice.loadSlice(preStr+"AGMCommonBehavior.ice")
Ice.loadSlice(preStr+"AGMAgent.ice")
Ice.loadSlice(preStr+"AGMExecutive.ice")
Ice.loadSlice(preStr+"AGMWorldModel.ice")
Ice.loadSlice(preStr+"Speech.ice")
import RoboCompAGMCommonBehavior
import RoboCompAGMAgent
import RoboCompAGMExecutive
import RoboCompAGMWorldModel
import RoboCompSpeech

import AGMModelConversion

class Executive(threading.Thread):
	def __init__(self, agglPath, initialModelPath, initialMissionPath, executiveTopic, executiveVisualizationTopic, speech):
		threading.Thread.__init__(self)
		self.agents = dict()

		# Set proxies
		self.executiveTopic = executiveTopic
		self.executiveVisualizationTopic = executiveVisualizationTopic
		self.speech = speech

		self.agglPath = agglPath
		print 'read agmfiledataparsing'
		self.agmData = AGMFileDataParsing.fromFile(self.agglPath)
		print 'generate domain active'
		self.agmData.generateAGGLPlannerCode("/tmp/domainActive.py", skipPassiveRules=False)
		print 'generate domain passive'
		self.agmData.generateAGGLPlannerCode("/tmp/domainPasive.py", skipPassiveRules=True)
		print 'read initialmodelpath'
		self.initialModel = xmlModelParser.graphFromXML(initialModelPath)
		print 'read initialmodelpath'
		self.setModel(xmlModelParser.graphFromXML(initialModelPath))
		print 'setmission'		
		self.setMission(xmlModelParser.graphFromXML(initialMissionPath))

	def setAgent(self, name, proxy):
		self.agents[name] = proxy
	def broadcastModel(self):
		#print '<<<broadcastinnn'
		#print '<<<broadcastinnn'
		#print self.currentModel
		#print 'broadcastinnn>>>'
		#print 'broadcastinnn>>>'
		ev = RoboCompAGMWorldModel.Event()
		ev.backModel = AGMModelConversion.fromInternalToIce(self.currentModel)
		ev.newModel = AGMModelConversion.fromInternalToIce(self.currentModel)
		self.executiveTopic.modelModified(ev)
	def reset(self):
		self.currentModel = xmlModelParser.graphFromXML(path)
		self.updatePlan()
	def setModel(self, model):
		self.currentModel = model
		self.broadcastModel()
	def setMission(self, target):
		self.target = target
		targetText = generateTarget(self.target)
		ofile = open("/tmp/target.py", 'w')
		ofile.write(targetText)
		ofile.close()
		self.updatePlan()
	def ignoreCommentsInPlan(self, plan):
		ret = []
		for i in plan:
			if len(i) > 0:
				if i[0] != '#':
					ret.append(i)
		return ret
	def updatePlan(self):
		# Save world
		self.currentModel.toXML("/tmp/lastWorld.xml")
		# Run planner
		import time
		print 'done\nRunning the planner...'
		start = time.time()
		subprocess.call(["agglplanner", "/tmp/domainActive.py", "/tmp/lastWorld.xml", "/tmp/target.py", "/tmp/result.txt"])
		end = time.time()
		print 'It took', end - start, 'seconds'
		# Get the output
		ofile = open("/tmp/result.txt", 'r')
		lines = self.ignoreCommentsInPlan(ofile.readlines())
		ofile.close()
		plan = []
		if len(lines) == 0:
			print 'No solutions found!'
			print 'No solutions found!'
			print 'No solutions found!'
			return
		line = lines[0]
		parts = line.split("@")
		action = parts[0]
		parameterMap = eval(parts[1])
		print 'action: <'+action+'>  parameters:  <'+str(parameterMap)+'>' 
		plan.append([action, parameterMap])
		# Prepare parameters
		params = dict()
		params['action'] = RoboCompAGMCommonBehavior.Parameter()
		params['action'].editable = False
		params['action'].value = action
		params['action'].type = 'string'
		params['plan'] = RoboCompAGMCommonBehavior.Parameter()
		params['plan'].editable = False
		params['plan'].value = '\n'.join(lines)
		params['plan'].type = 'string'
		for p in parameterMap.keys():
			params[p] = RoboCompAGMCommonBehavior.Parameter()
			params[p].editable = False
			params[p].value = parameterMap[p]
			params[p].type = 'string'
		#print params
		# Send plan
		print '<<<<<<<<<<<<<<<<<'
		print params
		print '>>>>>>>>>>>>>>>>>'
		print 'Send plan to'
		for agent in self.agents:
			try:
				print '\t', agent
				self.agents[agent].activateAgent(params)
			except:
				print 'Can\'t connect to', agent

		# Publish new information using the executiveVisualizationTopic
		#try
			#self.executiveVisualizationTopic.update(self.worldModelICE, self.targetModelICE, self.currentSolution)
		#except:
			#print "can't publish executiveVisualizationTopic.update"

	def modificationProposal(self, modification):
		print 'modificationProposal core'
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		self.worldModelICE = modification.newModel
		self.setModel(AGMModelConversion.fromIceToInternal_model(self.worldModelICE))
		self.updatePlan()



