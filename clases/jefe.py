# Contiene la clase jefe

import pyxel

class Jefe:
    """
    Controla las apariciones y animaciones del personaje 'The Boss'.
    Maneja dos estados principales: 'TRABAJO' (fin de descanso) y 'CASTIGO'
    (fallo).
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visible = False
        self.mirando_izquierda = False
        self.timer_animacion = 0
        self.modo = "TRABAJO"

        # Control de animación
        self.frame_actual = 0
        self.contador_cambio = 0
        self.velocidad_animacion = 10

    # -------------------------------------------------------------------------
    # GESTIÓN DE ESTADOS Y VISIBILIDAD

    def aparecer_trabajo(self, x: int, y: int, duracion: int):
        """Configura al Jefe para ordenar la vuelta al trabajo."""
        self.x = x
        self.y = y
        self.visible = True
        self.modo = "TRABAJO"
        self.timer_animacion = duracion
        self.frame_actual = 0
        self.contador_cambio = 0
        self.mirando_izquierda = False

    def aparecer_castigo(self, x: int, y: int, duracion: int,
                         mirar_izquierda: bool):
        """Configura al Jefe para regañar al jugador tras un error."""
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

    # -------------------------------------------------------------------------
    # BUCLE PRINCIPAL (UPDATE & DRAW)

    def update(self):
        if self.visible:
            self.timer_animacion -= 1
            if self.timer_animacion <= 0:
                self.ocultar()

            # Ciclo de animación (toggle entre frames)
            self.contador_cambio += 1
            if self.contador_cambio >= self.velocidad_animacion:
                self.contador_cambio = 0
                if self.frame_actual == 0:
                    self.frame_actual = 1
                else:
                    self.frame_actual = 0

    def draw(self):
        if self.visible:
            # Configuración de orientación
            ancho = 16
            if self.mirando_izquierda:
                ancho = -16

            # Selección de sprite según el modo (Coordenadas en el banco de
            # imágenes)
            u = 0
            v = 0

            if self.modo == "TRABAJO":
                v = 32
                if self.frame_actual == 0:
                    u = 0
                else:
                    u = 16
                texto = "¡A TRABAJAAAAR!"

            elif self.modo == "CASTIGO":
                u = 0
                if self.frame_actual == 0:
                    v = 48
                else:
                    v = 64
                texto = "¡¡#@%&?$#!!"

            pyxel.blt(self.x, self.y, 0, u, v, ancho, 16, 15)
            pyxel.text(self.x - 10, self.y - 10, texto, 7)