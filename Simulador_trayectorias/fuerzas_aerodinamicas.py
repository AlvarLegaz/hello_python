"""
Modulo: fuerzas_aerodinamicas.py
Descripción: Funciones que modelan fuerzas aerodinámicas en vuelo de un cohete
Autor: Álvar Ginés Legaz Aparicio

IMPORTANTE: LAS MAGNITUDES SIEMPRE EN SISTEMA INTERNACIÓNAL.
"""

import math

g0 = 9.80665 # gravedad estándar [m/s²]
Re = 6371e3 # radio terrestre [m]
rho0 = 1.225 # densidad a nivel del mar [kg/m³]
H = 7200.0 # escala atmósfera [m]
p0 = 101325.0 # presión al nivel del mar [Pa]


def empuje(empuje_vacio, empuje_nivel_mar, tiempo_quemado, procentaje_empuje, altitud, tiempo_vuelo):
    Ae = (empuje_vacio - empuje_nivel_mar)/p0
    if tiempo_vuelo < tiempo_quemado:
        return empuje_nivel_mar
    else:
        return 0


def arrastre(altitud, velocidad, area_efectiva):
    return 0.5*rho(altitud)*(velocidad**2)*Cd(altitud, velocidad)*area_efectiva


def peso(altitud, masa):
    g_actual = g0 * (Re / (Re + altitud))**2
    return masa*g_actual


def Cd(altitud, velocidad):
    #Modelo muy simplificado
    linea_karman = 100e3; #Line a de Karman- pasado esto suponemos no atmósfera
    if altitud < linea_karman:
        return 0.25
    else:
        return 0

def gravedad(altitud):
    return g0 * (Re / (Re + altitud))**2

# Estrés aerodinamico
def q(altitud, velocidad):
    return 0.5*rho(altitud)*(velocidad**2)
    

# Modelo presión
def pa(altitud, velocidad): # presión ambiente
    return p0 * math.exp(-altitud/H)


# Modelo densidad
def rho(altitud): 
    return rho0 * math.exp(-altitud/H)

