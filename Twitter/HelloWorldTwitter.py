# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:55:06 2021

HelloWorldBotChulo

    Requerimientos:
        pip install tweepy

@author: alvar
"""
import sys
import tweepy
import requests


#Llaves del API Tweeter
consumer_key = 'AEGK4pzjVEvnA5WcdAbiVk23Y'
consumer_secret ='twvXzFSrKKIWX2PN8AwHX9slrcNEh92qhdhuyZkLKDsdDKuWgg'
access_token ='101906747-RMP92KsRl6eE3hUrgPuKegiztiCfdIzduejpe5Qy'
secret = '2J8laXBvzmMgsy5mq1OAePmvXfs6Dah9BDsVIXCDcoxTu'

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self,status):#Procesa nuevos tweets
        if not hasattr(status, 'retweeted_status'):#ignora retweets
            print("=== Nuevo tweet ===")
            print("Nombre:"+status.user.name)
            print("Txt:" +status.text)
            print("Fecha:"+str(status.created_at))
            print()
            
    
    def on_error(self,status_code):
        print("Ocurrió un error")
        return False

tauth = tweepy.OAuthHandler(consumer_key,consumer_secret) #Autenticar
tauth.set_access_token(access_token,secret)
streamListener = MyStreamListener()
twStream = tweepy.Stream(auth = tauth,listener =streamListener)

#Especificar el filtro
twStream.filter(track=['Manowar'])