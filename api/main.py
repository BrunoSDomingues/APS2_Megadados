# Código original disponível em https://github.com/Insper/Megadados2020-2-Projeto1-alunos/blob/master/main.py
# A partir do código original fez-se uma nova versão

from fastapi import FastAPI
from api.routers import task

tags_metadata = [
    {
        "name": "task",
        "description": "Operations related to tasks.",
    },
]

app = FastAPI(
    title="Task list",
    description="Task-list project for the **Megadados** course",
    openapi_tags=tags_metadata,
)

app.include_router(task.router, prefix="/task",tags=["task"])
