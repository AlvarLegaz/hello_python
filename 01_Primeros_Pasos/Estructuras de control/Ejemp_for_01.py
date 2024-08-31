# -*- coding: utf-8 -*-
"""
Porgama para mostrar una cadena de texto un número de repeticiones

    Cadena y repeticiones se introducen por usuario
    Estructura de control Bucle For
"""

print("Ejemplo 1: repeticion de una cadena mediante bucle For.")

print("\nIntroduzca un texto:")
cadena = input();

print("\n¿Cuántas veces quiere que se repita?")
repeticiones = int(input());

print("\nMostrando cadena ...")


for i in range(repeticiones):
    print(cadena);

    
print("\nPrograma terminado");