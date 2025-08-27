# trayectoria.py
# Integración iterativa de la trayectoria 2D (plano x–z, z hacia arriba) de un cohete.
# Unidades: SI

import math
import csv
import sys  # <-- para mostrar progreso en la misma línea
import fuerzas_aerodinamicas as fa
import dinamica_vehiculo as dv
import matplotlib.pyplot as plt  # <-- para la gráfica

# -------------------------------
# Configuración del vehículo
# -------------------------------
veh = {
    "m_seco": 500.0,                 # kg
    "m_prop": 1500.0,                # kg
    "Aref": math.pi * (0.5**2),     # m^2 (Ø=1 m)
    "empuje_vacio": 160_000.0,       # N
    "empuje_nivel_mar": 158_000.0,   # N
    "tiempo_quemado": 51.0          # s
}

# -------------------------------
# Estado inicial
# -------------------------------
t0 = 0.0           # s
h0 = 0           # m (altitud)
V0 = 0.0           # m/s (reposo)
gamma0_deg = 90.0  # deg (vertical)
gamma0 = math.radians(gamma0_deg)

# Componentes iniciales de velocidad
Vx = V0 * math.cos(gamma0)
Vz = V0 * math.sin(gamma0)

# Posición horizontal inicial
x = 0.0  # m

# -------------------------------
# Leyes de guiado (puedes editarlas)
# -------------------------------
def ley_pitch(t, h):
    if t < 2.0:
        deg = 90.0
    elif t < 12.0:
        f = (t - 2.0) / 10.0  # 0..1
        deg = 90.0 + (45.0 - 90.0) * f
    else:
        deg = 45.0
    return math.radians(deg)

def ley_throttle(t, h):
    return 1.0

# -------------------------------
# Utilidad: impresión de progreso
# -------------------------------
def _print_progress(frac, t, t_max):
    """
    Muestra progreso en una sola línea: 0..100%.
    frac en [0,1].
    """
    pct = max(0.0, min(100.0, 100.0 * frac))
    sys.stdout.write(f"\rProgreso: {pct:6.2f}%  (t = {t:7.2f} s / {t_max:7.2f} s)")
    sys.stdout.flush()

# -------------------------------
# Integrador: paso a paso (Euler explícito)
# -------------------------------
def simular(dt=0.01, t_max=60.0):
    """
    Devuelve la lista 'historia' con los estados temporales.
    Bucle: while (t <= t_max) or (h > 0.0)
    """

    t = t0
    h = h0
    vx = Vx
    vz = Vz
    xx = x

    historia = []

    # Max-Q en subida
    qmax_up = 0.0
    t_qmax_up = 0.0
    h_qmax_up = 0.0


    en_subida = True  # antes del apogeo

    # --- Bucle principal ---
    while (t <= t_max) or (h > 0.0):
        # Estado actual
        V = math.hypot(vx, vz)
        gamma = math.atan2(vz, vx) if V > 1e-12 else ley_pitch(t, h)
        estado = {"t": t, "altitud": h, "velocidad": V}
        pitch = ley_pitch(t, h)
        throttle = ley_throttle(t, h)

        # Fuerzas/aceleraciones en estado actual
        out = dv.dinamica_vehiculo(pitch, throttle, estado, veh)
        ax = out["ax"]; az = out["az"]
        T  = out["T"];  D  = out["D"]
        m  = out["m"];  g  = out["g"]

        # Métrica: q en estado actual
        qi = fa.q(h, V)

        # Max-Q por fase
        if en_subida:
            if qi > qmax_up:
                qmax_up, t_qmax_up, h_qmax_up = qi, t, h

        # --- Registro del estado ACTUAL (antes del paso) ---
        historia.append({
            "t": t, "x": xx, "h": h, "V": V,
            "vx": vx, "vz": vz, "az": az, "pitch": pitch, "gamma": gamma,
            "T": T, "D": D, "m": m, "g": g, "q": qi
        })

        # Si ya hemos superado t_max y estamos a nivel del suelo, salimos
        if (t > t_max) and (h <= 0.0):
            break

        # Predicción (semi-implícito en posición para algo más de estabilidad)
        vx_next = vx + ax * dt
        vz_next = vz + az * dt
        xx_next = xx + vx_next * dt
        h_next  = h  + vz_next * dt
        t_next  = t  + dt

        # -----------------------------
        # Eventos dentro del paso
        # -----------------------------

        # 1) Impacto con suelo: cruza h=0 del lado positivo
        if h > 0.0 and h_next <= 0.0:
            tau = h / (h - h_next)            # fracción del paso hasta h=0
            dt_hit = tau * dt

            # Interpola dinámicamente a t_hit
            vx_hit = vx + ax * dt_hit
            vz_hit = vz + az * dt_hit
            x_hit  = xx + vx_hit * dt_hit
            t_hit  = t  + dt_hit

            # Fija estado final coherente en el suelo
            t, xx, h, vx, vz = t_hit, x_hit, 0.0, vx_hit, 0.0
            V  = math.hypot(vx, vz)
            qi = fa.q(h, V)

            # Sustituye el último registro por el de contacto exacto
            historia[-1] = {
                "t": t, "x": xx, "h": h, "V": V,
                "vx": vx, "vz": vz, "az": az, "pitch": pitch, "gamma": gamma,
                "T": T, "D": D, "m": m, "g": g, "q": qi
            }

            print(f"Impacto con el suelo en t={t:.2f} s")
            break

        # 2) Apogeo: motor apagado y cambio de signo en vz (de + a <= 0)
        if (T <= 0.0) and (vz > 0.0) and (vz_next <= 0.0):
            tau = vz / (vz - vz_next)         # fracción del paso hasta vz=0
            dt_peak = tau * dt

            vx_peak = vx + ax * dt_peak
            vz_peak = 0.0
            x_peak  = xx + vx_peak * dt_peak
            h_peak  = h  + vz * dt_peak + 0.5 * az * dt_peak * dt_peak
            t_peak  = t  + dt_peak

            # Fija estado en apogeo
            t, xx, h, vx, vz = t_peak, x_peak, h_peak, vx_peak, vz_peak
            V = math.hypot(vx, vz)
            qi = fa.q(h, V)

            historia[-1] = {
                "t": t, "x": xx, "h": h, "V": V,
                "vx": vx, "vz": vz, "az": az, "pitch": pitch, "gamma": gamma,
                "T": T, "D": D, "m": m, "g": g, "q": qi
            }

            # Cambiamos a fase de bajada
            en_subida = False
            print(f"Apogeo alcanzado en t={t:.2f} s, h={h:.1f} m")
            # (continuamos hasta impacto o t_max)

        # 3) Tiempo máximo: si el siguiente paso excede t_max y seguimos por encima del suelo
        if t_next > t_max and h_next >= 0.0:
            tau = (t_max - t) / dt
            vx = vx + ax * (tau * dt)
            vz = vz + az * (tau * dt)
            xx = xx + vx * (tau * dt)
            h  = h  + vz * (tau * dt)
            t  = t_max
            V  = math.hypot(vx, vz)
            qi = fa.q(h, V)

            historia.append({
                "t": t, "x": xx, "h": h, "V": V,
                "vx": vx, "vz": vz, "az": az, "pitch": pitch, "gamma": gamma,
                "T": T, "D": D, "m": m, "g": g, "q": qi
            })

            print(f"Tiempo máximo alcanzado (t={t:.2f} s)")
            # No rompemos: el while permite continuar si h>0.
            # Si no quieres continuar, añade: break

        # Si no hubo eventos “duros”, avanzar al siguiente paso
        vx, vz, xx, h, t = vx_next, vz_next, xx_next, h_next, t_next


    # Resumen consola
    if historia:
        final = historia[-1]
        print(f"Simulación terminada en t={final['t']:.2f} s, h={final['h']:.1f} m, x={final['x']:.1f} m, V={final['V']:.1f} m/s")
        print(f"Max-Q SUBIDA = {qmax_up:.0f} Pa en t={t_qmax_up:.2f} s, h={h_qmax_up:.1f} m")

    return historia

