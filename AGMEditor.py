#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------
#  -----  AGMEditor  -----
#  -----------------------
#
#  A libre graph grammar drawing tool.
#
#    Copyright (C) 2011-2011 by Luis J. Manso
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyQt4.Qt import *
from ui_guiAGMEditor import Ui_MainWindow
from ui_appearance import Ui_Appearance

from parseAGM import *

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
	def __init__(self, parentw, main):
		QWidget.__init__(self, parentw)
		self.parentW = parentw
		self.main = main
		self.graph = AGMGraph(dict(), [])
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
	def paintOnPainter(self, painter, w, h):
		global vertexDiameter
		global nodeThickness
		w = float(w)
		h = float(h)
		w2 = w/2
		h2 = h/2
		painter.fillRect(QRectF(0, 0, w, h), Qt.white)
		painter.drawLine(QLine(0,   0, w-1,   0))
		painter.drawLine(QLine(0, h-1, w-1, h-1))
		painter.drawLine(QLine(0,   0, 0,   h-1))
		painter.drawLine(QLine(w-1, 0, w-1, h-1))
		pen = QPen()
		pen.setWidth(nodeThickness)
		painter.setPen(pen)
		brush = QBrush(QGradient.LinearGradient)
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
			painter.fillRect(QRectF(rect.x()-4, rect.y()-3, rect.width()+8, rect.height()+6), Qt.black)
			painter.fillRect(QRectF(rect.x()-2, rect.y()-1.5, rect.width()+4, rect.height()+3), Qt.white)
			painter.drawText(rect, align, str(e.linkType))
			painter.setBrush(QColor(0, 0, 0))
			vw = 0.5*vertexDiameter
			painter.drawPie(xend-vw/2, yend-vw/2, vw, vw, (-angleD-20)*16, 40*16)
	def mousePressEvent(self, e):
		global vertexDiameter
		if self.main.tool == 'Node - Add':
			self.graph.addNode(e.x(), e.y(), 'a', 'type')
		elif self.main.tool == 'Node - Remove':
			x, y = self.graph.getName(e.x(), e.y(), vertexDiameter)
			if x>=0:
				self.graph.removeNode(e.x(), e.y(), vertexDiameter)
			else:
				print 'No node'
			
		elif self.main.tool == 'Node - Rename':
			x, y = self.graph.getCenter(e.x(), e.y(), vertexDiameter)
			if x>=0:
				r = NodeNameReader(x, y, self)
				r.setFocus(Qt.OtherFocusReason)
			else:
				print 'No node'
		elif self.main.tool == 'Node - Change type':
			x, y = self.graph.getCenter(e.x(), e.y(), vertexDiameter)
			if x>=0:
				r = NodeTypeReader(x, y, self)
				r.setFocus(Qt.OtherFocusReason)
			else:
				print 'No node'
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
	def __init__(self):
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
		self.lhsPainter = GraphDraw(self.ui.lhsParentWidget, self)
		self.rhsPainter = GraphDraw(self.ui.rhsParentWidget, self)
		self.addRule()
		self.timer = QTimer()
		self.tool = ''
		self.appearance = Appearance()
		self.connect(self.timer,                           SIGNAL('timeout()'),              self.draw)
		self.connect(self.ui.toolsList,                    SIGNAL('currentRowChanged(int)'), self.selectTool)
		self.connect(self.ui.rulesList,                    SIGNAL('currentRowChanged(int)'), self.changeRule)
		self.connect(self.ui.actionChangeFont,             SIGNAL("triggered(bool)"),        self.changeFont)
		self.connect(self.ui.actionChangeAppearance,       SIGNAL("triggered(bool)"),        self.changeAppearance)
		self.connect(self.ui.actionAddRule,                SIGNAL("triggered(bool)"),        self.addRule)
		self.connect(self.ui.actionRemoveCurrentRule,      SIGNAL("triggered(bool)"),        self.removeCurrentRule)
		self.connect(self.ui.actionRenameCurrentRule,      SIGNAL("triggered(bool)"),        self.renameCurrentRule)
		self.connect(self.ui.actionExport,                 SIGNAL("triggered(bool)"),        self.exportRule)
		self.connect(self.ui.actionGenerateCode,           SIGNAL("triggered(bool)"),        self.generateCode)
		self.connect(self.ui.actionExportAllRules,         SIGNAL("triggered(bool)"),        self.exportAll)
		self.connect(self.ui.actionSave,                   SIGNAL("triggered(bool)"),        self.save)
		self.connect(self.ui.actionOpen,                   SIGNAL("triggered(bool)"),        self.open)
		self.connect(self.ui.actionQuit,                   SIGNAL("triggered(bool)"),        self.close)
		self.connect(self.ui.actionGraphmar,               SIGNAL("triggered(bool)"),        self.about)
		self.connect(self.ui.tabWidget,                    SIGNAL("currentChanged(int)"),    self.tabChanged)
		#self.connect(self.ui.addBehaviorButton,           SIGNAL("clicked()"),              self.newBehavior)
		self.connect(self.ui.tabWidget,                    SIGNAL("currentChanged(int)"),    self.tabChanged)
		self.connect(self.ui.actionNew_agent,              SIGNAL("triggered(bool)"),        self.newAgent)
		self.connect(self.ui.actionRemove_current_agent,   SIGNAL("triggered(bool)"),        self.removeCurrentAgent)
		self.connect(self.ui.actionNew_configuration,      SIGNAL("triggered(bool)"),        self.newConfig)
		self.connect(self.ui.actionRemove_current_config,  SIGNAL("triggered(bool)"),        self.removeCurrentConfig)
		self.timer.start(20)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.ui.toolsList.setCurrentRow(4)
		self.selectTool(4)
		self.tabChanged(self.ui.tabWidget.currentIndex())
	def newAgent(self, val):
		print 'newAgent', val
		pass
	def removeCurrentAgent(self, val):
		print 'remove agent', val
		pass
	def newConfig(self, val):
		print 'newConfig', val
		pass
	def removeCurrentConfig(self, val):
		print 'remove config', val
		pass
	def newBehavior(self):
		self.ui.behaviorListWidget.setAlternatingRowColors(True)
		#delegate = SpinBoxDelegate()
		#self.ui.behaviorListWidget.setItemDelegate(delegate)
		item1 = QListWidgetItem(self.ui.behaviorListWidget)
		item1.setText("new behavior")
		item1.setFlags(item1.flags() | Qt.ItemIsEditable)
	def tabChanged(self, index):
		if index == 0:
			self.ui.productionsWidget.show()
			self.ui.toolsWidget.show()
			self.ui.behaviorsWidget.show()
			self.ui.agentsDock.hide()
			self.ui.agentConfigurationsDock.hide()
			self.ui.menuRules.setEnabled(True)
			self.ui.menuBehaviors.setEnabled(False)
		elif index == 1:
			self.ui.productionsWidget.hide()
			self.ui.toolsWidget.hide()
			self.ui.behaviorsWidget.show()
			self.ui.agentsDock.show()
			self.ui.agentConfigurationsDock.show()
			self.ui.menuRules.setEnabled(False)
			self.ui.menuBehaviors.setEnabled(True)
		else:
			print 'Internal error: AGMEditor::tabChanged: Unknown tab index'
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
		self.ui.rulesList.addItem('Rule ' + str(len(self.agmData.agm.rules)))
		self.agmData.agm.addRule(AGMRule('new rule', AGMGraph(dict(), [], 'L'), AGMGraph(dict(), [], 'R')))
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
	def generateCode(self):
		print 'Generate'
	def exportRule(self):
		path = str(QFileDialog.getSaveFileName(self, "Export rule", "", "*.svg"))
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
			rule = self.rulesagmData.agm.rules[i]
			self.lhsPainter.graph = rule.lhs
			self.lhsPainter.export(str(path)+'/rule'+str(i)+'_lhs.svg')
			self.rhsPainter.graph = rule.rhs
			self.rhsPainter.export(str(path)+'/rule'+str(i)+'_rhs.svg')
		self.lhsPainter.graph = lhs
		self.rhsPainter.graph = rhs
	def open(self):
		path = str(QFileDialog.getOpenFileName(self, "Export rule", "", "*.agm"))
		self.openFromFile(path)
	def openFromFile(self, path):
		print 'Opening', path
		if path[-4:] != '.agm': path = path + '.agm'
		self.agmData = AGMFileDataParsing.fromFile(path, verbose=True)
		self.ui.rulesList.clear()
		for rule in self.agmData.agm.rules:
			q = QListWidgetItem()
			q.setText(rule.name)
			self.ui.rulesList.addItem(q)
		self.changeRule(0)
	def save(self):
		path = str(QFileDialog.getSaveFileName(self, "Save as", "", "*.agm"))
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
		self.agmData.toFile(path)

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
			clase = AGMEditor()
			clase.openFromFile(sys.argv[1])
			clase.show()
			app.exec_()
	else:
			clase = AGMEditor()
			clase.show()
			app.exec_()
