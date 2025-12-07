# Contiene las clases Personaje, Mario y Luigi.

class Personaje:

    def __init__(self, x: int,y: int, piso:int, nombre:str):
        self.x = x
        self.y = y
        self.piso = piso
        self.nombre = nombre
        self.invertido = False

        if self.nombre == "Luigi":
            self.u_original = 0
        else:  # Mario
            self.u_original = 16

        # Creamos el sprite inicial
        self.actualizar_sprite()

    def actualizar_sprite(self):
        """Regenera la tupla del sprite según si está invertido o no"""
        ancho = 16
        if self.invertido:
            ancho = -16  # Invertir horizontalmente

        self.sprite = (0, self.u_original, 0, 16, 16, 15)

        # Nota: pyxel.blt usa el ancho para hacer el flip.
        # Si queremos que miren al lado CONTRARIO, cambiamos el signo del ancho
        # al dibujarlo. Pero como self.sprite es una tupla fija, la modificamos aquí.

        # Truco: Si blt recibe ancho negativo, voltea la imagen.
        self.sprite = (0, self.u_original, 0, ancho, 16, 15)

    def set_mirada_invertida(self, estado: bool):
        self.invertido = estado
        self.actualizar_sprite()

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
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise TypeError(
                "El nombre debe ser un string " + str(type(valor)))
        elif valor != "Mario" and valor != "Luigi":
            raise ValueError("El nombre debe ser 'Mario' o 'Luigi'")
        else:
            self.__nombre = valor

#Función mover
    def subir(self, nueva_y: int):
        """
        Sube un piso al personaje y actualiza su posición Y.
        Incrementa el piso en 1.
        """
        # Actualizamos el piso (el setter ya validará que sea entero)
        self.piso += 2
        # Actualizamos la coordenada visual
        self.y = nueva_y

    def bajar(self, nueva_y: int):
        """
        Baja un piso al personaje y actualiza su posición Y.
        Decrementa el piso en 1.
        """
        # Actualizamos el piso
        self.piso -= 2
        # Actualizamos la coordenada visual
        self.y = nueva_y


