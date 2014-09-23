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
preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
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

#ret, stepsFwd, planMonitoring = 
def AGMExecutiveMonitoring(domain, init, currentModel, target, plan, stepsFwd=0):
	try:
		currentPlan = AGGLPlannerPlan(plan)
	except:
		traceback.print_exc()
		sys.exit(134)

	try:
		ret2 = False
		if len(currentPlan)>0:
			try:
				#print 'Trying one step ahead...', stepsFwd
				newPlan = currentPlan.removeFirstAction(currentModel)
				ret2, stepsFwd2, planMonitoring2 = AGMExecutiveMonitoring(domain, init, currentModel, target, newPlan, stepsFwd+1)
			except:
				#print steps, 'steps ahead did not work'
				traceback.print_exc()
				ret2 = False
		if ret2:
			#print 'ok', stepsFwd
			return ret2, stepsFwd2, planMonitoring2
		else:
			try:
				#print 'CHECK with a plan of', len(plan), 'steps,', stepsFwd, 'forward'
				#print plan
				p = PyPlanChecker(domain, init, currentPlan, target, '', verbose=False)
				if p.valid:
					#print 'GOT PLAN FROM MONITORING!!!'
					#print currentPlan
					return True, stepsFwd, currentPlan
				else:
					#print 'doesn\'t work'
					return False, 0, None
			except:
				traceback.print_exc()
				return False, 0, None
	except:
		traceback.print_exc()
		sys.exit(4991)
	traceback.print_exc()
	sys.exit(692)



