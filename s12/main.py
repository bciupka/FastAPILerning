import dependencies
from fastapi import FastAPI, Depends, BackgroundTasks
from routers import users, items
from internal import admin
from typing import Annotated

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"])


def sample_background(numbers: list[int]):
    result = sum([i * j for i in numbers for j in numbers])
    print(result)
    return


def sample_bg_2(some_txt: str):
    print(some_txt)
    return


async def sample_dependency(numbers: list[int], bg_task: BackgroundTasks):
    print("Running dep")
    bg_task.add_task(sample_background, numbers)
    return numbers


@app.get("/", dependencies=[Depends(dependencies.random_dep)])
async def main():
    return {"msg": "main"}


@app.post("/bg_tasks")
async def bg_tasks(
    numbers: Annotated[list[int], Depends(sample_dependency)],
    text: str,
    bg_task: BackgroundTasks,
):
    print("Running endp")
    bg_task.add_task(sample_bg_2, " ".join([text, str(numbers)]))
    return {"msg": "bg_test_enp_echo"}
