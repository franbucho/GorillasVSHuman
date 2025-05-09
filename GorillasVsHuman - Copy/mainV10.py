from ursina import *
from random import choice
import os

app = Ursina()

# --- Configuración de Recursos ---
ASSETS_DIR = "assets"  # Directorio principal de assets

def load_asset(path, asset_type, **kwargs):
    """Carga un asset y maneja errores."""
    full_path = os.path.join(ASSETS_DIR, path)
    if not os.path.exists(full_path):
        print(f"❌ ERROR: No se encontró el archivo: {full_path}")
        exit()
    if asset_type == "texture":
        return load_texture(full_path, **kwargs)
    elif asset_type == "model":
        return load_model(full_path, **kwargs)
    else:
        raise ValueError(f"Tipo de asset desconocido: {asset_type}")

# Cargar assets
arena_texture = load_asset("textures/arena.jpg", "texture")
wall_texture = load_asset("textures/wall.jpg", "texture")
gorilla_model = load_asset("models/gorilla.gltf", "model")  # Reemplazar con modelo detallado
human_model = load_asset("models/human.gltf", "model")    # Reemplazar con modelo detallado

# --- Escena ---

# Piso
ground = Entity(model='plane', texture=arena_texture, scale=(40, 1, 20), collider='box', y=0)

# Pared
wall = Entity(
    model='plane',
    texture=wall_texture,
    scale=(40, 10),
    position=(0, 5, 10),
    rotation_y=180,
    double_sided=True
)

# Iluminación
directional_light = DirectionalLight(direction=(-1, -1, -1), intensity=1)
ambient_light = AmbientLight(color=color.rgba(100, 100, 100, 255))  # Luz ambiental suave

# Sombras (ejemplo - ajustar según el rendimiento)
directional_light.shadows = True
directional_light.shadow_map_resolution = (2048, 2048)  # Ajustar resolución

# Cámara
camera.position = (0, 10, -30)
camera.rotation_x = 15

# --- Combatientes ---

class Combatiente(Entity):
    def __init__(self, nombre, salud, fuerza, model, texture, position=(0, 0, 0)):
        super().__init__(
            model=model,
            texture=texture,
            position=position,
            scale=(2, 2, 2),  # Ajustar escala
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
            position=(0, 2.5, -0.1),
            scale=(1.5, 0.1)
        )
        self.animator = Animator(animations={
            "idle": None,  # Reemplazar con animación de idle
            "attack": None, # Reemplazar con animación de ataque
            "hurt": None,   # Reemplazar con animación de daño
        })
        self.animator.play("idle")

    def recibir_dano(self, cantidad):
        self.salud -= cantidad
        self.salud = max(0, self.salud)
        self.actualizar_barra_salud()
        self.animator.play("hurt")  # Reproducir animación de daño
        if self.salud <= 0:
            destroy(self)
            # Añadir partículas de muerte (opcional)

    def atacar(self, objetivo):
        objetivo.recibir_dano(self.fuerza)
        self.animator.play("attack") # Reproducir animación de ataque

    def actualizar_barra_salud(self):
        escala_x = self.salud / self.salud_max
        self.barra_salud.scale_x = escala_x
        self.barra_salud.color = color.green if escala_x > 0.5 else (color.yellow if escala_x > 0.2 else color.red)

    def animacion_golpe(self):  # Mantener para efectos menores
        original = self.x
        animar = Sequence(
            self.animate_x(original + 0.3, duration=0.1),
            self.animate_x(original - 0.3, duration=0.1),
            self.animate_x(original, duration=0.1)
        )
        animar.start()

# Instancias
gorilas = [
    Combatiente("Gorila 1", 120, 20, gorilla_model, None, position=(4, 1, 2)), # None para textura si la tiene el modelo
    Combatiente("Gorila 2", 120, 20, gorilla_model, None, position=(4, 1, -2))
]

humanos = [
    Combatiente("Humano 1", 100, 15, human_model, None, position=(-4, 1, 2)),
    Combatiente("Humano 2", 100, 15, human_model, None, position=(-4, 1, -2))
]

# --- Lógica de Combate ---

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

# --- Post-Procesamiento (Ejemplo) ---
# window.color_grade = True
# window.bloom = True
# window.vignette = 0.5

app.run()