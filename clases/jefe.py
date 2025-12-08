# Clase jefe

import pyxel


class Jefe:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visible = False
        self.mirando_izquierda = False
        self.timer_animacion = 0

        # Modo de animación: "TRABAJO" o "CASTIGO"
        self.modo = "TRABAJO"

        # Animación
        self.frame_actual = 0
        self.contador_cambio = 0
        self.velocidad_animacion = 10

    def aparecer_trabajo(self, x: int, y: int, duracion: int):
        """El jefe sale para mandar a trabajar (descanso camión)"""
        self.x = x
        self.y = y
        self.visible = True
        self.modo = "TRABAJO"
        self.timer_animacion = duracion
        self.frame_actual = 0
        self.contador_cambio = 0
        self.mirando_izquierda = False  # Mira al centro

    def aparecer_castigo(self, x: int, y: int, duracion: int,
                         mirar_izquierda: bool):
        """El jefe sale para castigar un fallo"""
        self.x = x
        self.y = y
        self.visible = True
        self.modo = "CASTIGO"
        self.timer_animacion = duracion
        self.frame_actual = 0
        self.contador_cambio = 0
        self.mirando_izquierda = mirar_izquierda

    def ocultar(self):
        self.visible = False
        self.timer_animacion = 0

    def update(self):
        if self.visible:
            self.timer_animacion -= 1
            if self.timer_animacion <= 0:
                self.ocultar()

            # Animación
            self.contador_cambio += 1
            if self.contador_cambio >= self.velocidad_animacion:
                self.contador_cambio = 0
                if self.frame_actual == 0:
                    self.frame_actual = 1
                else:
                    self.frame_actual = 0

    def draw(self):
        if self.visible:
            # 1. Determinar dirección (Flip H)
            ancho = 16
            if self.mirando_izquierda:
                ancho = -16

            # 2. Determinar coordenadas según el MODO
            u = 0
            v = 0

            if self.modo == "TRABAJO":
                # Animación: (0, 32) y (16, 32)
                v = 32
                if self.frame_actual == 0:
                    u = 0
                else:
                    u = 16
                texto = "¡A TRABAJAAAAR!"

            elif self.modo == "CASTIGO":
                # Animación: (0, 48) y (0, 64) -> Coordenadas verticales
                u = 0
                if self.frame_actual == 0:
                    v = 48
                else:
                    v = 64
                texto = "¡¡#@%&?$#!!"  # Gruñido/Insultos censurados

            # 3. Dibujar
            pyxel.blt(self.x, self.y, 0, u, v, ancho, 16, 15)

            # Texto (Blanco = 7)
            pyxel.text(self.x - 10, self.y - 10, texto, 7)