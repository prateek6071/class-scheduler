#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class NewTeacher():

	def __init__(self, name, teacherId):

		self.name = name
		self.id = teacherId

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def returnAsDict(self):
		return {self.name: self.id}