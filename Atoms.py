import json
import math
import random

VEL_ESCALA = 0.2   # ajusta para que la velocidad en píxeles/frame se vea bien


class Element:
    """Datos fijos de un elemento, cargados desde el JSON."""
    def __init__(self, datos):
        self.nombre = datos["nombre"]
        self.simbolo = datos["simbolo"]
        self.numero_atomico = datos["numero_atomico"]
        self.masa = datos["masa_atomica"]
        self.valencia = datos["valencia"]
        self.estados_oxidacion = datos["estados_oxidacion"]
        self.electronegatividad = datos["electronegatividad"]
        self.punto_fusion = datos["punto_fusion_K"]
        self.punto_ebullicion = datos["punto_ebullicion_K"]
        self.radio_px = datos["visual"]["radio_px"]
        self.color = datos["visual"]["color"]


def cargar_elementos(ruta="elementos.json"):
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    return {e["simbolo"]: Element(e) for e in datos["elementos"]}


class Atom:
    """Un átomo concreto dentro de la simulación."""
    def __init__(self, elemento, x, y):
        self.elemento = elemento
        self.posX = x
        self.posY = y
        self.velX = 0.0
        self.velY = 0.0
        self.carga = 0
        self.enlaces = []        # luego: lista de objetos Bond
        self.id_canvas = None

    # Atajos para no escribir atomo.elemento.xxx todo el rato
    @property
    def simbolo(self):
        return self.elemento.simbolo

    @property
    def masa(self):
        return self.elemento.masa

    @property
    def radio(self):
        return self.elemento.radio_px

    @property
    def valencia(self):
        return self.elemento.valencia

    @property
    def electronegatividad(self):
        return self.elemento.electronegatividad

    @property
    def color(self):
        return self.elemento.color

    def asignar_velocidad(self, temperatura):
        """Rapidez según la temperatura (K) y la masa, dirección aleatoria."""
        rapidez = VEL_ESCALA * math.sqrt(temperatura / self.masa)
        angulo = random.uniform(0, 2 * math.pi)
        self.velX = rapidez * math.cos(angulo)
        self.velY = rapidez * math.sin(angulo)

    def energia_cinetica(self):
        return 0.5 * self.masa * (self.velX ** 2 + self.velY ** 2)