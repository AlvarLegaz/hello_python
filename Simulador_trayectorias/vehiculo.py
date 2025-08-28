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

        # Empuje (con corrección por presión ambiente implementada en fa.empuje)
        T = fa.empuje(self.empuje_vacio, self.empuje_nivel_mar, self.tiempo_quemado, thr, h, t)
      
        # Peso y masa
        m = max(self.masa_instantanea(t), 1e-9)  # evita división por cero
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
    def masa_instantanea(self, t: float) -> float:
        """
        veh: dict con claves:
            'm_seco' [kg], 'm_prop' [kg], 'tiempo_quemado' [s]
        """
        t = max(0.0, float(t))
        m_prop0 = self.m_prop
        tburn   = self.tiempo_quemado
        mdot    = (m_prop0 / tburn) if tburn > 0.0 else 0.0
        m_prop  = max(m_prop0 - mdot * t, 0.0)
        return self.m_seco + m_prop