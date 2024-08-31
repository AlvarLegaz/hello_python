# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:32:03 2024

@author: id2int

@brief: script para calcular datos vuelo Kerbal Space Program

"""

# Data

g = 9.8

# Command module> Mk1 Command Pod

Mass_Module = 0.84e3

#RT-5 "Flea" Solid Fuel Booster Engine data: 
Mass_Engine_Full = 1.50e3
Mass_Engine_Empty = 0.45e3
Mass_Propellant = Mass_Engine_Full - Mass_Engine_Empty
Thrust = 162.90e3
Burn_Time = 8.8

# LV-T30 "Reliant" Liquid Fuel Engine + #FL-T800
Mass_Engine_Empty = 1.5e3
Thrust = 205.16e3
Mass_Propellant = 4.5e3;
Burn_Time = 51



# Calculos> Aproximación fácil suponemos masa de combustible al 50%

#Mass_Laucher = Mass_Module + Mass_Engine_Full;
Corr_factor = 0.2
Mass_Laucher = Mass_Module + Mass_Engine_Empty + Corr_factor*Mass_Propellant;
print("Mass Launcher = " + str(Mass_Laucher))
print("Correction factor = " + str(Corr_factor))

print(" ")

Drag = Mass_Laucher * g
Lift_Force = Thrust - Drag
Lift_acceletarion =  Lift_Force/Mass_Laucher
print("Lift acceleration = " + str(Lift_acceletarion))

Speed_at_MECO = Lift_acceletarion*Burn_Time;
Height_at_MECO = Lift_acceletarion*(Burn_Time**2)/2;

print("Speed at MECO (m/s) = " + str(Speed_at_MECO))
print("Height at MECO (m) = " + str(Height_at_MECO))

print(" ")

Time_From_MECO_to_0speed = Speed_at_MECO/g;
Max_Lift_Time = Burn_Time + Speed_at_MECO/g;
print("Max Lift Time = " + str(Max_Lift_Time))

Apoapsis = Height_at_MECO + Speed_at_MECO*Time_From_MECO_to_0speed - g * (Time_From_MECO_to_0speed**2)/2
print("Apoapsis(m) = " + str(Apoapsis))
