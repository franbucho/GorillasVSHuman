from ursina import *
from random import randint, choice

app = Ursina()
window.title = 'Pelea Mortal Kombat - Gorila vs Humano'
window.borderless = False
camera.position = (0, 5, -20)
camera.rotation_x = 20
Sky()

# Área de pelea
ground = Entity(model='plane', scale=(30, 1, 10), color=color.gray, collider='box', y=-1)

# Texturas (asegúrate de tenerlas o cambia los nombres)
human_texture = load_texture('textures/human_texture.png') or color.azure
gorila_texture = load_texture('textures/gorila_texture.png') or color.brown

class Combatiente(Entity):
    def __init__(self, nombre, salud, fuerza, textura, pos_inicial, sentido):
        super().__init__(
            model='cube',
            texture=textura if isinstance(textura, Texture) else None,
            color=color.white if isinstance(textura, Texture) else textura,
            scale=(1.5, 2.5, 1),
            position=pos_inicial
        )
        self.nombre = nombre
        self.salud = salud
        self.salud_max = salud
        self.fuerza = fuerza
        self.sentido = sentido  # -1 o 1, define hacia qué lado está el enemigo
        self.vivo = True
        self.enemigo = None

        self.barra_salud = Entity(parent=self, model='quad', color=color.green, position=(0, 1.6, 0.51), scale=(1, 0.1, 1))
        self.texto_nombre = Text(text=self.nombre, parent=self, y=1.9, x=-0.6, scale=1, origin=(0, 0), background=True)

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        self.salud = max(0, self.salud)
        self.barra_salud.scale_x = self.salud / self.salud_max
        self.barra_salud.color = color.green if self.salud > 60 else color.yellow if self.salud > 30 else color.red

        self.color = color.red
        invoke(setattr, self, 'color', color.white, delay=0.2)

        if self.salud <= 0:
            self.vivo = False
            self.disable()
            self.texto_nombre.text += " 💀"
            self.barra_salud.disable()

    def atacar(self):
        if not (self.vivo and self.enemigo.vivo):
            return

        distancia = abs(self.x - self.enemigo.x)
        if distancia > 1.6:
            # Acercarse
            direccion = self.sentido
            self.x += 0.1 * direccion
        else:
            # Golpear
            dano = randint(5, self.fuerza)
            print(f"{self.nombre} ataca a {self.enemigo.nombre} por {dano} de daño.")
            self.enemigo.recibir_dano(dano)

            # Retroceder un poco
            self.x -= 0.2 * self.sentido

# Crear combatientes (posiciones en eje X)
humano = Combatiente("Humano", 100, 15, human_texture, pos_inicial=(-4, 0, 0), sentido=1)
gorila = Combatiente("Gorila", 120, 20, gorila_texture, pos_inicial=(4, 0, 0), sentido=-1)

# Apuntar al enemigo
humano.enemigo = gorila
gorila.enemigo = humano

# Texto final
texto_resultado = Text(text='', origin=(0, 0), scale=2, y=0.4, enabled=False)
resultado_mostrado = False

def update():
    global resultado_mostrado

    if not humano.vivo or not gorila.vivo:
        if not resultado_mostrado:
            ganador = humano.nombre if humano.vivo else gorila.nombre
            texto_resultado.text = f'🏆 ¡{ganador} gana la pelea! 🏆'
            texto_resultado.enabled = True
            resultado_mostrado = True
        return

    if randint(0, 50) == 1:
        atacante = choice([humano, gorila])
        atacante.atacar()

app.run()
