#!/usr/bin/python

class Player:
	salary = 0
	name = ""
	team = ""
	position = ""
	projected_pts = float(0.0)

	def __init__(self, salary, name, team, position, projected_pts):
		self.salary = salary
		self.name = name
		self.team = team
		self.position = position
		self.projected_pts = projected_pts

	def setPoints(points):
		self.projected_pts = points

	def printPlayer(self):
		print self.name, self.position, self.team
		print "Salary:\t\t", self.salary
		print "Projected:\t", self.projected_pts