# -*- coding: utf-8 -*-
"""
Porgama para mostrar una cadena de texto un número de repeticiones

    Cadena y repeticiones se introducen por usuario
    Estructura de control Bucle While
"""

print("Ejemplo 1: repeticion de una cadena mediante bucle while.")

print("\nIntroduzca un texto:")
cadena = input();
print("\n¿Cuántas veces quiere que se repita?")
repeticiones = int(input());
print("\nMostrando cadena ...")

i = 0;
while i < repeticiones:
    print(cadena);
    i += 1;
    
print("\nPrograma terminado");