class Executive(threading.Thread):
	def __init__(self, agglPath, initialModelPath, initialMissionPath, executiveTopic, executiveVisualizationTopic, speech):
		threading.Thread.__init__(self)
		self.mutex = threading.RLock()
		self.agents = dict()
		self.plan = None
		self.modifications = 0
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
		self.initialModelPath = initialModelPath
		self.initialModel = xmlModelParser.graphFromXML(initialModelPath)
		print 'set mission'
		self.backModelICE  = None
		self.setModel(xmlModelParser.graphFromXML(initialModelPath))
		self.worldModelICE = AGMModelConversion.fromInternalToIce(self.currentModel)
		print 'setmission'
		self.setMission(xmlModelParser.graphFromXML(initialMissionPath))

	def setAgent(self, name, proxy):
		self.agents[name] = proxy
	def broadcastModel(self):
		try:
			print '<<<broadcastinnn'
			print self.currentModel
			ev = RoboCompAGMWorldModel.Event()
			if self.backModelICE == None:
				ev.backModel = AGMModelConversion.fromInternalToIce(self.currentModel)
			else:
				ev.backModel = self.backModelICE
			ev.newModel = AGMModelConversion.fromInternalToIce(self.currentModel)
			self.executiveTopic.modelModified(ev)
			self.backModelICE = AGMModelConversion.fromInternalToIce(self.currentModel)
			print 'broadcastinnn>>>'
		except:
			print 'There was some problem broadcasting'
			sys.exit(1)
	def reset(self):
		self.currentModel = xmlModelParser.graphFromXML(self.initialModelPath)
		self.updatePlan()
	def setModel(self, model):
		print model
		self.currentModel = model
		self.broadcastModel()
	def setMission(self, target):
		self.target = target
		self.target.toXML("/tmp/target.xml")
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
	
	def callMonitoring(self):
		stored = False
		stepsFwd = 0
		print 'Trying with the last steps of the current plan...'
		domain = '/tmp/domainActive.py'
		init   = '/tmp/lastWorld.xml'
		target = '/tmp/target.py'
		try:
			#print '<<<Call Monitoring'
			#print '<<<Call Monitoring'
			#print self.plan
			#print '   Call Monitoring>>>'
			#print '   Call Monitoring>>>'
			ret, stepsFwd, planMonitoring = AGMExecutiveMonitoring(domain, init, self.currentModel, target, AGGLPlannerPlan(self.plan))
			print ret, stepsFwd, planMonitoring
			if ret:
				print 'Using a ', stepsFwd, 'step forwarded version of the previous plan'
				stored = True
				self.plan = planMonitoring
			else:
				print 'No modified version of the current plan satisfies the goal. Replanning is necessary.'
				stored = False
		except:
			print traceback.print_exc()
			print 'PARECE QUE NO FUNCIONO...'
			stored = False
		print 'done callMonitoring', stored, stepsFwd
		return stored, stepsFwd

	def updatePlan(self):
		# Save world
		self.currentModel.toXML("/tmp/lastWorld.xml")

		# First, try with the current plan
		stored = False
		if self.plan != None:
			stored, stepsFwd = self.callMonitoring()
			print stored, stepsFwd
		else:
			print 'No habia plan previo'

		print 'Running the planner?', stored==False
		if stored == False:
			# Run planner
			import time
			print 'Running the planner...'
			start = time.time()
			subprocess.call(["agglplanner", "/tmp/domainActive.py", "/tmp/lastWorld.xml", "/tmp/target.py", "/tmp/result.txt"])
			end = time.time()
			print 'It took', end - start, 'seconds'
			# Get the output
			ofile = open("/tmp/result.txt", 'r')
			lines = self.ignoreCommentsInPlan(ofile.readlines())
			ofile.close()
			self.plan = AGGLPlannerPlan('\n'.join(lines), direct=True)
			stored, stepsFwd = self.callMonitoring()
			#if len(lines) == 0:
				#self.plan = None
				#print 'No solutions found!'
				#print 'No solutions found!'
				#print 'No solutions found!'
				#return
		else:
			print 'Got plan from monitorization'
			print 'plan'
			print self.plan
			print 'plan'
			print 'Got plan from monitorization'

		# Extract first action
		action = "none"
		parameterMap = dict()
		if len(self.plan) > 0:
			action = self.plan.data[0].name
			parameterMap = self.plan.data[0].parameters
			
		print 'action: <'+action+'>  parameters:  <'+str(parameterMap)+'>' 
		# Prepare parameters
		params = dict()
		params['action'] = RoboCompAGMCommonBehavior.Parameter()
		params['action'].editable = False
		params['action'].value = action
		params['action'].type = 'string'
		params['plan'] = RoboCompAGMCommonBehavior.Parameter()
		params['plan'].editable = False
		params['plan'].value = str(self.plan)
		params['plan'].type = 'string'
		for p in parameterMap.keys():
			params[p] = RoboCompAGMCommonBehavior.Parameter()
			params[p].editable = False
			params[p].value = parameterMap[p]
			params[p].type = 'string'
		# Send plan
		print 'Send plan to'
		for agent in self.agents:
			print '\t', agent,
			try:
				self.agents[agent].activateAgent(params)
			except:
				print '     (can\'t connect to', agent, '!!!)',
			print ''

		# Publish new information using the executiveVisualizationTopic
		try:
			print self.plan
			planPDDL = RoboCompPlanning.Plan() # Generate a PDDL-like version of the current plan for visualization
			planPDDL.cost = -2.
			try:
				planPDDL.cost = -1.
				planPDDL.actions = []
				for step in self.plan:
					action = RoboCompPlanning.Action()
					action.name = step.name
					action.symbols = str(step.parameters).translate(None, '{}').split(',')
					planPDDL.actions.append(action)
			except:
				traceback.print_exc()
				print 'Error generating PDDL-like version of the current plan'
			self.executiveVisualizationTopic.update(self.worldModelICE, AGMModelConversion.fromInternalToIce(self.target), planPDDL)
		except:
			traceback.print_exc()
			print "can't publish executiveVisualizationTopic.update"
		print 'done'
	def modificationProposal(self, modification):
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		#  H E R E     W E     S H O U L D     C H E C K     T H E     M O D I F I C A T I O N     I S     V A L I D
		#
		self.worldModelICE = modification.newModel
		internalModel = AGMModelConversion.fromIceToInternal_model(self.worldModelICE, ignoreInvalidEdges=True)
		self.modifications += 1
		internalModel.toXML('modification'+(str(self.modifications).zfill(4))+'.xml')
		self.setModel(internalModel)
		self.updatePlan()

	def updateNode(self, nodeModification):
		internal = AGMModelConversion.fromIceToInternal_node(nodeModification)
		self.currentModel.nodes[internal.name] = copy.deepcopy(internal)
		self.executiveTopic.modelUpdated(nodeModification)		
