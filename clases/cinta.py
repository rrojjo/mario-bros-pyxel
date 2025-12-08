# Contiene la clase Cinta.

from clases.paquete import Paquete

class Cinta:
    """
    Representa una cinta transportadora.
    Controla el movimiento direccional y la evolución visual de los paquetes.
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, numero: int, x: int, y: int, piso: int):
        self.numero = numero
        self.x = x
        self.y = y
        self.piso = piso
        self._paquetes = []

        self.ancho = 146
        # Punto medio visual (+8px offset) para ocultar el cambio de sprite
        # tras la columna
        self.centro_cinta = self.x + ((self.ancho + 8) / 2)

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS Y SETTERS)

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if not isinstance(numero, int):
            raise TypeError(
                "El número debe ser un entero " + str(type(numero)))
        elif numero < 0:
            raise ValueError("El número no debe ser un número negativo")
        else:
            self.__numero = numero

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
    def paquetes(self) -> list:
        return self._paquetes

    # -------------------------------------------------------------------------
    # GESTIÓN DE LA LISTA DE PAQUETES

    def agregar_paquete(self, paquete: Paquete):
        if type(paquete) != Paquete:
            raise TypeError("Solo objetos Paquete.")
        self._paquetes.append(paquete)

    def retirar_paquete(self, paquete: Paquete):
        if paquete in self._paquetes:
            self._paquetes.remove(paquete)

    # -------------------------------------------------------------------------
    # LÓGICA DE ACTUALIZACIÓN Y MOVIMIENTO (SPRINT 3)

    def actualizar_paquetes(self):
        """
        Gestiona el movimiento en zig-zag y la transformación de paquetes al
        cruzar el centro.
        """
        velocidad = 1

        for p in self._paquetes:

            # 1. Movimiento Zig-Zag:
            # Cintas 0 e Impares -> Izquierda | Cintas Pares -> Derecha
            if self.numero == 0 or self.numero % 2 != 0:
                p.x -= velocidad
            else:
                p.x += velocidad

            # 2. Evolución Visual:
            # El paquete adopta la forma de la cinta actual al cruzar su mitad
            if p.indice_sprite != self.numero:

                # Chequeo de cruce según la dirección de la cinta
                if ((self.numero == 0 or self.numero % 2 != 0) and p.x <
                        self.centro_cinta):
                    p.evolucionar(self.numero)

                elif (self.numero % 2 == 0) and p.x > self.centro_cinta:
                    p.evolucionar(self.numero)

    def paquete_llego_al_final(self):
        """
        Verifica si algún paquete ha alcanzado el punto de recogida o caída.
        """
        for p in self._paquetes:

            # Límite izquierdo para cintas 0 e impares
            if self.numero == 0 or self.numero % 2 != 0:
                if p.x <= self.x:
                    return p

            # Límite derecho para cintas pares
            else:
                if p.x >= self.x + self.ancho:
                    return p
        return None