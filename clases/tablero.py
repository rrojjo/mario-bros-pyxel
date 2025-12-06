# Contiene el tablero Juego/MarioBrosGame (lógica principal).

from clases.personaje import Personaje
from clases.camion import Camion
from clases.cinta import Cinta
from clases.paquete import Paquete
import pyxel


class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int, pisos):
        # 1. Asignar atributos usando los setters
        self.ancho = ancho
        self.alto = alto
        self.pisos = pisos

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
        # x_izq: Donde está Luigi esperando
        # x_der: Donde está Mario esperando
        x_izq = 106
        x_der = 282  # Un poco antes de 299 para que conecte con el tabique

        # Cinta 0 (Inicio Mario - Abajo Derecha)
        self.cintas.append(
            Cinta(numero=0, x=x_der, y=152, piso=0))

        # Cinta 1 (Luigi - Nivel 1 Izq)
        self.cintas.append(
            Cinta(numero=1, x=x_izq, y=152, piso=1))

        # Cinta 2 (Mario - Nivel 1 Der)
        self.cintas.append(
            Cinta(numero=2, x=x_izq, y=128, piso=2))

        # Cinta 3 (Luigi - Nivel 2 Izq)
        self.cintas.append(
            Cinta(numero=3, x=x_izq, y=104, piso=3))

        # Cinta 4 (Mario - Nivel 2 Der)
        self.cintas.append(
            Cinta(numero=4, x=x_izq, y=80, piso=4))

        # Cinta 5 (Luigi - Nivel 3 - Hacia el camión)
        self.cintas.append(
            Cinta(numero=5, x=x_izq, y=56, piso=5))



        # Marcadores
        self.puntos = 0
        self.fallos = 0

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


    def update(self):
        """ Este es un metodo pyxel que se ejecuta en cada iteración del
        juego (cada
        fotograma). Necesitas poner aquí todo el código que tiene que ser ejecutado en cada frame. Ahora
        contiene sólo la lógica para mover el personaje si se pulsa una tecla."""
        # Para salir del juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
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
        self.contador_frames += 1
        if self.contador_frames >= self.tiempo_aparicion:
            self.contador_frames = 0
            # Nace a la derecha de la cinta 0
            cinta0 = self.cintas[0]
            # Ajuste: nace al final de la cinta visualmente (x + ancho)
            nuevo = Paquete(cinta0.x + 60, cinta0.y, 0, 0)
            cinta0.agregar_paquete(nuevo)

        # B. Mover y Transferir
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
                        self.camion.cargar_paquete()
                        self.puntos += 10
                else:
                    self.fallos += 1

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
        pyxel.blt(self.camion.x, self.camion.y, *self.camion.sprite)
        pyxel.text(10, 5, f"PUNTOS: {self.puntos}", 7) # Color 7 es blanco
        pyxel.text(100, 5, f"FALLOS: {self.fallos}", 8)  # Color 8 es rojo

        # PAQUETES (Sprint 3)
        for cinta in self.cintas:
            for p in cinta.paquetes:
                # Usamos el sprite del paquete (se ajusta solo si está vacío o lleno)
                # El * desempaqueta la tupla (0, u, v, w, h, colkey)
                pyxel.blt(p.x, p.y, *p.sprite)

        # --- COLUMNA CENTRAL (Forma simple) ---
        for cinta in self.cintas:
            # Dibuja un trozo de columna por CADA cinta.
            # Si dos cintas están a la misma altura, se dibujará dos veces (no se nota).
            pyxel.blt(184, cinta.y - 3, 0, 136, 8, 16, 16)

        # DEBUG: Ver dónde están las cintas invisibles (Puntos Rojos)
        # Esto te ayudará a saber si la lógica coincide con el dibujo
        for cinta in self.cintas:
            pyxel.pset(cinta.x, cinta.y, 8)
            # Texto pequeño para identificar cintas
            pyxel.text(cinta.x, cinta.y - 6, str(cinta.numero), 5)
            # --- Código corregido ---

            # 1. Muestra la coordenada REAL (sin sumar +1 ni +5)
            coord_texto = f"{pyxel.mouse_x},{pyxel.mouse_y}"

            # 2. Dibuja el texto un poco apartado para que no tape el cursor
            pyxel.text(pyxel.mouse_x + 5, pyxel.mouse_y - 10, coord_texto, 7)

            # 3. Usa un píxel real (pset) o una cruz para marcar la posición exacta
            # Esto asegura que lo que ves es EXACTAMENTE donde está el ratón
            pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 7)