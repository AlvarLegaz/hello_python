# -*- coding: utf-8 -*-

print("\nIntroduzca un texto:")
mensaje = input();

print ("La cadena es:"+mensaje)

print("Muestro desde que encuentre la letra a:")

encontrada = False

for i in range(len(mensaje)):
    if(mensaje[i]=='a'):
        encontrada=True
    if(encontrada==True):    
        print(mensaje[i],end="");
    
