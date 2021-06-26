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
from TimeSchedule import *

class EnterTimeSchedule(QWidget):

	def __init__(self, planner, school):
		super().__init__()

		self.initUI(planner, school)

	def initUI(self, planner, school):

		self.planner = planner
		self.school = school

		self.periods = QListWidget()
		self.periods.setDragDropMode(self.periods.InternalMove)
		self.periods.model().rowsMoved.connect(self.listEdited)
		self.nameBox = QLineEdit(self)
		self.nameBox.setPlaceholderText("Time schedule name")
		self.addPeriod = QPushButton("Add period", self)
		self.addPeriod.clicked.connect(self.addPeriods)
		self.addSchedule = QPushButton("Add time schedule", self)
		self.addSchedule.clicked.connect(self.sendSchedule)
		self.input = QLineEdit(self)
		self.input.setPlaceholderText("Time range")
		self.input.returnPressed.connect(self.addPeriod.click)

		self.remove = QPushButton("Remove period", self)
		self.remove.clicked.connect(self.removePeriods)

		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.input)
		self.vbox.addWidget(self.addPeriod)
		self.vbox.addWidget(self.remove)
		self.vbox.addStretch(1)
		self.vbox.addWidget(self.addSchedule)

		self.vbox2 = QVBoxLayout()
		self.vbox2.addWidget(self.nameBox)
		self.vbox2.addWidget(self.periods)

		self.hbox = QHBoxLayout()
		self.hbox.addLayout(self.vbox2)
		self.hbox.addSpacing(10)
		self.hbox.addLayout(self.vbox)

		self.setLayout(self.hbox)
		self.setGeometry(0, 0, 500, 500)
		centerWindow(self)
		self.setWindowTitle("Enter a new time schedule")
		self.show()

	# Change the period numbers
	def listEdited(self):

		for i in range(self.periods.count()):
			self.getPeriod = self.periods.item(i).text().split(": ")
			self.newItem = "Period " + str(i + 1) + ": " + self.getPeriod[1]
			self.periods.item(i).setText(self.newItem)

	# Add periods to the list
	def addPeriods(self):

		self.timeRange = self.input.text()
		self.insertIndex = self.periods.count() + 1
		self.periods.addItem("Period " + str(self.insertIndex) + ": " + self.timeRange)

	# Remove periods from the list and change the period numbers
	def removePeriods(self):

		self.itemsToRemove = self.periods.selectedItems()
		if (self.itemsToRemove):
			for item in self.itemsToRemove:
				removedPeriod = self.periods.row(item) + 1
				self.periods.takeItem(self.periods.row(item))

				for i in range(removedPeriod, self.periods.count() + 1):
					self.splitPeriod = self.periods.item(i - 1).text().split(": ")
					self.newString = "Period " + str(i) + ": " + self.splitPeriod[1]
					self.periods.item(i - 1).setText(self.newString)

	# Write the schedule to the file and send it to the main window
	def sendSchedule(self):

		self.listOfPeriods = []

		for i in range(self.periods.count()):
			self.listOfPeriods.append(self.periods.item(i).text())

		self.id = str(uuid.uuid4())

		if (self.nameBox.text().isspace() or self.nameBox.text() == ""):

			self.timeScheduleEntry = TimeSchedule("(Untitled)", self.listOfPeriods, self.periods.count(), self.id)
			
		else:

			self.timeScheduleEntry = TimeSchedule(self.nameBox.text(), self.listOfPeriods, self.periods.count(), self.id)

		self.school.timeSchedules.append(self.timeScheduleEntry.returnAsDict())

		with open(self.school.id + ".json", mode = "w+") as f:
			f.write(json.dumps(self.school.data, indent = 2))
			f.flush()
			os.fsync(f)

		self.planner.mainWidgets.addTimeSchedulesToTree()
		self.close()