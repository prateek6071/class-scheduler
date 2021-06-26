#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import json
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CommonWindowFunctions import *
from Year import *

class EnterYear(QWidget):

	def __init__(self, planner, school):
		super().__init__()

		self.initUI(planner, school)

	def initUI(self, planner, school):

		self.school = school
		self.planner = planner

		self.now = datetime.datetime.now()

		# Set up error message
		self.displayTimer = QTimer()
		self.displayTimer.isSingleShot()
		self.displayTimer.timeout.connect(self.hideErrorMessage)

		self.add = QPushButton("Add", self)
		self.add.clicked.connect(self.sendYear)
		self.add.setAutoDefault(True)
		self.enterYearSpan = QLabel("Enter year span:")
		self.errorMessage = QLabel("Year has already been added")
		self.errorMessage.hide()
		self.yearSelection = QComboBox(self)

		# Get a range of years to display, centered around current year
		for i in range(10):
			self.yearSelection.addItem(str(self.now.year - 4 + i) + " - " + str(self.now.year - 3 + i))

		self.yearSelection.setCurrentIndex(self.yearSelection.findText(str(self.now.year) + " - " + str(self.now.year + 1)))

		self.hbox = QHBoxLayout()
		self.hbox.addWidget(self.enterYearSpan)
		self.hbox.addSpacing(10)
		self.hbox.addWidget(self.yearSelection)
		self.hbox.addSpacing(10)

		self.errorBox = QHBoxLayout()
		self.errorBox.addStretch(1)
		self.errorBox.addWidget(self.errorMessage)

		self.buttonPos = QHBoxLayout()
		self.buttonPos.addStretch(1)
		self.buttonPos.addWidget(self.add)

		self.vbox = QVBoxLayout()
		self.vbox.addLayout(self.hbox)
		self.vbox.addStretch(1)
		self.vbox.addLayout(self.errorBox)
		self.vbox.addStretch(1)
		self.vbox.addLayout(self.buttonPos)

		self.setLayout(self.vbox)
		self.setGeometry(0, 0, 500, 200)
		centerWindow(self)
		self.setWindowTitle("Enter a new year")
		self.show()

	# Check and send year to main window
	def sendYear(self):
		
		# Create new year for easier processing
		self.yearEntry = Year(self.yearSelection.currentText(), [])

		# See if checking is necessary
		if (not self.school.years):

			self.addYearToSchool()

		else:

			# Make sure year is not a duplicate
			for item in self.school.years:

				if (list(item.keys())[0] == self.yearEntry.getYearSpan()):

					self.errorMessage.show()
					self.displayTimer.start(2000)

					return None

			self.addYearToSchool()

	# Sort years in file before sending
	def addYearToSchool(self):

		self.indexNum = 0

		for i in range(len(self.school.years)):
			for key in self.school.years[i].keys():

				self.oldYearSpan = key.split(" - ")

				if (self.yearEntry.getFirstYear() > int(self.oldYearSpan[0])):
					self.indexNum = i + 1

		if (self.indexNum == len(self.school.years)):
			self.school.years.append(self.yearEntry.returnAsDict())
		else:
			self.school.years.insert(self.indexNum, self.yearEntry.returnAsDict())

		with open(self.school.id + ".json", mode = "w+") as f:
			f.write(json.dumps(self.school.data, indent = 2))
			f.flush()
			os.fsync(f)

		self.planner.mainWidgets.addYearsToTree()
		self.close()

	def hideErrorMessage(self):
		self.errorMessage.hide()