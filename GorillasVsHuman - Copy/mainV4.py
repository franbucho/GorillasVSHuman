from ursina import *
from random import randint, choice, random

# Inicialización de la aplicación
app = Ursina()
window.title = "Simulación de Pelea: Humanos vs Gorilas"
window.borderless = False
camera.position = (0, 10, -20)
camera.rotation_x = 30

# Crear luz para mejorar las sombras
light = DirectionalLight(parent=scene, color=color.white, rotation=(45, 45, 0))
light.position = (0, 10, -10)

# Fondo y suelo
ground = Entity(model='plane', scale=20, color=color.lime.tint(-.2), collider='box', y=-1)
sky = Sky()

class Combatiente(Entity):
    def __init__(self, nombre, salud, fuerza, color_combate, position, modelo, textura=None):
        super().__init__(
            model=modelo,  # Usamos un modelo más complejo que un simple cubo
            color=color_combate,
            position=position,
            scale=(1.2, 2, 1),
            collider='box'
        )

        # Aplicar textura si existe
        if textura:
            self.texture = textura

        self.nombre = nombre
        self.salud_max = salud
        self.salud = salud
        self.fuerza = fuerza
        self.vivo = True
        self.color_original = color_combate

        # Barra de salud
        self.barra_salud = Entity(parent=self, model='quad', color=color.green,
                                  position=(0, 1.4, 0.51), scale=(1, 0.1, 1))
        # Nombre flotante
        self.texto_nombre = Text(text=self.nombre, scale=1, parent=self, y=1.8, x=-0.6,
                                 origin=(0, 0), background=True)

    def recibir_dano(self, cantidad):
        self.salud = max(self.salud - cantidad, 0)
        self.actualizar_barra_salud()

        # Efecto visual de golpe
        self.color = color.red
        invoke(setattr, self, 'color', self.color_original, delay=0.3)

        # Si muere
        if self.salud == 0:
            self.vivo = False
            self.disable()
            self.barra_salud.disable()
            self.texto_nombre.text += " (X)"

    def actualizar_barra_salud(self):
        proporción = self.salud / self.salud_max
        self.barra_salud.scale_x = proporción
        if proporción > 0.5:
            self.barra_salud.color = color.lime
        elif proporción > 0.2:
            self.barra_salud.color = color.yellow
        else:
            self.barra_salud.color = color.red

    def atacar(self, objetivo):
        if self.vivo and objetivo.vivo:
            daño = randint(5, self.fuerza)
            print(f"{self.nombre} ataca a {objetivo.nombre} por {daño} de daño.")
            objetivo.recibir_dano(daño)

# Crear modelos 3D (puedes reemplazar estos por modelos .obj o .fbx)
human_texture = load_texture("human_texture.jpg")  # Usa una textura adecuada para los humanos
gorila_texture = load_texture("gorila_texture.jpg")  # Usa una textura adecuada para los gorilas

# Equipos
humanos = [
    Combatiente("Humano 1", 100, 15, color.azure, position=(-3, 0, 0), modelo='humano_modelo', textura=human_texture),
    Combatiente("Humano 2", 100, 15, color.azure, position=(-1, 0, 0), modelo='humano_modelo', textura=human_texture)
]

gorilas = [
    Combatiente("Gorila 1", 150, 20, color.brown, position=(1, 0, 0), modelo='gorila_modelo', textura=gorila_texture),
    Combatiente("Gorila 2", 150, 20, color.brown, position=(3, 0, 0), modelo='gorila_modelo', textura=gorila_texture)
]

# Resultado de la pelea
resultado_mostrado = False
texto_resultado = Text(text="", origin=(0, 0), scale=2, y=0.4, enabled=False)

def update():
    global resultado_mostrado

    vivos_humanos = [h for h in humanos if h.vivo]
    vivos_gorilas = [g for g in gorilas if g.vivo]

    # Fin de la batalla
    if not vivos_humanos or not vivos_gorilas:
        if not resultado_mostrado:
            ganador = "Gorilas" if vivos_gorilas else "Humanos"
            print(f"\nLa pelea ha terminado. Ganador: {ganador}")
            texto_resultado.text = f"🏆 Ganaron los {ganador} 🏆"
            texto_resultado.enabled = True
            resultado_mostrado = True
        return

    # Turno aleatorio de ataque
    if random() < 0.03:
        atacante = choice(vivos_humanos + vivos_gorilas)
        objetivo = choice(vivos_gorilas if atacante in humanos else vivos_humanos)
        atacante.atacar(objetivo)

app.run()
