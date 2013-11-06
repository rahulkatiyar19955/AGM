#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------
#  -----  GraphViewer  -----
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


import Image, ImageOps
import numpy as np

from inspect import currentframe, getframeinfo

sys.path.append('/opt/robocomp/share')
from ui_guiGraphViewer import Ui_MainWindow
from ui_appearance import Ui_Appearance
from parseAGGL import *

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
global fontName
fontName = "Arial"
global fontSize
fontSize = 14


from AGMModule import *
import libxml2


class GraphViewer(QMainWindow):
	def __init__(self, fileList):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# Graph painters
		self.tool = 'Node - Move'
		self.connect(self.ui.actionChangeAppearance,           SIGNAL("triggered(bool)"),                                      self.changeAppearance)
		self.connect(self.ui.actionQuit,                       SIGNAL("triggered(bool)"),                                      self.appClose)
		self.drawers = []
		self.widgets = []

		
		global vertexDiameter
		global fontName
		global fontSize
		vertexDiameter = 45
		fontName = 'Arial 14'

		# Node appearance
		self.appearance = Appearance()
		self.appearance.ui.radius.setValue(vertexDiameter)

		# Font
		font = QFont(fontName, fontSize)
		font.setItalic(False)
		font.setItalic(False)
		self.fontDialog = QFontDialog(font, self)
		self.fontDialog.setCurrentFont(font)
		self.font = self.fontDialog.currentFont()
		self.connect(self.ui.actionChangeFont,                 SIGNAL("triggered(bool)"),                                      self.changeFont)

		self.resize(1200,700)
		for fil in range(len(fileList)):
			self.widgets.append(QWidget())
			self.widgets[fil].resize(1200/len(fileList), 700)
			self.widgets[fil].show()
			self.ui.horizontalLayout.addWidget(self.widgets[fil])
		for fil in range(len(fileList)):
			self.drawers.append(GraphDraw(self.widgets[fil], self, "xxxx"))
			self.drawers[fil].graph = self.graphFromXML(fileList[fil])
			self.drawers[fil].show()

		self.timer = QTimer()
		self.connect(self.timer, SIGNAL('timeout()'), self.draw)
		self.timer.start(100)

	def appClose(self):
		#if self.modified:
			#self.close()
		#else:
			#self.close()
		self.close()
	# Manages close events
	def closeEvent(self, closeevent):
		settings = QSettings("AGM", "mainWindowGeometry");
		g = self.saveGeometry()
		settings.setValue("geometry", g)

	def about(self):
		QMessageBox.information(self, "About", "Active Grammar-based Modeling:\nhttps://github.com/ljmanso/AGM/wiki")
	def draw(self):

		for d in self.drawers:
			d.update()

	def changePassive(self, passive):
		p = True
		if passive == Qt.Unchecked:
			p = False
		self.agmData.agm.rules[self.ui.rulesList.currentRow()].passive = p
	def selectTool(self, tool):
		self.tool = str(self.ui.toolsList.item(tool).text())
	def changeFont(self):
		self.fontDialog.show()
	def changeAppearance(self):
		self.appearance.show()
	def graphFromXML(self, path):
		# Initialize empty graph
		nodes = dict()
		links = list()
		# Open XML
		try:
			file = open(path, 'r')
		except:
			print 'Can\'t open ' + path + '.'
			return AGMGraph(dict(), list())
		data = file.read()
		xmldoc = libxml2.parseDoc(data)
		root = xmldoc.children
		if root is not None:
			nodes, links = self.parseRoot(root, nodes, links)
		xmldoc.freeDoc()
		return AGMGraph(nodes, links)
	def parseRoot(self, root, nodes, links):
		if root.type == "element" and root.name == "AGMModel":
			child = root.children
			while child is not None:
				if child.type == "element":
					if child.name == "symbol":
						nodes, links = self.parseSymbol(child, nodes, links)
					elif child.name == "link":
						nodes, links = self.parseLink(child, nodes, links)
					else:
						print "error: "+str(child.name)
				child = child.next
		return nodes, links
	def parseSymbol(self, root, nodes, links):
		if root.type == "element" and root.name == "symbol":
			# props
			child = root.children
			idens = self.parseSingleValue(root,   'id')
			types = self.parseSingleValue(root, 'type')
			x = 0
			xs = self.parseSingleValue(root, 'x', False)
			if xs != None:
				x = int(xs)
			y = 0
			ys = self.parseSingleValue(root, 'y', False)
			if ys != None:
				y = int(ys)
			nodes[idens] = AGMSymbol(idens, types, [int(x), int(y)])
			# children
			while child is not None:
				if child.type == "element":
					if child.name == "attribute":
						#parseAttribute(child, component)
						pass
					else:
						print 'boooooooooo'
				child = child.next
		else:
			print 'parseSymbol with no symbol element'
		return nodes, links
	def parseLink(self, root, nodes, links):
		if root.type == "element" and root.name == "link":
			# props
			child = root.children
			src = self.parseSingleValue(root, 'src')
			dst = self.parseSingleValue(root, 'dst')
			lab = self.parseSingleValue(root, 'label')
			links.append(AGMLink(src, dst, lab, True))
			# children
			while child is not None:
				if child.type == "element":
						print 'boooooooooo'
				child = child.next
		else:
			print 'parseLink with no link element'
		return nodes, links
	def parseSingleValue(self, node, arg, doCheck=True):
		if not node.hasProp(arg) and doCheck: print 'WARNING: ' + arg + ' attribute expected'
		else:
			ret = node.prop(arg)
			node.unsetProp(arg)
			return ret

if __name__ == '__main__':
	app = QApplication(sys.argv)
	if len(sys.argv)>1:
		clase = GraphViewer(sys.argv[1:])
		clase.show()
		app.exec_()
	else:
		print 'Usage:\n\t'+sys.argv[0]


