# Contiene el tablero Juego/MarioBrosGame (lógica principal).

from clases.personaje import Personaje
import pyxel
import os


class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int):
        """ Método que crea el tablero
        :param ancho: El ancho del tablero
        :param alto: El alto del tablero
        """
        # Estableciendo los atributos
        self.ancho = ancho
        self.alto = alto
        # El personaje estará en la mitad del tablero
        self.personaje = Personaje(self.ancho//2, self.alto//2, 1, "Mario")

        # En el init se inicializará pyxel también
        # Esta instrucción inicializará pyxel, ver la API para más parámetros
        pyxel.init(self.ancho, self.alto, title="Mario Bros Game")

        #----------------------------------------------------
        # Cargando el fichero pyxres con las imágenes
        # 1. Buscamos la carpeta donde vive este archivo (juego.py)
        # Esto devolverá algo como: "C:\...\Mario Bros\clases"
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))

        # 2. Construimos la ruta hacia el archivo de recursos
        # join: une las partes con la barra correcta (\ o /)
        # "..": significa "subir un nivel hacia atrás" (salir de 'clases' a la raíz)
        ruta_recursos = os.path.join(carpeta_actual, "..", "assets",
                                     "graficosprc-copia.pyxres")

        # 3. (Opcional pero recomendado) Limpiamos la ruta para que se vea bonita
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
    def ancho(self, ancho: int):
        if not isinstance(ancho, int):
            raise TypeError("El ancho debe ser un entero " + str(type(ancho)))
        elif ancho < 1 or ancho > 368:
            raise ValueError("El ancho debe estar entre 1 y 368")
        else:
            self.__ancho = ancho

    @alto.setter
    def alto(self, alto: int):
        if not isinstance(alto, int):
            raise TypeError("El alto debe ser un entero " + str(type(alto)))
        elif alto < 1 or alto > 192:
            raise ValueError("El alto debe estar en el rango entre 1 y 192")
        else:
            self.__alto = alto

    def update(self):
        """ Este es un método pyxel que se ejecuta en cada iteración del juego (cada
        fotograma). Necesitas poner aquí todo el código que tiene que ser ejecutado en cada frame. Ahora
        contiene sólo la lógica para mover el personaje si se pulsa una tecla."""
        # Para salir del juego
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Movimiento horizontal
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.personaje.mover('derecha', self.ancho)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.personaje.mover('izquierda', self.ancho)

    def draw(self):
        """Este es un método pyxel que se ejecuta en cada iteración del juego (cada
        fotograma). Debes poner aquí el código para dibujar los elementos del juego.
        """
        # Borra la pantalla
        pyxel.cls(0)
        # Dibuja el personaje, los parámetros de pyxel.blt son (x, y, sprite tuple)
        pyxel.bltm(0, 0, 0, 0, 0, self.ancho, self.alto)
        pyxel.blt(self.personaje.x, self.personaje.y, *self.personaje.sprite)
