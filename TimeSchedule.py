#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class TimeSchedule():

	def __init__(self, name, periodList, periodCount, timeId):
		self.name = name
		self.periodList = periodList
		self.periodCount = periodCount
		self.id = timeId

	def getName(self):
		return self.name

	def getPeriods(self):
		return self.periodList

	def getPeriodCount(self):
		return self.periodCount

	def getId(self):
		return self.id

	def returnAsDict(self):
		self.timeScheduleAsDict = {self.name: [self.periodList, self.periodCount, self.id]}
		return self.timeScheduleAsDict
