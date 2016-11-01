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

	def setPoints(self, points):
		self.projected_pts = points

	def __str__(self):
		return "{} {} {} {}".format(self.name, self.position, self.salary, self.projected_pts)