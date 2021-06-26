#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CommonWindowFunctions import *
from EnterSchoolName import *

class SchoolSelect(QWidget):
    
    def __init__(self, planner):
        super().__init__()
        
        self.initUI(planner)
        
    def initUI(self, planner):

        self.planner = planner

        # Create the dropdown box of school
        self.schoolList = QComboBox(self)

        # Open the file with the list of school names and ids
        with open("SchoolNames.json") as f:
            data = json.load(f)
            listOfSchoolNames = data.get("Schools")

            for item in range(len(listOfSchoolNames)):
                dataDict = listOfSchoolNames[item]

                # Add the schools to the dropdown box
                self.schoolList.addItem(list(dataDict.values())[0], list(dataDict.keys())[0])

        self.addSchool = QPushButton("Add School", self)
        self.addSchool.clicked.connect(self.buildNameBox)

        self.continueButton = QPushButton("Continue", self)
        self.continueButton.clicked.connect(self.sendName)
        self.isSchoolSelected()

        self.schoolList.currentIndexChanged.connect(self.isSchoolSelected)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch(1)
        self.buttons.addWidget(self.addSchool)
        self.buttons.addWidget(self.continueButton)

        self.selector = QHBoxLayout()
        self.selector.addSpacing(100)
        self.selector.addWidget(self.schoolList)
        self.selector.addSpacing(100)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.selector)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.buttons)
        self.setLayout(self.vbox)

    # Create window to add a school
    def buildNameBox(self):

        self.textBox = EnterSchoolName(self.schoolList)

    # Send the selected school's id to the main window
    def sendName(self):

        self.schoolId = self.schoolList.currentData()

        self.planner.loadSchool(self.schoolId)
        self.close()

    # Check to see if a school is selected in order to enable continue button
    def isSchoolSelected(self):

        if (self.schoolList.currentIndex() == -1):
            self.continueButton.setDisabled(True)
        else:
            self.continueButton.setDisabled(False)

        self.resize(700, 500)
        centerWindow(self)
        self.setWindowTitle("Select a school")
        self.show()