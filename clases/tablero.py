# Contiene el tablero Juego/MarioBrosGame (lógica principal).

from clases.personaje import Personaje
from clases.camion import Camion
import pyxel
import os


class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int, pisos):
        # 1. Asignar atributos usando los setters
        self.ancho = ancho
        self.alto = alto
        self.pisos = pisos

        # 2. Definir alturas de los pisos (calculadas para 192px de alto)
        # Suponemos 4 niveles. Dejamos espacio abajo para el suelo.
        #Alturas de los pisos de Luigi
        self.y_piso1 = 168
        self.y_piso3 = 128
        self.y_piso5 = 88
        self.y_piso7 = 48
        # Alturas de los pisos de Mario
        self.y_piso0 = 168
        self.y_piso2 = 136
        self.y_piso4 = 94
        self.y_piso6 = 54

        # Crear personaje
        #Mario
        self.mario = Personaje(265, 154, 0, "Mario")
        # Luigi
        self.luigi = Personaje(93, 154, 1, "Luigi")
        #Crear camión
        self.camion = Camion(10, 74)
        # Marcadores
        self.puntos = 0
        self.fallos = 0

        # En el init se inicializará pyxel también
        # Esta instrucción inicializará pyxel, ver la API para más parámetros
        pyxel.init(self.ancho, self.alto, title="Mario Bros "
                                                "Game")

        #----------------------------------------------------
        # Cargando el fichero pyxres con las imágenes
        # 1. Buscamos la carpeta donde vive este archivo (tablero.py)
        # Esto devolverá algo como: "C:\…\Mario Bros\clases"
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))

        # 2. Construimos la ruta hacia el archivo de recursos
        # join: une las partes con la barra correcta (\ o /)
        # "..": significa "subir un nivel hacia atrás" (salir de 'clases' a la raíz)
        ruta_recursos = os.path.join(carpeta_actual, "..", "assets",
                                     "graficosprc.pyxres")

        # 3. (Opcional, pero recomendado) Limpiamos la ruta para que se vea bonita
        # Esto quita los ".." y deja la ruta absoluta limpia
        ruta_final = os.path.normpath(ruta_recursos)

        # 4. Cargamos el archivo
        print(
            f"Cargando recursos desde: {ruta_final}")  # Esto es para que veas en consola qué ruta ha calculado
        pyxel.load(ruta_final)
        #----------------------------------------------------

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
        """ Este es un método pyxel que se ejecuta en cada iteración del juego (cada
        fotograma). Necesitas poner aquí todo el código que tiene que ser ejecutado en cada frame. Ahora
        contiene sólo la lógica para mover el personaje si se pulsa una tecla."""
        # Para salir del juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            # --- MOVIMIENTO DE MARIO (Flechas) ---
            # Subir: Solo si no está en el piso máximo (Piso 3)
        if pyxel.btnp(pyxel.KEY_UP):
            if self.mario.piso < (self.pisos - 1) and self.mario.piso:
                # Salto normal
                nueva_y = self.mario.y - 48
                self.mario.subir(nueva_y)
            elif self.mario.piso == 0:
                # Salto especial desde piso 2
                nueva_y = self.mario.y - 32
                self.mario.subir(nueva_y)

        # Bajar: Solo si no está en el piso mínimo (Piso 0)
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.mario.piso == 2:
                # salto especial de 32
                nueva_y = self.mario.y + 32
                self.mario.bajar(nueva_y)
            elif 0 < self.mario.piso <= 6:
                # resto de pisos: 48
                nueva_y = self.mario.y + 48
                self.mario.bajar(nueva_y)

        # --- MOVIMIENTO DE LUIGI (W / S) ---
        # Subir (Tecla W)
        if pyxel.btnp(pyxel.KEY_W) and self.luigi.piso < self.pisos:
            nueva_y = self.luigi.y - 48
            self.luigi.subir(nueva_y)

        # Bajar (Tecla S)
        if pyxel.btnp(pyxel.KEY_S) and self.luigi.piso > 1:
            nueva_y = self.luigi.y + 48
            self.luigi.bajar(nueva_y)

    def draw(self):
        """Este es un método pyxel que se ejecuta en cada iteración del juego (cada
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

        #Código temporal, sirva para ubicar las coordenadas con el ratón
        coord_texto = f"{pyxel.mouse_x+1},{pyxel.mouse_y+5}"
        punto = "."
        pyxel.text(pyxel.mouse_x + 5, pyxel.mouse_y - 5, coord_texto, 7)
        pyxel.text(pyxel.mouse_x, pyxel.mouse_y, punto, 7)
