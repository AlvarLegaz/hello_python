"""
Modulo: dinamica_vehiculo.py
Descripción: Escenario donde se va a mover el vehículo
Unidades: SI

Autor: Álvar Ginés Legaz Aparicio
"""

import math
import fuerzas_aerodinamicas as fa
import vehiculo as dv
import matplotlib.pyplot as plt  # <-- para la gráfica
from datos_vehiculos import VEHICULOS

class Escenario:
    def __init__(self, nombre_vehiculo="testV"):
        self.veh = VEHICULOS[nombre_vehiculo]  # carga el diccionario del vehículo elegido

        # -------------------------------
        # Estado inicial
        # -------------------------------
        
        t0 = 0.0           # s
        h0 = 0           # m (altitud)
        x0 = 0           # m (distancia)
        Vx = 0.0           # m/s (reposo)
        Vz = 0.0           # m/s (reposo)

        self.t = t0
        self.h = h0
        self.xx = x0
        self.vx = Vx
        self.vz = Vz
        
        self.vehiculo = dv.Vehiculo(self.veh)

        self.historia =[]

    def reset(self):
        # -------------------------------
        # Estado inicial
        # -------------------------------
        t0 = 0.0           # s
        h0 = 0           # m (altitud)
        x0 = 0           # m (distancia)
        Vx = 0.0           # m/s (reposo)
        Vz = 0.0           # m/s (reposo)

        self.t = t0
        self.h = h0
        self.xx = x0
        self.vx = Vx
        self.vz = Vz

        self.vehiculo = dv.Vehiculo(self.veh)

        self.historia =[]
    
    def update(self, pitch, porcentaje_empuje, dt):

        estado = {"t": self.t, "altitud": self.h, "Vz": self.vx, "Vx": self.vz}
        pitch = pitch

        # Fuerzas/aceleraciones en estado actual
        out = self.vehiculo.dinamica_vehiculo(pitch, porcentaje_empuje, estado)
        ax = out["ax"]
        az = out["az"]
        T  = out["T"]
        Dx  = out["Dx"]
        Dz  = out["Dz"]
        W = out["W"]
        m = out["m"]

        # Predicción (semi-implícito en posición para algo más de estabilidad)
        vx_next = self.vx + ax * dt
        vz_next = self.vz + az * dt
        xx_next = self.xx + vx_next * dt
        h_next  = self.h  + vz_next * dt
        t_next  = self.t  + dt

        # -----------------------------
        # Eventos dentro del paso
        # -----------------------------
        # 1) Pasado en el suelo sin empuje
        if self.h == 0 and h_next <= 0.0:
            V  = math.hypot(self.vx, self.vz)
        # 2) Impacto con suelo: cruza h=0 del lado positivo
        elif self.h > 0.0 and h_next <= 0.0:
            V  = math.hypot(self.vx, self.vz)
            qi = fa.q(self.h, V)
            print(f"Impacto con el suelo en t={self.t:.2f} s")
            raise RuntimeError(f"Impacto con el suelo en t={self.t:.2f} s, V={V:.2f} m/s, q={qi:.2f} Pa")
        else:
            self.vx = vx_next
            self.vz = vz_next
            self.xx = xx_next
            self.h = h_next
            self.t = t_next 
        
        # Nivel combustible
        fuel_var = self.vehiculo.porcentaje_combustible()

        self.historia.append({"tiempo":self.t, "altitud":self.h, "distancia":self.xx, "vx":self.vx, "vz":self.vz, "ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m, "pitch":pitch, "nivel_combustible":fuel_var})
        
        return {"tiempo":self.t, "altitud":self.h, "distancia":self.xx, "vx":self.vx, "vz":self.vz, "ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m, "pitch":pitch, "nivel_combustible":fuel_var}
    
    def obtener_datos_vuelo(self):
        return self.historia


