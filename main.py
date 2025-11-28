# main

from clases.juego import Tablero
# NOMBRE DEL ARCHIVO: main.py
from clases.app import App

# Creando el objeto tablero que también inicializará pyxel
tablero = Tablero(368, 192)

if __name__ == "__main__":
    # Simplemente arrancamos la aplicación
    App()