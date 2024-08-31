# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 21:30:05 2020

@author: ALegaz
"""
import turtle

print("\nEjemplo 1 con Turtle:\n")

j = 6

for i in range(j):
    turtle.forward(200/j)
    turtle.right(-360/j)

turtle.done() # <------------