# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:55:06 2021

HelloWorldBotChulo

    Requerimientos:
        pip install tweepy

@author: alvar
"""

import tweepy

#Claves del API Tweeter
consumer_key = 'AEGK4pzjVEvnA5WcdAbiVk23Y'
consumer_secret ='twvXzFSrKKIWX2PN8AwHX9slrcNEh92qhdhuyZkLKDsdDKuWgg'
access_token ='101906747-5eVs1WgOePZSCkg331B4aWoH0m59YbMwAeoxpzl2'
secret = 'vDOjDxksXEv0BrzPo9Jr8ZzFMxIf72BNObhJefQbfeT6A'


tauth = tweepy.OAuthHandler(consumer_key,consumer_secret) #Autenticar
tauth.set_access_token(access_token,secret)

api = tweepy.API(tauth)


img = open("img01.png", 'rb')
id_imagen = api.media_upload("img01.png")
print(id_imagen)


#!Publicar tweet
#!api.update_status('Hola mundo desde Tweepy :P')

#!Publicar tweet con imagen
api.update_status('@Roccobott eres una looser, yo ya twitteo desde python :P Y CON IMAGENES',media_ids=[id_imagen.media_id_string])

#!Publicar tweet respondiendo a otro tweet
#!api.update_status('funcionará la imagen?', in_reply_to_status_id="1420818345109110792")
