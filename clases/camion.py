# Contiene la clase Camion.

class Camion:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._paquetes_cargados=0 #contador
        self._capacidad=8 #fijo

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

#Propiedad paquetes_cargados

    @property
    def paquetes_cargados(self) -> int:
        return self._paquetes_cargados

    @property
    def capacidad(self) -> int:
        return self._capacidad

#LÓGICA DE COMPORTAMIENTO

    def cargar_paquete(self):
        #Incrementa el contador de paquetes si no está lleno.
        if self._paquetes_cargados < self._capacidad:
            self._paquetes_cargados += 1

    def esta_lleno(self) -> bool:
        #Devuelve True si el camión ha alcanzado su capacidad máxima.
        return self._paquetes_cargados >= self._capacidad

    def vaciar(self):
        #Resetea el contador de paquetes (se usará cuando el camión vuelva  del reparto).
        self._paquetes_cargados = 0

    def __str__(self) -> str:
        return "Camión en (" + str(self.x) + "," + str(self.y) + ") - Carga: " + str(self.paquetes_cargados) + "/" + str(self.capacidad)