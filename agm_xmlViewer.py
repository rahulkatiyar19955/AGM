#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import numpy as np

from inspect import currentframe, getframeinfo

import AGGL

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



class GraphViewer(QWidget):
	def __init__(self, fileList):
		QWidget.__init__(self)
		self.layout = QHBoxLayout(self)
		self.drawers = []
		self.widgets = []
		font = QFont("Helvetica [Cronyx]", 12)
		self.fontDialog = QFontDialog(font, self)
		self.fontDialog.setCurrentFont(font)
		self.font = self.fontDialog.currentFont()

		self.resize(1200,700)
		for fil in range(len(fileList)):
			self.widgets.append(QWidget())
			self.widgets[fil].resize(1200/len(fileList), 700)
			self.widgets[fil].show()
			self.layout.addWidget(self.widgets[fil])
		for fil in range(len(fileList)):
			self.drawers.append(GraphDraw(self.widgets[fil], self, "xxxx"))
			self.drawers[fil].graph = self.graphFromXML(fileList[fil])
			self.drawers[fil].show()
		self.timer = QTimer()
		self.connect(self.timer, SIGNAL('timeout()'), self.draw)
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
		if node.type == "element" and node.name == "AGMModel":
			child = root.children
			while child is not None:
				if child.type == "element":
					if child.name == "symbol":
						nodes, links = parseSymbol(child, nodes, links)
					elif child.name == "link":
						nodes, links = parseLink(child, nodes, links)
				child = child.next
		return nodes, links
	def parseNode(self, root, nodes, links):
		if node.type == "element" and node.name == "symbol":
			child = root.children
			component = CompInfo()
			component.alias = parseSingleValue(node, 'alias', False)
			component.endpoint = parseSingleValue(node, 'endpoint', False)
			mandatory = 0
			block_optional = 0
			while child is not None:
				if child.type == "element":
					if child.name == "workingDir":
						parseWorkingDir(child, component)
						mandatory = mandatory + 1
					elif child.name == "upCommand":
						parseUpCommand(child, component)
						mandatory = mandatory + 2
			child = child.next
			components.append(component
		return nodes, links
		#nodes[t.symbol] = AGMSymbol(t.symbol, t.symbolType, pos)
		#links.append(AGMLink(l.lhs, l.rhs, l.linkType, lV))
	elif node.type == "text":
		if stringIsUseful(str(node.properties)):
			print '    tssssssss'+str(node.properties)
	else:
		print "error: "+str(node.name)

	def draw(self):
		for d in self.drawers:
			d.update()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	if len(sys.argv)>1:
		clase = GraphViewer(sys.argv[1:])
		clase.show()
		app.exec_()
	else:
		print 'Usage:\n\t'+sys.argv[0]


