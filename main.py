#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.Params import Params
from src.Riot import Riot

import telebot
import os
from telebot import types

tb = telebot.TeleBot( Params.token_telegram ) 
riot = Riot( Params.key, Params.tmp_folder )

@tb.message_handler(commands=['start'])
def handle_start_help(message):
	mensaje = '<b>Bienvenido al canal League of Laughs, esperemos que te sea de utilidad ;)</b>'
	tb.send_message( message.chat.id, mensaje, parse_mode = 'HTML' )

@tb.callback_query_handler(func=lambda call: True)
def test_callback(call):
	global participaciones, premiado, usuario_premiado

	if call.from_user.username == usuario_premiado:
		premiado = True
		tb.send_message( call.from_user.id, '<b>Felicidades has sido premiad@</b>'+os.linesep +'Escribanos su email para ponernos en contacto con usted en las próximas 48h.', parse_mode = 'HTML' )
	else:
		if premiado == False:
			if call.from_user.id in participaciones:
				tb.send_message( call.from_user.id, 'Ya ha realizado la participación en el sorteo, vuelva a intentarlo en el próximo.' )
			else:
				participaciones.append(call.from_user.id)
				tb.send_message( call.from_user.id, 'Lo sentimos no ha tenido suerte, vuelve a intentarlo en el próximo sorteo.' )
		else:
			tb.send_message( call.from_user.id, 'Ya tenemos ganador, vuelva a intentarlo en el próximo sorteo.' )

@tb.message_handler(commands=['summoner'])
def handle_text_doc(message):
	summoner = message.text.split(' ', 1)[1]
	reponse_riot = riot.getSummonerInfo( summoner )
	# print( message.from_user.id+': '+message.text )
	# print( json_dumps( message.from_user ) )
	tb.send_message( message.from_user.id, reponse_riot )

@tb.message_handler(commands=['chest'])
def handle_text_doc(message):
	if len( message.text.split(' ') ) == 3:
		mensaje = message.text.split(' ', 1)[1]
		summoner_name = mensaje.split(' ', 1)[0]
		champ_name = mensaje.split(' ', 1)[1]

		reponse_riot = riot.getHaveChest( summoner_name, champ_name )

		tb.send_message( message.from_user.id, reponse_riot )
	else:
		tb.send_message( message.from_user.id, 'Mala solicitud' )


tb.polling(none_stop=True)
