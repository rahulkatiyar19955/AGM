# Python distribution imports
import sys, traceback, os, re, threading, time, string, math
import numpy as np
# Qt interface
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *
#from PySide.Qt import *

from ui_appearance import Ui_Appearance

from parseAGGL import *

global vertexDiameter
vertexDiameter = 40.
global nodeThickness
nodeThickness = 2.
global lineThickness
lineThickness = 2.
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

class EdgeReader(QLineEdit):
	def __init__(self, x, y, index, parent):
		QLineEdit.__init__(self, parent)
		self.resize(100, 32)
		self.move(x-50, y-16)
		self.show()
		self.x = x
		self.y = y
		self.ind = index
		self.parentW = parent
		self.connect(self, SIGNAL('returnPressed()'), self.got)
	def got(self):
		self.parentW.graph.links[self.ind].linkType = str(self.text())
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
		self.readOnly = False
		self.pressName = -1
		self.releaseName = -1
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.move(0,0)
		self.pressed = False
		self.show()
		self.linkPositionMap = dict()
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
		pixmap = QPixmap(self.parentW.size())
		painter = QPainter(pixmap)
		painter.setRenderHint(QPainter.Antialiasing, True)
		self.paintOnPainter(painter, self.size().width()*5, self.size().height()*5, drawlines=False)
		pixmap.save(path, "png")
		painter.end()
		painter = None
	def paintOnPainter(self, painter, w, h, drawlines=True):
		global vertexDiameter
		global nodeThickness
		self.linkPositionMap.clear()
		w = float(w)
		h = float(h)
		w2 = w/2
		h2 = h/2
		# Clear the canvas and draw its borders
		painter.fillRect(QRectF(0., 0., float(w), float(h)), Qt.white)
		if drawlines:
			painter.drawLine(QLine(0,   0, w-1,   0))
			painter.drawLine(QLine(0, h-1, w-1, h-1))
			painter.drawLine(QLine(0,   0, 0,   h-1))
			painter.drawLine(QLine(w-1, 0, w-1, h-1))
		# Compute offset
		minX = 0
		minY = 0
		maxX = 0
		maxY = 0
		first = True
		for ww in self.graph.nodes:
			x = self.graph.nodes[ww].pos[0]
			y = self.graph.nodes[ww].pos[1]
			if minX > x or first: minX = x
			if maxX < x or first: maxX = x
			if minY > y or first: minY = y
			if maxY < y or first: maxY = y
			first = False
		#if not self.pressed:
		self.sumaX = sumaX = w2 - (maxX+minX)/2.
		self.sumaY = sumaY = h2 - (maxY+minY)/2.
		painter.translate(self.sumaX, self.sumaY)
		# Draw nodes
		pen = QPen()
		pen.setWidth(nodeThickness)
		painter.setPen(pen)
		brush = QBrush(QLinearGradient())
		painter.setBrush(brush)
		painter.setFont(self.main.fontDialog.currentFont())
		for w in self.graph.nodes:
			v = self.graph.nodes[w]
			grid = 5
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
			painter.drawEllipse(v.pos[0]-(vertexDiameter/2), v.pos[1]-0.7001*(vertexDiameter/2), vertexDiameter, vertexDiameter*0.7001)
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
		lengthPointer = 0.5*0.35*vertexDiameter
		anglePointer = 38.
		linkindex = 0
		for a in [True, False]:
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
				offsetSrc = 1.
				offsetDst = 1.
				offsetDstL = 5.
				xinit = float(v1.pos[0])-math.cos(angleR)*      (float(vertexDiameter)/2.+offsetSrc)
				xend  = float(v2.pos[0])+math.cos(angleR)*      (float(vertexDiameter)/2.+offsetDst)
				yinit = float(v1.pos[1])-math.sin(angleR)*0.700*(float(vertexDiameter)/2.+offsetSrc)
				yend  = float(v2.pos[1])+math.sin(angleR)*0.700*(float(vertexDiameter)/2.+offsetDst)
				aa = np.array([v2.pos[0]-xinit, v2.pos[1]-yinit])
				bb = aa*(lengthPointer/np.linalg.norm(aa))
				xendLine = xend-bb[0]
				yendLine = yend-bb[1]

				angleR = math.atan2(yinit-yendLine, xinit-xendLine)
				angleD = angleR*(57.2957795)

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
				
				if a:
					painter.drawLine(xinit, yinit, xendLine, yendLine)
					pen.setWidth(0.5)
					painter.drawLine(xinit, yinit, xendLine, yendLine)
					pen.setWidth(lineThickness)

				lpos = [(xinit + xendLine)/2, (yinit + yendLine) / 2]
				langle = math.atan2(yend-yinit, xend-xinit)
				align = Qt.AlignLeft
				rect = painter.boundingRect(QRectF(float(lpos[0]), float(lpos[1]), 1, 1), align, str(e.linkType))
				rect.translate(-rect.width()/2, -rect.height()/2) # Right now it will be centered on the link's center
				linkHeight = rect.height()+5
				linkGroupBase = (-linkGroupCount+1)*linkHeight/2
				rect.translate(0, linkHeight*pos + linkGroupBase) # Right now it will be centered on the link's center

				painter.setBrush(QColor(255, 255, 255))
				d = 2
				outterLinkRect = QRectF(rect.x()-5+d, rect.y()-3, rect.width()+10, rect.height()+6)
				innerLinkRect = QRectF(rect.x()-3+d, rect.y()-1.5, rect.width()+6, rect.height()+3)
				self.linkPositionMap[linkindex] = outterLinkRect
				painter.fillRect(outterLinkRect, Qt.black)
				painter.fillRect(innerLinkRect, Qt.white)
				rect.translate(2, 0)
				painter.drawText(rect, align, str(e.linkType))
				rect.translate(-2, 0)
				painter.setBrush(QColor(0, 0, 0))
				angleD = float(angleD)
				if a:
					an = angleD
					painter.translate(xendLine, yendLine)
					painter.rotate(an)
					points = []
					pointW = 0.25*lengthPointer
					points.append(QPointF(0, pointW))
					points.append(QPointF(0, -pointW))
					points.append(QPointF(-lengthPointer, 0))
					painter.drawPolygon(points)
					painter.rotate(-an)
					painter.translate(-xendLine, -yendLine)
					pass
	def mousePressEvent(self, e):
		tool = self.main.tool
		self.pressed = True
		if self.readOnly == True:
			tool = 'Node - Move'
		eX = e.x()-self.sumaX
		eY = e.y()-self.sumaY
		global vertexDiameter
		if tool == 'Node - Add':
			try:
				self.lastNumber
			except:
				self.lastNumber = 1
			self.graph.addNode(eX, eY, 'newid'+str(self.lastNumber)+self.name, 'type')
			self.lastNumber +=1

		elif tool == 'Node - Remove':
			x, y = self.graph.getName(eX, eY, vertexDiameter)
			if x>=0:
				self.graph.removeNode(eX, eY, vertexDiameter)

		elif tool == 'Node - Rename':
			x, y = self.graph.getCenter(self.sumaX+eX, self.sumaY+eY, vertexDiameter)
			if x>=0:
				r = NodeNameReader(x, y, self)
				r.show()
				r.setFocus(Qt.OtherFocusReason)
		elif tool == 'Node - Change type':
			x, y = self.graph.getCenter(self.sumaX+eX, self.sumaY+eY, vertexDiameter)
			if x>=0:
				r = NodeTypeReader(x, y, self)
				r.show()
				r.setFocus(Qt.OtherFocusReason)
		elif tool == 'Node - Move':
			self.pressName, found = self.graph.getName(eX, eY, 100)
			if not found: self.pressName = ''
		elif tool == 'Node - (Dis/En)able':
			self.graph.switchNode(eX, eY)
		elif tool == 'Edge - Add':
			self.pressName, found = self.graph.getName(eX, eY, vertexDiameter)
			if not found: self.pressName = ''
		elif tool == 'Edge - Remove':
			self.graph.removeEdge(eX, eY)
		elif tool == 'Edge - Rename':
			for linkindex in range(len(self.graph.links)):
				if self.linkPositionMap[linkindex].contains(eX, eY):
					print self.graph.links[linkindex].linkType
					r = EdgeReader(self.sumaX+eX, self.sumaY+eY, linkindex, self)
					r.show()
					r.setFocus(Qt.OtherFocusReason)
		elif tool == 'Edge - (Dis/En)able':
			self.edgeSwitchA = self.graph.getName(eX, eY, vertexDiameter)
	def mouseReleaseEvent(self, e):
		tool = self.main.tool
		self.pressed = False
		eX = e.x()-self.sumaX
		eY = e.y()-self.sumaY
		if self.readOnly == True:
			tool = 'Node - Move'

		if tool == 'Node - Add':
			pass
		elif tool == 'Node - Remove':
			pass
		elif tool == 'Node - Rename':
			pass
		elif tool == 'Node - Change type':
			pass
		elif tool == 'Node - Move':
			global vertexDiameter
			self.graph.moveNode(self.pressName, eX, eY, vertexDiameter)
		elif tool == 'Node - (Dis/En)able':
			pass
		elif tool == 'Edge - Add':
			self.releaseName, found = self.graph.getName(eX, eY, vertexDiameter)
			if not found: self.releaseName = ''
			if self.pressName != '' and self.releaseName != '':
				self.graph.addEdge(self.pressName, self.releaseName)
		elif tool == 'Edge - Remove':
			pass
		elif tool == 'Edge - Rename':
			pass
		elif tool == 'Edge - (Dis/En)able':
			self.edgeSwitchB = self.graph.getName(eX, eY, vertexDiameter)
			for e in self.graph.edges:
				if (e.a==self.edgeSwitchA and e.b==self.edgeSwitchB) or (e.a==self.edgeSwitchB and e.b==self.edgeSwitchA):
					e.enabled = not e.enabled
	def mouseMoveEvent(self, e):
		tool = self.main.tool
		eX = e.x()-self.sumaX
		eY = e.y()-self.sumaY
		if self.readOnly == True:
			tool = 'Node - Move'

		global vertexDiameter
		if tool == 'Node - Move':
			self.graph.moveNode(self.pressName, eX, eY, vertexDiameter)



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

