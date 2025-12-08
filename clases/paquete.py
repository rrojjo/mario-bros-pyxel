# Contiene la clase Paquete

class Paquete:
    """
    Representa un objeto transportable en las cintas.
    Gestiona su posición física y su estado visual (sprite) evolutivo.
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, x: int, y: int, piso: int, cinta_actual: int):
        self.x = x
        self.y = y
        self.piso = piso
        self.cinta_actual = cinta_actual

        # El paquete hereda la forma de la cinta anterior para dar
        # continuidad visual, excepto si nace en la primera cinta.
        if cinta_actual == 0:
            self.indice_sprite = 0
        else:
            self.indice_sprite = cinta_actual - 1

        self.velocidad = 1
        self.sprites = {
            0: (0, 32, 36, 16, 12, 0),  # Forma Inicial
            1: (0, 48, 36, 16, 12, 0),  # Forma 1 (Cinta 1)
            2: (0, 64, 36, 16, 12, 0),  # Forma 2 (Cinta 2)
            3: (0, 80, 36, 16, 12, 0),  # ...
            4: (0, 96, 36, 16, 12, 0),
            5: (0, 112, 36, 16, 12, 0),
            # Reutilización de sprites para cintas extra en niveles altos
            6: (0, 112, 36, 16, 12, 0),
            7: (0, 112, 36, 16, 12, 0)
        }

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS Y SETTERS)

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
    def cinta_actual(self) -> int:
        return self.__cinta_actual

    @cinta_actual.setter
    def cinta_actual(self, valor: int):
        if not isinstance(valor, int):
            raise TypeError("La cinta debe ser un entero")
        elif valor < 0:
            raise ValueError("La cinta no puede ser negativa")
        else:
            self.__cinta_actual = valor

    # -------------------------------------------------------------------------
    # MÉTODOS DE LÓGICA VISUAL

    @property
    def sprite(self):
        """
        Retorna las coordenadas del sprite basado en el estado de evolución.
        """
        return self.sprites.get(self.indice_sprite, self.sprites[0])

    def evolucionar(self, numero_cinta: int):
        """
        Actualiza la forma del paquete para coincidir con la cinta actual.
        """
        self.indice_sprite = numero_cinta

    def esta_en_extremo(self, limite_x: int) -> bool:
        return self.x >= limite_x