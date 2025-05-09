# GorillasVSHuman
# 🥊 Simulación de Pelea: Humanos vs Gorilas

Este proyecto es una simulación visual interactiva desarrollada en Python con [Ursina Engine](https://www.ursinaengine.org/), donde dos equipos —humanos y gorilas— se enfrentan en una batalla animada. Cada combatiente tiene salud, fuerza y una barra de vida visible. Los ataques se ejecutan de forma aleatoria hasta que un equipo gana.

## 🎮 Características

- Entorno 3D básico con cámara y cielo.
- Cuatro combatientes con atributos únicos.
- Lógica de combate con daño aleatorio.
- Barras de salud visuales que cambian de color según el estado.
- Indicador visual del equipo ganador al finalizar la batalla.
- Nombres flotantes con actualización visual al morir.

## 📸 Captura de pantalla

*(Puedes agregar aquí una imagen del juego corriendo)*

## 🚀 Requisitos

- Python 3.7 o superior
- [Ursina Engine](https://pypi.org/project/ursina/)

Puedes instalar Ursina con:

pip install ursina
🧠 Cómo funciona
Cada ciclo (update) evalúa si hay combatientes vivos.

Si ambos equipos aún tienen miembros, se selecciona un atacante y un objetivo aleatorios.

Se aplica daño y se actualiza la barra de salud.

Una vez que un equipo pierde todos sus miembros, se declara un ganador.

▶️ Ejecución
Clona el repositorio y ejecuta el script principal:

bash
Copy
Edit
python pelea_simulacion.py
(Asegúrate de renombrar tu archivo si usas otro nombre.)

🛠 Estructura del Código
Combatiente: Clase que representa a cada luchador.

update(): Lógica que se ejecuta en cada frame.

main: Inicialización del entorno y creación de personajes.

📄 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información.

¡Explora, modifica y diviértete observando quién gana la batalla! 🦍🧍
