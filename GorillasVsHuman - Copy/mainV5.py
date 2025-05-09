from ursina import *
from random import randint, choice, random

app = Ursina()
window.title = "Simulación de Pelea: Humanos vs Gorilas"
window.borderless = False
camera.position = (0, 10, -20)
camera.rotation_x = 30

# Fondo y suelo
ground = Entity(model='plane', scale=20, color=color.lime.tint(-.2), collider='box', y=-1)
sky = Sky()

class Combatiente(Entity):
    def __init__(self, nombre, salud, fuerza, color, position, textura=None):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=(1.2, 2, 1),
            collider='box'
        )
        self.nombre = nombre
        self.salud = salud
        self.salud_maxima = salud
        self.fuerza = fuerza
        self.vivo = True
        self.color_original = color

        # Si se proporciona una textura, asignarla al combatiente
        if textura:
            self.texture = textura

        # Barra de salud flotante
        self.barra_salud = Entity(parent=self, model='quad', color=(0, 255, 0, 1), position=(0, 1.4, 0.51), scale=(1, 0.1, 1))
        self.texto_nombre = Text(text=self.nombre, scale=1, parent=self, y=1.8, x=-0.6, origin=(0,0), background=True)

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        self.salud = max(self.salud, 0)
        self.barra_salud.scale_x = self.salud / self.salud_maxima
        self.barra_salud.color = (0, 255, 0, 1) if self.salud > 50 else (255, 255, 0, 1) if self.salud > 20 else (255, 0, 0, 1)

        self.color = color.red
        invoke(setattr, self, 'color', self.color_original, delay=0.3)

        if self.salud <= 0:
            self.vivo = False
            self.disable()
            self.texto_nombre.text += " (X)"
            self.barra_salud.disable()

    def atacar(self, objetivo):
        if self.vivo and objetivo.vivo:
            dano = randint(5, self.fuerza)
            print(f"{self.nombre} ataca a {objetivo.nombre} por {dano} de daño.")
            objetivo.recibir_dano(dano)

# Cargar texturas
human_texture = load_texture('textures/human_texture.png')  # Cambia el nombre del archivo según sea necesario
gorila_texture = load_texture('textures/gorila_texture.png')  # Cambia el nombre del archivo según sea necesario

# Crear equipos
humanos = [
    Combatiente("Humano 1", 100, 15, color.azure, position=(-6, 0, 0), textura=human_texture),
    Combatiente("Humano 2", 100, 15, color.azure, position=(-3, 0, 0), textura=human_texture)
]
gorilas = [
    Combatiente("Gorila 1", 150, 20, color.brown, position=(3, 0, 0), textura=gorila_texture),
    Combatiente("Gorila 2", 150, 20, color.brown, position=(6, 0, 0), textura=gorila_texture)
]

# Resultado de pelea
resultado_mostrado = False
texto_resultado = Text(text="", origin=(0,0), scale=2, y=0.4, enabled=False)

def update():
    global resultado_mostrado

    vivos_h = [h for h in humanos if h.vivo]
    vivos_g = [g for g in gorilas if g.vivo]

    if not vivos_h or not vivos_g:
        if not resultado_mostrado:
            ganador = "Gorilas" if vivos_g else "Humanos"
            print(f"\nLa pelea ha terminado. Ganador: {ganador}")
            texto_resultado.text = f"🏆 Ganaron los {ganador} 🏆"
            texto_resultado.enabled = True
            resultado_mostrado = True
        return

    if random() < 0.03:
        atacante = choice(vivos_h + vivos_g)
        objetivo = choice(vivos_g if atacante in humanos else vivos_h)
        atacante.atacar(objetivo)

app.run()
