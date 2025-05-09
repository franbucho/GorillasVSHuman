from ursina import *
from random import randint, choice

app = Ursina()

# Cargar texturas desde carpeta "textures"
arena_texture = load_texture('textures/arena.jpg')
wall_texture = load_texture('textures/wall.jpg')
gorilla_texture = load_texture('textures/gorilla.png')
human_texture = load_texture('textures/human.png')

# Escenario: suelo y fondo
ground = Entity(model='plane', texture=arena_texture, scale=(40, 1, 20), collider='box', y=-1)
wall = Entity(model='cube', texture=wall_texture, scale=(40, 10, 0.5), position=(0, 4, 10.5), collider='box')

# Luz y cámara
DirectionalLight().look_at(Vec3(1, -1, -1))
camera.position = (0, 5, -20)
camera.rotation_x = 15

# Clase Combatiente
class Combatiente(Entity):
    def __init__(self, nombre, salud, fuerza, textura, position=(0, 0, 0)):
        super().__init__(
            model='quad',
            texture=textura,
            position=position,
            scale=(2, 2),
            collider='box'
        )
        self.nombre = nombre
        self.salud = salud
        self.salud_max = salud
        self.fuerza = fuerza
        self.barra_salud = Entity(
            parent=self,
            model='quad',
            color=color.green,
            position=(0, 1.2, -0.1),
            scale=(1, 0.1)
        )

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        self.salud = max(0, self.salud)
        self.actualizar_barra_salud()
        if self.salud <= 0:
            destroy(self)

    def atacar(self, objetivo):
        objetivo.recibir_dano(self.fuerza)
        self.animacion_golpe()

    def actualizar_barra_salud(self):
        escala_x = self.salud / self.salud_max
        self.barra_salud.scale_x = escala_x
        self.barra_salud.color = color.green if escala_x > 0.5 else (color.yellow if escala_x > 0.2 else color.red)

    def animacion_golpe(self):
        original = self.x
        animar = Sequence(
            self.animate_x(original + 0.3, duration=0.1),
            self.animate_x(original - 0.3, duration=0.1),
            self.animate_x(original, duration=0.1)
        )
        animar.start()

# Crear combatientes
gorilas = [
    Combatiente("Gorila 1", 120, 20, gorilla_texture, position=(6, 0, 2)),
    Combatiente("Gorila 2", 120, 20, gorilla_texture, position=(6, 0, -2))
]

humanos = [
    Combatiente("Humano 1", 100, 15, human_texture, position=(-6, 0, 2)),
    Combatiente("Humano 2", 100, 15, human_texture, position=(-6, 0, -2))
]

# Lógica de combate por turnos
turno = 0

def siguiente_turno():
    global turno
    vivos_gorilas = [g for g in gorilas if g.salud > 0]
    vivos_humanos = [h for h in humanos if h.salud > 0]

    if not vivos_gorilas:
        print("¡Los humanos ganan!")
        return
    if not vivos_humanos:
        print("¡Los gorilas ganan!")
        return

    atacante = vivos_gorilas[turno % len(vivos_gorilas)] if turno % 2 == 0 else vivos_humanos[turno % len(vivos_humanos)]
    objetivo = choice(vivos_humanos) if turno % 2 == 0 else choice(vivos_gorilas)

    atacante.atacar(objetivo)
    turno += 1
    invoke(siguiente_turno, delay=1.2)

siguiente_turno()
app.run()
