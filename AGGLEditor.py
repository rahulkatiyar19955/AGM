#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------
#  -----  AGGLEditor  -----
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
from ui_guiAGGLEditor import Ui_MainWindow
from ui_appearance import Ui_Appearance

from parseAGGL import *


from inspect import currentframe, getframeinfo


# Code generator
#from cogapp import Cog


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


def distance(x, y, x2, y2):
	return math.sqrt(pow(float(x)-float(x2), 2) + pow(float(y)-float(y2), 2))

class NodeNameReader(QLineEdit):
	def __init__(self, x, y, parent):
		QLineEdit.__init__(self, parent)
		self.resize(100, 32)
		self.move(x-50, y-16)
		self.show()
		self.x = x
		self.y = y
		self.parentW = parent
		self.connect(self, SIGNAL('returnPressed()'), self.got)
	def got(self):
		ty = ''
		newName = str(self.text())
		bacName = ''
		pos = []
		for v in self.parentW.graph.nodes.keys():
			if self.parentW.graph.nodes[v].pos[0] == self.x:
				if self.parentW.graph.nodes[v].pos[1] == self.y:
					ty = self.parentW.graph.nodes[v].sType
					bacName = self.parentW.graph.nodes[v].name
					pos = self.parentW.graph.nodes[bacName].pos
					del self.parentW.graph.nodes[bacName]
					self.parentW.graph.nodes[newName] = AGMSymbol(newName, ty, pos)
		self.hide()
		self.close()

class NodeTypeReader(QLineEdit):
	def __init__(self, x, y, parent):
		QLineEdit.__init__(self, parent)
		self.resize(100, 32)
		self.move(x-50, y-16)
		self.show()
		self.x = x
		self.y = y
		self.parentW = parent
		self.connect(self, SIGNAL('returnPressed()'), self.got)
	def got(self):
		for v in self.parentW.graph.nodes.keys():
			try:
				if self.parentW.graph.nodes[v].pos[0] == self.x:
					if self.parentW.graph.nodes[v].pos[1] == self.y:
						self.parentW.graph.nodes[v].sType = str(self.text())
			except:
				pass
		self.hide()
		self.close()

class RuleRenamer(QLineEdit):
	def __init__(self, x, y, rule, widget):
		QLineEdit.__init__(self, widget)
		self.resize(200, 40)
		self.move(50, 50)
		self.x = x
		self.y = y
		self.rule = rule
		self.connect(self, SIGNAL('returnPressed()'), self.got)
		self.setWindowTitle("Type new name")
		self.show()
	def got(self):
		self.rule.name = self.text()
		self.hide()
		self.close()


