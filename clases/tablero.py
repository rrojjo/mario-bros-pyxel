# Contiene el tablero Juego/MarioBrosGame (lógica principal).

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
    """Esta clase contiene un simple tablero"""

    def __init__(self):
        # Inicializamos Pyxel con el tamaño MÁXIMO posible (240 de alto para Nivel Medio)
        # De esta forma mantenemos la relación de aspecto sin reiniciar la ventana.
        self.ancho_max = 368
        self.alto_max = 192

        pyxel.init(self.ancho_max, self.alto_max, title="Mario Bros Game")
        pyxel.load("assets/graficosprc.pyxres")

        # Estado inicial: MENÚ
        self.estado_juego = MENU

        # Opciones de menú
        self.dificultades_disponibles = ["FACIL", "MEDIO"]
        self.indice_dificultad = 0

        # Definir sonidos
        self.definir_sonidos()

        # Las variables del juego se inician en 'configurar_partida'
        self.mario = None
        self.luigi = None
        self.camion = None
        self.jefe = None
        self.cintas = []
        self.paquetes_cayendo = []
        self.puntos = 0
        self.fallos = 0

        # Ejecutando el juego
        pyxel.run(self.update, self.draw)

    def definir_sonidos(self):
        """Define los efectos de sonido en los bancos de Pyxel"""
        pyxel.sound(0).set("g2", "p", "7", "n", 4)
        pyxel.sound(1).set("c1d1", "n", "7", "f", 10)
        pyxel.sound(2).set("c3e3g3c4", "s", "6", "n", 8)
        pyxel.sound(3).set("c3b2a2g2", "t", "7", "s", 15)

    def configurar_partida(self, dificultad: str):
        """
        Configura todas las coordenadas, cintas y personajes
        según la dificultad elegida.
        """
        self.nivel = Nivel(dificultad)

        self.ancho = self.nivel.ancho_pantalla
        self.alto = self.nivel.alto_pantalla
        self.puntos_levelup = self.nivel.puntos_levelup

        # Reset de marcadores
        self.puntos = 0
        self.fallos = 0
        self.tiempo_reparto = 60
        self.contador_reparto = 0
        self.camion_volviendo = False
        self.paquetes_cayendo = []
        self.contador_frames = 0
        self.tiempo_aparicion = 120

        # --- CÁLCULO DE OFFSET Y MAPA ---
        # Si es MEDIO (alto 240), usamos todo el alto.
        # Si es FACIL (alto 192), dibujamos arriba (offset 0) y sobra negro abajo.

        if dificultad == "MEDIO":
            # Diferencia de altura para "bajar" el suelo y que quepan más pisos arriba
            self.offset_y = 0  # 240 - 192

            # Coordenada V del Tilemap (en TILES) para el fondo de nivel medio.
            # Según instrucciones: Coordenadas 0, 39 del tilemap.
            self.tilemap_y = 24 * 8  # Multiplicamos por 8 para tener píxeles
        else:
            # Nivel FACIL
            self.offset_y = 0
            self.tilemap_y = 0

        # --- 1. DEFINICIÓN DE ALTURAS ---
        # Base (Piso 0) desplazado según el offset (más abajo en nivel medio)
        suelo_y = 155 + self.offset_y

        # ALTURAS MARIO (Pisos Pares)
        self.alturas_mario = {
            0: suelo_y,
            2: 123 + self.offset_y,
            4: 75 + self.offset_y,
        }

        # Si hay más pisos (Nivel Medio), añadimos altura superior
        if self.nivel.num_pisos > 5:
            # Piso 6: 48 píxeles más arriba que el piso 4 original
            self.alturas_mario[6] = 75 + self.offset_y - 48

            # ALTURAS LUIGI (Pisos Impares)
        self.alturas_luigi = {
            1: suelo_y,
            3: 107 + self.offset_y,
            5: 59 + self.offset_y,
        }

        if self.nivel.num_pisos > 5:
            # Piso 7: 48 píxeles más arriba que el piso 5 original
            self.alturas_luigi[7] = 59 + self.offset_y - 48

        # --- CREAR OBJETOS ---
        # Posiciones iniciales
        self.inicio_mario = {'x': 265, 'y': self.alturas_mario[0], 'piso': 0}
        self.inicio_luigi = {'x': 93, 'y': self.alturas_luigi[1], 'piso': 1}

        # Altura del camión: Siempre en el piso más alto de Luigi (Impar)
        # En fácil: Piso 5 (y=59). En Medio: Piso 7 (y=11 aprox).
        y_camion = self.alturas_luigi[
                       self.nivel.num_pisos] + 15  # Ajuste visual
        self.inicio_camion = {'x': 10, 'y': y_camion}

        self.mario = Personaje(self.inicio_mario['x'], self.inicio_mario['y'],
                               self.inicio_mario['piso'], "Mario")
        self.luigi = Personaje(self.inicio_luigi['x'], self.inicio_luigi['y'],
                               self.inicio_luigi['piso'], "Luigi")
        self.camion = Camion(self.inicio_camion['x'], self.inicio_camion['y'])
        self.jefe = Jefe(0, 0)

        # Variables de castigo
        self.personaje_castigado = None
        self.memoria_personaje = {}

        # --- 3. CREACIÓN DE CINTAS ---
        self.cintas = []
        x_cinta0 = 282
        x_resto_cintas = 106

        # Cintas Originales (0-5) ajustadas con offset_y
        self.cintas.append(Cinta(0, x_cinta0, 152 + self.offset_y, 0))
        self.cintas.append(Cinta(1, x_resto_cintas, 152 + self.offset_y, 1))
        self.cintas.append(Cinta(2, x_resto_cintas, 128 + self.offset_y, 2))
        self.cintas.append(Cinta(3, x_resto_cintas, 104 + self.offset_y, 3))
        self.cintas.append(Cinta(4, x_resto_cintas, 80 + self.offset_y, 4))
        self.cintas.append(Cinta(5, x_resto_cintas, 56 + self.offset_y, 5))

        # Cintas Nuevas (MEDIO) - Se añaden encima
        if self.nivel.num_cintas > 6:
            # Cinta 6 (Mario) -> Encima de la 5
            self.cintas.append(
                Cinta(6, x_resto_cintas, 56 + self.offset_y - 24, 6))
            # Cinta 7 (Luigi) -> Encima de la 6
            self.cintas.append(
                Cinta(7, x_resto_cintas, 56 + self.offset_y - 48, 7))

        self.estado_juego = JUGANDO

    def reiniciar_juego(self):
        """Reinicia la partida manteniendo la dificultad actual"""
        self.configurar_partida(self.nivel.dificultad)

    def iniciar_reparto(self):
        pyxel.play(1, 2)
        self.estado_juego = REPARTO
        self.contador_reparto = self.tiempo_reparto
        self.camion_volviendo = False
        for cinta in self.cintas:
            paquete_borde = cinta.paquete_llego_al_final()
            if paquete_borde:
                cinta.retirar_paquete(paquete_borde)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- LÓGICA DE MENÚ ---
        if self.estado_juego == MENU:
            # Navegar menú
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                if self.indice_dificultad == 0:
                    self.indice_dificultad = 1
                else:
                    self.indice_dificultad = 0

            # Seleccionar con ESPACIO
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                dificultad_elegida = self.dificultades_disponibles[
                    self.indice_dificultad]
                self.configurar_partida(dificultad_elegida)
            return

        # --- LÓGICA DE GAME OVER ---
        if self.fallos >= 3:
            if pyxel.btnp(pyxel.KEY_R):
                # VOLVER AL MENÚ
                self.estado_juego = MENU
            return

        self.jefe.update()
        self.mario.update()
        self.luigi.update()

        # --- ESTADO: CASTIGO ---
        if self.estado_juego == CASTIGO:
            if not self.jefe.visible:
                p = self.personaje_castigado
                datos = self.memoria_personaje
                p.piso = datos['piso']
                p.y = datos['y']
                p.set_mirada_invertida(False)
                self.estado_juego = JUGANDO
            return

        # --- ESTADO: REPARTO ---
        if self.estado_juego == REPARTO:
            velocidad_camion = 2
            if not self.camion_volviendo:
                if self.camion.x > -60:
                    self.camion.mover(-velocidad_camion)
                else:
                    self.contador_reparto -= 1
                    if self.contador_reparto <= 0:
                        self.camion.vaciar()
                        self.camion_volviendo = True
            else:
                if self.camion.x < 10:
                    self.camion.mover(velocidad_camion)
                else:
                    self.camion.x = 10
                    self.camion_volviendo = False
                    self.estado_juego = JEFE_MANDANDO
                    # Jefe aparece en posición de trabajo (siempre visible arriba)
                    self.jefe.aparecer_trabajo(39, self.alturas_luigi[
                        self.nivel.num_pisos] + 100, 180)
                    # Corregimos Y del jefe para que salga cerca del camión o techo
                    # En fácil sale en Y=39, 171 (No tiene sentido coordenadas fijas si cambia altura)
                    # Lo dejamos fijo arriba relativo al techo del nivel
                    self.jefe.aparecer_trabajo(39, 171 + self.offset_y, 180)
            return

        # --- ESTADO: JEFE MANDANDO ---
        if self.estado_juego == JEFE_MANDANDO:
            if not self.jefe.visible:
                self.estado_juego = JUGANDO
            return

        # ==========================================
        #  LÓGICA PRINCIPAL (JUGANDO)
        # ==========================================
        velocidad_caida = 4
        paquetes_validos = []
        for p in self.paquetes_cayendo:
            p.y += velocidad_caida
            if p.y < self.alto_max:  # Usamos alto_max para que caigan hasta el fondo de pantalla
                paquetes_validos.append(p)
        self.paquetes_cayendo = paquetes_validos

        # --- MOVIMIENTO MARIO ---
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

        # --- MOVIMIENTO LUIGI ---
        if pyxel.btnp(pyxel.KEY_W):
            if self.luigi.piso == 0:
                siguiente_piso = 1
            else:
                siguiente_piso = self.luigi.piso + 2

            if siguiente_piso in self.alturas_luigi:
                nueva_y = self.alturas_luigi[siguiente_piso]
                self.luigi.subir(nueva_y)
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

        # --- LÓGICA DE PAQUETES ---
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
                # Ajustamos spawn X relativo a cinta 0
                nuevo = Paquete(cinta0.x + 70, cinta0.y, 0, 0)
                cinta0.agregar_paquete(nuevo)
            else:
                self.contador_frames = self.tiempo_aparicion

        for i in range(len(self.cintas)):
            cinta = self.cintas[i]
            cinta.actualizar_paquetes()
            paquete_saliente = cinta.paquete_llego_al_final()

            if paquete_saliente:
                recogido = False

                # Cintas PARES (0, 2, 4, 6) -> MARIO
                if cinta.numero % 2 == 0:
                    if self.mario.piso == cinta.piso:
                        recogido = True
                # Cintas IMPARES (1, 3, 5, 7) -> LUIGI
                else:
                    if self.luigi.piso == cinta.piso:
                        recogido = True

                cinta.retirar_paquete(paquete_saliente)

                if recogido:
                    self.puntos += 1
                    pyxel.play(0, 0)
                    if cinta.numero % 2 == 0:
                        self.mario.animar_recogida()
                    else:
                        self.luigi.animar_recogida()

                    # Si NO es la última cinta
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

                    # Si ES la última cinta (Va al camión)
                    elif cinta.numero == (self.nivel.num_cintas - 1):
                        self.camion.cargar_paquete(paquete_saliente)
                        if self.camion.esta_lleno():
                            self.puntos += 10
                            self.iniciar_reparto()
                else:
                    # FALLO
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

                    self.personaje_castigado = culpable
                    self.memoria_personaje = {
                        'piso': culpable.piso,
                        'y': culpable.y
                    }
                    culpable.set_mirada_invertida(True)

                    # LOGICA CASTIGO (Piso superior dinámico)
                    piso_max_mario = self.nivel.num_pisos - 1 if self.nivel.num_pisos % 2 != 0 else self.nivel.num_pisos
                    # En fácil (5 pisos): Mario max piso 4. En medio (7 pisos): Mario max piso 6.
                    piso_max_mario = self.nivel.num_pisos - 1
                    # Corrección: si num_pisos es 5, mario va al 4. Si es 7, mario va al 6. Correcto.

                    piso_max_luigi = self.nivel.num_pisos  # Piso del camión (5 o 7)

                    if es_culpa_mario:
                        culpable.piso = piso_max_mario
                        culpable.y = self.alturas_mario[piso_max_mario]

                        # Jefe aparece junto a Mario
                        self.jefe.aparecer_castigo(295, culpable.y, 180,
                                                   mirar_izquierda=True)
                    else:
                        culpable.piso = piso_max_luigi
                        culpable.y = self.alturas_luigi[piso_max_luigi]

                        # Jefe aparece junto a Luigi
                        self.jefe.aparecer_castigo(77, culpable.y, 180,
                                                   mirar_izquierda=False)

                    self.estado_juego = CASTIGO
                    return

    def draw(self):
        # Borra la pantalla
        pyxel.cls(0)

        # --- DIBUJO DEL MENÚ (Primero) ---
        if self.estado_juego == MENU:
            centro_x = self.ancho_max // 2
            centro_y = self.alto_max // 2

            # Dibujamos el fondo del menú en coordenadas 152, 200 (pixels)
            # Centrado en pantalla
            pyxel.blt(centro_x - 50, centro_y - 20, 0, 152, 200, 100, 40)

            # Textos del menú
            pyxel.text(centro_x - 60, centro_y - 12, "SELECCIONA EL NIVEL DE "
                                                     "DIFICULTAD"
                                                     ":", 10)

            col_facil = 7
            col_medio = 7

            if self.indice_dificultad == 0:
                col_facil = 8  # Rojo si seleccionado
                pyxel.text(centro_x - 10, centro_y, "> FACIL", col_facil)
                pyxel.text(centro_x - 10, centro_y + 10, "  MEDIO", col_medio)
            else:
                col_medio = 8
                pyxel.text(centro_x - 10, centro_y, "  FACIL", col_facil)
                pyxel.text(centro_x - 10, centro_y + 10, "> MEDIO", col_medio)

            pyxel.text(centro_x - 47, centro_y + 25, "(ESPACIO o ENTER para "
                                                     "jugar)", 6)
            return

        # --- DIBUJO DEL JUEGO ---
        # Dibujamos tilemap.
        # tilemap_y = 0 para Fácil.
        # tilemap_y = 39*8 para Medio (según instrucciones).
        # self.alto es el alto lógico del nivel (192 o 240).
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

        # Columna central
        for cinta in self.cintas:
            pyxel.blt(184, cinta.y - 3, 0, 136, 8, 16, 16)

        # Dispensador
        pyxel.blt(352, 158 + self.offset_y, 0, 128, 70, 16, 6)

        self.jefe.draw()

        pyxel.text(10, 5, f"PUNTOS: {self.puntos}", 7)
        pyxel.text(100, 5, f"FALLOS: {self.fallos}/3", 8)

        # PANTALLA GAME OVER
        if self.fallos >= 3:
            centro_x = 192
            centro_y = self.alto_max // 2  # Centrado en la ventana total

            pyxel.blt(centro_x - 50, centro_y - 20, 0, 152, 200, 100, 40)

            pyxel.text(centro_x - 18, centro_y - 12, "GAME OVER", 8)
            pyxel.text(centro_x - 34, centro_y - 2, "Pulsa Q para salir", 6)
            pyxel.text(centro_x - 34, centro_y + 8, "Pulsa R para MENU", 6)