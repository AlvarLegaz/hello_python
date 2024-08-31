#Actividad 2. Hacer un dibujo. Soraya Dos Santos Carrillo.

import turtle

turtle.title("Nos vigilan")
turtle.bgcolor("midnight blue")
turtle.speed(100)

#A. Objeto nave
#A1. Objeto base nave
turtle.penup()
turtle.goto(-250,0)
turtle.pendown()
def draw(rad): 
  for i in range(2):    
    turtle.begin_fill()
    turtle.pencolor("slate gray")
    turtle.fillcolor("slate gray")
    turtle.circle(rad,90) 
    turtle.circle(rad//2,90) 
    turtle.end_fill()
turtle.seth(-45)  
draw(170)

#A2. Luces
turtle.penup()
turtle.goto(-143,-35)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("yellow")
turtle.fillcolor("yellow")
turtle.circle(20)
turtle.end_fill()

turtle.penup()
turtle.goto(-75,-15)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("yellow")
turtle.fillcolor("yellow")
turtle.circle(20)
turtle.end_fill()

turtle.penup()
turtle.goto(-210,-15)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("yellow")
turtle.fillcolor("yellow")
turtle.circle(20)
turtle.end_fill()

turtle.penup()
turtle.goto(-25,30)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("yellow")
turtle.fillcolor("yellow")
turtle.circle(20)
turtle.end_fill()

turtle.penup()
turtle.goto(-260,25)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("yellow")
turtle.fillcolor("yellow")
turtle.circle(20)
turtle.end_fill()

#A3.objeto cúpula nave
turtle.pensize(2)

turtle.penup()
turtle.goto(-195,70)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("deep sky blue")
turtle.fillcolor("light blue")
turtle.circle(90)
turtle.end_fill()

#A4.objeto marcianito
#A4.1. Cuerpo
turtle.penup()
turtle.goto(-160,55)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("lime green")
turtle.fillcolor("lime green")
turtle.circle(40)
turtle.end_fill()

#A4.2. Cabeza
turtle.penup()
turtle.goto(-153,130)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("lime green")
turtle.fillcolor("lime green")
turtle.circle(30)
turtle.end_fill()

#A4.3. Antenas
turtle.pensize(3)

turtle.penup()
turtle.goto(-153,170)
turtle.pendown()

turtle.pencolor("lime green")
turtle.right(-150)
turtle.forward(20)

turtle.pensize(3)

turtle.penup()
turtle.goto(-110,170)
turtle.pendown()

turtle.pencolor("lime green")
turtle.left(-45)
turtle.forward(20)

#A4.4. Puntas antenas 
turtle.penup()
turtle.goto(-158,190)
turtle.pendown()

from turtle import *
fillcolor("lime green")
pencolor("lime green")
begin_fill()
for i in range(3):
    forward(20)
    left(120)
end_fill()

turtle.penup()
turtle.goto(-99,188)
turtle.pendown()

from turtle import *
fillcolor("lime green")
pencolor("lime green")
begin_fill()
for i in range(3):
    forward(20)
    left(120)
end_fill()

#A5. Ondas
turtle.pencolor("white")
turtle.pensize(2)

turtle.penup()
turtle.goto(-85,-130)
turtle.pendown()

turtle.pencolor("white")
turtle.circle(50)

turtle.penup()
turtle.goto(-75,-190)
turtle.pendown()

turtle.pencolor("white")
turtle.circle(60)

turtle.penup()
turtle.goto(-65,-260)
turtle.pendown()

turtle.pencolor("white")
turtle.circle(70)

turtle.penup()
turtle.goto(-55,-340)
turtle.pendown()

turtle.pencolor("white")
turtle.circle(80)

turtle.penup()
turtle.goto(-45,-420)
turtle.pendown()

turtle.pencolor("white")
turtle.circle(90)

#B.Dibujo objeto luna
turtle.penup()
turtle.goto(350,180)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("white")
turtle.fillcolor("white")
turtle.circle(100)
turtle.end_fill()

turtle.penup()
turtle.goto(300,180)
turtle.pendown()

turtle.begin_fill()
turtle.pencolor("midnight blue")
turtle.fillcolor("midnight blue")
turtle.circle(100)
turtle.end_fill()

turtle.penup()
turtle.goto(-170,100)
turtle.pendown()

#C. Estrellas
#C1. Estrella 1
turtle.penup()
turtle.goto(170,100)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(50)
    turtle.right(144)
turtle.end_fill()

#C2. Estrella 2
turtle.penup()
turtle.goto(300,-350)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(70)
    turtle.right(144)
turtle.end_fill()

#C3. Estrella 3
turtle.penup()
turtle.goto(-400,-250)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(40)
    turtle.right(144)
turtle.end_fill()

#C4. Estrella 4
turtle.penup()
turtle.goto(-420,-100)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(20)
    turtle.right(144)
turtle.end_fill()

#C5. Estrella 5
turtle.penup()
turtle.goto(-410,300)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(50)
    turtle.right(144)
turtle.end_fill()

#C6. Estrella 6
turtle.penup()
turtle.goto(-79,250)
turtle.pendown()

turtle.pencolor("yellow")

turtle.begin_fill()
turtle.fillcolor("lemon chiffon")
for i in range(5):
    turtle.forward(70)
    turtle.right(144)
turtle.end_fill()

#D. Estrella fugaz
#D1. Estrella
turtle.penup()
turtle.goto(180,-250)
turtle.pendown()

turtle.begin_fill()
turtle.fillcolor("gold")
turtle.pencolor("gold")
for i in range(5):
    turtle.forward(150)
    turtle.right(144)
turtle.end_fill()

#D2. Líneas fugaces
turtle.pensize(5)
turtle.pencolor("gold")

for i in range(3):
    if i == 1:
        turtle.penup()
        turtle.goto(80-i*90,-20-i*60)
        turtle.pendown()
        turtle.goto(230-i*90,-90-i*60)
    else:
        turtle.penup()
        turtle.goto(80-i*60,-20-i*60)
        turtle.pendown()
        turtle.goto(230-i*60,-90-i*60)

turtle.done() 

