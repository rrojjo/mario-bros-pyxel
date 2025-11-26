# NOMBRE DEL ARCHIVO: app.py
import pyxel
from clases.constantes import ANCHO_PANTALLA, ALTO_PANTALLA
from clases.nivel import Nivel
from clases.mapa import Mapa


class App:
    def __init__(self):
        # Inicializamos la ventana con las dimensiones 368x192
        pyxel.init(ANCHO_PANTALLA, ALTO_PANTALLA, title="Mario Bros UC3M")

        # 1. Instanciamos el Nivel (puedes cambiar "FACIL" por "EXTREMO" para probar)
        # Esto define cuántas cintas tendrá el escenario[cite: 85].
        self.nivel = Nivel("FACIL")

        # 2. Creamos el Mapa pasándole el objeto nivel
        self.mapa = Mapa(self.nivel)

        # Arrancamos el bucle del juego
        pyxel.run(self.update, self.draw)

    def update(self):
        # Si pulsas Q, se cierra el juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Aquí irá la lógica de actualización en futuros Sprints
        pass

    def draw(self):
        # Limpiamos la pantalla (color negro = 0)
        pyxel.cls(0)

        # Dibujamos el escenario estático (Sprint 1)
        self.mapa.dibujar()