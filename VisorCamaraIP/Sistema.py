# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:27:28 2020

@author: Vonliendres
"""
from time import sleep
from time import time

class Esperas:
    def espera_ms(mseg):
        
        start_time = time()
        
        for i in range(1, mseg, 1):
            elapsed_time = (time()-start_time)
            if(elapsed_time>(mseg/1000)):
                print("                                                       ")
                return
            if(i%2==0):
                print("//////",end="\r")
                sleep(10/1000)
            else:
                print("------",end="\r")
                sleep(10/1000)
                
            
            
            