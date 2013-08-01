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


from AGMModule import *



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

		self.timer.start(100)
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

	def newAgent(self, val=True, name='', createAgent=True):
		self.ui.agentListWidget.setAlternatingRowColors(True)
		if name == '': name = self.agmData.agm.addUnnamedAgent()
		item1 = QListWidgetItem(self.ui.agentListWidget)
		item1.setText(name)
		self.agmData.agm.addAgent(name)
		self.redrawConfigurationTable()
		if createAgent:
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
	def generateTableFromUI(self):
		self.agmData.agm.table = []
		for r in range(self.ui.tableWidget.rowCount()):
			rowList = []
			for c in range(self.ui.tableWidget.columnCount()):
				combo = self.ui.tableWidget.cellWidget(r,c)
				rowList.append(combo.currentText())
			self.agmData.agm.table.append(rowList)

	def processTableAndDrawCombos(self):
		self.agmData.agm.table = self.agmData.listToTable(self.agmData.parsedTable, len(self.agmData.parsedAgents))
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
			self.newAgent(name=agent, createAgent=False)
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
