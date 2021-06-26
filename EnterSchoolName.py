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

class EnterSchoolName(QWidget):

    def __init__(self, schoolList):
        super().__init__()

        self.initUI(schoolList)

    def initUI(self, schoolList):

        # Get the current list of schools
        self.schoolList = schoolList

        self.add = QPushButton("Add", self)
        self.add.clicked.connect(self.addItemToList)
        self.add.setAutoDefault(True)
        self.textBox = QLineEdit(self)
        self.textBox.setPlaceholderText("School name")
        self.textBox.returnPressed.connect(self.add.click)

        self.hbox = QHBoxLayout()
        self.hbox.addSpacing(10)
        self.hbox.addWidget(self.textBox)
        self.hbox.addSpacing(10)

        self.buttonPos = QHBoxLayout()
        self.buttonPos.addStretch(1)
        self.buttonPos.addWidget(self.add)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.buttonPos)

        self.setLayout(self.vbox)
        self.setGeometry(0, 0, 500, 200)
        centerWindow(self)
        self.show()

    # Add an new school to the list of school
    def addItemToList(self):

        # Get entered name
        self.name = self.textBox.text()

        # Create a uuid
        self.id = str(uuid.uuid4())

        # Write the new school to the file
        with open("SchoolNames.json") as f:
            data = json.load(f)
            listOfSchoolNames = data.get("Schools")
            schoolEntry = {self.id: self.name}
            listOfSchoolNames.append(schoolEntry)

        with open("SchoolNames.json", mode = "w+") as f:
            f.write(json.dumps(data, indent=2))
            f.flush()
            os.fsync(f)

        # Add the new school to the list
        self.schoolList.addItem(self.name, self.id)
        self.schoolList.setCurrentIndex(self.schoolList.findData(self.id))

        # Create a new data file for the school
        with open(self.id + ".json", "a+") as f:
            schoolData = {"Years": [], "Teachers": [], "Students": [],
            "Classes": [], "Rooms": [], "Time Schedules": [], "Grades": []}
            data = {self.name: schoolData}
            f.write(json.dumps(data, indent = 2))

        self.close()