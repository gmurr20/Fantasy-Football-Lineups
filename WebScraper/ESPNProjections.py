#!/usr/bin/python

from threading import Thread
import requests
import re
from bs4 import BeautifulSoup
import math

class ESPNProjections:
	espnUrl = ""
	espnPlayers = {}
	playersPerPage = 0

	def __init__(self):
		self.espnUrl = "http://games.espn.com/ffl/tools/projections?startIndex="
		self.espnPlayers = {}
		self.playersPerPage = 40

	def getESPNInfo(self, playerInfo, espnPlayers):
		for info in playerInfo:
			name = ""
			pts = -1000.0
			player = info.find_all("a", {"class": "flexpop"})
			for link in player:
				if link.has_attr("playerid"):
					name = link.text.replace("D/ST","")
					break
			projected = info.find_all("td", {"class": "playertableStat", "class": "appliedPoints", "class": "sortedCell"})
			if len(projected) == 1:
				try:
					pts = float(projected[0].text)
				except:
					pts = 0.0
			if pts != -1000.0 and name != "":
				self.espnPlayers[name] = pts

	def getProjectedFromEspn(self, startIndex):
		url = self.espnUrl+startIndex
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		playerInfo = soup.find_all("tr")
		self.getESPNInfo(playerInfo, self.espnPlayers)
		return

	def pullData(self, numberOfPlayers):
		numberOfPages = int(math.ceil(numberOfPlayers/40))
		threads = []
		for i in range(numberOfPages):
			try:
				t = Thread(target=self.getProjectedFromEspn, args=(str(i*40),))
				threads.append(t)
				t.start()
			except:
				print "cant start thread"

		for t in threads:
			t.join()
		return self.espnPlayers

	def getEspnPlayers(self):
		return self.espnPlayers


