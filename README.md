# Game & Watch: Mario Bros (Adaptación en Python)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Pyxel](https://img.shields.io/badge/Pyxel-Retro_Game_Engine-red.svg)](https://github.com/kitao/pyxel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">
  <img src="clases/assets/GameplayReadme.gif" alt="Demo de Gameplay Mario Bros Pyxel" width="600">
</div>

Adaptación basada en las mecánicas del clásico "Mario Bros Game & Watch" con diseño propio, desarrollada en Python utilizando la librería Pyxel. 

Este es el proyecto final de la asignatura de Programación (1º de Ingeniería Informática, Universidad Carlos III de Madrid - UC3M), diseñado para aplicar conceptos de Programación Orientada a Objetos (POO).

## Características Técnicas

* **Arquitectura:** Uso de una Máquina de Estados Finita (FSM) para gestionar el flujo del juego (Menú, Jugando, Animaciones, Game Over).
* **Algoritmos lógicos:** Implementación de movimiento en "zig-zag" para los paquetes mediante paridad de cintas, y cálculo matemático de offsets para el apilado visual optimizado en el camión.
* **Jugabilidad:** Dificultad escalable (Fácil/Medio) y audio retro integrado.
* **Estructura:** Código modularizado en clases (`Tablero`, `Personaje`, `Cinta`, etc.) siguiendo un *flat layout*.

## Controles

| Entidad / Acción | Input |
| :--- | :--- |
| Personaje Derecho | `Flecha Arriba` / `Flecha Abajo` |
| Personaje Izquierdo | `W` / `S` |
| Menú / Confirmar | `Flechas` / `Espacio` o `Enter` |
| Salir / Reiniciar | `Q` / `R` |

## Instalación y Ejecución

Requiere Python 3.x instalado.

1. Clonar y acceder al repositorio:
   ```bash
   git clone [https://github.com/rrojjo/mario-bros-pyxel.git](https://github.com/rrojjo/mario-bros-pyxel.git)
   cd mario-bros-pyxel
   ```

2. Instalar dependencias:
   ```bash
   pip install pyxel
   ```

3. Ejecutar:
   ```bash
   python main.py
   ```

## Documentación y Licencia

* En la carpeta `docs/` se encuentra la memoria técnica completa del proyecto.
* Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
*Desarrollado por Juan Gimeno Merino y Pablo Rojo Castaño*
