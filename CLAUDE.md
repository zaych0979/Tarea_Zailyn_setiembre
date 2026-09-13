# Convenciones del proyecto

## Metodología: Spec-Driven Development

- Toda especificación (existente o nueva) vive en `especificaciones/`.
- Cada especificación es un archivo `NNN-nombre-corto.md` (numeración secuencial: 001, 002, ...).
- Antes de implementar una funcionalidad nueva, debe existir su especificación en esa carpeta.

## Arquitectura de código: MVC

Código de la aplicación en `src/control_contratos/`:

- `models/` — entidades y acceso a datos (SQLAlchemy).
- `views/` — plantillas (Jinja2 en `views/templates/`) y presentación.
- `controllers/` — rutas/lógica de orquestación (Flask blueprints).

## Gestión de librerías: uv

- Añadir dependencias: `uv add <paquete>`.
- Ejecutar la app: `uv run <script>`.
- Sincronizar el entorno: `uv sync`.
- No usar `pip install` directo ni editar `pyproject.toml` a mano para dependencias.
