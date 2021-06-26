#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

class Year():

	def __init__(self, yearSpan, terms):
		self.yearSpan = yearSpan
		self.terms = terms
		self.listOfYears = self.yearSpan.split(" - ")
		self.firstYear = int(self.listOfYears[0])

	def addTerms(self, terms):
		for item in terms:
			self.terms.append(item)

	def getTerms(self):
		return self.terms

	def getYearSpan(self):
		return self.yearSpan

	def getFirstYear(self):
		return self.firstYear

	def returnAsDict(self):
		self.yearAsDict = {self.yearSpan: self.terms}
		return self.yearAsDict