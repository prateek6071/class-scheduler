#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class Term():

	def __init__(self, name, termId, timeSchedule, teachers, students, classes, rooms, grades):
		self.name = name
		self.id = termId
		self.timeSchedule = timeSchedule
		self.teachers = teachers
		self.students = students
		self.classes = classes
		self.rooms = rooms
		self.grades = grades

	def addTeachers(self, teachers):
		for item in teachers:
			self.teachers.append(item)

	def addStudents(self, students):
		for item in students:
			self.students.append(item)

	def addClasses(self, classes):
		for item in classes:
			self.classes.append(item)

	def addRooms(self, rooms):
		for item in rooms:
			self.rooms.append(item)

	def addGrades(self, grades):
		for item in grades:
			self.grades.append(item)

	def getName(self):
		return self.name

	def getId(self):
		return self.termId

	def getTimeSchedule(self):
		return self.timeSchedule

	def getTeachers(self):
		return self.teachers

	def getStudents(self):
		return self.students

	def getClasses(self):
		return self.classes

	def getRooms(self):
		return self.rooms

	def getGrades(self):
		return self.grades

	def returnAsDict(self):
		self.termAsDict = {self.id: [{"Name": self.name}, {"Teachers": self.teachers}, {"Students": self.students}, {"Classes": self.classes}, {"Rooms": self.rooms}, {"Grades": self.grades}]}
		return self.termAsDict
