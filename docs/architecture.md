# Arquitectura del Display Manager

Este proyecto está diseñado para manejar la disposición de monitores en Linux mediante un backend específico del compositor.

## Componentes principales

- `src/backend.py`
  - Define una interfaz `DisplayBackend` para listar monitores y aplicar perfiles.

- `src/monitor.py`
  - Modelo de datos `Monitor` con propiedades como nombre, resolución, posición y escala.

- `src/profile.py`
  - Define `MonitorProfile` y funciones para guardar/cargar perfiles a JSON.

- `src/hyprland.py`
  - Backend concreto para Hyprland.
  - Usa `hyprctl monitors -j` para detectar monitores.
  - Aplica perfiles mediante `hyprctl dispatch setmonitor ...`.

- `src/caelestia.py`
  - Backend concreto para Caelestia.
  - Usa `caelestiactl monitors -j` para detectar monitores.
  - Aplica perfiles mediante `caelestiactl set-monitor ...`.

- `src/backend_factory.py`
  - Selecciona el backend activo según el compositor.

- `src/gui.py`
  - Interfaz GTK para ver monitores, guardar perfiles y aplicar configuraciones.

- `src/main.py`
  - Inicializa la aplicación y arranca la ventana principal.

## Flujo de datos

1. `gui.py` solicita la lista de monitores al backend.
2. `hyprland.py` obtiene los datos desde Hyprland y los convierte en `Monitor`.
3. El usuario guarda una configuración en `profiles.json`.
4. Cuando se aplica un perfil, el backend ejecuta los comandos necesarios.

## Extensiones futuras

- Añadir un backend `caelestia.py` para soportar el compositor de Caelestia.
- Implementar detección de resolución y posicionamiento dinámico.
- Añadir editor visual de disposición de monitores.
- Mejorar validación de comandos del compositor.
