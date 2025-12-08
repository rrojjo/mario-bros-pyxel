# Contiene constantes de estado y la clase Tablero (lógica principal).

from clases.personaje import Personaje
from clases.camion import Camion
from clases.cinta import Cinta
from clases.paquete import Paquete
from clases.jefe import Jefe
from clases.nivel import Nivel
import pyxel

# --- CONSTANTES DE ESTADO ---
MENU = 0
JUGANDO = 1
REPARTO = 2
GAMEOVER = 3
JEFE_MANDANDO = 4
CASTIGO = 5


class Tablero:
    """
    Controlador principal del juego. Gestiona la máquina de estados,
    el bucle principal (Update/Draw) y la interacción entre entidades.
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN Y CONFIGURACIÓN

    def __init__(self):
        # Se inicializa con dimensiones máximas para soportar todos los
        # niveles de dificultad sin redimensionar
        self.ancho_max = 368
        self.alto_max = 192

        pyxel.init(self.ancho_max, self.alto_max, title="Mario Bros Game")
        pyxel.load("assets/graficosprc.pyxres")

        self.estado_juego = MENU
        self.dificultades_disponibles = ["FACIL", "MEDIO"]
        self.indice_dificultad = 0

        self.definir_sonidos()

        # --- DECLARACIÓN DE VARIABLES (Corrección de avisos) ---
        # Inicializamos todo aquí con valores por defecto para evitar
        # el aviso "defined outside __init__".

        # Variables de Nivel y Entorno
        self.nivel = None
        self.ancho = 0
        self.alto = 0
        self.puntos_levelup = 0
        self.offset_y = 0
        self.tilemap_y = 0
        self.alturas_mario = {}
        self.alturas_luigi = {}

        # Puntos de inicio
        self.inicio_mario = {}
        self.inicio_luigi = {}
        self.inicio_camion = {}

        # Entidades (Se crean realmente en configurar_partida)
        self.mario = None
        self.luigi = None
        self.camion = None
        self.jefe = None
        self.cintas = []

        # Lógica de juego y puntuación
        self.puntos = 0
        self.fallos = 0

        # Lógica de tiempos y estados
        self.tiempo_reparto = 60
        self.contador_reparto = 0
        self.camion_volviendo = False
        self.paquetes_cayendo = []
        self.contador_frames = 0
        self.tiempo_aparicion = 0

        # Variables para bonus de vida
        self.camiones_completados = 0
        self.meta_camiones = 0

        # Variables de lógica de castigo
        self.personaje_castigado = None
        self.memoria_personaje = {}

        # Arrancar el bucle principal (SIEMPRE AL FINAL DEL INIT)
        pyxel.run(self.update, self.draw)

    def definir_sonidos(self):
        pyxel.sound(0).set("g2", "p", "7", "n", 4)
        pyxel.sound(1).set("c1d1", "n", "7", "f", 10)
        pyxel.sound(2).set("c3e3g3c4", "s", "6", "n", 8)
        pyxel.sound(3).set("c3b2a2g2", "t", "7", "s", 15)

    def configurar_partida(self, dificultad: str):
        """
        Inicializa nivel, cintas y personajes calculando posiciones dinámicas
        según la dificultad y el tamaño del tilemap.
        """
        self.nivel = Nivel(dificultad)

        self.ancho = self.nivel.ancho_pantalla
        self.alto = self.nivel.alto_pantalla
        self.puntos_levelup = self.nivel.puntos_levelup

        self.puntos = 0
        self.fallos = 0

        self.camiones_completados = 0
        if dificultad == "FACIL":
            self.meta_camiones = 3
        else:
            self.meta_camiones = 5

        self.tiempo_reparto = 60
        self.contador_reparto = 0
        self.camion_volviendo = False
        self.paquetes_cayendo = []
        self.contador_frames = 0
        self.tiempo_aparicion = 120

        # --- Cálculo de Mapa ---
        # Ajuste vertical del escenario para niveles con mayor número de pisos
        if dificultad == "MEDIO":
            self.offset_y = 0 # Desplazamiento para poder implementar más
            # dificultad
            self.tilemap_y = 24 * 8
        else:
            self.offset_y = 0
            self.tilemap_y = 0

        suelo_y = 155 + self.offset_y

        # Definición de alturas para Mario (Pisos Pares)
        self.alturas_mario = {
            0: suelo_y,
            2: 123 + self.offset_y,
            4: 75 + self.offset_y,
        }

        if self.nivel.num_pisos > 5:
            self.alturas_mario[6] = 75 + self.offset_y - 48

        # Definición de alturas para Luigi (Pisos Impares)
        self.alturas_luigi = {
            1: suelo_y,
            3: 107 + self.offset_y,
            5: 59 + self.offset_y,
        }

        if self.nivel.num_pisos > 5:
            self.alturas_luigi[7] = 59 + self.offset_y - 48

        # --- Instanciación de Objetos ---
        self.inicio_mario = {'x': 265, 'y': self.alturas_mario[0], 'piso': 0}
        self.inicio_luigi = {'x': 93, 'y': self.alturas_luigi[1], 'piso': 1}

        # El camión siempre aparece en el nivel del techo (piso máximo de
        # Luigi)
        y_camion = self.alturas_luigi[
                       self.nivel.num_pisos] + 15
        self.inicio_camion = {'x': 10, 'y': y_camion}

        self.mario = Personaje(self.inicio_mario['x'], self.inicio_mario['y'],
                               self.inicio_mario['piso'], "Mario")
        self.luigi = Personaje(self.inicio_luigi['x'], self.inicio_luigi['y'],
                               self.inicio_luigi['piso'], "Luigi")
        self.camion = Camion(self.inicio_camion['x'], self.inicio_camion['y'])
        self.jefe = Jefe(0, 0)

        self.personaje_castigado = None
        self.memoria_personaje = {}

        # --- Generación de Cintas ---
        self.cintas = []
        x_cinta0 = 282
        x_resto_cintas = 106

        # Cintas Base (0-5)
        self.cintas.append(Cinta(0, x_cinta0, 152 + self.offset_y, 0))
        self.cintas.append(Cinta(1, x_resto_cintas, 152 + self.offset_y, 1))
        self.cintas.append(Cinta(2, x_resto_cintas, 128 + self.offset_y, 2))
        self.cintas.append(Cinta(3, x_resto_cintas, 104 + self.offset_y, 3))
        self.cintas.append(Cinta(4, x_resto_cintas, 80 + self.offset_y, 4))
        self.cintas.append(Cinta(5, x_resto_cintas, 56 + self.offset_y, 5))

        # Cintas Extra (Dificultad Media/Alta)
        if self.nivel.num_cintas > 6:
            self.cintas.append(
                Cinta(6, x_resto_cintas, 56 + self.offset_y - 24, 6))
            self.cintas.append(
                Cinta(7, x_resto_cintas, 56 + self.offset_y - 48, 7))

        self.estado_juego = JUGANDO

    def reiniciar_juego(self):
        self.configurar_partida(self.nivel.dificultad)

    def iniciar_reparto(self):
        """Pausa el juego e inicia la secuencia del camión."""
        pyxel.play(1, 2)
        self.estado_juego = REPARTO
        self.contador_reparto = self.tiempo_reparto
        self.camion_volviendo = False

        # Limpieza de paquetes en bordes para evitar glitches visuales
        for cinta in self.cintas:
            paquete_borde = cinta.paquete_llego_al_final()
            if paquete_borde:
                cinta.retirar_paquete(paquete_borde)

    # -------------------------------------------------------------------------
    # BUCLE DE ACTUALIZACIÓN (UPDATE)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- ESTADO: MENÚ ---
        if self.estado_juego == MENU:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                if self.indice_dificultad == 0:
                    self.indice_dificultad = 1
                else:
                    self.indice_dificultad = 0

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                dificultad_elegida = self.dificultades_disponibles[
                    self.indice_dificultad]
                self.configurar_partida(dificultad_elegida)
            return

        # --- ESTADO: GAME OVER ---
        if self.fallos >= 3:
            if pyxel.btnp(pyxel.KEY_R):
                self.estado_juego = MENU
            return

        self.jefe.update()
        self.mario.update()
        self.luigi.update()

        # --- ESTADO: CASTIGO (Pausa temporal por fallo) ---
        if self.estado_juego == CASTIGO:
            if not self.jefe.visible:
                # Restaurar personaje a su posición original
                p = self.personaje_castigado
                datos = self.memoria_personaje
                p.piso = datos['piso']
                p.y = datos['y']
                p.set_mirada_invertida(False)
                self.estado_juego = JUGANDO
            return

        # --- ESTADO: REPARTO (Animación Camión) ---
        if self.estado_juego == REPARTO:
            velocidad_camion = 2
            if not self.camion_volviendo:
                # Ida
                if self.camion.x > -60:
                    self.camion.mover(-velocidad_camion)
                else:
                    self.contador_reparto -= 1
                    if self.contador_reparto <= 0:
                        self.camion.vaciar()
                        self.camion_volviendo = True
            else:
                # Vuelta
                if self.camion.x < 10:
                    self.camion.mover(velocidad_camion)
                else:
                    self.camion.x = 10
                    self.camion_volviendo = False
                    self.estado_juego = JEFE_MANDANDO
                    # El jefe ordena volver al trabajo
                    self.jefe.aparecer_trabajo(39, 171 + self.offset_y, 180)
            return

        # --- ESTADO: JEFE MANDANDO (Pausa narrativa) ---
        if self.estado_juego == JEFE_MANDANDO:
            if not self.jefe.visible:
                self.estado_juego = JUGANDO
            return

        # ---------------------------------------------------------------------
        #  LÓGICA PRINCIPAL (JUGANDO)

        velocidad_caida = 4
        paquetes_validos = []
        for p in self.paquetes_cayendo:
            p.y += velocidad_caida
            if p.y < self.alto_max:
                paquetes_validos.append(p)
        self.paquetes_cayendo = paquetes_validos

        # Control Mario (Pisos Pares)
        if pyxel.btnp(pyxel.KEY_UP):
            siguiente_piso = self.mario.piso + 2
            if siguiente_piso in self.alturas_mario:
                nueva_y = self.alturas_mario[siguiente_piso]
                self.mario.subir(nueva_y)

        if pyxel.btnp(pyxel.KEY_DOWN):
            siguiente_piso = self.mario.piso - 2
            if siguiente_piso in self.alturas_mario:
                nueva_y = self.alturas_mario[siguiente_piso]
                self.mario.bajar(nueva_y)

        # Control Luigi (Pisos Impares)
        if pyxel.btnp(pyxel.KEY_W):
            if self.luigi.piso == 0:
                siguiente_piso = 1
            else:
                siguiente_piso = self.luigi.piso + 2

            if siguiente_piso in self.alturas_luigi:
                nueva_y = self.alturas_luigi[siguiente_piso]
                self.luigi.subir(nueva_y)
                # Corrección visual si se salta desde piso 0
                if self.luigi.piso == 2 and siguiente_piso == 1:
                    self.luigi.piso = 1

        if pyxel.btnp(pyxel.KEY_S):
            if self.luigi.piso == 1:
                siguiente_piso = 0
            else:
                siguiente_piso = self.luigi.piso - 2

            if siguiente_piso in self.alturas_luigi:
                nueva_y = self.alturas_luigi[siguiente_piso]
                self.luigi.bajar(nueva_y)
                if siguiente_piso == 0:
                    self.luigi.piso = 0

        # --- Generación de Paquetes (Dificultad Progresiva) ---
        base_minima = 3
        incremento_dificultad = self.puntos // self.puntos_levelup
        min_paquetes = base_minima + incremento_dificultad

        paquetes_en_juego = 0
        for c in self.cintas:
            paquetes_en_juego += len(c.paquetes)
        paquetes_en_juego += len(self.paquetes_cayendo)

        self.contador_frames += 1

        if self.contador_frames >= self.tiempo_aparicion:
            if paquetes_en_juego < min_paquetes:
                self.contador_frames = 0
                cinta0 = self.cintas[0]
                nuevo = Paquete(cinta0.x + 70, cinta0.y, 0, 0)
                cinta0.agregar_paquete(nuevo)
            else:
                self.contador_frames = self.tiempo_aparicion

        # --- Actualización de Cintas y Colisiones ---
        for i in range(len(self.cintas)):
            cinta = self.cintas[i]
            cinta.actualizar_paquetes()
            paquete_saliente = cinta.paquete_llego_al_final()

            if paquete_saliente:
                recogido = False

                # Lógica de Responsabilidad:
                # Cintas PARES -> Mario | Cintas IMPARES -> Luigi
                if cinta.numero % 2 == 0:
                    if self.mario.piso == cinta.piso:
                        recogido = True
                else:
                    if self.luigi.piso == cinta.piso:
                        recogido = True

                cinta.retirar_paquete(paquete_saliente)

                if recogido:
                    # Éxito: Puntos y transferencia
                    self.puntos += 1
                    pyxel.play(0, 0)
                    if cinta.numero % 2 == 0:
                        self.mario.animar_recogida()
                    else:
                        self.luigi.animar_recogida()

                    # Si no es la última cinta, pasa a la siguiente
                    if cinta.numero < (self.nivel.num_cintas - 1):
                        siguiente_cinta = self.cintas[i + 1]

                        if siguiente_cinta.numero % 2 != 0:
                            paquete_saliente.x = siguiente_cinta.x + 146
                        else:
                            paquete_saliente.x = siguiente_cinta.x

                        paquete_saliente.y = siguiente_cinta.y
                        paquete_saliente.piso = siguiente_cinta.piso
                        paquete_saliente.cinta_actual = siguiente_cinta.numero
                        siguiente_cinta.agregar_paquete(paquete_saliente)

                    # Si es la última, va al camión
                    elif cinta.numero == (self.nivel.num_cintas - 1):
                        self.camion.cargar_paquete(paquete_saliente)
                        if self.camion.esta_lleno():
                            self.puntos += 10
                            self.camiones_completados += 1
                            if self.camiones_completados % self.meta_camiones == 0:
                                if self.fallos > 0:
                                    self.fallos -= 1
                                    pyxel.play(0, 0)
                            self.iniciar_reparto()
                else:
                    # Fallo: Castigo
                    self.fallos += 1
                    pyxel.play(0, 1)
                    if self.fallos >= 3:
                        pyxel.play(1, 3)
                    self.paquetes_cayendo.append(paquete_saliente)

                    es_culpa_mario = (cinta.numero % 2 == 0)
                    if es_culpa_mario:
                        culpable = self.mario
                    else:
                        culpable = self.luigi

                    # Configurar escena de castigo (Teletransporte al piso
                    # superior)
                    self.personaje_castigado = culpable
                    self.memoria_personaje = {
                        'piso': culpable.piso,
                        'y': culpable.y
                    }
                    culpable.set_mirada_invertida(True)

                    piso_max_mario = self.nivel.num_pisos - 1
                    piso_max_luigi = self.nivel.num_pisos

                    if es_culpa_mario:
                        culpable.piso = piso_max_mario
                        culpable.y = self.alturas_mario[piso_max_mario]
                        self.jefe.aparecer_castigo(295, culpable.y, 180,
                                                   mirar_izquierda=True)
                    else:
                        culpable.piso = piso_max_luigi
                        culpable.y = self.alturas_luigi[piso_max_luigi]
                        self.jefe.aparecer_castigo(77, culpable.y, 180,
                                                   mirar_izquierda=False)

                    self.estado_juego = CASTIGO
                    return

    # -------------------------------------------------------------------------
    # RENDERIZADO

    def draw(self):
        pyxel.cls(0)

        # --- MENÚ ---
        if self.estado_juego == MENU:
            centro_x = self.ancho_max // 2
            centro_y = self.alto_max // 2

            pyxel.blt(centro_x - 50, centro_y - 20, 0, 152, 200, 100, 40)
            pyxel.text(centro_x - 60, centro_y - 27, "SELECCIONA EL NIVEL DE "
                                                     "DIFICULTAD"
                                                     ":", 10)

            col_facil = 7
            col_medio = 7

            if self.indice_dificultad == 0:
                col_facil = 8
                pyxel.text(centro_x - 10, centro_y - 15, "> FACIL", col_facil)
                pyxel.text(centro_x - 10, centro_y - 5, "  MEDIO", col_medio)
            else:
                col_medio = 8
                pyxel.text(centro_x - 10, centro_y - 15, "  FACIL", col_facil)
                pyxel.text(centro_x - 10, centro_y - 5, "> MEDIO", col_medio)

            pyxel.text(centro_x - 47, centro_y + 10, "(ESPACIO o ENTER para "
                                                     "jugar)", 6)
            pyxel.text(centro_x - 38, centro_y + 25, "(Q para cerrar el "
                                                     "juego)", 6)
            return

        # --- JUEGO ---
        pyxel.bltm(0, 0, 0, 0, self.tilemap_y, self.ancho, self.alto, 0)

        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)

        pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprite)
        for caja in self.camion.carga_visual:
            pyxel.blt(caja["x"], caja["y"], *caja["sprite"])

        for cinta in self.cintas:
            for p in cinta.paquetes:
                pyxel.blt(p.x, p.y, *p.sprite)

        for p in self.paquetes_cayendo:
            pyxel.blt(p.x, p.y, *p.sprite)

        # Decoración (Columna central y dispensador)
        for cinta in self.cintas:
            pyxel.blt(184, cinta.y - 3, 0, 136, 8, 16, 16)

        pyxel.blt(352, 158 + self.offset_y, 0, 128, 70, 16, 6)

        self.jefe.draw()

        pyxel.text(10, 5, f"PUNTOS: {self.puntos}", 7)
        pyxel.text(100, 5, f"FALLOS: {self.fallos}/3", 8)

        # --- Pantalla de GAME OVER ---
        if self.fallos >= 3:
            centro_x = 192
            centro_y = self.alto_max // 2

            pyxel.blt(centro_x - 50, centro_y - 20, 0, 152, 200, 100, 40)

            pyxel.text(centro_x - 18, centro_y - 12, "GAME OVER", 8)
            pyxel.text(centro_x - 34, centro_y - 2, "Pulsa Q para salir", 6)
            pyxel.text(centro_x - 34, centro_y + 8, "Pulsa R para MENU", 6)