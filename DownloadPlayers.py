#!/usr/bin/python
import csv

from Player import Player

#Download Players from csv file and returns a dictionary of Players
def DownloadPlayers(fileName):
	allEligiblePlayers = {}
	with open(fileName, 'r') as file:
		fileReader = csv.reader(file)
		skipFirst = True
		for row in fileReader:
			if skipFirst:
				skipFirst = False
				continue
			position = row[0]
			name = row[1]
			salary = int(row[2])
			projected = float(row[4])
			team = row[5]
			newPlayer = Player(salary, name, team, position, projected)
			allEligiblePlayers[name] = newPlayer
	return allEligiblePlayers





