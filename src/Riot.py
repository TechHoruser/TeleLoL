#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json


class Riot(object):
	def __init__( self, key, summoner_name ):
		super( Riot, self ).__init__()
		self.key = key
		self.summoner_name = summoner_name
		self.headers = {
		    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
		    "X-Riot-Token": "5e9e5832-1ccd-43f0-97aa-2a26c9071c2b",
		    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
		    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
		     }

	def getSummonerInfo( self ):
		try:
			# Obtain summoner's info
			url_summoner = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + self.summoner_name
			summoner_response = self.getResponse( url_summoner )

			print 'Info de Invocador:\n'
			print summoner_response

			try:
				# Obtain current game info
				url_current_game = 'https://euw1.api.riotgames.com/observer-mode/rest/consumer/getSpectatorGameInfo/EUW1/' + str( summoner_response['id'] )
				current_game_response = self.getResponse( url_current_game )

				print 'Info de Partida Actual:\n'
				print json.dumps(current_game_response)

				print '\n\n'

			except urllib2.HTTPError as err:
				print 'Error al encontrar partida'

		except urllib2.HTTPError as err:
			print 'Invocador no encontrado'


	def getResponse( self, url ):
		request  = urllib2.Request( url, headers = self.headers )
		response = urllib2.urlopen( request )
		response = response.read()

		return json.loads( response )
