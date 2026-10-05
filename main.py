import tkinter as tk
import math
import random
from Atoms import Atom, cargar_elementos

ANCHO, ALTO = 800, 600
ANGULO_MAX = math.radians(15)

temperatura = 300   # K
elementos = cargar_elementos("Elements.json")
atomos = []

# ---------------- Ventana ----------------
ventana = tk.Tk()
ventana.title("Simulador químico")

panel = tk.Frame(ventana)
panel.pack(side="left", fill="y", padx=5, pady=5)

canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="white")
canvas.pack(side="right")

# ---------------- Lógica ----------------
def crear_atomo(simbolo, x, y):
    elem = elementos[simbolo]
    atomo = Atom(elem, x, y)
    atomo.asignar_velocidad(temperatura)
    r = atomo.radio
    atomo.id_canvas = canvas.create_oval(
        x - r, y - r, x + r, y + r, fill=elem.color
    )
    atomos.append(atomo)


def perturbar_direccion(atomo):
    """Tras un rebote, desvía un poco la dirección conservando la rapidez."""
    rapidez = math.hypot(atomo.velX, atomo.velY)
    angulo = math.atan2(atomo.velY, atomo.velX)
    angulo += random.uniform(-ANGULO_MAX, ANGULO_MAX)
    atomo.velX = rapidez * math.cos(angulo)
    atomo.velY = rapidez * math.sin(angulo)


def mover_atomos():
    for a in atomos:
        a.posX += a.velX
        a.posY += a.velY
        r = a.radio
        rebote = False

        if a.posX + r >= ANCHO:
            a.posX = ANCHO - r
            a.velX = -a.velX
            rebote = True
        elif a.posX - r <= 0:
            a.posX = r
            a.velX = -a.velX
            rebote = True

        if a.posY + r >= ALTO:
            a.posY = ALTO - r
            a.velY = -a.velY
            rebote = True
        elif a.posY - r <= 0:
            a.posY = r
            a.velY = -a.velY
            rebote = True

        if rebote:
            perturbar_direccion(a)

        canvas.coords(a.id_canvas,
                      a.posX - r, a.posY - r,
                      a.posX + r, a.posY + r)

    ventana.after(20, mover_atomos)


def cambiar_temperatura(valor):
    global temperatura
    nueva = float(valor)
    factor = math.sqrt(nueva / temperatura)
    for a in atomos:
        a.velX *= factor
        a.velY *= factor
    temperatura = nueva


def limpiar():
    for a in atomos:
        canvas.delete(a.id_canvas)
    atomos.clear()

# ---------------- Controles ----------------
seleccionado = tk.StringVar(value="H")

tk.Label(panel, text="Elemento").pack(anchor="w")
for simbolo, elem in sorted(elementos.items(), key=lambda kv: kv[1].numero_atomico):
    tk.Radiobutton(
        panel, text=f"{elem.simbolo} - {elem.nombre}",
        variable=seleccionado, value=simbolo, anchor="w"
    ).pack(fill="x")

escala = tk.Scale(panel, from_=10, to=1000, orient="horizontal",
                  label="Temperatura (K)", command=cambiar_temperatura)
escala.set(temperatura)
escala.pack(fill="x", pady=10)

tk.Button(panel, text="Limpiar", command=limpiar).pack(fill="x")

canvas.bind("<Button-1>", lambda e: crear_atomo(seleccionado.get(), e.x, e.y))

mover_atomos()
ventana.mainloop()