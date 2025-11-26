#Contiene las estructuras visuales y los cambios estructurales del mapa
# según el nivel del juego.

# mapa.py
import pyxel
from clases.constantes import *  # Asegúrate de que la ruta sea correcta


class Mapa:
    def __init__(self, nivel):
        self.nivel = nivel
        self.grid = []
        self.generar_escenario()

    def generar_escenario(self):
        """
        Define el mapa visualmente usando variables directas.
        """
        # 1. Asignamos las constantes a variables de 1 letra
        V = VACIO
        T = CAMION
        S = SUELO
        H = ESCALERA
        C = CINTA
        I = INICIO_PAQUETE

        # 2. Definimos la Matriz Final DIRECTAMENTE en self.grid
        self.grid = [
            # Fila 0: Cielo
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 1: Cielo
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 2: Cielo
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 3: Techo
            [T, T, S, H, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, H, V, V,
             V],
            # Fila 4: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 5: Cinta 5
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 6: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 7: Cinta 4
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 8: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 9: Cinta 3
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 10: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 11: Cinta 2
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 12: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 13: Cinta 1
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 14: Espacio
            [V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,
             V],
            # Fila 15: Cinta 0
            [V, V, V, H, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, H, V, V,
             V],
            # Fila 16: Suelo Base
            [S, S, S, H, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, H, I, V,
             V]
        ]

        # HE ELIMINADO LA LÍNEA QUE DABA ERROR AQUÍ.
        # Ya no necesitamos convertir nada porque self.grid ya está listo.

    def dibujar(self):
        for y, fila in enumerate(self.grid):
            for x, celda in enumerate(fila):
                # Importante verificar que la celda tiene dibujo asociado
                if celda in SPRITES:
                    u, v, w, h, colkey = SPRITES[celda]
                    px, py = x * TAMANO_BLOQUE, y * TAMANO_BLOQUE

                    # Ajustes de centrado
                    offset_y = TAMANO_BLOQUE - h if h < TAMANO_BLOQUE else 0
                    offset_x = (
                                           TAMANO_BLOQUE - w) // 2 if w < TAMANO_BLOQUE else 0

                    pyxel.blt(px + offset_x, py + offset_y, 0, u, v, w, h,
                              colkey)
