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

# Propiedad piso

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

# Propiedad nombre

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str):
        if not isinstance(nombre, str):
            raise TypeError(
                "El nombre debe ser un string " + str(type(nombre)))
        else:
            self.__nombre = nombre

#Función mover
    def subir(self, nueva_y: int):
        """
        Sube un piso al personaje y actualiza su posición Y.
        Incrementa el piso en 1.
        """
        # Actualizamos el piso (el setter ya validará que sea entero)
        self.piso += 1
        # Actualizamos la coordenada visual
        self.y = nueva_y

    def bajar(self, nueva_y: int):
        """
        Baja un piso al personaje y actualiza su posición Y.
        Decrementa el piso en 1.
        """
        # Actualizamos el piso
        self.piso -= 1
        # Actualizamos la coordenada visual
        self.y = nueva_y

    def __str__(self):
        return f"Personaje {self.nombre} en posición ({self.x}, {self.y}) en el piso {self.piso}"


