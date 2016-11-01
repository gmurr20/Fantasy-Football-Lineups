#!/usr/bin/python

from threading import Thread
import requests
import re
from bs4 import BeautifulSoup
import math

class FOXProjections:
	foxUrl=""
	foxPlayers = {}
	playersPerPage = 0

	def __init__(self):
		self.foxUrl="http://www.foxsports.com/fantasy/football/commissioner/Research/Projections.aspx?page="
		self.foxPlayers = {}
		self.playersPerPage = 25

	def parseFoxInfo(self, playerInfo):
		for info in playerInfo:
			name = ""
			pts = -1000.0
			player = info.find_all("a", {"class": "wis_playerProfileLink"})
			if len(player) > 0:
				name = player[0].text
			projected = info.find_all("td", {"class": "wis_col_highlight"})
			if len(projected) > 0:
				try:
					pts = float(projected[0].text)
				except:
					pts = 0.0
			if name != "" and pts != -1000.0:
				self.foxPlayers[name] = pts
		return

	def populateFoxPlayersDict(self, offset):
		url =""+self.foxUrl+offset
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		self.parseFoxInfo(playerInfo)
		return

	def pullData(self, numberOfPlayers):
		numberOfPages = int(math.ceil(numberOfPlayers/self.playersPerPage))
		threads = []
		for i in range(numberOfPages):
			try:
				t = Thread(target=self.populateFoxPlayersDict, args=((str(i+1),)))
				threads.append(t)
				t.start()
			except:
				print "cant start thread"
		for t in threads:
			t.join()
		return