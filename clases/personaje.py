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

        # Temporizador para la animación de coger paquete
        self.timer_animacion = 0

        # Creamos el sprite inicial
        self.actualizar_sprite()

    def update(self):
        """Actualiza temporizadores internos"""
        if self.timer_animacion > 0:
            self.timer_animacion -= 1
            # Cuando acaba la animación, forzamos actualización para volver a normal
            if self.timer_animacion == 0:
                self.actualizar_sprite()

        # IMPORTANTE: Mario en el piso 0 siempre revisa su orientación
        if self.nombre == "Mario" and self.piso == 0 and self.timer_animacion == 0:
            self.actualizar_sprite()

    def animar_recogida(self):
        """Activa la animación de cargar paquete durante unos frames"""
        self.timer_animacion = 10  # Duración de la pose (aprox 0.3 seg)
        self.actualizar_sprite()

    def actualizar_sprite(self):
        """
        Calcula qué sprite mostrar basándose en:
        1. Si está cogiendo un paquete (Prioridad máxima).
        2. Si es Mario en el piso 0 (Regla especial).
        3. Estado normal o invertido (Castigo).
        """

        # --- 1. COORDENADAS DEL SPRITE (u, v) ---
        if self.timer_animacion > 0:
            # Sprite de recogida solicitado: (0, 16)
            u = 0
            v = 16
        else:
            # Sprite normal (Idle)
            u = self.u_original
            v = 0

        # --- 2. ORIENTACIÓN (ANCHO) ---
        ancho = 16  # Por defecto, mirando a la derecha (o normal del sprite)

        if self.nombre == "Mario":
            # REGLA 1: Animación de recogida -> Invertido
            if self.timer_animacion > 0:
                ancho = -16

            # REGLA 2: Mario esperando en el piso 0 -> Invertido
            elif self.piso == 0:
                ancho = -16

            # REGLA 3: Estado general invertido (por castigo del Jefe)
            elif self.invertido:
                ancho = -16

            # Normal (Pisos 2, 4 esperando)
            else:
                ancho = 16

        elif self.nombre == "Luigi":
            # REGLA: Luigi solo se invierte si está castigado (Jefe)
            # O si quisieras que la recogida fuera invertida (no especificado, lo dejo normal)
            if self.invertido:
                ancho = -16
            else:
                ancho = 16

        # --- 3. GENERAR TUPLA FINAL ---
        # (banco, u, v, ancho, alto, color_transparente)
        self.sprite = (0, u, v, ancho, 16, 15)

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
        self.actualizar_sprite()

    def bajar(self, nueva_y: int):
        """
        Baja un piso al personaje y actualiza su posición Y.
        Decrementa el piso en 1.
        """
        # Actualizamos el piso
        self.piso -= 2
        # Actualizamos la coordenada visual
        self.y = nueva_y
        self.actualizar_sprite()