# Contiene la clase Nivel

class Nivel:
    """
    Encapsula la configuración del juego (velocidad, dimensiones, cantidad de
    cintas) basada en la dificultad seleccionada.
    """

    # -------------------------------------------------------------------------
    # INICIALIZACIÓN

    def __init__(self, dificultad):
        self.dificultad = dificultad
        self._configurar_dimensiones()
        self._configurar_pisos()
        self.num_cintas = self._configurar_cintas()
        self.puntos_levelup = self._configurar_puntos_paquetes()

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS Y SETTERS)

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, valor):
        if not isinstance(valor, str):
            raise TypeError(
                "La dificultad debe ser una cadena " + str(type(valor)))
        elif valor not in ["FACIL", "MEDIO"]:
            raise ValueError("Dificultad no reconocida: " + str(valor))
        else:
            self.__dificultad = valor

    @property
    def ancho_pantalla(self):
        return self.__ancho_pantalla

    @ancho_pantalla.setter
    def ancho_pantalla(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El ancho de pantalla debe ser un entero " +
                            str(type(valor)))
        elif valor <= 0:
            raise ValueError(
                "El ancho de pantalla debe ser un número positivo")
        else:
            self.__ancho_pantalla = valor

    @property
    def alto_pantalla(self):
        return self.__alto_pantalla

    @alto_pantalla.setter
    def alto_pantalla(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El alto de pantalla debe ser un entero " + str(
                type(valor)))
        elif valor <= 0:
            raise ValueError("El alto de pantalla debe ser un número positivo")
        else:
            self.__alto_pantalla = valor

    @property
    def num_pisos(self):
        return self.__num_pisos

    @num_pisos.setter
    def num_pisos(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El número de pisos debe ser un entero " + str(
                type(valor)))
        elif valor != 5 and valor != 7:
            raise ValueError("El número de pisos debe ser 5 o 7")
        else:
            self.__num_pisos = valor

    # -------------------------------------------------------------------------
    # MÉTODOS DE CONFIGURACIÓN INTERNA

    def _configurar_dimensiones(self):
        """Establece la resolución de la ventana según la dificultad."""

        if self.dificultad == "FACIL" or self.dificultad == "MEDIO":
            self.ancho_pantalla = 368
            self.alto_pantalla = 192

        # Preparado para poder implementar un nivel con un tamaño de mapa mayor
        # elif self.dificultad == "EXTREMO":
            # self.ancho_pantalla = 736
            # self.alto_pantalla = 384

        else:
            raise ValueError("Dificultad no reconocida en dimensiones: " + str(
                self.dificultad))

    def _configurar_cintas(self):
        if self.dificultad == "FACIL":
            return 6  # Cintas 0 a 5
        elif self.dificultad == "MEDIO":
            return 8  # Cintas 0 a 7
        else:
            return 6

    def _configurar_pisos(self):
        if self.dificultad == "FACIL":
            self.num_pisos = 5  # Pisos 0 a 5
        elif self.dificultad == "MEDIO":
            self.num_pisos = 7  # Pisos 0 a 7

    def _configurar_puntos_paquetes(self):
        """
        Define el umbral de puntuación para incrementar la dificultad (más
        paquetes).
        """
        if self.dificultad == "FACIL":
            return 50
        elif self.dificultad == "MEDIO":
            return 30
        else:
            return 50