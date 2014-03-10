#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2014 by Luis J. Manso
#
#    This file is part of AGM
#
#    AGM is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AGM is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
#    the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AGM.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, traceback, Ice, subprocess, threading, time, Queue, os
import IceStorm

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
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


class ExecutiveI (RoboCompAGMExecutive.AGMExecutive):
	def __init__(self, _handler):
		self.handler = _handler
	def broadcastModel(self, current=None):
		self.handler.broadcastModel()
	def activate(self, current=None):
		pass
	def deactivate(self, current=None):
		pass
	def reset(self, current=None):
		self.handler.reset()
	def modificationProposal(self, modification, current=None):
		self.handler.modificationProposal(modification)
	def setMission(self, target, current=None):
		self.handler.setMission(target)
	def getData(self, current=None):
		pass
		return world, target, plan

class AGMCommonBehaviorI (RoboCompAGMCommonBehavior.AGMCommonBehavior):
	def __init__(self, _handler):
		self.handler = _handler

class AGMAgentTopicI (RoboCompAGMAgent.AGMAgentTopic):
	def __init__(self, _handler):
		self.handler = _handler

from AGMExecutive_core import Executive


class Server (Ice.Application):
	def run (self, argv):
		status = 0;
		try:
			self.shutdownOnInterrupt()
			initialModelPath =   self.communicator().getProperties().getProperty( "InitialModelPath" )
			agglPath =           self.communicator().getProperties().getProperty( "AGGLPath" )
			initialMissionPath = self.communicator().getProperties().getProperty( "InitialMissionPath" )

			# Get a proxy for the Speech
			proxy = self.communicator().getProperties().getProperty( "SpeechProxy" )
			if len(proxy)<1:
				print 'SpeechProxy variable is empty, check the configuration file if speech output is desired.'
				speech = None
			else:
				speech = RoboCompSpeech.SpeechPrx.checkedCast(self.communicator().stringToProxy(proxy))

			# Proxy to publish AGMExecutiveTopic
			proxy = self.communicator().getProperties().getProperty("IceStormProxy")
			obj = self.communicator().stringToProxy(proxy)
			topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
			try:
				topic = False
				topic = topicManager.retrieve("AGMExecutiveTopic")
			except:
				pass
			while not topic:
				try:
					topic = topicManager.retrieve("AGMExecutiveTopic")
				except IceStorm.NoSuchTopic:
					try:
						topic = topicManager.create("AGMExecutiveTopic")
					except:
						print 'Another client created the AGMExecutiveTopic topic... ok'
			pub = topic.getPublisher().ice_oneway()
			executiveTopic = RoboCompAGMExecutive.AGMExecutiveTopicPrx.uncheckedCast(pub)


			# Proxy to publish AGMExecutiveVisualizationTopic
			proxy = self.communicator().getProperties().getProperty("IceStormProxy");
			obj = self.communicator().stringToProxy(proxy)
			topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
			try:
				topic = False
				topic = topicManager.retrieve("AGMExecutiveVisualizationTopic")
			except:
				pass
			while not topic:
				try:
					topic = topicManager.retrieve("AGMExecutiveVisualizationTopic")
				except IceStorm.NoSuchTopic:
					try:
						topic = topicManager.create("AGMExecutiveVisualizationTopic")
					except:
						print 'Another client created the AGMExecutiveVisualizationTopic topic... ok'
			pub = topic.getPublisher().ice_oneway()
			executiveVisualizationTopic = RoboCompAGMExecutive.AGMExecutiveVisualizationTopicPrx.uncheckedCast(pub)


			## Read config parameters
			#executive.agglPath = self.communicator().getProperties().getProperty( "AGGLPath" )
			#executive.initialModelXML = self.communicator().getProperties().getProperty( "InitialModelPath" )

			executive = Executive(agglPath, initialModelPath, initialMissionPath, executiveTopic, executiveVisualizationTopic, speech)
			executiveI = ExecutiveI(executive)
			agmcommonbehaviorI = AGMCommonBehaviorI(executive)

			# AGMExecutive server
			adapterExecutive = self.communicator().createObjectAdapter('AGMExecutive')
			adapterExecutive.add(executiveI, self.communicator().stringToIdentity('agmexecutive'))
			adapterExecutive.activate()

			# AGMCommonBehavior
			adapterAGMCommonBehavior = self.communicator().createObjectAdapter('AGMCommonBehavior')
			adapterAGMCommonBehavior.add(agmcommonbehaviorI, self.communicator().stringToIdentity('agmcommonbehavior'))
			adapterAGMCommonBehavior.activate()


			# Read agent's configurations and create the correspoding proxies
			agentConfigs = self.communicator().getProperties().getProperty( "AGENTS" ).split(',')
			for agent in agentConfigs:
				proxy = self.communicator().getProperties().getProperty(agent)
				behavior_proxy = RoboCompAGMCommonBehavior.AGMCommonBehaviorPrx.uncheckedCast(self.communicator().stringToProxy(proxy))
				if not behavior_proxy:
					print parameters.agents[i].c_str()
					print parameters.agents[i].c_str()
					print "Error loading behavior proxy!"
					sys.exit(1)
				executive.setAgent(agent,  behavior_proxy)
				print "Agent" , agent, "initialized ok"


			# Subscribe to AGMAgentTopic
			proxy = self.communicator().getProperties().getProperty( "IceStormProxy")
			obj = self.communicator().stringToProxy(proxy)
			topicManager = IceStorm.TopicManagerPrx.checkedCast(obj);
			adapterT = self.communicator().createObjectAdapter("AGMAgentTopic")
			agentTopic = AGMAgentTopicI(executive)
			proxyT = adapterT.addWithUUID(agentTopic).ice_oneway()
			try:
				topic = topicManager.retrieve("AGMAgentTopic")
				#qos = IceStorm.theQoS()
				topic.subscribeAndGetPublisher(None, proxyT)
			except IceStorm.NoSuchTopic:
				print "Error! No topic found!"
			adapterT.activate()



			print 'AGMExecutive initialization ok'
			executive.start()
			print '-------------------------------------------------------------'
			print '----     R u n     A G M E x e c u t i v e,     r u n   -----'
			print '-------------------------------------------------------------'
			executive.updatePlan()
			self.communicator().waitForShutdown()
		except:
			traceback.print_exc()
			status = 1

		if self.communicator():
			try:
				self.communicator().destroy()
			except:
				traceback.print_exc()
				status = 1

Server( ).main(sys.argv)
