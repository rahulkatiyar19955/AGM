import sys, traceback, Ice, subprocess, threading, time, Queue, os
import IceStorm

# AGM
sys.path.append('/usr/local/share/agm')

from parseAGGL import *
from generateAGGLPlannerCode import *
from agglplanner import *
from agglplanchecker import *

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
Ice.loadSlice(preStr+"Planning.ice")
import RoboCompAGMCommonBehavior
import RoboCompAGMAgent
import RoboCompAGMExecutive
import RoboCompAGMWorldModel
import RoboCompSpeech
import RoboCompPlanning

import AGMModelConversion

class Executive(threading.Thread):
	def __init__(self, agglPath, initialModelPath, initialMissionPath, executiveTopic, executiveVisualizationTopic, speech):
		threading.Thread.__init__(self)
		self.agents = dict()
		self.plan = None
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
		print 'set mission'
		self.setModel(xmlModelParser.graphFromXML(initialModelPath))
		self.worldModelICE = AGMModelConversion.fromInternalToIce(self.currentModel)
		print 'setmission'
		self.setMission(xmlModelParser.graphFromXML(initialMissionPath))

	def setAgent(self, name, proxy):
		self.agents[name] = proxy
	def broadcastModel(self):
		try:
			print '<<<broadcastinnn'
			print '<<<broadcastinnn'
			print self.currentModel
			ev = RoboCompAGMWorldModel.Event()
			ev.backModel = AGMModelConversion.fromInternalToIce(self.currentModel)
			ev.newModel = AGMModelConversion.fromInternalToIce(self.currentModel)
			self.executiveTopic.modelModified(ev)
			print 'broadcastinnn>>>'
			print 'broadcastinnn>>>'
		except:
			print 'There was some problem broadcasting'
			sys.exit(1)
	def reset(self):
		self.currentModel = xmlModelParser.graphFromXML(self.initialModel)
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

		# First, try with the current plan
		stored = False
		if self.plan != None:
			try:
				print 'Habia plan previo'
				currentPlanObj = AGGLPlannerPlan(self.plan)
				print '1'
				forwardPlanObj = currentPlanObj.removeFirstAction()
				domain = '/tmp/domainActive.py'
				init   = '/tmp/lastWorld.xml'
				target = '/tmp/target.py'
				# First of all, check without the first action of the current plan
				print '2'
				p = PyPlanChecker(domain, init, forwardPlanObj, target, '')
				print '3'
				if p.valid:
					stored = True
					plan = forwardPlanObj
					print 'LA VERSION FORWARD FUNCA'
				# If the forward version does not succeed, check with the current plan
				else:
					print '4'
					p = PyPlanChecker(domain, init, currentPlanObj, target, '')
					print '5'
					if p.valid:
						stored = True
						plan = currentPlanObj
						print 'LA VERSION ACTUAL FUNCA'
			except:
				stored = False

		if stored == False:
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
			self.plan = []
			if len(lines) == 0:
				self.plan = None
				print 'No solutions found!'
				print 'No solutions found!'
				print 'No solutions found!'
				return
		else:
			lines = str(plan)

		line = lines[0]
		parts = line.split("@")
		action = parts[0]
		parameterMap = eval(parts[1])
		print 'action: <'+action+'>  parameters:  <'+str(parameterMap)+'>' 
		self.plan.append([action, parameterMap])
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
		# Send plan
		print 'Send plan to'
		for agent in self.agents:
			try:
				print '\t', agent
				self.agents[agent].activateAgent(params)
			except:
				print 'Can\'t connect to', agent

		# Publish new information using the executiveVisualizationTopic
		try:
			planPDDL = RoboCompPlanning.Plan() # Generate a PDDL-like version of the current plan for visualization
			planPDDL.cost = -2.
			try:
				planPDDL.cost = -1.
				planPDDL.actions = []
				for step in self.plan:
					action = RoboCompPlanning.Action()
					action.name = step[0]
					action.symbols = []
					for ii in step[1]:
						action.symbols.append(ii+':'+step[1][ii])
				planPDDL.actions.append(action)
			except:
				traceback.print_exc()
				print 'Error generating PDDL-like version of the current plan'
			self.executiveVisualizationTopic.update(self.worldModelICE, AGMModelConversion.fromInternalToIce(self.target), planPDDL)
		except:
			traceback.print_exc()
			print "can't publish executiveVisualizationTopic.update"

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