class GraphDraw(QWidget):
	def __init__(self, parentw, main, name=''):
		self.name = name
		QWidget.__init__(self, parentw)
		self.parentW = parentw
		self.main = main
		self.graph = AGMGraph()
		self.pressName = -1
		self.releaseName = -1
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.move(0,0)
		self.show()
	def paintEvent(self, event=None):
		if self.size() != self.parentW.size():
			self.resize(self.parentW.size())
		self.painter = QPainter(self)
		self.painter.setRenderHint(QPainter.Antialiasing, True)
		self.paintOnPainter(self.painter, self.size().width(), self.size().height())
		self.painter = None
	def export(self, path):
		generator = QSvgGenerator()
		generator.setFileName(path)
		generator.setSize(self.size());
		generator.setViewBox(QRect(0, 0, self.size().width(), self.size().height()))
		generator.setTitle("PyQtSVNGenerator")
		generator.setDescription("SVG generated using Qt+Python")
		svgPainter = QPainter()
		svgPainter.begin(generator)
		self.paintOnPainter(svgPainter, self.size().width()*5, self.size().height()*5, drawlines=False)
		svgPainter.end()

	def exportPNG(self, path):
		pixmap = QPixmap(self.size())
		painter = QPainter(pixmap)
		#painter.begin()
		self.paintOnPainter(painter, self.size().width()*5, self.size().height()*5, drawlines=False)
		painter.end()
		pixmap.save(path, "png")
		

	def paintOnPainter(self, painter, w, h, drawlines=True):
		global vertexDiameter
		global nodeThickness
		w = float(w)
		h = float(h)
		w2 = w/2
		h2 = h/2
		painter.fillRect(QRectF(0, 0, w, h), Qt.white)
		if drawlines:
			painter.drawLine(QLine(0,   0, w-1,   0))
			painter.drawLine(QLine(0, h-1, w-1, h-1))
			painter.drawLine(QLine(0,   0, 0,   h-1))
			painter.drawLine(QLine(w-1, 0, w-1, h-1))
		pen = QPen()
		pen.setWidth(nodeThickness)
		painter.setPen(pen)
		brush = QBrush(QLinearGradient())
		painter.setBrush(brush)
		painter.setFont(self.main.fontDialog.selectedFont())
		for w in self.graph.nodes:
			v = self.graph.nodes[w]
			grid = 10
			if v.pos[0] % grid > grid/2:
				v.pos[0] = v.pos[0] + grid - (v.pos[0] % grid)
			else:
				v.pos[0] = v.pos[0] - (v.pos[0] % grid)
			if v.pos[0] % grid > grid/2:
				v.pos[0] = v.pos[1] + grid - (v.pos[1] % grid)
			else:
				v.pos[1] = v.pos[1] - (v.pos[1] % grid)
			if True:#v.enabled:
				painter.setBrush(QBrush())
			else:
				painter.setBrush(QColor(120, 120, 120, 255))
			# Draw node
			painter.drawEllipse(v.pos[0]-(vertexDiameter/2), v.pos[1]-(vertexDiameter/2), vertexDiameter, vertexDiameter)
			# Temp
			align = Qt.AlignLeft
			# Draw identifier
			rect = painter.boundingRect(QRectF(float(v.pos[0]), float(v.pos[1]), 1, 1), align, str(v.name))
			rect.translate(-rect.width()/2, -rect.height())
			painter.drawText(rect, align, str(v.name))
			# Draw type
			rect = painter.boundingRect(QRectF(float(v.pos[0]), float(v.pos[1]), 1, 1), align, str(v.sType))
			rect.translate(-rect.width()/2, 0)
			painter.drawText(rect, align, str(v.sType))
		linkindex = 0
		for linkindex in range(len(self.graph.links)):
			e = self.graph.links[linkindex]
			v1 = self.graph.nodes[e.a]
			v2 = self.graph.nodes[e.b]
			pos = 0
			linkGroupCount = 0
			for linkindex2 in range(len(self.graph.links)):
				lp = self.graph.links[linkindex2]
				if e.a == lp.a and e.b == lp.b:
					if linkindex == linkindex2: pos = int(linkGroupCount)
					linkGroupCount = linkGroupCount + 1
			angleR = math.atan2(v1.pos[1]-v2.pos[1], v1.pos[0]-v2.pos[0])
			angleD = angleR*(57.2957795)
			xinc = v2.pos[0] - v1.pos[0]
			yinc = v2.pos[1] - v1.pos[1]
			xinit = v1.pos[0]-math.cos(angleR)*(vertexDiameter/2)+1
			yinit = v1.pos[1]-math.sin(angleR)*(vertexDiameter/2)+1
			xend = v2.pos[0]+math.cos(angleR)*(vertexDiameter/2)
			yend = v2.pos[1]+math.sin(angleR)*(vertexDiameter/2)

			global lineThickness
			if e.enabled:
				pen = QPen(QColor(0, 0, 0))
				pen.setStyle(Qt.SolidLine)
				pen.setWidth(lineThickness)
				painter.setPen(pen)
				painter.setBrush(QColor(0, 0, 0))
			else:
				pen = QPen(QColor(255, 0, 0))
				global dashPattern
				pen.setDashPattern(dashPattern)
				pen.setWidth(lineThickness)
				painter.setPen(pen)
				painter.setBrush(QColor(255, 0, 0))
			painter.drawLine(xinit, yinit, xend, yend)


			vw2 = 0.125*vertexDiameter
			lpos1 = [(xinit + xend)/2, (yinit + yend) / 2]
			langle = math.atan2(yend-yinit, xend-xinit)
			lpos  = [lpos1[0]-vw2*math.cos(langle), lpos1[1]-vw2*math.sin(langle)]
			align = Qt.AlignLeft
			rect = painter.boundingRect(QRectF(float(lpos[0]), float(lpos[1]), 1, 1), align, str(e.linkType))
			rect.translate(-rect.width()/2, -rect.height()/2) # Right now it will be centered on the link's center
			linkHeight = rect.height()+6
			linkGroupBase = (-linkGroupCount+1)*linkHeight/2
			rect.translate(0, linkHeight*pos + linkGroupBase) # Right now it will be centered on the link's center

			painter.setBrush(QColor(255, 255, 255))
			d = 2
			painter.fillRect(QRectF(rect.x()-4+d, rect.y()-3, rect.width()+8, rect.height()+6), Qt.black)
			painter.fillRect(QRectF(rect.x()-2+d, rect.y()-1.5, rect.width()+4, rect.height()+3), Qt.white)
			painter.drawText(rect, align, str(e.linkType))
			painter.setBrush(QColor(0, 0, 0))
			vw = 0.5*vertexDiameter
			painter.drawPie(xend-vw/2, yend-vw/2, vw, vw, (-angleD-20)*16, 40*16)
	def mousePressEvent(self, e):
		global vertexDiameter
		if self.main.tool == 'Node - Add':
			try:
				self.lastNumber
			except:
				self.lastNumber = 1
			self.graph.addNode(e.x(), e.y(), 'newid'+str(self.lastNumber)+self.name, 'type')
			self.lastNumber +=1
			
		elif self.main.tool == 'Node - Remove':
			x, y = self.graph.getName(e.x(), e.y(), vertexDiameter)
			if x>=0:
				self.graph.removeNode(e.x(), e.y(), vertexDiameter)

		elif self.main.tool == 'Node - Rename':
			x, y = self.graph.getCenter(e.x(), e.y(), vertexDiameter)
			if x>=0:
				r = NodeNameReader(x, y, self)
				r.setFocus(Qt.OtherFocusReason)
		elif self.main.tool == 'Node - Change type':
			x, y = self.graph.getCenter(e.x(), e.y(), vertexDiameter)
			if x>=0:
				r = NodeTypeReader(x, y, self)
				r.setFocus(Qt.OtherFocusReason)
		elif self.main.tool == 'Node - Move':
			self.pressName, found = self.graph.getName(e.x(), e.y(), 100)
			if not found: self.pressName = ''
		elif self.main.tool == 'Node - (Dis/En)able':
			self.graph.switchNode(e.x(), e.y())
		elif self.main.tool == 'Edge - Add':
			self.pressName, found = self.graph.getName(e.x(), e.y(), vertexDiameter)
			if not found: self.pressName = ''
		elif self.main.tool == 'Edge - Remove':
			self.graph.removeEdge(e.x(), e.y())
		elif self.main.tool == 'Edge - Rename':
			self.graph.renameEdge(e.x(), e.y(), newName)
		elif self.main.tool == 'Edge - (Dis/En)able':
			self.edgeSwitchA = self.graph.getName(e.x(), e.y(), vertexDiameter)
	def mouseReleaseEvent(self, e):
		if self.main.tool == 'Node - Add':
			pass
		elif self.main.tool == 'Node - Remove':
			pass
		elif self.main.tool == 'Node - Rename':
			pass
		elif self.main.tool == 'Node - Change type':
			pass
		elif self.main.tool == 'Node - Move':
			global vertexDiameter
			self.graph.moveNode(self.pressName, e.x(), e.y(), vertexDiameter)
		elif self.main.tool == 'Node - (Dis/En)able':
			pass
		elif self.main.tool == 'Edge - Add':
			self.releaseName, found = self.graph.getName(e.x(), e.y(), vertexDiameter)
			if not found: self.releaseName = ''
			if self.pressName != '' and self.releaseName != '':
				self.graph.addEdge(self.pressName, self.releaseName)
		elif self.main.tool == 'Edge - Remove':
			pass
		elif self.main.tool == 'Edge - Rename':
			pass
		elif self.main.tool == 'Edge - (Dis/En)able':
			self.edgeSwitchB = self.graph.getName(e.x(), e.y(), vertexDiameter)
			for e in self.graph.edges:
				if (e.a==self.edgeSwitchA and e.b==self.edgeSwitchB) or (e.a==self.edgeSwitchB and e.b==self.edgeSwitchA):
					e.enabled = not e.enabled
	def mouseMoveEvent(self, e):
		global vertexDiameter
		if self.main.tool == 'Node - Move':
			self.graph.moveNode(self.pressName, e.x(), e.y(), vertexDiameter)

