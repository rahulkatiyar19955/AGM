#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------
#  -----  AGGLExecutiveClient  -----
#  -----------------------
#
#  A libre graph grammar drawing tool.
#
#    Copyright (C) 2012-2013 by Luis J. Manso
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
import sys, traceback, os, re, threading, time, string, math
# Qt interface
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *
#from PySide.Qt import *
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
		self.agmData = AGMFileData()
		self.lhsPainter = GraphDraw(self.ui.lhsParentWidget, self, "LHS")
		self.rhsPainter = GraphDraw(self.ui.rhsParentWidget, self, "RHS")
		self.timer = QTimer()
		self.tool = ''
		self.appearance = Appearance()
		self.connect(self.timer,                               SIGNAL('timeout()'),                                            self.draw)
		self.connect(self.ui.toolsList,                        SIGNAL('currentRowChanged(int)'),                               self.selectTool)

		self.timer.start(100)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)

	def draw(self):
		self.lhsPainter.update()
		self.rhsPainter.update()
		for r in range(len(self.agmData.agm.rules)):
			item = self.ui.rulesList.item(r)
			item.setText(self.agmData.agm.rules[r].name)
	def selectTool(self, tool):
		self.tool = str(self.ui.toolsList.item(tool).text())
	def changeFont(self):
		self.fontDialog.show()
	def changeAppearance(self):
		self.appearance.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	if len(sys.argv)>1:
		if len(sys.argv)>3:
			inputFile   = sys.argv[1]
			compileFlag = sys.argv[2]
			outputFile  = sys.argv[3]
			if compileFlag == '-c':
				agmData = AGMFileData.fromFile(inputFile, verbose=False)
				agmData.generatePDDL(outputFile)
		else:
			clase = AGMExecutiveClient(sys.argv[1])
			clase.show()
			app.exec_()
	else:
			clase = AGMExecutiveClient()
			clase.show()
			app.exec_()
