# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:21:27 2024

@author: ALegaz
"""

class Spacecraft:
    
    def __init__(self, name, model, posX, posY, posZ):
        self.name = str(name);
        self.model = str(model)
        self.posX = int(posX)
        self.posY = int(posY)
        self.posZ = int(posZ)
    
    def setThrust(self val):
        self.thurst = int (val)
    
    def setFlightPath(self, alpha, bravo, charlie)
        self.alpha = alpha
    
    def update():
    