# NOMBRE DEL ARCHIVO: app.py
import pyxel
from clases.tablero import Tablero

class App:
    def __init__(self):
        # Creamos el tablero directamente.
        # Él se encargará de gestionar el Pyxel init y el Menú
        self.tablero = Tablero()

    def update(self):
        # Si pulsas Q, se cierra el juego (gestionado dentro de Tablero también)
        pass