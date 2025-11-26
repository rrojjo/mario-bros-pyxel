# (Opcional) Módulo para definir variables constantes (ej: velocidades, puntos, colores).

# constantes.py

# Dimensiones de la pantalla
ANCHO_PANTALLA = 368
ALTO_PANTALLA = 192
TAMANO_BLOQUE = 16

# Dimensiones en Bloques (Tiles)
ANCHURA_GRID = ANCHO_PANTALLA // TAMANO_BLOQUE  # 23 bloques
ALTURA_GRID = ALTO_PANTALLA // TAMANO_BLOQUE    # 12 bloques

# Posiciones clave en el eje X (Columnas 0 a 22)
COL_ESCALERA_LUIGI = 3
COL_ESCALERA_MARIO = 19
# Las cintas irán entre estas dos columnas

# Símbolos del mapa (Leyenda visual para tu lista)
VACIO = "V"
SUELO = "S"        # Suelo solido
ESCALERA = "H"
CINTA = "C"
CAMION = "T"       # Truck
INICIO_PAQUETE = "I"

# constantes.py

# --- Mapeo de Gráficos (Pyxres) ---
# Nueva Estructura: (u, v, ancho, alto, colkey)
SPRITES = {
    SUELO:          (32,  27,  16, 5, 0),
    ESCALERA:       (32, 0,  16,  16, 0),
    CINTA:          (49, 4,  15, 8,  0),
    CAMION:         (32, 64,  48, 48, 0),
    INICIO_PAQUETE: (80, 0,  16, 16, 0),
}