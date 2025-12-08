# Contiene la clase Camion.

class Camion:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.x_inicial=x
        self._paquetes_cargados=0 #contador
        self._capacidad=8 #fijo
        self.sprite= (0, 32, 64, 47, 48, 15)
        # NUEVO: Lista para guardar las coordenadas y sprites de las cajas en el camión
        self.carga_visual = []

#Propiedad x

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("La x debe ser un entero " + str(type(x)))
        # ELIMINAMOS LA RESTRICCIÓN DE NEGATIVOS para que pueda salir de pantalla
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

    def mover(self, dx: int):
        """Mueve el camión (y su carga) horizontalmente"""
        self.x += dx
        # ¡Importante! También movemos las cajas visuales que lleva encima
        for caja in self.carga_visual:
            caja["x"] += dx

    def cargar_paquete(self, paquete_objeto):
        """
        Recibe el objeto paquete, calcula su posición en la pila
        y guarda los datos para dibujarlo.
        """
        if self._paquetes_cargados < self._capacidad:
            # 1. CÁLCULO DE POSICIÓN (APILADO)
            # Vamos a hacer 2 columnas de 4 cajas cada una.
            # Columna 0: Paquetes 0, 2, 4, 6
            # Columna 1: Paquetes 1, 3, 5, 7

            # Índice actual (0 a 7)
            idx = self._paquetes_cargados

            columna = idx % 2
            fila = idx // 2

            # Ajustes visuales relativos a la X, Y del camión
            # offset_x: Movemos las cajas a la parte trasera del camión
            # offset_y: Las apilamos hacia arriba (restamos Y)

            offset_x = 17 +(columna * 16)  # Separación horizontal de 10px
            offset_y = 26 + (-fila * 12)  # Separación vertical de 6px

            nueva_x = self.x + offset_x
            nueva_y = self.y + offset_y

            # Guardamos un diccionario con lo necesario para dibujar
            info_caja = {
                "x": nueva_x,
                "y": nueva_y,
                "sprite": paquete_objeto.sprite
                # Copiamos el sprite del paquete
            }

            self.carga_visual.append(info_caja)
            self._paquetes_cargados += 1

    def esta_lleno(self) -> bool:
        #Devuelve True si el camión ha alcanzado su capacidad máxima.
        return self._paquetes_cargados >= self._capacidad

    def vaciar(self):
        #Resetea el contador de paquetes (se usará cuando el camión vuelva  del reparto).
        self._paquetes_cargados = 0
        self.carga_visual = []  # Limpiamos también el dibujo