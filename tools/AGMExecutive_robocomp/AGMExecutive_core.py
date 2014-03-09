import sys, traceback, Ice, subprocess, threading, time, Queue, os
import IceStorm

import xmlModelParser

# AGM
sys.path.append('/usr/local/share/agm')

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
	def __init__(self, agglPath, initialModelPath, initialMissionPath)
		threading.Thread.__init__(self)

		self.agglPath = agglPath
		self.agmData = AGMFileDataParsing.fromFile(self.agglPath)
		self.agmData.generateAGGLPlannerCode("/tmp/domainActive.py", skipPassiveRules=False)
		self.agmData.generateAGGLPlannerCode("/tmp/domainPasive.py", skipPassiveRules=True)

		self.initialModel = xmlModelParser.graphFromXML(initialModelPath)
		self.currentModel = xmlModelParser.graphFromXML(initialModelPath)
		
		self.setMission(xmlModelParser.graphFromXML(initialMissionPath))

		self.agents = dict()
	def setAgent(self, name, proxy):
		self.agents[name] = proxy
	def broadcastModel(self):
		print 'broadcastinnn'
		ev = RoboCompAGMWorldModel.Event()
		ev.backModel = AGMModelConversion.fromInternalToIce(self.currentModel)
		ev.newModel = AGMModelConversion.fromInternalToIce(self.currentModel)
		self.executiveTopic.modelModified(ev)
	def reset(self):
		self.currentModel = xmlModelParser.graphFromXML(path)
		self.updatePlan()
	def setMission(self, target):
		self.target = target
		targetText = generateTarget(self.target)
		ofile = open("/tmp/target.py", 'w')
		ofile.write(targetText)
		ofile.close()
		self.updatePlan()
	def updatePlan(self):
		# Run planner
		import time
		print 'done\nRunning the planner...'
		start = time.time()
		subprocess.call(["agglplanner", "/tmp/domainActive.py", worldFile, "/tmp/target.py", "/tmp/result.txt"])
		end = time.time()
		print 'It took', end - start, 'seconds'
		
		


