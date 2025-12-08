from clases.paquete import Paquete
# Contiene la clase Cinta.

class Cinta:

    def __init__(self, numero: int, x: int, y: int, piso: int):
        self.numero = numero #numero de cinta
        self.x = x
        self.y = y
        self.piso = piso
        self._paquetes=[] #lista de paquetes en la cinta

        self.ancho=146 #ancho visual de la cinta
        self.centro_cinta = self.x + ((self.ancho + 8) / 2) # +8 para que el
        # cambio de forma se produzca detrás de la columna


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

# Métodos de gestión de paquetes

    @property
    def paquetes(self) -> list:
        return self._paquetes

    def agregar_paquete(self, paquete: Paquete):
        #Agrega un paquete a la cinta
        if type(paquete) != Paquete:
            raise TypeError("Solo objetos Paquete.")
        self._paquetes.append(paquete)

    def retirar_paquete(self, paquete: Paquete):
        #Retira un paquete específico de la cinta
        if paquete in self._paquetes:
            self._paquetes.remove(paquete)

    # --- LÓGICA SPRINT 3 ---

    def actualizar_paquetes(self):
        velocidad = 1

        for p in self._paquetes:

            # --- 1. MOVIMIENTO (Zig-Zag) ---
            if self.numero == 0 or self.numero % 2 != 0:
                p.x -= velocidad  # Izquierda
            else:
                p.x += velocidad  # Derecha

            # --- 2. CAMBIO DE FORMA (Al cruzar la mitad) ---
            # Solo si el paquete aún no tiene la forma de esta cinta
            if p.indice_sprite != self.numero:

                # Caso A: La cinta mueve a la IZQUIERDA
                # Si el paquete pasa el centro hacia la izq (x es menor que centro)
                if ((self.numero == 0 or self.numero % 2 != 0) and p.x <
                        self.centro_cinta):
                    p.evolucionar(self.numero)

                # Caso B: La cinta mueve a la DERECHA
                # Si el paquete pasa el centro hacia la der (x es mayor que centro)
                elif (self.numero % 2 == 0) and p.x > self.centro_cinta:
                    p.evolucionar(self.numero)

    def paquete_llego_al_final(self):
        """Detecta si el paquete llegó al punto de recogida"""
        for p in self._paquetes:

            # Cintas que van a la IZQUIERDA (0, 1, 3, 5)
            # El final es cuando x <= self.x (el inicio visual de la cinta)
            if self.numero == 0 or self.numero % 2 != 0:
                if p.x <= self.x:
                    return p

            # Cintas que van a la DERECHA (2, 4)
            # El final es cuando x >= self.x + ancho
            else:
                if p.x >= self.x + self.ancho:
                    return p
        return None