from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from datetime import date, datetime
from itertools import count

app =FastAPI()

class Task(BaseModel):
    id: int | None  = None
    title: str
    description: str
    completed: bool = False
    creation_date: date | None = None

task_db = []
add_id = count(1)

# Funciones de apoyo
def task_exit(task: Task):
    """Verifica si la tarea ya existe"""
    for existing_task in task_db:
        if existing_task.title == task.title and existing_task.description == task.description:
            return True
    return False

def find_task_by_id(id: int):
    for task in task_db:
        if task.id == id:
            return task
    return None

# Crear nueva tarea
@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task : Task):
    if task_exit(task):
        raise HTTPException(status_code=400, detail="Ya existe una tarea con ese título y descripción")

    task.id = next(add_id)
    task.creation_date = date.today()
    task_db.append(task)
    return {"mesasge" : "Tarea creada con exito", "task": task}

# Obtener lista de tareas
@app.get("/tasks/", response_model=list[Task], status_code=status.HTTP_200_OK)
async def task_list():
    return task_db

# Obetener tarea por id
@app.get("/tasks/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def task_by_id(id: int):
    task = find_task_by_id(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe una tarea con ese ID")

    return task

# Actualizar tarea completada por id
@app.put("/tasks/", status_code=status.HTTP_202_ACCEPTED)
async def update_task(id: int):
    task = find_task_by_id(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe una tarea con ese ID")

    task.completed = True
    return {"message": "La tarea ha sido completada"}

# Eliminar tarea por id
@app.delete("/tasks/{id}")
async def delete_task(id: int):
    task = find_task_by_id(id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe una tarea con ese ID")

    task_db.remove(task)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Tarea eliminada correctamente"})

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}