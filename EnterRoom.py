#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import json
import uuid
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CommonWindowFunctions import *
from NewRoom import *

class EnterRoom(QWidget):

	def __init__(self, planner, school):
		super().__init__()

		self.initUI(planner, school)

	def initUI(self, planner, school):

		self.planner = planner
		self.school = school

		self.nameBox = QLineEdit(self)
		self.nameBox.setPlaceholderText("Room name")
		self.add = QPushButton("Add", self)
		self.add.clicked.connect(self.sendRoom)
		self.nameBox.returnPressed.connect(self.add.click)

		self.hbox = QHBoxLayout()
		self.hbox.addWidget(self.nameBox)

		self.hbox2 = QHBoxLayout()
		self.hbox2.addStretch(1)
		self.hbox2.addWidget(self.add)

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.hbox)
		self.vbox.addStretch(1)
		self.vbox.addLayout(self.hbox2)

		self.setLayout(self.vbox)
		self.setGeometry(0, 0, 400, 200)
		centerWindow(self)
		self.setWindowTitle("Enter a new room")
		self.show()

	def sendRoom(self):

		self.id = str(uuid.uuid4())

		if (self.nameBox.text().isspace() or self.nameBox.text() == ""):

			self.roomEntry = NewRoom("(Untitled)", self.id)

		else:

			self.roomEntry = NewRoom(self.nameBox.text(), self.id)

		self.school.rooms.append(self.roomEntry.returnAsDict())

		with open(self.school.id + ".json", mode = "w+") as f:
			f.write(json.dumps(self.school.data, indent = 2))
			f.flush()
			os.fsync(f)

		self.planner.mainWidgets.addRoomsToTree()
		self.close()