class Appearance(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.ui = Ui_Appearance()
		self.ui.setupUi(self)
		global vertexDiameter
		self.ui.radius.setValue(34)
		global nodeThickness
		self.ui.nodeThickness.setValue(nodeThickness)
		global lineThickness
		self.ui.lineThickness.setValue(lineThickness)
		global longPattern
		self.ui.longPattern.setValue(longPattern)
		global shortPattern
		self.ui.shortPattern.setValue(shortPattern)
		global spacePattern
		self.ui.spacePattern.setValue(spacePattern)
		self.connect(self.ui.okButton,      SIGNAL('clicked()'),         self.okClicked)
		self.connect(self.ui.nodeThickness, SIGNAL('valueChanged(int)'), self.commit)
		self.connect(self.ui.lineThickness, SIGNAL('valueChanged(int)'), self.commit)
		self.connect(self.ui.radius,        SIGNAL('valueChanged(int)'), self.commit)
		self.connect(self.ui.shortPattern,  SIGNAL('valueChanged(int)'), self.commit)
		self.connect(self.ui.longPattern,   SIGNAL('valueChanged(int)'), self.commit)
		self.connect(self.ui.spacePattern,  SIGNAL('valueChanged(int)'), self.commit)
		self.commit()
	def okClicked(self):
		self.commit()
		self.hide()
	def commit(self):
		global vertexDiameter
		vertexDiameter = self.ui.radius.value()*2
		global nodeThickness
		nodeThickness = self.ui.nodeThickness.value()
		global lineThickness
		lineThickness = self.ui.lineThickness.value()
		global dashPattern
		dashPattern = []
		dashPattern.append(self.ui.longPattern.value()  * lineThickness)
		dashPattern.append(self.ui.spacePattern.value() * lineThickness)
		dashPattern.append(self.ui.shortPattern.value() * lineThickness)
		dashPattern.append(self.ui.spacePattern.value() * lineThickness)


class AGMEditor(QMainWindow):
	def __init__(self, filePath=''):
		QMainWindow.__init__(self)
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
		self.connect(self.ui.rulesList,                        SIGNAL('currentRowChanged(int)'),                               self.changeRule)
		self.connect(self.ui.configurationListWidget,          SIGNAL('currentRowChanged(int)'),                               self.changeConfig)
		self.connect(self.ui.actionChangeFont,                 SIGNAL("triggered(bool)"),                                      self.changeFont)
		self.connect(self.ui.actionChangeAppearance,           SIGNAL("triggered(bool)"),                                      self.changeAppearance)
		self.connect(self.ui.actionAddRule,                    SIGNAL("triggered(bool)"),                                      self.addRule)
		self.connect(self.ui.actionRemoveCurrentRule,          SIGNAL("triggered(bool)"),                                      self.removeCurrentRule)
		self.connect(self.ui.actionRenameCurrentRule,          SIGNAL("triggered(bool)"),                                      self.renameCurrentRule)
		self.connect(self.ui.actionExport,                     SIGNAL("triggered(bool)"),                                      self.exportRule)
		self.connect(self.ui.actionGenerateCode,               SIGNAL("triggered(bool)"),                                      self.generateCode)
		self.connect(self.ui.actionExportAllRules,             SIGNAL("triggered(bool)"),                                      self.exportAll)
		self.connect(self.ui.actionExportAllRulesPNG,          SIGNAL("triggered(bool)"),                                      self.exportAllPNG)
		self.connect(self.ui.actionSave,                       SIGNAL("triggered(bool)"),                                      self.save)
		self.connect(self.ui.actionOpen,                       SIGNAL("triggered(bool)"),                                      self.open)
		self.connect(self.ui.actionQuit,                       SIGNAL("triggered(bool)"),                                      self.close)
		self.connect(self.ui.actionGraphmar,                   SIGNAL("triggered(bool)"),                                      self.about)
		self.connect(self.ui.tabWidget,                        SIGNAL("currentChanged(int)"),                                  self.tabChanged)
		self.connect(self.ui.actionNew_agent,                  SIGNAL("triggered(bool)"),                                      self.newAgent)
		self.connect(self.ui.actionRemove_current_agent,       SIGNAL("triggered(bool)"),                                      self.removeCurrentAgent)
		self.connect(self.ui.actionNew_configuration,          SIGNAL("triggered(bool)"),                                      self.newConfig)
		self.connect(self.ui.actionRemove_current_config,      SIGNAL("triggered(bool)"),                                      self.removeCurrentConfig)
		self.connect(self.ui.actionNew_agent_state,            SIGNAL("triggered(bool)"),                                      self.newAgentState)
		self.connect(self.ui.actionRemove_current_agent_state, SIGNAL("triggered(bool)"),                                      self.removeCurrentAgentState)

		self.timer.start(20)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.tabChanged(self.ui.tabWidget.currentIndex())
		
		if len(filePath)>0:
			self.openFromFile(filePath)
		else:
			self.addRule()
			frameinfo = getframeinfo(currentframe())
			self.newConfig(val=True)
			frameinfo = getframeinfo(currentframe())
			self.newAgent(True)
		self.ui.rulesList.setCurrentRow(0)
	def redrawConfigurationTable(self, b=None, re=True):
		self.ui.tableWidget.setRowCount(len(self.agmData.agm.configurations))
		self.ui.tableWidget.setColumnCount(len(self.agmData.agm.agents))
		count = 0
		for config in self.agmData.agm.configurationList:
			self.ui.tableWidget.setVerticalHeaderItem(count, QTableWidgetItem(config))
			count+=1
		count = 0
		for agent in self.agmData.agm.agentList:
			self.ui.tableWidget.setHorizontalHeaderItem(count, QTableWidgetItem(agent))
			count+=1
		self.ui.tableWidget.resizeColumnsToContents()

	def newConfig(self, val=True, config=''):
		#self.ui.configurationListWidget.setAlternatingRowColors(True)
		if config == '':
			config = self.agmData.agm.addUnnamedConfiguration()
		elif type(config) == type(''):
			config = AGMConfiguration(config)
			self.agmData.agm.addConfiguration(config)
		else:
			self.agmData.agm.addConfiguration(config)
		item1 = QListWidgetItem(self.ui.configurationListWidget)
		item1.setText(config.name)
		self.redrawConfigurationTable()
		for r in range(self.ui.tableWidget.rowCount()):
			if self.ui.tableWidget.verticalHeaderItem(r).text() == config.name:
				for c in range(self.ui.tableWidget.columnCount()):
					combo = QComboBox()
					agent = self.agmData.agm.agents[self.agmData.agm.agentList[c]]
					for s in agent.states:
						combo.addItem(s.name)
					self.ui.tableWidget.setCellWidget(r,c,combo)

	def newAgent(self, val=True, name=''):
		self.ui.agentListWidget.setAlternatingRowColors(True)
		if name == '': name = self.agmData.agm.addUnnamedAgent()
		item1 = QListWidgetItem(self.ui.agentListWidget)
		item1.setText(name)
		self.agmData.agm.addAgent(name)
		self.redrawConfigurationTable()
		self.newAgentState(agentName=name)

	def newAgentState(self, val=True, agentName='', stateName=''):
		if agentName == '':
			try:
				agentName = str(self.ui.agentListWidget.currentItem().text())
			except:
				return
		agent = self.agmData.agm.agents[agentName]
		if stateName == '':
			stateName = self.agmData.agm.addUnnamedAgentState(agentName)
		else:
			self.agmData.agm.addAgentState(agentName, AGMAgentState(stateName, agentName))
		for c in range(self.ui.tableWidget.columnCount()):
			if self.ui.tableWidget.horizontalHeaderItem(c).text() == agentName:
				for r in range(self.ui.tableWidget.rowCount()):
					combo = QComboBox()
					for s in agent.states:
						combo.addItem(s.name)
					self.ui.tableWidget.setCellWidget(r,c,combo)
		self.ui.tableWidget.resizeColumnsToContents()
		#return
		self.redrawConfigurationTable()
	def listToTable(self, l, n):
		t =  [l[i:i+n] for i in range(0, len(l), n)]
		length = None
		for i in t:
			if length == None:
				length = len(t)
			else:
				assert len(t) == length, "not squared table"
		return t
	def generateTableFromUI(self):
		self.agmData.agm.table = []
		for r in range(self.ui.tableWidget.rowCount()):
			rowList = []
			for c in range(self.ui.tableWidget.columnCount()):
				combo = self.ui.tableWidget.cellWidget(r,c)
				rowList.append(combo.currentText())
			self.agmData.agm.table.append(rowList)

	def processTableAndDrawCombos(self):
		self.agmData.agm.table = self.listToTable(self.agmData.parsedTable, len(self.agmData.parsedAgents))
		rows = len(self.agmData.agm.table)
		cols = len(self.agmData.agm.table[0])
		assert rows == len(self.agmData.agm.configurations), "the size of the table ("+str(rows)+") does not match with the number of configurations ("+str(len(self.agmData.agm.configurations))+")"
		assert cols == len(self.agmData.agm.agents), "the size of the table does not match with the number of agents"

		conf=0
		for c in self.agmData.agm.configurationList:
			conf += 1
		for agentName in self.agmData.agm.agentList:
			cols = self.ui.tableWidget.columnCount()
			for i in range(cols):
				if self.ui.tableWidget.horizontalHeaderItem(i).text() == agentName:
					rows = self.ui.tableWidget.rowCount()
					for r in range(rows):
						combo = QComboBox()
						for s in self.agmData.agm.agents[agentName].states:
							combo.addItem(s.name)
						self.ui.tableWidget.setCellWidget(r,i,combo)
			self.ui.tableWidget.resizeColumnsToContents()

		for agent in self.agmData.agm.agentList:
			# Find which column corresponds to the current agent: c
			c = -1
			for ag in range(len(self.agmData.agm.agentList)):
				if self.ui.tableWidget.horizontalHeaderItem(ag).text() == agent:
					c = ag
			assert c != -1, "wrooooooong"
			# Valid state nanmes for agent
			validStateNames = self.agmData.agm.agents[agent].validStateNames()
			for i in range(len(self.agmData.agm.configurations)):
				assert self.agmData.agm.table[i][c] in validStateNames, "invalid state name ("+self.agmData.agm.table[i][c]+") for row "+str(i)+" column "+str(c)+" for agent "+agent
				item = self.ui.tableWidget.cellWidget(i,c)
				idx = item.findText(self.agmData.agm.table[i][c])
				self.ui.tableWidget.cellWidget(i,c).setCurrentIndex(idx)


	def removeCurrentAgentState(self, val):
		self.redrawConfigurationTable()
	def removeCurrentAgent(self, val):
		self.redrawConfigurationTable()
	def removeCurrentConfig(self, val):
		self.redrawConfigurationTable()


	def tabChanged(self, index):
		if index == 0:
			self.ui.productionsWidget.show()
			self.ui.toolsWidget.show()
			self.ui.behaviorsWidget.show()
			self.ui.agentsDock.hide()
			self.ui.menuRules.setEnabled(True)
			self.ui.menuBehaviors.setEnabled(False)
		elif index == 1:
			self.ui.productionsWidget.hide()
			self.ui.toolsWidget.hide()
			self.ui.behaviorsWidget.hide()
			self.ui.agentsDock.show()
			self.ui.menuRules.setEnabled(False)
			self.ui.menuBehaviors.setEnabled(True)
		else:
			print 'Internal error: AGGLEditor::tabChanged: Unknown tab index'
	def about(self):
		QMessageBox.information(self, "About", "Active Grammar-based Modeling:\nhttps://github.com/ljmanso/AGM/wiki")
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
	def addRule(self):
		ddd = 'rule' + str(len(self.agmData.agm.rules))
		self.ui.rulesList.addItem(ddd)
		l = AGMGraph(side='L')
		r = AGMGraph(side='R')
		self.agmData.agm.addRule(AGMRule(ddd, AGMConfiguration(''), l, r))
	def removeCurrentRule(self):
		pos = self.ui.rulesList.currentRow()
		self.agmData.agm.rules = self.agmData.agm.rules[:pos] + self.agmData.agm.rules[pos+1:]
		self.ui.rulesList.takeItem(pos)
	def renameCurrentRule(self):
		pos = self.ui.rulesList.currentRow()
		r = RuleRenamer(self.width()/2, self.height()/2, self.agmData.agm.rules[pos], self)
		r.setFocus(Qt.OtherFocusReason)
	def changeRule(self, ruleN):
		self.lhsPainter.graph = self.agmData.agm.rules[ruleN].lhs
		self.rhsPainter.graph = self.agmData.agm.rules[ruleN].rhs
		currRule = self.ui.rulesList.currentItem().text()
		currConf = self.agmData.agm.getConfigRule(currRule)
		found = -1
		if currConf != None:
			for l in range(self.ui.configurationListWidget.count()):
				itemText = self.ui.configurationListWidget.item(l).text()
				confName = currConf.name
				if itemText == confName:
					found = l
					break
		if currConf!=None:
			if found == -1 and self.ui.configurationListWidget.count() > 0 and currConf.name != '':
				sys.exit(1)
		if found > -1:
			self.ui.configurationListWidget.setCurrentRow(found)
	def changeConfig(self, configN):
		currRule = self.ui.rulesList.currentItem().text()
		currConf = self.ui.configurationListWidget.currentItem().text()
		self.agmData.agm.setConfigRule(currRule, currConf)
	def generateCode(self):
		path_pddl = QFileDialog.getSaveFileName(self, "Save as", "", "*.pddl")[0]
		self.agmData.generatePDDL(path_pddl)
		path_agmbd = QFileDialog.getSaveFileName(self, "Save as", "", "*.agmbd")[0]
		self.agmData.generateAGMBehaviorDescription(path_agmbd)
	def exportRule(self):
		path = str(QFileDialog.getSaveFileName(self, "Export rule", "", "*"))
		if path[-4:] == '.svg': path = path[:-4]
		pathLHS = path + 'LHS.png'
		self.lhsPainter.export(pathLHS)
		pathRHS = path + 'RHS.png'
		self.rhsPainter.export(pathRHS)
	def exportAll(self):
		path = str(QFileDialog.getExistingDirectory(self, "Export all rules", ""))
		lhs = self.lhsPainter.graph
		rhs = self.rhsPainter.graph
		for i in range(len(self.agmData.agm.rules)):
			rule = self.agmData.agm.rules[i]
			self.lhsPainter.graph = rule.lhs
			self.lhsPainter.export(str(path)+'/rule'+str(i)+'_lhs.svg')
			self.rhsPainter.graph = rule.rhs
			self.rhsPainter.export(str(path)+'/rule'+str(i)+'_rhs.svg')
		self.lhsPainter.graph = lhs
		self.rhsPainter.graph = rhs
	def exportAllPNG (self):
		path = str(QFileDialog.getExistingDirectory(self, "Export all rules", ""))
		lhs = self.lhsPainter.graph
		rhs = self.rhsPainter.graph
		for i in range(len(self.agmData.agm.rules)):
			rule = self.agmData.agm.rules[i]
			self.lhsPainter.graph = rule.lhs
			self.lhsPainter.exportPNG(str(path)+'/rule'+str(i)+'_lhs.png')
			self.rhsPainter.graph = rule.rhs
			self.rhsPainter.exportPNG(str(path)+'/rule'+str(i)+'_rhs.png')
		self.lhsPainter.graph = lhs
		self.rhsPainter.graph = rhs
	def open(self):
		path = str(QFileDialog.getOpenFileName(self, "Export rule", "", "*.aggl")[0])
		self.openFromFile(path)
	def openFromFile(self, path):
		if path[-5:] != '.aggl': path = path + '.aggl'
		self.agmData = AGMFileDataParsing.fromFile(path, verbose=True)
		# Include parsed agents
		for agent in self.agmData.parsedAgents:
			self.newAgent(name=agent)
			for state in self.agmData.parsedAgents[agent]:
				self.newAgentState(agentName=agent, stateName=state)
		# Include pared configurations
		for config in self.agmData.parsedConfigurations:
			self.newConfig(config=config)

		self.processTableAndDrawCombos()

		self.ui.rulesList.clear()
		for rule in self.agmData.agm.rules:
			q = QListWidgetItem()
			q.setText(rule.name)
			self.ui.rulesList.addItem(q)
		#self.changeRule(0)
		self.redrawConfigurationTable()
	def save(self):
		path = QFileDialog.getSaveFileName(self, "Save as", "", "*.aggl")[0]
		self.agmData.properties['name'] = path.split('/')[-1].split('.')[0]
		global vertexDiameter
		self.agmData.properties['vertexDiameter'] = vertexDiameter
		global nodeThickness
		self.agmData.properties['nodeThickness'] = nodeThickness
		global lineThickness
		self.agmData.properties['lineThickness'] = lineThickness
		global longPattern
		self.agmData.properties['longPattern'] = longPattern
		global shortPattern
		self.agmData.properties['shortPattern'] = shortPattern
		global spacePattern
		self.agmData.properties['spacePattern'] = spacePattern
	
		self.agmData.tableString = self.setTableStringForAGMData()

		self.agmData.toFile(path)

	def setTableStringForAGMData(self):
		writeString = 'table\n'
		writeString += '{\n'
		for r in range(self.ui.tableWidget.rowCount()):
			for c in range(self.ui.tableWidget.columnCount()):
				writeString += ' ' + self.ui.tableWidget.cellWidget(r, c).currentText()
			writeString += '\n'
		writeString += '}\n'
		return writeString

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
			clase = AGMEditor(sys.argv[1])
			clase.show()
			app.exec_()
	else:
			clase = AGMEditor()
			clase.show()
			app.exec_()
