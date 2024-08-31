# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 19:03:09 2020

@author: ALegaz
"""


import turtle

print("\nEjercicio con Turtle:\n")

turtle.bgcolor("black")
turtle.speed(100)


# < Dibujo objeto luna
turtle.penup()
turtle.goto(200,100)
turtle.pendown()


turtle.begin_fill()
turtle.fillcolor("white")
turtle.circle(60)
turtle.end_fill()

turtle.goto(170,100)

turtle.begin_fill()
turtle.fillcolor("black")
turtle.circle(60)
turtle.end_fill()

# < Dibujo objeto estrella 1
turtle.penup()
turtle.goto(-170,100)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("yellow")
for i in range(5):
    turtle.forward(100)
    turtle.right(144)
turtle.end_fill()

# < Dibujo objeto estrella 2
turtle.penup()
turtle.goto(-250,150)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("yellow")
for i in range(5):
    turtle.forward(50)
    turtle.right(144)
turtle.end_fill()

# < Dibujo objeto estrella fugaz: estrella
turtle.penup()
turtle.goto(180,-150)
turtle.pendown()

turtle.begin_fill()
turtle.fillcolor("yellow")
for i in range(5):
    turtle.forward(150)
    turtle.right(144)
turtle.end_fill()


# < Dibujo objeto estrella fugaz: lineas fugaces
turtle.pensize(5)


turtle.penup()
turtle.goto(80,-20)
turtle.pendown()
turtle.goto(230,-90)

turtle.penup()
turtle.goto(40,-160)
turtle.pendown()
turtle.goto(190,-230)

turtle.penup()
turtle.goto(10,-80)
turtle.pendown()
turtle.goto(160,-150)

turtle.done() 