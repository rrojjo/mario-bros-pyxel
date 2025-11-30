# Contiene el nivel de dificultad del juego y la configuración del mismo.

# nivel.py
class Nivel:
    def __init__(self, dificultad):
        self.dificultad = dificultad
        self._configurar_dimensiones()
        self.num_cintas = self._configurar_cintas()

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, valor):
        if not isinstance(valor, str):
            raise TypeError("La dificultad debe ser una cadena " + str(type(valor)))
        elif valor not in ["FACIL", "MEDIO", "EXTREMO", "CRAZY"]:
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
            raise ValueError("El ancho de pantalla debe ser un número positivo")
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


    def _configurar_dimensiones(self):
        """Asigna valores directos a ancho y alto según la dificultad"""

        if self.dificultad == "FACIL" or self.dificultad == "CRAZY":
            self.ancho_pantalla = 368
            self.alto_pantalla = 192

        elif self.dificultad == "MEDIO" or self.dificultad == "EXTREMO":
            self.ancho_pantalla = 368
            self.alto_pantalla = 240  # Valor directo (ejemplo)

        else:
            raise ValueError("Dificultad no reconocida en dimensiones: " + str(
                self.dificultad))


    def _configurar_cintas(self):
        if self.dificultad == "FACIL" or self.dificultad == "CRAZY":
            return 6 # Cintas 0 a 5
        elif self.dificultad == "MEDIO":
            return 8 # Cintas 0 a 7
        elif self.dificultad == "EXTREMO":
            return 10 # Cintas 0 a 9
        else:
            return 6