# -------------------------------
# Gráfica h(t)
# -------------------------------
def graficar_altitud(historia, fichero_png="altitud_tiempo.png"):
    t = [r["t"] for r in historia]
    h = [r["h"] for r in historia]

    plt.figure()
    plt.plot(t, h)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Altitud h [m]")
    plt.title("Altitud vs. tiempo")
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

def graficar_velocidad(historia, fichero_png="velocidad_tiempo.png"):
    t = [r["t"] for r in historia]
    V = [r["V"] for r in historia]

    plt.figure()
    plt.plot(t, V)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad V [m/s]")
    plt.title("Velocidad vs. tiempo")
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

def graficar_velocidad_z(historia, fichero_png="velocidades_tiempo.png"):
    t = [r["t"] for r in historia]
    vz = [r["vz"] for r in historia]

    plt.figure()
    plt.plot(t, vz, label="Vz (vertical)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Velocidad [m/s]")
    plt.title("Velocidad en z vs. tiempo")
    plt.legend()
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

def graficar_aceleracion_z(historia, fichero_png="aceleracion_z_tiempo.png"):
    t = [r["t"] for r in historia]
    az = [r["az"] for r in historia]

    plt.figure()
    plt.plot(t, az, label="Az (vertical)")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Aceleracion [m/s^2]")
    plt.title("Aceleracion en z vs. tiempo")
    plt.legend()
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()    
   
    
def graficar_empuje(historia, fichero_png="empuje_tiempo.png"):
    t = [r["t"] for r in historia]
    T = [r["T"] for r in historia]

    plt.figure()
    plt.plot(t, T)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Empuje T [N]")
    plt.title("Empuje vs. tiempo")
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

def graficar_pitch(historia, fichero_png="pitch_tiempo.png"):
    t = [r["t"] for r in historia]
    pitch = [r["pitch"] for r in historia]
    pitch_deg = [r["pitch"]*180/math.pi for r in historia]

    plt.figure()
    plt.plot(t, pitch_deg)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Pitch [grados]")
    plt.title("Pitch vs. tiempo")
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

def graficar_masa(historia, fichero_png="masa_vehiculo_tiempo.png"):
    t = [r["t"] for r in historia]
    m = [r["m"] for r in historia]

    plt.figure()
    plt.plot(t, m)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Masa vehiculo [kg]")
    plt.title("Masa vehiculo vs. tiempo")
    plt.grid(True)
    if fichero_png:
        plt.savefig(fichero_png, dpi=150, bbox_inches="tight")
    plt.show()

# -------------------------------
# Ejecución directa
# -------------------------------
if __name__ == "__main__":
    dt = 1
    tmax = 1800.0

    hist = simular(dt=dt, t_max=tmax)
    graficar_altitud(hist)
    graficar_velocidad_z(hist)
    graficar_aceleracion_z(hist)
    #graficar_empuje(hist)
    #graficar_pitch(hist)
    #graficar_masa(hist)
    

