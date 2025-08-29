"""
Modulo: dinamica_vehiculo.py
Descripción: Dinámica traslacional 2D (plano x–z, z hacia arriba) de un cohete.
Unidades: SI

Autor: Álvar Ginés Legaz Aparicio
"""

import math
import fuerzas_aerodinamicas as fa  # requiere: g(h), empuje(...), arrastre(...)

class Vehiculo:

    def __init__(self, datos_vehiculo):
        self.empuje_vacio = float(datos_vehiculo["empuje_vacio"])
        self.empuje_nivel_mar= float(datos_vehiculo["empuje_nivel_mar"])
        self.tiempo_quemado = float(datos_vehiculo["tiempo_quemado"])
        self.area_efectiva = float(datos_vehiculo["Aref"])
        self.m_seco = float(datos_vehiculo["m_seco"])
        self.m_prop = float(datos_vehiculo["m_prop"])
        self.m_prop_max = float(datos_vehiculo["m_prop"]) 

    # ------------------------------------------------------------
    # Dinámica (fuerzas → aceleraciones)
    # Control del vehículo a trevés de pitch y procentaje_empuje
    # Posicion actual
    # ------------------------------------------------------------
    def dinamica_vehiculo(self, pitch: float, porcentaje_empuje: float, estado: dict):
        # Control del vehículo con ángulo de trayectoria (≈ actitud) y porcentaje empuje
        thr =  max(0.0, float(porcentaje_empuje))
        gamma = float(pitch)

        # Estado actual
        t = float(estado["t"])
        h = max(0.0, float(estado["altitud"]))
        Vz = max(0.0, float(estado["Vz"]))
        Vx = max(0.0, float(estado["Vx"]))
        V = math.sqrt(Vx**2 + Vz**2)
        dt = float(estado["dt"])

        # Empuje (con corrección por presión ambiente implementada en fa.empuje)
        T = fa.empuje(self.empuje_vacio, self.empuje_nivel_mar, self.tiempo_quemado, thr, self.m_prop,h)
      
        # Peso y masa
        m = max(self.masa_instantanea(dt, porcentaje_empuje), 1e-9)  # evita división por cero
        W= fa.peso(h, m)

        # Arrastre (con corrección por presión ambiente implementada en fa.empuje)
        if V > 1e-9:
            invV = 1.0 / V
            Dx = fa.arrastre_x(h, Vx, V, self.area_efectiva)
            Dz = fa.arrastre_z(h, Vz, V, self.area_efectiva)
        else:
            Dx = 0.0
            Dz = 0.0

        # Ecuaciones de movimiento (traslación)
        ax = (T * math.cos(gamma) - Dx) / m
        az = (T * math.sin(gamma) - Dz - W) / m

        return {"ax": ax, "az": az, "T": T, "Dz": Dz, "Dx": Dx, "W": W, "m": m, "gamma": gamma}

    # ------------------------------------------------------------
    # Masa instantánea (consumo lineal medio)
    # ------------------------------------------------------------
    def masa_instantanea(self, dt: float, porcentaje_empuje) -> float:
        """
        veh: dict con claves:
            'm_seco' [kg], 'm_prop' [kg], 'tiempo_quemado' [s]
        """
       
        tburn   = self.tiempo_quemado
        mdot    = (porcentaje_empuje/100)*(self.m_prop_max / tburn) 
        self.m_prop  = max(self.m_prop - mdot * dt, 0.0)
        #print(f"Tiempo quemado at {tburn:.2f} dt = {dt:.2f}º")
        return self.m_seco + self.m_prop
    
    def porcentaje_combustible(self):
        #print(f"Porcentaje quemado {(self.m_prop/self.m_prop_max)*100:.2f}")
        return (self.m_prop/self.m_prop_max)*100
        