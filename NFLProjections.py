#!/usr/bin/python

from threading import Thread
import requests
import re
from bs4 import BeautifulSoup
import math

class NFLProjections:
	nflUrl=""
	nflPlayers = {}
	playersPerPage = 0

	def __init__(self):
		self.nflUrl = "http://fantasy.nfl.com/research/projections?offset="
		self.nflPlayers = {}
		self.playersPerPage = 25

	def getNFLInfo(self, playerInfo, nflPlayers):
		for info in playerInfo:
			name = ""
			projected = -1000.0
			player = info.find_all("a", {"class": "playerName"})
			if len(player) > 0:
				name = player[0].text
			pts = info.find_all("span" ,{"class": "playerWeekProjectedPts"})
			if len(pts) > 0:
				try:
					projected = float(pts[0].text)
				except:
					projected = 0.0
			if name != "" and projected != -1000.0:
				self.nflPlayers[name] = projected
		return

	def populateNflPlayersDict(self, offset):
		url = self.nflUrl+offset
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		self.getNFLInfo(playerInfo, self.nflPlayers)
		return

	def pullData(self, numberOfPlayers):
		numberOfPages = int(math.ceil(numberOfPlayers/self.playersPerPage))
		threads = []
		for i in range(numberOfPages):
			try:
				t = Thread(target=self.populateNflPlayersDict, args=(str((i+1)*self.playersPerPage),))
				threads.append(t)
				t.start()
			except:
				print "cant start thread"
		for t in threads:
			t.join()
		return

	def getNFLPlayers(self):
		return self.nflPlayers