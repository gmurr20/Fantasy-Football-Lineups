#!/usr/bin/python
import csv
import requests
from bs4 import BeautifulSoup

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

#get Projected values from NFL site
def getProjectedFromNFL(n):
	ogUrl="http://fantasy.nfl.com/research/projections"
	url = "http://fantasy.nfl.com/research/projections"
	count = 0
	nflPlayers = {}
	while count < n:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		for info in playerInfo:
			name = ""
			projected = -100.0
			for tag in info:
				player = tag.find_all("a", {"class": "playerName"})
				if len(player) > 0:
					name = player[0].text
				pts = tag.find_all("span" ,{"class": "playerWeekProjectedPts"})
				if len(pts) > 0:
					projected = pts[0].text
			if name != "" and projected != -100.0:
				nflPlayers[name] = projected
				print name, projected
				count+=1
		nextLink = soup.find_all("li", {"class": "next"})
		url = ogUrl+nextLink[0].find_all("a")[0].get("href")
	return nflPlayers



