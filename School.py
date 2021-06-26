#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import json

class School():

	def __init__(self, schoolId):

		self.id = schoolId

		with open(self.id + ".json") as f:
			self.data = json.load(f)
			self.name = list(self.data.keys())[0]
			self.years = list(self.data.values())[0]["Years"]
			self.teachers = list(self.data.values())[0]["Teachers"]
			self.students = list(self.data.values())[0]["Students"]
			self.classes = list(self.data.values())[0]["Classes"]
			self.rooms = list(self.data.values())[0]["Rooms"]
			self.timeSchedules = list(self.data.values())[0]["Time Schedules"]
			self.grades = list(self.data.values())[0]["Grades"]