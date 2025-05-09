from ursina import *
from random import randint

app = Ursina()

camera.position = (0, 10, -20)
camera.rotation_x = 30

# Crear humanos y gorilas como cubos o modelos simples
humano1 = Entity(model='cube', color=color.azure, position=(-3,0,0), scale=(1,2,1))
humano2 = Entity(model='cube', color=color.azure, position=(-1,0,0), scale=(1,2,1))

gorila1 = Entity(model='cube', color=color.brown, position=(1,0,0), scale=(1.2,2.5,1))
gorila2 = Entity(model='cube', color=color.brown, position=(3,0,0), scale=(1.2,2.5,1))

salud = {
    humano1: 100,
    humano2: 100,
    gorila1: 150,
    gorila2: 150
}

def ataque(atacante, defensor):
    if defensor.enabled:
        dmg = randint(10, 25)
        salud[defensor] -= dmg
        print(f"{atacante} ataca a {defensor}, daño: {dmg}")
        defensor.color = color.red
        invoke(setattr, defensor, 'color', color.brown if defensor in [gorila1, gorila2] else color.azure, delay=0.3)
        if salud[defensor] <= 0:
            defensor.enabled = False
            defensor.color = color.black

def update():
    if random.random() < 0.02:
        vivos_h = [h for h in [humano1, humano2] if h.enabled]
        vivos_g = [g for g in [gorila1, gorila2] if g.enabled]

        if not vivos_h or not vivos_g:
            return

        if random.choice([True, False]):
            ataque(random.choice(vivos_h), random.choice(vivos_g))
        else:
            ataque(random.choice(vivos_g), random.choice(vivos_h))

app.run()
