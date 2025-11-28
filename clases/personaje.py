# Contiene las clases Personaje, Mario y Luigi.

class Personaje:

    def __init__(self, x: int,y: int, piso:int, nombre:str):
        self.x=x
        self.y=y
        self.piso=piso
        self.nombre=nombre
        self.sprite = (0, 0, 0, 16, 16)

#Propiedad x

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("La x no debe ser un número negativo")
        else:
            self.__x = x

#Propiedad y

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError ("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y no debe ser un número negativo")
        else:
            self.__y = y

#Función mover
    def mover(self, direccion: str, ancho_tablero: int):
        """ Este es un ejemplo de como mover un personaje horizontalmente. No se considerarán los obstáculos.
        :param direccion: un string que puede ser derecha o izquierda
        :param ancho_tablero: el ancho del tablero para comprobar límites
        """
        # Variable local para almacenar el ancho del personaje y poder  comprobar colisiones con borde derecho
        # del tablero
        ancho_personaje = self.sprite[3]
        if (direccion.lower() == "derecha" and self.x + ancho_personaje < ancho_tablero):
            self.x += 1
        elif (direccion.lower() == "izquierda" and self.x > 0):
            self.x -= 1

#Propiedad piso

    @property
    def piso(self) -> int:
        return self.__piso

    @piso.setter
    def piso(self, piso: int):
        if not isinstance(piso, int):
            raise TypeError ("El piso debe ser un entero " + str(type(piso)))
        elif piso < 0:
            raise ValueError("El piso no debe ser un número negativo")
        else:
            self.__piso = piso

#Propiedad nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser un string " + str(type(nombre)))
        else:
            self.__nombre = nombre

    def __str__(self):
        return f"Personaje {self.nombre} en posición ({self.x}, {self.y}) en el piso {self.piso}"


