# NOMBRE DEL ARCHIVO: app.py
import pyxel
from clases.nivel import Nivel
from clases.tablero import Tablero


class App:
    def __init__(self):
        # 1. Instanciamos el Nivel
        self.nivel = Nivel("FACIL")

        # Creamos el tablero usando las dimensiones del nivel
        # Tablero hará pyxel.init(...) y pyxel.run(...)
        self.tablero = Tablero(self.nivel.ancho_pantalla,
                               self.nivel.alto_pantalla, self.nivel.num_pisos)

    def update(self):
        # Si pulsas Q, se cierra el juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Aquí irá la lógica de actualización en futuros Sprints
        pass