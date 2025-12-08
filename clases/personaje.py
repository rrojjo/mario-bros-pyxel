# Contiene la clase Personaje (Mario y Luigi).

class Personaje:
    """
    Clase base para los jugadores (Mario y Luigi). Gestiona coordenadas,
    estado de piso, y renderizado condicional (invertido/cargando).
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, x: int, y: int, piso: int, nombre: str):
        self.x = x
        self.y = y
        self.piso = piso
        self.nombre = nombre
        self.invertido = False

        if self.nombre == "Luigi":
            self.u_original = 0
        else:  # Mario
            self.u_original = 16

        # Timer para animación temporal de recogida de paquete
        self.timer_animacion = 0

        self.actualizar_sprite()

    # -------------------------------------------------------------------------
    # GESTIÓN DE ANIMACIONES Y SPRITES

    def update(self):
        """Actualiza temporizadores y estados transitorios."""
        if self.timer_animacion > 0:
            self.timer_animacion -= 1
            if self.timer_animacion == 0:
                self.actualizar_sprite()

        # Validación continua de orientación para Mario en planta baja
        if self.nombre == "Mario" and self.piso==0 and self.timer_animacion==0:
            self.actualizar_sprite()

    def animar_recogida(self):
        """Activa brevemente la animación de cargar paquete."""
        self.timer_animacion = 10
        self.actualizar_sprite()

    def actualizar_sprite(self):
        """
        Determina el sprite a dibujar basándose en prioridades:
        1. Animación activa (Cargando).
        2. Reglas de posición (Mario en piso 0).
        3. Estado de castigo (Invertido).
        """

        # 1. Coordenadas base del sprite
        if self.timer_animacion > 0:
            # Sprite de acción/carga
            u = 0
            v = 16
        else:
            # Sprite Idle
            u = self.u_original
            v = 0

        # 2. Orientación (Flip horizontal)
        ancho = 16

        if self.nombre == "Mario":
            # Mario se invierte al cargar, estar en piso 0 o ser castigado
            if self.timer_animacion > 0:
                ancho = -16
            elif self.piso == 0:
                ancho = -16
            elif self.invertido:
                ancho = -16
            else:
                ancho = 16

        elif self.nombre == "Luigi":
            # Luigi solo se invierte si está bajo castigo
            if self.invertido:
                ancho = -16
            else:
                ancho = 16

        self.sprite = (0, u, v, ancho, 16, 15)

    def set_mirada_invertida(self, estado: bool):
        self.invertido = estado
        self.actualizar_sprite()

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS & SETTERS)

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número negativo")
        else:
            self.__x = x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y no debe ser un número negativo")
        else:
            self.__y = y

    @property
    def piso(self) -> int:
        return self.__piso

    @piso.setter
    def piso(self, piso: int):
        if not isinstance(piso, int):
            raise TypeError("El piso debe ser un entero " + str(type(piso)))
        elif piso < 0:
            raise ValueError("El piso no debe ser un número negativo")
        else:
            self.__piso = piso

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError(
                "El nombre debe ser un string " + str(type(valor)))
        elif valor != "Mario" and valor != "Luigi":
            raise ValueError("El nombre debe ser 'Mario' o 'Luigi'")
        else:
            self.__nombre = valor

    # -------------------------------------------------------------------------
    # LÓGICA DE MOVIMIENTO VERTICAL

    def subir(self, nueva_y: int):
        """Aumenta el piso (+2) y actualiza la posición gráfica."""
        self.piso += 2
        self.y = nueva_y
        self.actualizar_sprite()

    def bajar(self, nueva_y: int):
        """Disminuye el piso (-2) y actualiza la posición gráfica."""
        self.piso -= 2
        self.y = nueva_y
        self.actualizar_sprite()