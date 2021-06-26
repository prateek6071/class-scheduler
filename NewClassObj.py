#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class NewClassObj():

	def __init__(self, name, classId):

		self.name = name
		self.id = classId

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def returnAsDict(self):
		return {self.name: self.id}