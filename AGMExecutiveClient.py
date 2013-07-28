#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ---------------------------------
#  -----  AGGLExecutiveClient  -----
#  ---------------------------------
#
#  A libre graph grammar drawing tool.
#
#    Copyright (C) 2013 by Luis J. Manso
#
#    Graphmar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Graphmar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Graphmar. If not, see <http://www.gnu.org/licenses/>.

# Python distribution imports
import sys, traceback, os, re, threading, time
import copy, string, math

# Qt interface
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *
from ui_guiAGMExecutiveClient import Ui_MainWindow
from ui_appearance import Ui_Appearance

from parseAGGL import *

import Ice, IceStorm

from inspect import currentframe, getframeinfo

from AGMModule import *

global vertexDiameter
vertexDiameter = 40
global nodeThickness
nodeThickness = 2.5
global lineThickness
lineThickness = 2.5
global longPattern
longPattern = 3
global shortPattern
shortPattern = 1
global spacePattern
spacePattern = 3
global dashPattern
dashPattern = []



def loadSliceFile(xxx):
	ROBOCOMP = ''
	try:
		ROBOCOMP = os.environ['ROBOCOMP']
	except:
		if len(ROBOCOMP)<1:
			print 'ROBOCOMP environment variable not set! Exiting.'
			sys.exit()

	sliceOpts = ''
	for directory in os.environ['SLICE_PATH'].split(";"):
		if len(directory)>0:
			sliceOpts = sliceOpts + ' -I' + directory + ' '
	sliceOpts = sliceOpts + ' -I. '
	sliceOpts = sliceOpts + ' -I' + ROBOCOMP + '/Interfaces '
	sliceOpts = sliceOpts + ' --all'

	try:
		#print '\nLooking in', ROBOCOMP+"/Interfaces"
		Ice.loadSlice(sliceOpts+" "+ROBOCOMP+'/Interfaces/'+xxx)
	except:
		found = False
		for p in os.environ['SLICE_PATH'].split(";"):
			#print '\nLooking in', p, type(p)
			Ice.loadSlice(sliceOpts+" "+p+xxx )
			found = True
			break
			#except:
				#pass
		if not found:
			print 'Couldn\'t load '+xxx+'. Verify that '+xxx+' is located in $ROBOCOM/Interfaces or $SLICE_PATH.'
			sys.exit()
			
loadSliceFile("GualzruExecutive.ice")
import RoboCompExecutive
loadSliceFile("GualzruBehavior.ice")
import RoboCompGualzruBehavior
print "\n\nModules imported successfully! (ignore previous errors)"

class AGMExecutiveClient(QMainWindow):
	def __init__(self, filePath=''):
		QMainWindow.__init__(self)
		
		self.ic = Ice.initialize(sys.argv)

		self.behaviorTopic = None
		try:
			obj = self.ic.stringToProxy("IceStorm/TopicManager:tcp -p 9999")
			topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
			topic = None
			while not topic:
				try:
					topic = topicManager.retrieve("GualzruBehavior")
				except:
					try:
						topic = topicManager.create("GualzruBehavior")
					except:
						pass
			pub = topic.getPublisher().ice_oneway()
			behaviorTopic = RoboCompGualzruBehavior.GualzruBehaviorTopicPrx.uncheckedCast(pub)
		except:
			print "Can't connect to IceStorm!"
			sys.exit(-1)
	
		# Remote object connection
		#try:
		basePrx = self.ic.stringToProxy("gualzruexecutive:tcp -h localhost -p 10198")
		self.executivePrx = RoboCompExecutive.ExecutivePrx.checkedCast(basePrx)
		#except:
			#print 'Cannot connect to the executive.'
			#return

		
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.toolsList.addItem('Node - Add')
		self.ui.toolsList.addItem('Node - Remove')
		self.ui.toolsList.addItem('Node - Rename')
		self.ui.toolsList.addItem('Node - Change type')
		self.ui.toolsList.addItem('Node - Move')
		self.ui.toolsList.addItem('Node - (Dis/En)able')
		self.ui.toolsList.addItem('Edge - Add')
		self.ui.toolsList.addItem('Edge - Remove')
		self.ui.toolsList.addItem('Edge - Rename')
		self.ui.toolsList.addItem('Edge - (Dis/En)able')
		self.ui.toolsList.addItem('Edge - Change type')
		self.fontDialog = QFontDialog(self)
		self.font = self.fontDialog.selectedFont()
		self.lhsPainter = GraphDraw(self.ui.lhsParentWidget, self, "LHS")
		self.rhsPainter = GraphDraw(self.ui.rhsParentWidget, self, "RHS")
		self.timer = QTimer()
		self.tool = ''
		self.appearance = Appearance()
		self.connect(self.timer,                          SIGNAL('timeout()'),              self.draw)
		self.connect(self.ui.toolsList,                   SIGNAL('currentRowChanged(int)'), self.selectTool)
		self.connect(self.ui.actionRefresh_current_model, SIGNAL("triggered(bool)"),        self.refreshModel)
		self.connect(self.ui.actionClear_proposal,        SIGNAL("triggered(bool)"),        self.clearProposal)
  		self.connect(self.ui.actionSend_proposal,         SIGNAL("triggered(bool)"),        self.sendProposal)
  
		self.timer.start(100)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)

	def draw(self):
		self.lhsPainter.update()
		self.rhsPainter.update()
	def selectTool(self, tool):
		self.tool = str(self.ui.toolsList.item(tool).text())
	def changeFont(self):
		self.fontDialog.show()
	def changeAppearance(self):
		self.appearance.show()
	def refreshModel(self):
		world, target, plan = self.executivePrx.getData()
		self.modelModified(world)
	def clearProposal(self):
		self.rhsPainter.graph = copy.deepcopy(self.lhsPainter.graph)
	def sendProposal(self):
		print 'sendProposal'

	def modelModified(self, newModel):
		print newModel

		self.lhsPainter.graph.links = list()
		self.lhsPainter.graph.nodes = dict()
		
		inte = 30
		for node in newModel.nodes:
			self.lhsPainter.graph.addNode(inte, inte, node.nodeIdentifier, node.nodeType)
			inte += 30
		for edge in newModel.edges:
			self.lhsPainter.graph.addEdge(edge.a, edge.b, edge.edgeType)
		inte = 0

		if len(self.rhsPainter.graph.nodes) == 0:
			self.rhsPainter.graph = copy.deepcopy(self.lhsPainter.graph)
		
	def modelUpdated(self, node):
		print node

class ExecutiveTopicI(RoboCompExecutive.ExecutiveTopic):
	def __init__(self, wk):
		RoboCompExecutive.ExecutiveTopic.__init__(self)
		self.worker = wk
	def modelModified(self, event, current):
		self.worker.modelModified(event.newModel)
	def modelUpdated(self, node, current):
		self.worker.modelUpdated(node)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	clase = AGMExecutiveClient()

	obj = clase.ic.stringToProxy("IceStorm/TopicManager:tcp -p 9999")

	topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
	adapterT = clase.ic.createObjectAdapterWithEndpoints("ExecutiveTopic", "tcp -p 12201")

	executiveTopic = ExecutiveTopicI(clase)
	proxyT = adapterT.addWithUUID(executiveTopic).ice_oneway()
	topic = None
	try:
		topic = topicManager.retrieve("ExecutiveTopic")
		qos = None
		topic.subscribeAndGetPublisher(qos, proxyT)
	except:
		print "Error! No topic found!\n"
	adapterT.activate()

	print 'aaa'

	clase.show()
	app.exec_()
