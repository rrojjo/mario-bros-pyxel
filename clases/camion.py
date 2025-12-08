# Contiene la clase Camion.

class Camion:
    """
    Gestiona la lógica de transporte y la representación visual de la carga.
    Implementa un sistema de apilado visual para los paquetes recolectados.
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.x_inicial = x
        self._paquetes_cargados = 0
        self._capacidad = 8
        self.sprite = (0, 32, 64, 47, 48, 15)

        # Almacena la posición y sprite de cada caja para dibujarlas apiladas
        self.carga_visual = []

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS Y SETTERS)

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("La x debe ser un entero " + str(type(x)))
        # Se permite x negativa para animar la salida del camión por la izquierda
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
    def paquetes_cargados(self) -> int:
        return self._paquetes_cargados

    @property
    def capacidad(self) -> int:
        return self._capacidad

    # -------------------------------------------------------------------------
    # LÓGICA DE COMPORTAMIENTO Y CARGA

    def mover(self, dx: int):
        """Desplaza el camión y sincroniza la posición de la carga visual."""
        self.x += dx
        for caja in self.carga_visual:
            caja["x"] += dx

    def cargar_paquete(self, paquete_objeto):
        """
        Registra un paquete y calcula su posición visual en la pila (2 columnas x 4 filas).
        """
        if self._paquetes_cargados < self._capacidad:
            # Determinamos posición en la matriz de carga
            indice = self._paquetes_cargados
            columna = indice % 2
            fila = indice // 2

            # Cálculo de desplazamientos para apilar las cajas dentro del
            # área del camión
            desplazamiento_x = 17 + (columna * 16)
            desplazamiento_y = 26 + (-fila * 12)

            nueva_x = self.x + desplazamiento_x
            nueva_y = self.y + desplazamiento_y

            info_caja = {
                "x": nueva_x,
                "y": nueva_y,
                "sprite": paquete_objeto.sprite
            }

            self.carga_visual.append(info_caja)
            self._paquetes_cargados += 1

    def esta_lleno(self) -> bool:
        return self._paquetes_cargados >= self._capacidad

    def vaciar(self):
        """Reinicia el estado del camión tras completar un reparto."""
        self._paquetes_cargados = 0
        self.carga_visual = []