#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.Riot import Riot

from config.Params import Params

riot = Riot( Params.key, 'Horuser' )

riot.getSummonerInfo()