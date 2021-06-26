#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import csv
import os
import json
import uuid
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from CommonWindowFunctions import * # Not needed
from EnterSchoolName import *
from SchoolSelect import *
from EnterYear import *
from School import *
from Year import * # Not needed
from EnterTimeSchedule import *
from TimeSchedule import * # Not needed
from EnterClass import *
from NewClassObj import * # Not needed
from EnterTeacher import *
from NewTeacher import * # Not needed
from EnterStudent import *
from NewStudent import * # Not needed
from EnterRoom import *
from NewRoom import * # Not needed
from EnterGrade import *
from NewGrade import * # Not needed
from Term import *

class Planner(QMainWindow):

    def __init__(self):
        super().__init__()
            
        self.initUI()
            
    def initUI(self):

        # Set up some of the universal widgets which are not dependent on school
        self.toolbar = self.addToolBar("Main Bar")
        self.toolbar.setMovable(False)

        self.initMenu()

        # Call the school selector
        self.selectedSchool = SchoolSelect(self)

        centerWindow(self)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    # Open another school window
    def openSchool(self):
        self.newSchool = MainWindow()

    # Load the school specific information into the window
    def loadSchool(self, schoolId):

        # Create a school object from the data
        self.school = School(schoolId)

        # Create the widgets
        self.mainWidgets = PlannerWidgets(self)
        self.setCentralWidget(self.mainWidgets)

        self.setWindowTitle(self.school.name)
        self.showMaximized()

    # Add a year to the school
    def openYear(self, school):
        self.newYear = EnterYear(self, self.school)

    # Add a time schedule to the school
    def openTimeSchedule(self, school):
        self.newTimeSchedule = EnterTimeSchedule(self, self.school)

    # Add a class to the school
    def openClass(self, school):
        self.newClass = EnterClass(self, self.school)

    # Add a teacher to the school
    def openTeacher(self, school):
        self.newTeacher = EnterTeacher(self, self.school)

    # Add a student to the school
    def openStudent(self, school):
        self.newStudent = EnterStudent(self, self.school)

    # Add a room to the school
    def openRoom(self, school):
        self.newRoom = EnterRoom(self, self.school)

    # Add a grade to the school
    def openGrade(self, school):
        self.newGrade = EnterGrade(self, self.school)

    # Set up the menu with actions
    def initMenu(self):

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu("&File")

        self.new = QMenu("New", self.fileMenu,)
        self.open = QMenu("Open", self.fileMenu)

        self.importMenu = QMenu("Import", self.fileMenu)

        self.schoolAction = QAction("School", self)
        self.schoolAction.setShortcut("Shift+Ctrl+N")
        self.schoolAction.triggered.connect(self.openSchool)

        self.yearAction = QAction("Year", self)
        self.yearAction.setShortcut("Ctrl+Y")
        self.yearAction.triggered.connect(self.openYear)

        self.teacherAction = QAction("Teacher", self)
        self.teacherAction.setShortcut("Ctrl+T")
        self.teacherAction.triggered.connect(self.openTeacher)

        self.studentAction = QAction("Student", self)
        self.studentAction.setShortcut("Ctrl+N")
        self.studentAction.triggered.connect(self.openStudent)

        self.classAction = QAction("Class", self)
        self.classAction.setShortcut("Ctrl+C")
        self.classAction.triggered.connect(self.openClass)

        self.roomAction = QAction("Room", self)
        self.roomAction.setShortcut("Ctrl+R")
        self.roomAction.triggered.connect(self.openRoom)

        self.timeScheduleAction = QAction("Time Schedule", self)
        self.timeScheduleAction.setShortcut("Shift+Ctrl+T")
        self.timeScheduleAction.triggered.connect(self.openTimeSchedule)

        self.gradeAction = QAction("Grade", self)
        self.gradeAction.setShortcut("Ctrl+G")
        self.gradeAction.triggered.connect(self.openGrade)

        self.importStudentsAction = QAction("Students", self)
        self.importStudentsAction.triggered.connect(self.importStudents)

        self.fileMenu.addMenu(self.new)
        self.new.addAction(self.schoolAction)
        self.new.addAction(self.yearAction)
        self.new.addAction(self.teacherAction)
        self.new.addAction(self.studentAction)
        self.new.addAction(self.classAction)
        self.new.addAction(self.roomAction)
        self.new.addAction(self.timeScheduleAction)
        self.new.addAction(self.gradeAction)

        self.fileMenu.addMenu(self.importMenu)
        self.importMenu.addAction(self.importStudentsAction)

    def importStudents(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        with open(fileName, newline='') as csvFile:
            studentReader = csv.reader(csvFile)
            next(studentReader)
            for line in csvFile:
                uniqueId = str(uuid.uuid4())
                studentName = line.strip()
                studentEntry = NewStudent(studentName, uniqueId)
                self.school.students.append(studentEntry.returnAsDict())
                self.mainWidgets.saveFile()

        self.mainWidgets.addStudentsToTree()

class PlannerWidgets(QWidget):

    def __init__(self, parent):        
        super().__init__(parent)

        self.parent = parent

        self.initWidgets(self.parent)

    def initWidgets(self, parent):

        self.parent = parent

        # Set up the tree to view information
        self.schoolTree = QTreeWidget(self)
        self.schoolTree.setColumnCount(1)
        self.schoolTree.header().close()

        self.yearSelect = QTreeWidgetItem(self.schoolTree)
        self.yearSelect.setText(0, "View years")
        # Add years from file to tree
        self.addYearsToTree()

        self.teacherSelect = QTreeWidgetItem(self.schoolTree, self.yearSelect)
        self.teacherSelect.setText(0, "View teachers")
        # Add teachers from file to tree
        self.addTeachersToTree()

        self.studentSelect = QTreeWidgetItem(self.schoolTree, self.teacherSelect)
        self.studentSelect.setText(0, "View students")
        # Add students from file to tree
        self.addStudentsToTree()

        self.classSelect = QTreeWidgetItem(self.schoolTree, self.studentSelect)
        self.classSelect.setText(0, "View classes")
        # Add classes from file to tree
        self.addClassesToTree()

        self.roomSelect = QTreeWidgetItem(self.schoolTree, self.classSelect)
        self.roomSelect.setText(0, "View rooms")
        # Add rooms from file to tree
        self.addRoomsToTree()

        self.scheduleSelect = QTreeWidgetItem(self.schoolTree, self.roomSelect)
        self.scheduleSelect.setText(0, "View time schedules")
        # Add time schedules from file to tree
        self.addTimeSchedulesToTree()

        self.gradeSelect = QTreeWidgetItem(self.schoolTree, self.scheduleSelect)
        self.gradeSelect.setText(0, "View grade levels")
        # Add grades from file to tree
        self.addGradesToTree()

        self.schoolTree.addTopLevelItem(self.yearSelect)
        self.schoolTree.itemSelectionChanged.connect(self.loadView)

        # --MARK--
        # Set up widgets for displays

        # Creates a small separator between the tree view and displayed data
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.hide()

        # Creates small box at top left corner of display window
        self.viewDescription = QLabel()
        self.viewDescription.hide()

        # Similar to viewDescription, but can be edited
        self.viewDescriptionEditable = QLineEdit(self)
        self.viewDescriptionEditable.hide()

        # Creates a list to display children of the tree
        self.listDisplay = QListWidget()
        self.listDisplay.hide()

        # Creates a generic 'add' button
        self.addItem = QPushButton("Add item", self)
        self.addItem.hide()

        # Creates a generic 'remove' button
        self.removeItem = QPushButton("Remove item", self)
        self.removeItem.hide()

        # Create a generic place to enter a string
        self.nameEntry = QLineEdit(self)
        self.nameEntry.hide()

        # Adds widgets to main window
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.nameEntry)
        self.vbox.addWidget(self.addItem)
        self.vbox.addWidget(self.removeItem)
        self.vbox.addStretch(1)

        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.viewDescription)
        self.vbox2.addWidget(self.viewDescriptionEditable)
        self.vbox2.addWidget(self.listDisplay)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.schoolTree)
        self.hbox.addWidget(self.separator)
        self.hbox.addLayout(self.vbox2)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

    def loadView(self):

        self.separator.hide()
        self.listDisplay.clear()
        self.listDisplay.hide()
        self.listDisplay.setDragDropMode(self.listDisplay.NoDragDrop)
        self.viewDescription.hide()
        self.addItem.hide()
        self.nameEntry.clear()
        self.nameEntry.hide()
        self.viewDescriptionEditable.hide()
        self.removeItem.hide()

        try:
            self.addItem.clicked.disconnect()
            self.nameEntry.returnPressed.disconnect()
            self.removeItem.disconnect()
            self.listDisplay.model().rowsMoved.disconnect()
        except Exception:
            pass
        
        if (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "year"):
            self.separator.show()
            self.listDisplay.show()
            self.addItem.show()
            self.addItem.clicked.connect(self.addTermToList)
            self.addItem.text = "Add term"
            self.nameEntry.show()
            self.nameEntry.setPlaceholderText("Term name")
            self.nameEntry.returnPressed.connect(self.addItem.click)
            self.viewDescription.setText(self.schoolTree.selectedItems()[0].text(0))
            self.viewDescription.show()

            for item in self.parent.school.years:

                self.viewYearEntry = Year(list(item.keys())[0], list(item.values())[0])

                if (self.schoolTree.selectedItems()[0].text(0) == self.viewYearEntry.getYearSpan()):

                    self.listOfTerms = self.viewYearEntry.getTerms()

                    for item in self.listOfTerms:

                        self.termId = list(item.keys())[0]
                        self.termName = list(list(item.values())[0][0].values())[0]

                        self.termEntry = QListWidgetItem()
                        self.termEntry.setText(self.termName)
                        self.termEntry.setData(Qt.UserRole, self.termEntry)

                        self.listDisplay.addItem(self.termEntry)

        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "teacher"):
            self.separator.show()
        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "student"):
            self.separator.show()
        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "class"):
            self.separator.show()
        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "room"):
            self.separator.show()
        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "schedule"):
            self.separator.show()
            self.listDisplay.show()
            self.listDisplay.setDragDropMode(self.listDisplay.InternalMove)
            self.listDisplay.model().rowsMoved.connect(self.periodsListEdited)
            self.viewDescriptionEditable.setText(self.schoolTree.selectedItems()[0].text(0))
            self.viewDescriptionEditable.show()
            self.viewDescriptionEditable.textChanged.connect(self.editScheduleName)
            self.addItem.show()
            self.addItem.clicked.connect(self.addPeriodToList)
            self.addItem.text = "Add period"
            self.nameEntry.show()
            self.nameEntry.setPlaceholderText("Time range")
            self.nameEntry.returnPressed.connect(self.addItem.click)
            self.removeItem.show()
            self.removeItem.text = "Remove period"
            self.removeItem.clicked.connect(self.removePeriodFromList)


            for item in self.parent.school.timeSchedules:

                if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):

                    for item in list(item.values())[0][0]:

                        self.listDisplay.addItem(item)

        elif (self.schoolTree.selectedItems()[0].data(1, Qt.UserRole) == "grade"):
            self.separator.show()

    def removePeriodFromList(self):

        itemsToRemove = self.listDisplay.selectedItems()

        if (itemsToRemove):

            for item in itemsToRemove:

                removedPeriod = self.listDisplay.row(item) + 1
                self.listDisplay.takeItem(self.listDisplay.row(item))

                for item in self.parent.school.timeSchedules:

                    if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):                    

                        listOfPeriods = list(item.values())[0][0]
                        listOfPeriods.pop(removedPeriod - 1)

                        for i in range(removedPeriod, self.listDisplay.count() + 1):

                            splitPeriod = self.listDisplay.item(i - 1).text().split(": ")
                            newString = "Period " + str(i) + ": " + splitPeriod[1]
                            self.listDisplay.item(i - 1).setText(newString)

                            splitFilePeriod = listOfPeriods[i - 1].split(": ")
                            newFileString = "Period " + str(i) + ": " + splitFilePeriod[1]
                            listOfPeriods[i - 1] = newFileString

        for item in self.parent.school.timeSchedules:

            # list(item.values())[0][2] is the uuid if a time schedue
            if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):

                # list(item.values())[0][1] is the number of periods in a time schedule
                list(item.values())[0][1] = self.listDisplay.count()

        self.saveFile()

    def periodsListEdited(self):

        for i in range(self.listDisplay.count()):

            getPeriod = self.listDisplay.item(i).text().split(": ")
            getInt = getPeriod[0].split(" ")
            newItem = "Period " + str(i + 1) + ": " + getPeriod[1]
            self.listDisplay.item(i).setText(newItem)

            for item in self.parent.school.timeSchedules:

                if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):

                    listOfPeriods = list(item.values())[0][0]

                    listOfPeriods[i] = newItem

        self.saveFile()

    def editScheduleName(self):

        self.schoolTree.selectedItems()[0].setText(0, self.viewDescriptionEditable.text())

        for item in self.parent.school.timeSchedules:

            if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):

                item[self.viewDescriptionEditable.text()] = item.pop(list(item.keys())[0])

                self.saveFile()

    def addPeriodToList(self):

        periodId = str(uuid.uuid4())

        self.periodEntry = QListWidgetItem()
        self.periodEntry.setData(Qt.UserRole, periodId)

        for item in self.parent.school.timeSchedules:

            if (list(item.values())[0][2] == self.schoolTree.selectedItems()[0].data(0, Qt.UserRole)):

                periodsList = list(item.values())[0][0]

                periodNum = list(item.values())[0][1]

                self.periodEntry.setText("Period " + str(periodNum + 1) + ": " + self.nameEntry.text())

                periodsList.append("Period " + str(periodNum + 1) + ": " + self.nameEntry.text())

                list(item.values())[0][0] = periodsList
                list(item.values())[0][1] = periodNum + 1

        self.saveFile()

        self.listDisplay.addItem(self.periodEntry)

    def addTermToList(self):

        termId = str(uuid.uuid4())

        self.termEntry = QListWidgetItem()
        self.termEntry.setText(self.nameEntry.text())
        self.termEntry.setData(Qt.UserRole, termId)
        
        self.listDisplay.addItem(self.termEntry)

        termAddition = Term(self.nameEntry.text(), termId, [], [], [], [], [], [])

        for item in self.parent.school.years:

            if (list(item.keys())[0] == self.schoolTree.selectedItems()[0].text(0)):

                terms = list(item.values())[0]

                terms.append(termAddition.returnAsDict())

        self.saveFile()

        self.yearSubSelect = self.schoolTree.selectedItems()[0]
        self.addTermToTree(self.yearSubSelect)

    def addTermToTree(self, parentItem):
        self.termParentItem = parentItem

        for item in self.parent.school.years:
            if (list(item.keys())[0] == self.termParentItem.text(0)):
                termsList = list(item.values())[0]

        for item in termsList:
            self.newTermChild = QTreeWidgetItem()
            self.newTermChild.setText(0, list(list(item.values())[0][0].values())[0])
            self.newTermChild.setData(0, Qt.UserRole, list(item.keys())[0])

            if (self.termParentItem.childCount() > 0):

                isDuplicate = False

                for i in range(self.termParentItem.childCount()):

                    if (self.termParentItem.child(i).data(0, Qt.UserRole) == self.newTermChild.data(0, Qt.UserRole)):
                        isDuplicate = True

                if (not isDuplicate):
                    self.termParentItem.addChild(self.newTermChild)

            else:

                self.termParentItem.addChild(self.newTermChild)

    def addYearsToTree(self):

        # Get the list of years
        self.years = self.parent.school.years

        for item in self.years:

            # Create a year object for easier processing
            self.yearEntry = Year(list(item.keys())[0], list(item.values())[0])

            self.newYearChild = QTreeWidgetItem()
            self.newYearChild.setText(0, self.yearEntry.getYearSpan())
            self.newYearChild.setData(1, Qt.UserRole, "year")

            # Check to see whether sorting is necessary
            if (self.yearSelect.childCount() > 0):

                self.indexNum = 0
                isDuplicate = False

                # Compare the new year's date to the date of the previous year
                for i in range(self.yearSelect.childCount()):

                    self.oldYearSpan = self.yearSelect.child(i).text(0).split(" - ")

                    # Make sure the year is not a duplicate
                    if (self.yearEntry.getFirstYear() > int(self.oldYearSpan[0])):
                        self.indexNum = self.yearSelect.indexOfChild(self.yearSelect.child(i)) + 1
                    elif (self.yearEntry.getFirstYear() == int(self.oldYearSpan[0])):
                        isDuplicate = True

                # Add year to tree
                if (self.indexNum == self.yearSelect.childCount() and (not isDuplicate)):
                    self.yearSelect.addChild(self.newYearChild)
                    self.addTermToTree(self.newYearChild)

                elif (not isDuplicate):
                    self.yearSelect.insertChild(self.yearSelect.indexOfChild(self.yearSelect.child(self.indexNum)), self.newYearChild)
                    self.addTermToTree(self.newYearChild)

            else:

                self.yearSelect.addChild(self.newYearChild)
                self.addTermToTree(self.newYearChild)

    def addTimeSchedulesToTree(self):

        # Get list of time schedules
        self.timeSchedules = self.parent.school.timeSchedules

        for item in self.timeSchedules:

            # Create a time schedule object for easier processing
            self.timeScheduleEntry = TimeSchedule(list(item.keys())[0], list(item.values())[0][0], list(item.values())[0][1], list(item.values())[0][2])
            self.newtimeScheduleChild = QTreeWidgetItem()
            self.newtimeScheduleChild.setText(0, self.timeScheduleEntry.getName())
            self.newtimeScheduleChild.setData(0, Qt.UserRole, self.timeScheduleEntry.getId())
            self.newtimeScheduleChild.setData(1, Qt.UserRole, "schedule")

            self.checkForDuplicates(self.scheduleSelect, self.newtimeScheduleChild)

    def addClassesToTree(self):

        self.classes = self.parent.school.classes

        for item in self.classes:

            name = list(item.keys())[0]
            classId = list(item.values())[0]

            self.classEntry = NewClassObj(name, classId)

            self.newClassChild = QTreeWidgetItem()
            self.newClassChild.setText(0, self.classEntry.getName())
            self.newClassChild.setData(0, Qt.UserRole, self.classEntry.getId())
            self.newClassChild.setData(1, Qt.UserRole, "class")

            self.checkForDuplicates(self.classSelect, self.newClassChild)

    def addTeachersToTree(self):

        self.teachers = self.parent.school.teachers

        for item in self.teachers:

            name = list(item.keys())[0]
            teacherId = list(item.values())[0]

            self.teacherEntry = NewTeacher(name, teacherId)

            self.newTeacherChild = QTreeWidgetItem()
            self.newTeacherChild.setText(0, self.teacherEntry.getName())
            self.newTeacherChild.setData(0, Qt.UserRole, self.teacherEntry.getId())
            self.newTeacherChild.setData(1, Qt.UserRole, "teacher")

            self.checkForDuplicates(self.teacherSelect, self.newTeacherChild)

    def addStudentsToTree(self):

        self.students = self.parent.school.students

        for item in self.students:

            name = list(item.keys())[0]
            studentId = list(item.values())[0]

            self.studentEntry = NewStudent(name, studentId)

            self.newStudentChild = QTreeWidgetItem()
            self.newStudentChild.setText(0, self.studentEntry.getName())
            self.newStudentChild.setData(0, Qt.UserRole, self.studentEntry.getId())
            self.newStudentChild.setData(1, Qt.UserRole, "student")

            self.checkForDuplicates(self.studentSelect, self.newStudentChild)

    def addRoomsToTree(self):

        self.rooms = self.parent.school.rooms

        for item in self.rooms:

            name = list(item.keys())[0]
            roomId = list(item.values())[0]

            self.roomEntry = NewRoom(name, roomId)

            self.newRoomChild = QTreeWidgetItem()
            self.newRoomChild.setText(0, self.roomEntry.getName())
            self.newRoomChild.setData(0, Qt.UserRole, self.roomEntry.getId())
            self.newRoomChild.setData(1, Qt.UserRole, "room")

            self.checkForDuplicates(self.roomSelect, self.newRoomChild)

    def addGradesToTree(self):

        self.grades = self.parent.school.grades

        for item in self.grades:

            name = list(item.keys())[0]
            gradeId = list(item.values())[0]

            self.gradeEntry = NewGrade(name, gradeId)

            self.newGradeChild = QTreeWidgetItem()
            self.newGradeChild.setText(0, self.gradeEntry.getName())
            self.newGradeChild.setData(0, Qt.UserRole, self.gradeEntry.getId())
            self.newGradeChild.setData(1, Qt.UserRole, "grade")

            self.checkForDuplicates(self.gradeSelect, self.newGradeChild)

    def checkForDuplicates(self, subTree, child):

        if (subTree.childCount() > 0):

            isDuplicate = False

            for i in range(subTree.childCount()):

                if (subTree.child(i).data(0, Qt.UserRole) == child.data(0, Qt.UserRole)):
                    isDuplicate = True

            if (not isDuplicate):
                subTree.addChild(child)

        else:
            subTree.addChild(child)

    def saveFile(self):

        with open(self.parent.school.id + ".json", mode = "w+") as f:
            f.write(json.dumps(self.parent.school.data, indent = 2))
            f.flush()
            os.fsync(f)
