# FastAPI Tasks API

Una simple API de tareas construida con FastAPI.

## Cómo usar

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
3. Ejecuta la aplicación:
   ```bash
   uvicorn app.main:app --reload

Endpoints disponibles
- GET / - Página de inicio

- GET /tasks - Obtener todas las tareas

- POST /tasks - Crear nueva tarea

- GET /tasks/{id} - Obtener tarea por ID

- PUT /tasks/ - Actualizar tarea

- DELETE /tasks/{id} - Eliminar tarea

La API estará en: http://localhost:8000
