#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class ClassObj():

	def __init__(self, name, classId, listOfStaticPeriods, listOfTeachers, listOfStudents, listOfRooms, listOfGrades):

		self.name = name
		self.id = classId
		self.listOfStaticPeriods = listOfStaticPeriods
		self.listOfTeachers = listOfTeachers
		self.listOfStudents = listOfStudents
		self.listOfRooms = listOfRooms
		self.listOfGrades = listOfGrades

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def getListOfStaticPeriods(self):
		return self.listOfStaticPeriods

	def getListOfTeachers(self):
		return self.listOfTeachers

	def getListOfStudents(self):
		return self.listOfStudents

	def getListOfRooms(self):
		return self.listOfRooms

	def getListOfGrades(self):
		return self.listOfGrades

	def returnAsSimpleDict(self):
		return {self.name: self.id}

	def returnAsDict(self):
		return {self.name: [self.id, {"Static Periods": self.listOfStaticPeriods}, {"Teachers": self.listOfTeachers}, {"Students": self.listOfStudents}, {"Rooms": self.listOfRooms}, {"Grades": self.listOfGrades}]}

