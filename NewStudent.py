#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class NewStudent():

	def __init__(self, name, studentId):

		self.name = name
		self.id = studentId

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def returnAsDict(self):
		return {self.name: self.id}