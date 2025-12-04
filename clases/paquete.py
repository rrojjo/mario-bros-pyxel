#Clase paquete

class Paquete:

    def __init__(self, x: int, y: int, piso: int, cinta_actual: int):
        self.x = x
        self.y = y
        self.piso = piso
        self.cinta_actual = cinta_actual
        # El paquete nace con la forma de la cinta anterior
        # (o 0 si es la primera)
        if cinta_actual == 0:
            self.indice_sprite = 0
        else:
            self.indice_sprite = cinta_actual - 1
        self.velocidad=1
        self.sprites = {
            0: (0, 32, 36, 16, 12,0),  # Forma Inicial
            1: (0, 48, 36, 16, 12,0),  # Forma 1 (Cinta 1)
            2: (0, 64, 36, 16, 12,0),  # Forma 2 (Cinta 2)
            3: (0, 80, 36, 16, 12,0),  # Forma 3 (Cinta 3)
            4: (0, 96, 36, 16, 12,0),  # Forma 4 (Cinta 4)
            5: (0, 112, 36, 16, 12,0)
            # Forma 5 (Cinta 5 - Última antes del camión)
        }

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

        # --- MÉTODOS VISUALES ---

    @property
    def sprite(self):
        """Devuelve el sprite basado en el INDICE VISUAL, no en la cinta"""
        return self.sprites.get(self.indice_sprite, self.sprites[0])

    def evolucionar(self, numero_cinta: int):
        """Cambia la forma a la correspondiente a esta cinta"""
        self.indice_sprite = numero_cinta


    def esta_en_extremo(self, limite_x: int) -> bool:
        """Verifica si el paquete llegó al extremo de la cinta"""
        return self.x >= limite_x

    def __str__(self) -> str:
        return f"Paquete en posición ({self.x}, {self.y}) en el piso {self.piso}, cinta {self.cinta_actual}"