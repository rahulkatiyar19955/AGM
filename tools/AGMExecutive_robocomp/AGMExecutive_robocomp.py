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

import xmlModelParser
import AGMModelConversion

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
import RoboCompAGMCommonBehavior
import RoboCompAGMAgent
import RoboCompAGMExecutive
import RoboCompAGMWorldModel
import RoboCompSpeech

from AGGL import *
from agglplanningcache import *

class ExecutiveI (RoboCompAGMExecutive.AGMExecutive):
	def __init__(self, _handler):
		self.handler = _handler
	def broadcastModel(self, current=None):
		self.handler.broadcastModel()
	def broadcastPlan(self, current=None):
		self.handler.broadcastPlan()
	def activate(self, current=None):
		pass
	def deactivate(self, current=None):
		pass
	def reset(self, current=None):
		self.handler.reset()
	def setMission(self, target, current=None):
		print target
		self.handler.setMission(xmlModelParser.graphFromXML(target), avoidUpdate=True)
	def getData(self, current=None):
		return world, target, plan
	def world2agmgraph(self, target):
		ret = AGMModelConversion.fromIceToInternal_model(target, ignoreInvalidEdges=True)
		#ret = AGMGraph()
		#for node in target.nodes:
			#ret.addNode(0,0, node.nodeIdentifier, node.nodeType, attributes=node.attributes)
		#for edge in target.edges:
			#ret.addEdge(edge.a, edge.b, edge.edgeType)
		return ret

class AGMCommonBehaviorI (RoboCompAGMCommonBehavior.AGMCommonBehavior):
	def __init__(self, _handler):
		self.handler = _handler

class AGMAgentTopicI (RoboCompAGMAgent.AGMAgentTopic):
	def __init__(self, _handler):
		self.handler = _handler
	def structuralChange(self, modification, current=None):
		self.handler.structuralChange(modification)
	def symbolUpdated(self, nodeModification, current=None):
		self.handler.symbolUpdated(nodeModification)
	def edgeUpdated(self, edgeModification, current=None):
		self.handler.edgeUpdated(edgeModification)

from AGMExecutive_core import Executive


class Server (Ice.Application):
	def run (self, argv):
		status = 0
		try:
			self.shutdownOnInterrupt()

			# Get component's parameters from config file
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

			# Create the executive
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
			print 'AGENT configs:', agentConfigs
			for agent in agentConfigs:
				print 'Configuring ', agent
				proxy = self.communicator().getProperties().getProperty(agent)
				if len(proxy)>0:
					behavior_proxy = RoboCompAGMCommonBehavior.AGMCommonBehaviorPrx.uncheckedCast(self.communicator().stringToProxy(proxy))
					if not behavior_proxy:
						print agentConfigs
						print parameters.agents[i].c_str()
						print parameters.agents[i].c_str()
						print "Error loading behavior proxy!"
						sys.exit(1)
					executive.setAgent(agent,  behavior_proxy)
					print "Agent" , agent, "initialized ok"
				else:
					print 'Agent', agent, 'was not properly configured. Check config file'


			# Subscribe to AGMAgentTopic
			print 'Subscribing to AGMAgentTopic'
			print 'Subscribing to AGMAgentTopic'
			proxy = self.communicator().getProperties().getProperty( "IceStormProxy")
			topicManager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().stringToProxy(proxy))
			adapterT = self.communicator().createObjectAdapter("AGMAgentTopic")
			agentTopic = AGMAgentTopicI(executive)
			proxyT = adapterT.addWithUUID(agentTopic).ice_oneway()
			AGMAgentTopic_subscription = False
			while not AGMAgentTopic_subscription:
				try:
					topic = topicManager.retrieve("AGMAgentTopic")
					qos = {}
					topic.subscribeAndGetPublisher(qos, proxyT)
					adapterT.activate()
					AGMAgentTopic_subscription = True
				except IceStorm.NoSuchTopic:
					print "Error! No topic found! Sleeping for a while..."
					time.sleep(1)

			# Run executive thread
			print 'AGMExecutive initialization ok'
			#executive.start()

			print '-------------------------------------------------------------'
			print '----     R u n     A G M E x e c u t i v e,     r u n   -----'
			print '-------------------------------------------------------------'
			#executive.mutex.acquire()
			executive.updatePlan()
			#executive.mutex.release()
			self.shutdownOnInterrupt()
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



if __name__ == '__main__':
	params = copy.deepcopy(sys.argv)
	if len(params) > 1:
		if not params[1].startswith('--Ice.Config='):
			params[1] = '--Ice.Config=' + params[1]
	elif len(params) == 0:
		params.append('--Ice.Config=config')
	Server( ).main(params)
