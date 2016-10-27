#!/usr/bin/python
import csv
import requests
from bs4 import BeautifulSoup

#goes through the tags and finds the name and projected pts for the week
def getNFLProjected(playerInfo, nflPlayers):
	for info in playerInfo:
		name = ""
		projected = -1000.0
		for tag in info:
			player = tag.find_all("a", {"class": "playerName"})
			if len(player) > 0:
				name = player[0].text
			pts = tag.find_all("span" ,{"class": "playerWeekProjectedPts"})
			if len(pts) > 0:
				projected = pts[0].text
		if name != "" and projected != -1000.0:
			nflPlayers[name] = projected

#get Projected values from NFL site
def getProjectedFromNFL(n):
	ogUrl="http://fantasy.nfl.com/research/projections"
	url = "http://fantasy.nfl.com/research/projections"
	count = 0
	nflPlayers = {}
	while len(nflPlayers) < n:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		getNFLProjected(playerInfo, nflPlayers)
		nextLink = soup.find_all("li", {"class": "next"})
		url = ogUrl+nextLink[0].find_all("a")[0].get("href")
	return nflPlayers

getProjectedFromNFL(25)