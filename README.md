# 🏭 Game & Watch: Mario Bros (Adaptación en Python)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pyxel](https://img.shields.io/badge/Pyxel-Retro_Game_Engine-red.svg)](https://github.com/kitao/pyxel)

Este proyecto es una adaptación basada en las mecánicas del clásico juego **"Mario Bros Game & Watch"** de Nintendo, reimaginado con una estética y diseño de personajes propios. Ha sido desarrollado íntegramente en **Python** utilizando el motor gráfico retro **Pyxel**. 

Este desarrollo forma parte del proyecto final de la asignatura de Programación del **primer año del Grado en Ingeniería Informática** en la **Universidad Carlos III de Madrid (UC3M)**. El objetivo principal fue aplicar los fundamentos de la Programación Orientada a Objetos (POO), encapsulación, herencia y gestión de estados en un entorno gráfico interactivo.

## 🎮 Características Principales

* **Adaptación de mecánicas clásicas:** Recreación del mítico sistema de paso de cajas en la fábrica, pero con una identidad visual renovada. Incluye un sistema de puntuación escalable y aumento progresivo de la dificultad.
* **Máquina de Estados Finita (FSM):** Arquitectura no lineal gobernada por un controlador principal (`Tablero`) que gestiona las transiciones entre: `MENU`, `JUGANDO`, `REPARTO` (animación del camión), `CASTIGO` (animación de error con "The Boss") y `GAMEOVER`.
* **Audio y Feedback Retro:** Integración de efectos de sonido interactivos y melodías completas mediante el motor de audio de Pyxel.
* **Dificultad Configurable:** Selector de niveles ("FÁCIL" y "MEDIO") que altera dinámicamente el número de cintas transportadoras y la velocidad global del bucle de juego.

## 🧠 Algoritmos Destacados

El proyecto resuelve varios retos lógicos propios de la simulación 2D:

* **Algoritmo de Movimiento "Zig-Zag" de Paquetes:** La dirección física de las cajas se calcula algorítmicamente mediante la paridad del ID de la cinta. Las cintas pares mueven la caja reduciendo su coordenada X, mientras que las impares la incrementan. Al interactuar el jugador, la caja se transfiere a la lista de la cinta superior, creando el efecto de subida.
* **Sistema de Apilado Visual Matemático:** En lugar de instanciar nuevas entidades físicas dentro del camión, se calcula un offset `(x, y)` exacto en función del índice de carga del paquete (`0..7`). Esto se logra usando operaciones modulares (`columna = indice % 2`, `fila = indice // 2`), optimizando enormemente el rendimiento en el renderizado.

## 📂 Estructura del Proyecto

Se ha seguido una estructura *flat layout* (típica en Python) modularizando la lógica en clases puras:

* `main.py`: Punto de entrada del juego y configuración inicial.
* `clases/`: Módulos principales separando responsabilidades (`Tablero`, `Personaje`, `Cinta`, `Paquete`, `Camion`, `Nivel`). Incluye los `assets` integrados para preservar las rutas relativas originales.
* `docs/`: Contiene la memoria técnica detallada original del proyecto.

## 🕹️ Controles

| Entidad / Acción | Input |
| :--- | :--- |
| **Personaje Derecho** | `Flecha Arriba` (Subir) / `Flecha Abajo` (Bajar) |
| **Personaje Izquierdo** | `W` (Subir) / `S` (Bajar) |
| **Menú / Navegación** | `Flechas` (Mover) / `Espacio` o `Enter` (Confirmar) |
| **Gestión de Partida**| `Q` (Salir) / `R` (Reiniciar o Menú) |

## 🚀 Instalación y Ejecución

**Requisitos previos:** Python 3.x instalado en el sistema.

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/rrojjo/Mario-Bros-Repository.git](https://github.com/rrojjo/Mario-Bros-Repository.git)
   cd Mario-Bros-Repository
   ```

2. Instala la dependencia gráfica (Pyxel):
   ```bash
   pip install pyxel
   ```

3. Ejecuta el juego:
   ```bash
   python main.py
   ```

---
*Desarrollado por Juan Gimeno Merino y Pablo Rojo Castaño*
