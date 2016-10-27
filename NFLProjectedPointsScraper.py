#!/usr/bin/python
import csv
import requests
from bs4 import BeautifulSoup


global nflUrl, foxUrl
nflUrl = "http://fantasy.nfl.com/research/projections"
foxUrl = "http://www.foxsports.com/fantasy/football/commissioner/Research/Projections.aspx"

#goes through the tags of playerInfo and finds the name and projected pts for the week
def getNFLProjected(playerInfo, nflPlayers):
	for info in playerInfo:
		name = ""
		projected = -1000.0
		player = info.find_all("a", {"class": "playerName"})
		if len(player) > 0:
			name = player[0].text
		pts = info.find_all("span" ,{"class": "playerWeekProjectedPts"})
		if len(pts) > 0:
			projected = float(pts[0].text)
		if name != "" and projected != -1000.0:
			nflPlayers[name] = projected
			print name, projected

#get Projected values from NFL site
def getProjectedFromNFL(n):
	url = ""+nflUrl
	nflPlayers = {}
	while len(nflPlayers) < n:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		getNFLProjected(playerInfo, nflPlayers)
		nextLink = soup.find_all("li", {"class": "next"})
		try:
			nextPage = nextLink[0].find_all("a")[0].get("href")
		except:
			print "Next page not found... Awkward"
			break
		url = nflUrl+nextPage
	return nflPlayers

def getFoxProjected(playerInfo, nflPlayers):
	for info in playerInfo:
		name = ""
		pts = -1000.0
		player = info.find_all("a", {"class": "wis_playerProfileLink"})
		if len(player) > 0:
			name = player[0].text
		projected = info.find_all("td", {"class": "wis_col_highlight"})
		if len(projected) > 0:
			pts = float(projected[0].text)
		if name != "" and pts != -1000.0:
			nflPlayers[name] = pts
			print name, pts

def getProjectedFromFox(n):
	url =""+foxUrl
	nflPlayers = {}
	while len(nflPlayers) < n:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		getFoxProjected(playerInfo, nflPlayers)
		nextLink = soup.find_all("a", {"class": "wis_nextPageLink"})
		try:
			nextPage = nextLink[0].get("href")
		except:
			print "Next page not found... Awkward"
			break
		url = foxUrl+nextPage
	return nflPlayers

