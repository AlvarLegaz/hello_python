import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps, Image
import time, math
import escenario as esc
import datos_vuelo_gui as dvgui

ROT_STEP_DEG = 5
EMP_STEP_PER = 5
TICK_MS = 100
IMG_SIZE = 200  # tamaño fijo 200x200

class App:
    def __init__(self, root):

        self.mi_escenario = esc.Escenario()

        self.altitud = 0
        self.distancia = 0
        self.porcentaje_empuje = 100

        self.root = root
        self.root.title("Rotación del cohete")
        self.root.geometry("1100x750")  # más alto para footer

        # ----- Layout principal: lateral izq + contenido + lateral dcha -----
        main = tk.Frame(root, bg="black")
        main.pack(expand=True, fill="both")

        # Lateral izquierdo (configuración)
        leftbar = tk.Frame(main, bg="#232323", width=220)
        leftbar.pack(side="left", fill="y")
        leftbar.pack_propagate(False)

        # Contenido central
        content = tk.Frame(main, bg="black")
        content.pack(side="left", expand=True, fill="both")

        # Lateral derecho (telemetría)
        rightbar = tk.Frame(main, bg="#1e1e1e", width=220)
        rightbar.pack(side="right", fill="y")
        rightbar.pack_propagate(False)

        # ---- Widgets contenido ----
        self.lbl_img_pitch = tk.Label(content, bg="white")
        self.lbl_img_pitch.pack(expand=True)

        self.lbl_angle = tk.Label(content, text="Pitch = 90°", font=("Arial", 14), bg="white")
        self.lbl_angle.pack(side=tk.LEFT, padx=10)
        
        self.lbl_porcentaje_empuje = tk.Label(content, text="Empuje = 100%", font=("Arial", 14), bg="white")
        self.lbl_porcentaje_empuje.pack(side=tk.LEFT, padx=10)

        self.lbl_time = tk.Label(content, text="Tiempo: 0 s", font=("Arial", 14), bg="white")
        self.lbl_time.pack(pady=10)

        # ---- Widgets lateral izquierdo ----
        tk.Label(leftbar, text="Cohete", font=("Arial", 16, "bold"),
                 fg="white", bg="#232323").pack(pady=(20, 10))

        self.mass_var   = tk.StringVar(value="0 kg")
        self.fuel_var   = tk.StringVar(value="0 %")
        self.stage_var  = tk.StringVar(value="0")

        self._make_row(leftbar, "Masa:", self.mass_var)
        self._make_row(leftbar, "Nivel combustible:", self.fuel_var)
        self._make_row(leftbar, "Nº etapas:", self.stage_var)

        tk.Label(leftbar, text="Fuerzas", font=("Arial", 16, "bold"),
                 fg="white", bg="#232323").pack(pady=(20, 10))
        self.T_var   = tk.StringVar(value="0 N")
        self.D_var   = tk.StringVar(value="0 N")
        self.W_var  = tk.StringVar(value="0 N")

        self._make_row(leftbar, "Empuje:", self.T_var)
        self._make_row(leftbar, "Arrastre:", self.D_var)
        self._make_row(leftbar, "Peso:", self.W_var)

        # ---- Widgets lateral derecho ----
        tk.Label(rightbar, text="Telemetría", font=("Arial", 16, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=(20, 10))

        self.alt_var = tk.StringVar(value="0 km")
        self.dist_var = tk.StringVar(value="0 km")
        self.vz_var = tk.StringVar(value="0 m/s")
        self.vx_var = tk.StringVar(value="0 m/s")
        self.az_var = tk.StringVar(value="0 m/s2")
        self.ax_var = tk.StringVar(value="0 m/s2")

        self._make_row(rightbar, "Altitud:", self.alt_var, bg="#1e1e1e")
        self._make_row(rightbar, "Distancia:", self.dist_var, bg="#1e1e1e")
        self._make_row(rightbar, "Velocidad Z:", self.vz_var, bg="#1e1e1e")
        self._make_row(rightbar, "Velocidad X:", self.vx_var, bg="#1e1e1e")
        self._make_row(rightbar, "Aceleración Z:", self.az_var, bg="#1e1e1e")
        self._make_row(rightbar, "Aceleración X:", self.ax_var, bg="#1e1e1e")

        # ---- Footer con botones ----
        footer = tk.Frame(root, bg="#333333", height=60)
        footer.pack(side="bottom", fill="x")

        btn_start = tk.Button(footer, text="Iniciar", font=("Arial", 12, "bold"),
                              command=self.start_timer, bg="green", fg="white", width=10)
        btn_start.pack(side="left", padx=20, pady=10)

        btn_stop = tk.Button(footer, text="Parar", font=("Arial", 12, "bold"),
                             command=self.stop_timer, bg="red", fg="white", width=10)
        btn_stop.pack(side="left", padx=10, pady=10)

        btn_reset = tk.Button(footer, text="Reset", font=("Arial", 12, "bold"),
                              command=self.reset_timer, bg="orange", fg="black", width=10)
        btn_reset.pack(side="left", padx=10, pady=10)

        btn_datos_vuelo = tk.Button(footer, text="Datos vuelo actual", font=("Arial", 12, "bold"),
                             command=self.mostrar_datos_vuelo, bg="red", fg="white", width=20)
        btn_datos_vuelo.pack(side="left", padx=10, pady=10)

        # ---- Estado ----
        self.left_down = False
        self.right_down = False
        self.up_down = False
        self.down_down = False
        self.x_down = False
        self.c_down = False

        # Imagen base con acolchado
        img = Image.open("cohete.png").convert("RGBA")
        w, h = img.size
        side = int(math.ceil(max(w, h) * math.sqrt(2)))
        pad_w = max(0, side - w)
        pad_h = max(0, side - h)
        self.base = ImageOps.expand(
            img,
            border=(pad_w//2, pad_h//2, pad_w - pad_w//2, pad_h - pad_h//2),
            fill=(0, 0, 0, 0)
        )

        self.angle = 0.0
        self._update_label_img_pitch_with(self.base)

        # Cronómetro
        self.start_time = None
        self.running = False
        self.elapsed_before = 0  # tiempo acumulado antes de parar

        # --- Eventos teclado ---
        root.bind_all("<KeyPress-Left>",  lambda e: self._set_key('left', True))
        root.bind_all("<KeyRelease-Left>", lambda e: self._set_key('left', False))
        root.bind_all("<KeyPress-Right>", lambda e: self._set_key('right', True))
        root.bind_all("<KeyRelease-Right>", lambda e: self._set_key('right', False))
        root.bind_all("<KeyPress-Up>",    lambda e: self._set_key('up', True))
        root.bind_all("<KeyRelease-Up>",  lambda e: self._set_key('up', False))
        root.bind_all("<KeyPress-Down>",  lambda e: self._set_key('down', True))
        root.bind_all("<KeyRelease-Down>",lambda e: self._set_key('down', False))
        root.bind_all("<KeyPress-x>",  lambda e: self._set_key('x', True))
        root.bind_all("<KeyRelease-x>",lambda e: self._set_key('x', False))
        root.bind_all("<KeyPress-c>",  lambda e: self._set_key('c', True))
        root.bind_all("<KeyRelease-c>",lambda e: self._set_key('c', False))

        self.tick()

    def _make_row(self, parent, label, var, bg="#232323"):
        row = tk.Frame(parent, bg=bg)
        tk.Label(row, text=label, font=("Arial", 13), fg="white", bg=bg).pack(side="left")
        tk.Label(row, textvariable=var, font=("Arial", 13, "bold"), fg="white", bg=bg).pack(side="right")
        row.pack(fill="x", padx=16, pady=6)

    # ---- Cronómetro ----
    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop_timer(self):
        if self.running:
            # acumular tiempo ya contado
            self.elapsed_before += time.time() - self.start_time
            self.running = False

    def reset_timer(self):
        self.running = False
        self.start_time = None
        self.elapsed_before = 0
        self.lbl_time.configure(text="Tiempo: 0 s")
        self.mi_escenario.reset()

    # ---- Rotación ----
    def _set_key(self, which, down):
        if which == 'left':
            self.left_down = down
        elif which == 'right':
            self.right_down = down
        elif which == 'up':
            self.up_down = down
        elif which == 'down':
            self.down_down = down
        elif which == 'x':
            self.x_down = down
        elif which == 'c':
            self.c_down = down

    def _update_label_img_pitch_with(self, pil_img):
        resized = pil_img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.BICUBIC)
        self.tk_img = ImageTk.PhotoImage(resized)
        self.lbl_img_pitch.configure(image=self.tk_img)
        self.lbl_img_pitch.image = self.tk_img

        angle_display = ((self.angle + 180) % 360) - 180
        self.lbl_angle.configure(text=f"Pitch = {int(round(90-angle_display))}°")

        

    def rotate_and_update(self, delta_deg):
        self.angle = (self.angle + delta_deg) % 360.0
        rotated = self.base.rotate(-self.angle, resample=Image.Resampling.BICUBIC, expand=False)
        self._update_label_img_pitch_with(rotated)
    
    def update_empuje(self, delta_empuje):
        self.porcentaje_empuje = self.porcentaje_empuje + delta_empuje
        if self.porcentaje_empuje + delta_empuje>100:
            self.porcentaje_empuje = 100
        elif self.porcentaje_empuje + delta_empuje<0:
            self.porcentaje_empuje = 0

        self.lbl_porcentaje_empuje.configure(text=f"Empuje = {self.porcentaje_empuje}%")    
           

    def tick(self):
        # Rotación
        delta = 0
        delta_empuje = 0
        
        if self.left_down:  
            delta -= ROT_STEP_DEG
        if self.right_down: 
            delta += ROT_STEP_DEG
        if delta != 0:
            self.rotate_and_update(delta)

        if self.up_down:  
            delta_empuje += EMP_STEP_PER
        if self.down_down: 
            delta_empuje -= EMP_STEP_PER
        if self.c_down:
            delta_empuje = -100
        if self.x_down:
            delta_empuje = 100
        if delta_empuje != 0:
            self.update_empuje(delta_empuje)
    

        # Cronómetro
        if self.running and self.start_time is not None:
            # Actualiza tiempo
            elapsed = self.elapsed_before + (time.time() - self.start_time)
            self.lbl_time.configure(text=f"Tiempo: {int(elapsed)} s")

            self.actualizar_escenario_y_gui()

        elif not self.running:
            # mostrar acumulado
            self.lbl_time.configure(text=f"Tiempo: {int(self.elapsed_before)} s")

        self.root.after(TICK_MS, self.tick)

    def actualizar_escenario_y_gui(self):
        # Acutaliza escenario.
        pitch =math.radians( 90 - (((self.angle + 180) % 360) - 180))
        try:
            out = self.mi_escenario.update(pitch,self.porcentaje_empuje,TICK_MS/1000)
            self.altitud = out["altitud"]
            self.distancia = out["distancia"]
            masa = out["m"]
            velocidad_z = out["vz"]
            velocidad_x = out["vx"]
            aceleracion_z = out["az"]
            aceleracion_x = out["ax"]
            empuje = out["T"]
            arrastre = out["Dz"]
            peso = out["W"]
            fuel_var = out["nivel_combustible"]

            # Actualiza telemetría
            self.alt_var.set(f"{self.altitud/1000:.3f} km")  
            self.dist_var.set(f"{self.distancia/1000:.3f} km") 
            self.vz_var.set(f"{3.6*velocidad_z:.1f} km/s") 
            self.vx_var.set(f"{3.6*velocidad_x:.1f} km/s") 
            self.az_var.set(f"{aceleracion_z:.1f} m/s2") 
            self.ax_var.set(f"{aceleracion_x:.1f} m/s2") 

            #A Actualizar datos vehiculo 
            self.mass_var.set(f"{masa:.1f} kg") 
            self.fuel_var.set(f"{fuel_var:.1f} %")
            self.T_var.set(f"{empuje:.1f} N") 
            self.D_var.set(f"{arrastre:.1f} N")
            self.W_var.set(f"{peso:.1f} N")

        except RuntimeError as e:
            self.mostrar_datos_vuelo()
            self.reset_timer()
            messagebox.showinfo("Vuelo terminado", "El vuelo ha finalizado por impacto con el suelo.")
    
    def mostrar_datos_vuelo(self):
        dvgui.mostrar_datos_trayectoria(self.mi_escenario.obtener_datos_vuelo())
            
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
