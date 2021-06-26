#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class NewGrade():

	def __init__(self, name, gradeId):

		self.name = name
		self.id = gradeId

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def returnAsDict(self):
		return {self.name: self.id}