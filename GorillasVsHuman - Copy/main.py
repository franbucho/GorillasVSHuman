import tkinter as tk
from tkinter import messagebox
import random

class Combatiente:
    def __init__(self, nombre, salud, fuerza, tipo):
        self.nombre = nombre
        self.salud = salud
        self.fuerza = fuerza
        self.tipo = tipo

    def esta_vivo(self):
        return self.salud > 0

    def atacar(self, enemigo):
        daño = random.randint(int(self.fuerza * 0.8), int(self.fuerza * 1.2))
        enemigo.salud -= daño
        return f"{self.nombre} ({self.tipo}) ataca a {enemigo.nombre} ({enemigo.tipo}) por {daño} de daño. Salud restante: {max(enemigo.salud, 0)}"

def seleccionar_objetivo(enemigos):
    vivos = [e for e in enemigos if e.esta_vivo()]
    return random.choice(vivos) if vivos else None

def iniciar_pelea():
    try:
        h_salud = int(humano_salud.get())
        h_fuerza = int(humano_fuerza.get())
        g_salud = int(gorila_salud.get())
        g_fuerza = int(gorila_fuerza.get())
    except ValueError:
        messagebox.showerror("Error", "Todos los valores deben ser números enteros.")
        return

    humanos = [
        Combatiente("Humano 1", h_salud, h_fuerza, "humano"),
        Combatiente("Humano 2", h_salud, h_fuerza, "humano")
    ]
    gorilas = [
        Combatiente("Gorila 1", g_salud, g_fuerza, "gorila"),
        Combatiente("Gorila 2", g_salud, g_fuerza, "gorila")
    ]

    log_text.delete("1.0", tk.END)
    turno = 1
    while any(h.esta_vivo() for h in humanos) and any(g.esta_vivo() for g in gorilas):
        log_text.insert(tk.END, f"\n--- Turno {turno} ---\n")
        for h in humanos:
            if h.esta_vivo():
                objetivo = seleccionar_objetivo(gorilas)
                if objetivo:
                    log_text.insert(tk.END, h.atacar(objetivo) + "\n")
        for g in gorilas:
            if g.esta_vivo():
                objetivo = seleccionar_objetivo(humanos)
                if objetivo:
                    log_text.insert(tk.END, g.atacar(objetivo) + "\n")
        turno += 1

    ganador = "🏆 ¡Humanos ganaron!" if any(h.esta_vivo() for h in humanos) else "🦍 ¡Gorilas ganaron!"
    log_text.insert(tk.END, f"\n{ganador}\n")

# GUI
root = tk.Tk()
root.title("Simulador de pelea: Humanos vs Gorilas")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Salud Humano:").grid(row=0, column=0)
humano_salud = tk.Entry(frame)
humano_salud.insert(0, "100")
humano_salud.grid(row=0, column=1)

tk.Label(frame, text="Fuerza Humano:").grid(row=1, column=0)
humano_fuerza = tk.Entry(frame)
humano_fuerza.insert(0, "15")
humano_fuerza.grid(row=1, column=1)

tk.Label(frame, text="Salud Gorila:").grid(row=2, column=0)
gorila_salud = tk.Entry(frame)
gorila_salud.insert(0, "150")
gorila_salud.grid(row=2, column=1)

tk.Label(frame, text="Fuerza Gorila:").grid(row=3, column=0)
gorila_fuerza = tk.Entry(frame)
gorila_fuerza.insert(0, "25")
gorila_fuerza.grid(row=3, column=1)

boton_pelea = tk.Button(frame, text="Iniciar pelea", command=iniciar_pelea)
boton_pelea.grid(row=4, column=0, columnspan=2, pady=10)

log_text = tk.Text(root, height=20, width=60)
log_text.pack(padx=10, pady=10)

root.mainloop()
