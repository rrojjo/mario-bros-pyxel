# Contiene el tablero Juego/MarioBrosGame (lógica principal).

from clases.personaje import Personaje
from clases.camion import Camion
from clases.cinta import Cinta
from clases.paquete import Paquete
from clases.jefe import Jefe
import pyxel

# --- CONSTANTES DE ESTADO ---
JUGANDO = 1
REPARTO = 2
GAMEOVER = 3
JEFE_MANDANDO = 4
CASTIGO = 5

class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int, pisos, puntos_levelup: int):
        # 1. Asignar atributos usando los setters
        self.ancho = ancho
        self.alto = alto
        self.pisos = pisos

        # Guardamos la regla de dificultad
        self.puntos_levelup = puntos_levelup

        # --- CONTROL DE ESTADOS (SPRINT 4) ---
        self.estado_juego = JUGANDO
        self.tiempo_reparto = 180  # 180 frames = 3 segundos de descanso
        self.contador_reparto = 0

        # --- 1. DEFINICIÓN DE ALTURAS (Basado en tu imagen) ---
        # Mapeamos: Número de Piso Lógico -> Coordenada Y visual
        # Esto soluciona que las distancias entre pisos no sean iguales.

        # PISO 0: Suelo común (Y=154 según tu código anterior)
        suelo_y = 155

        # ALTURAS MARIO (Lado Derecho - Pisos Pares)
        # Piso 0: Suelo
        # Piso 2: Primera plataforma derecha
        # Piso 4: Segunda plataforma derecha
        # Piso 6: Tercera plataforma derecha (si existe)
        self.alturas_mario = {
            0: suelo_y,
            2: 123,  # Aprox 34px más arriba
            4: 75,  # Aprox 34px más arriba
        }

        # ALTURAS LUIGI (Lado Izquierdo - Pisos Impares)
        # Nota: Luigi empieza en el suelo (que trataremos visualmente como inicio)
        # pero su primer "salto" lógico es al Piso 1.
        # Piso 1: Primera plataforma izquierda
        # Piso 3: Segunda plataforma izquierda
        # Piso 5: Plataforma del camión
        self.alturas_luigi = {
            1: suelo_y,  # Luigi empieza abajo
            3: 107,  # Misma altura que el piso 2 de Mario
            5: 59,  # Misma altura que el piso 4 de Mario
        }

        # Crear personaje
        #Mario
        self.mario = Personaje(265, self.alturas_mario[0], 0, "Mario")
        # Luigi
        self.luigi = Personaje(93, self.alturas_luigi[1], 1, "Luigi")
        #Crear camión
        self.camion = Camion(10, 74)
        # --- 3. CREACIÓN DE CINTAS (CRÍTICO PARA SPRINT 3) ---
        # Creamos las cintas invisibles donde se moverán los paquetes.
        # Las coordenadas Y deben coincidir con las plataformas.
        self.cintas = []

        # Coordenadas X aproximadas (AJUSTA ESTOS VALORES SEGÚN TU DIBUJO)
        x_cinta0 = 282
        x_resto_cintas = 106

        # Cinta 0 (Inicio Mario - Abajo Derecha)
        self.cintas.append(
            Cinta(numero=0, x=x_cinta0, y=152, piso=0))

        # Cinta 1 (Luigi - Nivel 1 Izq)
        self.cintas.append(
            Cinta(numero=1, x=x_resto_cintas, y=152, piso=1))

        # Cinta 2 (Mario - Nivel 1 Der)
        self.cintas.append(
            Cinta(numero=2, x=x_resto_cintas, y=128, piso=2))

        # Cinta 3 (Luigi - Nivel 2 Izq)
        self.cintas.append(
            Cinta(numero=3, x=x_resto_cintas, y=104, piso=3))

        # Cinta 4 (Mario - Nivel 2 Der)
        self.cintas.append(
            Cinta(numero=4, x=x_resto_cintas, y=80, piso=4))

        # Cinta 5 (Luigi - Nivel 3 - Hacia el camión)
        self.cintas.append(
            Cinta(numero=5, x=x_resto_cintas, y=56, piso=5))

        # Crear JEFE
        # Lo colocamos abajo a la izquierda para finalizar el descanso
        self.jefe = Jefe(0, 0)

        # Variables para restaurar personaje tras castigo
        self.personaje_castigado = None
        self.memoria_personaje = {}  # Para guardar piso y Y

        # Marcadores
        self.puntos = 0
        self.fallos = 0

        # --- Lista para animación de caída ---
        self.paquetes_cayendo = []

        # SPRINT 3: Generador de paquetes
        self.tiempo_aparicion = 120  # Frames (2 segundos)
        self.contador_frames = 0

        # En el init se inicializará pyxel también
        # Esta instrucción inicializará pyxel, ver la API para más parámetros
        pyxel.init(self.ancho, self.alto, title="Mario Bros Game")

        pyxel.load("assets/graficosprc.pyxres")

        # Ejecutando el juego
        pyxel.run(self.update, self.draw)

    # Properties and setters
    @property
    def ancho(self) -> int:
        return self.__ancho

    @property
    def alto(self) -> int:
        return self.__alto

    @ancho.setter
    def ancho(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError(
                "El ancho debe ser un entero " + str(type(valor)))
        elif valor < 0:
            raise ValueError("El ancho debe ser un número positivo")
        else:
            self.__ancho = valor

    @alto.setter
    def alto(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError(
                "El alto debe ser un entero " + str(type(valor)))
        elif valor < 0:
            raise ValueError(
                "El alto debe estar un número positivo")
        else:
            self.__alto = valor

    @property
    def pisos(self) -> int:
        return self.__pisos

    @pisos.setter
    def pisos(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError(
                "El número de pisos debe ser un entero " + str(type(valor)))
        elif valor != 5 and valor != 7:
            raise ValueError("El número de pisos debe ser 5 o 7")
        else:
            self.__pisos = valor

    def reiniciar_juego(self):
        """Reinicia variables para jugar otra vez"""
        self.puntos = 0
        self.fallos = 0
        self.camion.vaciar()
        self.estado_juego = JUGANDO
        # Limpiar paquetes de las cintas
        for cinta in self.cintas:
            # Accedemos a la lista protegida a través de la property (si existe setter)
            # o limpiamos uno a uno. Como _paquetes es interno, usaremos un truco:
            while len(cinta.paquetes) > 0:
                cinta.retirar_paquete(cinta.paquetes[0])

    def iniciar_reparto(self):
        """
        Activa el estado de REPARTO.
        Las cintas se paran y se limpia el borde.
        """
        self.estado_juego = REPARTO
        self.contador_reparto = self.tiempo_reparto

        # REGLA: Si un paquete está en la última posición, desaparece.
        for cinta in self.cintas:
            paquete_borde = cinta.paquete_llego_al_final()
            if paquete_borde:
                # Lo retiramos sin sumar puntos ni fallos (desaparece)
                cinta.retirar_paquete(paquete_borde)


    def update(self):
        """ Este es un metodo pyxel que se ejecuta en cada iteración del
        juego (cada
        fotograma). Necesitas poner aquí todo el código que tiene que ser ejecutado en cada frame. Ahora
        contiene sólo la lógica para mover el personaje si se pulsa una tecla."""
        # Para salir del juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- LÓGICA DE GAME OVER ---
        # Si tenemos 3 fallos o más, NO ejecutamos nada más del juego
        if self.fallos >= 3:
            if pyxel.btnp(pyxel.KEY_R):  # Opción de reinicio rápido
                self.reiniciar_juego()
            return  # Se acaba la función aquí (el juego se congela)

        self.jefe.update()

        # --- ESTADO: CASTIGO ---
        if self.estado_juego == CASTIGO:
            # Esperamos a que el jefe termine
            if not self.jefe.visible:
                # Restaurar personaje
                p = self.personaje_castigado
                datos = self.memoria_personaje

                p.piso = datos['piso']
                p.y = datos['y']
                p.set_mirada_invertida(False)  # Vuelve a mirar normal

                self.estado_juego = JUGANDO
            return

        # --- LÓGICA DE REPARTO (PAUSA) ---
        if self.estado_juego == REPARTO:
            # Descontamos tiempo
            self.contador_reparto -= 1

            # Animación de paquetes cayendo (opcional, dejamos que terminen de caer)
            velocidad_caida = 4
            paquetes_validos = []
            for p in self.paquetes_cayendo:
                p.y += velocidad_caida
                if p.y < self.alto:
                    paquetes_validos.append(p)
            self.paquetes_cayendo = paquetes_validos

            # Si acaba el tiempo, volvemos a jugar
            if self.contador_reparto <= 0:
                self.camion.vaciar()  # El camión vuelve vacío y listo
                # --- ACTIVAR AL JEFE ---
                self.estado_juego = JEFE_MANDANDO
                # Aparece por 60 frames (1 segundo),
                # False = mirando a la derecha (hacia Luigi o general)
                # Puedes poner True para que mire a Mario si prefieres.
                self.jefe.aparecer_trabajo(39, 171, 180)
            return

        # --- ESTADO: JEFE MANDANDO (Post-reparto) ---
        if self.estado_juego == JEFE_MANDANDO:
            # Esperamos a que el jefe termine su animación
            if not self.jefe.visible:
                # Cuando el jefe se oculta, volvemos a jugar
                self.estado_juego = JUGANDO
            return

        # ==========================================
        #  LÓGICA PRINCIPAL (SOLO SI ESTADO == JUGANDO)
        # ==========================================

        # --- Actualizar paquetes cayendo ---
        velocidad_caida = 4
        for p in self.paquetes_cayendo:
            p.y += velocidad_caida

        paquetes_validos = []
        for p in self.paquetes_cayendo:
            if p.y < self.alto:
                paquetes_validos.append(p)
        self.paquetes_cayendo = paquetes_validos

        # --- Actualizar paquetes cayendo (Física de gravedad) ---
        velocidad_caida = 4
        # Movemos los paquetes hacia abajo
        for p in self.paquetes_cayendo:
            p.y += velocidad_caida

        # Eliminamos de la memoria los que ya salieron de la pantalla (limpieza)
        # 1. Creamos una lista vacía temporal
        paquetes_validos = []

        # 2. Recorremos la lista original
        for p in self.paquetes_cayendo:
            # 3. Verificamos la condición (si está dentro de la pantalla)
            if p.y < self.alto:
                # 4. Si cumple, lo agregamos a la lista temporal
                paquetes_validos.append(p)

        # 5. Reemplazamos la lista original con la lista filtrada
        self.paquetes_cayendo = paquetes_validos

        # --- MOVIMIENTO DE MARIO (Flechas) ---
        # Sube y baja de 2 en 2 pisos (0 -> 2 -> 4)

        # SUBIR
        if pyxel.btnp(pyxel.KEY_UP):
            siguiente_piso = self.mario.piso + 2
            # Verificamos si ese piso existe en el diccionario de Mario
            if siguiente_piso in self.alturas_mario:
                # Vamos a la altura EXACTA definida en el diccionario
                nueva_y = self.alturas_mario[siguiente_piso]
                self.mario.subir(
                    nueva_y)  # Tu metodo subir ya suma +2 al piso

        # BAJAR
        if pyxel.btnp(pyxel.KEY_DOWN):
            siguiente_piso = self.mario.piso - 2
            if siguiente_piso in self.alturas_mario:
                nueva_y = self.alturas_mario[siguiente_piso]
                self.mario.bajar(nueva_y)

        # --- MOVIMIENTO DE LUIGI (W / S) ---
        # Luigi tiene una excepción: Del 0 sube al 1. Luego va de 2 en 2 (1->3->5).

        # SUBIR (W)
        if pyxel.btnp(pyxel.KEY_W):
            if self.luigi.piso == 0:
                siguiente_piso = 1  # Del suelo salta al 1
            else:
                siguiente_piso = self.luigi.piso + 2  # Resto normal

            if siguiente_piso in self.alturas_luigi:
                nueva_y = self.alturas_luigi[siguiente_piso]
                self.luigi.subir(nueva_y)

                # CORRECCIÓN DE PISO LOGICO:
                # Tu metodo 'subir' en Personaje suma +2 por defecto.
                # Si subimos de 0 a 1, el metodo pondrá piso=2. ¡Mal!
                # Lo corregimos manualmente aquí:
                if self.luigi.piso == 2 and siguiente_piso == 1:
                    self.luigi.piso = 1

        # BAJAR (S)
        if pyxel.btnp(pyxel.KEY_S):
            if self.luigi.piso == 1:
                siguiente_piso = 0
            else:
                siguiente_piso = self.luigi.piso - 2

            if siguiente_piso in self.alturas_luigi:
                nueva_y = self.alturas_luigi[siguiente_piso]
                self.luigi.bajar(nueva_y)

                # Corrección manual si bajamos al 0
                if siguiente_piso == 0:
                    self.luigi.piso = 0

        # --- 2. LÓGICA DE PAQUETES (Sprint 3) ---

        # A. Generar paquetes nuevos en Cinta 0

        # Regla: "Siempre debe haber, al menos, un paquete en juego" (PDF)
        # Tú has pedido empezar con 3.
        base_minima = 3
        incremento_dificultad = self.puntos // self.puntos_levelup

        # El número mínimo de paquetes que debe haber en pantalla:
        min_paquetes = base_minima + incremento_dificultad

        # 2. Contar cuántos paquetes hay REALMENTE en juego
        paquetes_en_juego = 0
        for c in self.cintas:
            paquetes_en_juego += len(c.paquetes)
        paquetes_en_juego += len(self.paquetes_cayendo)

        # 3. Lógica de aparición
        self.contador_frames += 1

        # Si tenemos MENOS paquetes que el MÍNIMO REQUERIDO, generamos uno nuevo
        if self.contador_frames >= self.tiempo_aparicion:
            if paquetes_en_juego < min_paquetes:
                self.contador_frames = 0  # Reseteamos temporizador

                # Nace a la derecha de la cinta 0
                cinta0 = self.cintas[0]
                nuevo = Paquete(cinta0.x + 70, cinta0.y, 0, 0)
                cinta0.agregar_paquete(nuevo)
            else:
                # Si ya cumplimos el mínimo, mantenemos el contador listo
                # para generar INMEDIATAMENTE si se pierde un paquete
                self.contador_frames = self.tiempo_aparicion

        # B. Mover y Transferir
        for i in range(len(self.cintas)):
            cinta = self.cintas[i]
            cinta.actualizar_paquetes()
            paquete_saliente = cinta.paquete_llego_al_final()

            if paquete_saliente:
                # 1. ¿Quién lo recoge?
                recogido = False

                # Cinta 0, 2, 4 -> Terminan en MARIO (Derecha) -> Mario debe estar en ese piso
                if cinta.numero in [0, 2, 4]:
                    if self.mario.piso == cinta.piso:
                        recogido = True

                # Cinta 1, 3, 5 -> Terminan en LUIGI (Izquierda) -> Luigi debe estar en ese piso
                else:
                    if self.luigi.piso == cinta.piso:
                        recogido = True

                # IMPORTANTE: El paquete se retira de la CINTA, pero seguimos teniendo la referencia en 'paquete_saliente'
                cinta.retirar_paquete(paquete_saliente)

                if recogido:
                    self.puntos += 1

                    if cinta.numero < 5:
                        # Pasamos a la siguiente cinta (La de ARRIBA)
                        siguiente_cinta = self.cintas[i + 1]

                        # --- CÁLCULO DE SPAWN (NACIMIENTO) ---
                        # Si la siguiente cinta mueve a la IZQUIERDA (1, 3, 5)
                        # El paquete debe aparecer a la DERECHA (x + ancho)
                        if siguiente_cinta.numero % 2 != 0:
                            # --- CORRECCIÓN: Siempre aparece a la derecha (inicio de movimiento) ---
                            # Esto hace que aparezca a la DERECHA de la cinta (x + 159)
                            # que visualmente está justo a la IZQUIERDA de Mario (donde acaba su lado)
                            paquete_saliente.x = siguiente_cinta.x + 146

                        # Si la siguiente cinta mueve a la DERECHA (2, 4)
                        # El paquete debe aparecer a la IZQUIERDA (x)
                        else:
                            paquete_saliente.x = siguiente_cinta.x

                        paquete_saliente.y = siguiente_cinta.y
                        paquete_saliente.piso = siguiente_cinta.piso
                        paquete_saliente.cinta_actual = siguiente_cinta.numero  # Esto actualiza el sprite solo

                        siguiente_cinta.agregar_paquete(paquete_saliente)


                    elif cinta.numero == 5:

                        # El paquete entra al camión

                        self.camion.cargar_paquete(paquete_saliente)

                        # REGLA 2: +10 puntos SOLO si el camión se completa

                        if self.camion.esta_lleno():
                            self.puntos += 10

                            # Temporalmente lo vaciamos aquí para seguir probando la puntuación

                            # (En el siguiente paso haremos que el camión "se vaya" de reparto)

                            self.iniciar_reparto()
                else:
                    # ============ FALLO DETECTADO ============
                    self.fallos += 1
                    self.paquetes_cayendo.append(paquete_saliente)

                    # 1. Identificar culpable
                    es_culpa_mario = (
                                cinta.numero % 2 == 0)  # Pares (0,2,4) son lado Mario

                    if es_culpa_mario:
                        culpable = self.mario
                    else:
                        culpable = self.luigi

                    # 2. Guardar estado actual
                    self.personaje_castigado = culpable
                    self.memoria_personaje = {
                        'piso': culpable.piso,
                        'y': culpable.y
                    }

                    # 3. Aplicar Castigo (Posición y Mirada)
                    culpable.set_mirada_invertida(True)

                    if es_culpa_mario:
                        # Mario al piso superior (4) -> Y=75
                        culpable.piso = 4
                        culpable.y = 75
                        # Jefe castiga a Mario
                        self.jefe.aparecer_castigo(295, 75, 180,
                                                   mirar_izquierda=True)
                        # mirar_izquierda=False porque Mario está a la derecha,
                        # el jefe se pone en 295 (misma X?), debería mirar a Mario?
                        # Si están en la misma X, se superponen.
                        # Asumo que 295 es la coord del jefe y mira hacia Mario o hacia el centro.
                        # Según instrucciones: "mirando al lado contrario al que suele mirar" (el personaje)
                    else:
                        # Luigi al piso superior (5) -> Y=59
                        culpable.piso = 5
                        culpable.y = 59
                        # Jefe castiga a Luigi
                        self.jefe.aparecer_castigo(77, 59, 180,
                                                   mirar_izquierda=False)

                    # 4. Cambiar estado
                    self.estado_juego = CASTIGO
                    return

    def draw(self):
        """Este es un metodo pyxel que se ejecuta en cada iteración del
        juego (cada
        fotograma). Debes poner aquí el código para dibujar los elementos del juego.
        """
        # Borra la pantalla
        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, 0, 0, self.ancho, self.alto, 0)

        # Dibuja el personaje, los parámetros de pyxel.blt son (x, y, sprite tuple)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)
        # CAMIÓN: Solo se dibuja si NO estamos en reparto (simula que se fue)
        if self.estado_juego != REPARTO:
            pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprite)
            # NUEVO: Dibujar la carga apilada dentro del camión
            for caja in self.camion.carga_visual:
                # caja es un diccionario con x, y, sprite
                pyxel.blt(caja["x"], caja["y"], *caja["sprite"])
        else:
            # Mensaje opcional durante el reparto
            pyxel.text(10, 60, "REPARTO...", 10)

        # PAQUETES (Sprint 3)
        for cinta in self.cintas:
            for p in cinta.paquetes:
                # Usamos el sprite del paquete (se ajusta solo si está vacío o lleno)
                # El * desempaqueta la tupla (0, u, v, w, h, colkey)
                pyxel.blt(p.x, p.y, *p.sprite)

        # --- Dibujar paquetes cayendo ---
        for p in self.paquetes_cayendo:
            pyxel.blt(p.x, p.y, *p.sprite)

        # --- COLUMNA CENTRAL (Forma simple) ---
        for cinta in self.cintas:
            # Dibuja un trozo de columna por CADA cinta.
            # Si dos cintas están a la misma altura, se dibujará dos veces (no se nota).
            pyxel.blt(184, cinta.y - 3, 0, 136, 8, 16, 16)

        # DISPENSADOR DE PAQUETES
        pyxel.blt(352, 158, 0, 128, 70, 16, 6)

        pyxel.text(10, 5, f"PUNTOS: {self.puntos}", 7) # Color 7 es blanco

        color_fallos = 8  # Rojo
        if self.fallos >= 3:
            # TEXTO GRANDE CENTRADO (Más o menos)
            pyxel.text(self.ancho // 2 - 20, self.alto // 2, "GAME OVER", 8)
            pyxel.text(self.ancho // 2 - 35, self.alto // 2 + 10,
                       "Pulsa Q para salir", 1)
            pyxel.text(self.ancho // 2 - 35, self.alto // 2 + 20, "Pulsa R "
                                                                  "para "
                                                                  "reiniciar", 1)

        pyxel.text(100, 5, f"FALLOS: {self.fallos}/3", color_fallos)

        # --- DIBUJAR AL JEFE ---
        self.jefe.draw()

        # 1. Muestra la coordenada REAL (sin sumar +1 ni +5)
        coord_texto = f"{pyxel.mouse_x},{pyxel.mouse_y}"

        # 2. Dibuja el texto un poco apartado para que no tape el cursor
        pyxel.text(pyxel.mouse_x + 5, pyxel.mouse_y - 10, coord_texto, 7)

        # 3. Usa un píxel real (pset) o una cruz para marcar la posición exacta
        # Esto asegura que lo que ves es EXACTAMENTE donde está el ratón
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 7)