"""
dinamica_vehiculo.py
Dinámica traslacional 2D (plano x–z, z hacia arriba) de un cohete.
Unidades: SI
"""

import math
import fuerzas_aerodinamicas as fa  # requiere: g(h), empuje(...), arrastre(...)

# ------------------------------------------------------------
# Masa instantánea (consumo lineal medio)
# ------------------------------------------------------------
def masa_instantanea(veh: dict, t: float) -> float:
    """
    veh: dict con claves:
        'm_seco' [kg], 'm_prop' [kg], 'tiempo_quemado' [s]
    """
    t = max(0.0, float(t))
    m_prop0 = float(veh["m_prop"])
    tburn   = float(veh["tiempo_quemado"])
    mdot    = (m_prop0 / tburn) if tburn > 0.0 else 0.0
    m_prop  = max(m_prop0 - mdot * t, 0.0)
    return float(veh["m_seco"]) + m_prop

# ------------------------------------------------------------
# Dinámica (fuerzas → aceleraciones)
# ------------------------------------------------------------
def dinamica_vehiculo(pitch: float,
                      porcentaje_empuje: float,
                      estado: dict,
                      veh: dict,
                      Cd_val: float | None = None) -> dict:
    """
    Entradas:
      - pitch: ángulo del vehículo [rad] (≈ gamma si no modelas AoA)
      - porcentaje_empuje: factor 0..1
      - estado: dict {'t':[s], 'altitud':[m], 'velocidad':[m/s]}
      - veh: dict {
            'm_seco':[kg], 'm_prop':[kg], 'Aref':[m^2],
            'empuje_vacio':[N], 'empuje_nivel_mar':[N], 'tiempo_quemado':[s]
        }
      - Cd_val: opcional; si se da, se usa ese Cd en el cálculo de D.

    Devuelve dict con:
      {'ax','az','T','D','m','g','Vx','Vz','gamma'}
    """
    # Estado
    t = float(estado["t"])
    h = max(0.0, float(estado["altitud"]))
    V = max(0.0, float(estado["velocidad"]))

    # Masa y gravedad
    m = max(masa_instantanea(veh, t), 1e-9)  # evita división por cero
    g = fa.gravedad(h)

    # Throttle robusto
    thr = min(1.0, max(0.0, float(porcentaje_empuje)))

    # Empuje (con corrección por presión ambiente implementada en fa.empuje)
    T = fa.empuje(
        float(veh["empuje_vacio"]),
        float(veh["empuje_nivel_mar"]),
        float(veh["tiempo_quemado"]),
        thr,
        h,
        t
    )


    D = fa.arrastre(h, V, area_efectiva=float(veh["Aref"]))

    # Ángulo de trayectoria (≈ actitud)
    gamma = float(pitch)

    # Componentes de velocidad
    Vx = V * math.cos(gamma)
    Vz = V * math.sin(gamma)

    # Proyección del arrastre opuesta a V
    if V > 1e-9:
        invV = 1.0 / V
        Dx = D * (Vx * invV)
        Dz = D * (Vz * invV)
    else:
        Dx = 0.0
        Dz = 0.0

    # Ecuaciones de movimiento (traslación)
    ax = (T * math.cos(gamma) - Dx) / m
    az = (T * math.sin(gamma) - Dz - m * g) / m

    return {
        "ax": ax, "az": az,
        "T": T, "D": D, "m": m, "g": g,
        "Vx": Vx, "Vz": Vz, "gamma": gamma
    }
