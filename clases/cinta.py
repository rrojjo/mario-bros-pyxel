# Contiene la clase Cinta.
#Faltan unas cosas

class Cinta:

    def __init__(self, numero: int, x: int, y: int, piso: int):
        self.numero = numero #numero de cinta
        self.x = x
        self.y = y
        self.piso = piso

#Propiedad numero

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if not isinstance(numero, int):
            raise TypeError ("El número debe ser un entero " + str(type(numero)))
        elif numero < 0:
            raise ValueError("El número no debe ser un número negativo")
        else:
            self.__numero = numero

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
