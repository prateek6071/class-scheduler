#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class NewRoom():

	def __init__(self, name, roomId):

		self.name = name
		self.id = roomId

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def returnAsDict(self):
		return {self.name: self.id}