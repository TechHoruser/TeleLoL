#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json


class Riot(object):
	def __init__( self, key, tmp_folder ):
		super( Riot, self ).__init__()
		self.key = key
		self.headers = {
		    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
		    "X-Riot-Token": key,
		    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
		    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
		     }
		self.tmp_folder = tmp_folder

	def getSummonerInfo( self, summoner_name ):
		try:
			# Obtain summoner's info
			url_summoner = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summoner_name
			summoner_response = self.getResponse( url_summoner )

			open( self.tmp_folder+'summoner.json', 'w').write(  json.dumps( summoner_response ) )

			try:
				# Obtain current game info
				url_current_game = 'https://euw1.api.riotgames.com/observer-mode/rest/consumer/getSpectatorGameInfo/EUW1/' + str( summoner_response['id'] )
				current_game_response = self.getResponse( url_current_game )

				game = {
					'allies' : {},
					'enemies' : {}
				}

				print current_game_response[ "gameMode" ]
				
				first_allies = False
				if ( current_game_response[ "gameMode" ] == 'ARAM' or current_game_response[ "gameMode" ] == 'CLASSIC' ):
					tam_team = 5
				elif ( current_game_response[ "gameMode" ] == 'ARAM' ):
					tam_team = 3

				for index in range( 0, tam_team*2 ):
					game[ 'allies' if ( ( first_allies and index < tam_team ) or ( not first_allies and index >= tam_team ) ) else 'enemies' ][ current_game_response[ 'participants' ][ index ][ 'summonerId' ] ] = {
						'name' : current_game_response[ 'participants' ][ index ][ 'summonerName' ],
						'champion' : current_game_response[ 'participants' ][ index ][ 'championId' ]
					}
				
				# open( self.tmp_folder+'game.json', 'w').write(  json.dumps( game ) )
				return json.dumps( game )
				# open( self.tmp_folder+'current_game.json', 'w').write(  json.dumps( current_game_response ) )

			except urllib2.HTTPError as err:
				return 'Error al encontrar partida'

		except urllib2.HTTPError as err:
			return 'Invocador ' + summoner_name + ' no encontrado'


	def getResponse( self, url ):
		request  = urllib2.Request( url, headers = self.headers )
		response = urllib2.urlopen( request )
		response = response.read()

		return json.loads( response )


	def getHaveChest( self, summoner_name, champ_name ):
		url = 'https://euw1.api.riotgames.com/lol/static-data/v3/champions?champListData=tags&tags=tags&dataById=true'
		request  = urllib2.Request( url, headers = self.headers )
		response = urllib2.urlopen( request )
		response = response.read()

		json_response = json.loads( response )

		json_response = json_response[ 'data' ]

		chmp_idx = 0

		for idx, champ in json_response.iteritems(): # Iterador JSON
			if champ_name == champ[ 'name' ]:
				chmp_idx = idx


		url = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summoner_name
		request  = urllib2.Request( url, headers = self.headers )
		response = urllib2.urlopen( request )
		response = response.read()

		json_response = json.loads( response )

		summoner_id = json_response[ 'id' ]

		url = 'https://euw1.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/' + (str)(summoner_id)
		request  = urllib2.Request( url, headers = self.headers )
		response = urllib2.urlopen( request )
		response = response.read()

		json_response = json.loads( response )

		for champ in json_response:
			if champ[ 'championId' ] == (int)(chmp_idx):
				return ( 'Caja conseguita' if champ[ 'chestGranted' ] else 'Caja no conseguita' )

		return 'No dispones del campeón'
