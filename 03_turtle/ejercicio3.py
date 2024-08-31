# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 18:41:23 2020

@author: ALegaz
"""


import turtle

print("\nEjemplo 3 con Turtle:\n")

turtle.bgcolor("red")

turtle.begin_fill()
turtle.pencolor("purple")
turtle.fillcolor("orange")
turtle.pensize(5)
turtle.circle(60)
turtle.end_fill()


turtle.penup()
turtle.left(-45)
turtle.forward(150)
turtle.pendown()
turtle.begin_fill()
turtle.pencolor("blue")
turtle.fillcolor("green")
turtle.pensize(5)

for i in range(5):
    turtle.circle(10*i)
turtle.end_fill()


turtle.done() # <------------
