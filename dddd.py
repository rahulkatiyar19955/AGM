#!/usr/bin/env python
from PySide.QtCore import *
from PySide.QtGui import *

class ListWidgetTest(QDialog):
	def __init__(self, parent=None):
		super(ListWidgetTest, self).__init__(parent)

		listWidget = QListWidget()
		layout = QVBoxLayout()
		layout.addWidget(listWidget)
		self.setLayout(layout)

		self.connect(listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem)"), self.printTest)
		self.connect(listWidget, SIGNAL("itemClicked(QListWidgetItem)"), self.printTest)
		self.connect(listWidget, SIGNAL("itemActivated(QListWidgetItem)"), self.printTest)

		#item = QListWidgetItem(self.tr("TESTING SIGNALS"))
		#item.setData(Qt.UserRole, QVariant(1))
		listWidget.insertItem(0, "ddd")

	def printTest(self, item):
		print "ok!!"


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	dialog = ListWidgetTest()
	dialog.show()
	app.exec_()