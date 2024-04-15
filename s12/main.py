import dependencies
from fastapi import FastAPI, Depends, BackgroundTasks
from routers import users, items
from internal import admin
from typing import Annotated

tags_metadata = [
    {
        "name": "users",
        "description": "Users endpoints",
        "externalDocs": {"url": "https://fastapi.tiangolo.com/tutorial/metadata/"},
    },
    {"name": "items", "description": "Items endpoints"},
]

app = FastAPI(
    title="S12 Guide API",
    summary="S12 guide chapter API",
    description="Thats a API developed for training **FastAPI** - S12 with BG Tasks, *Metadata* and multiple files applications",
    version="1.0.2",
    contact={"name": "BC", "email": "bc@email.com"},
    terms_of_service="https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-api",
    license_info={
        "name": "Apache Licence 2.0",
        "identifier": "Apache-2.0",
    },
    openapi_tags=tags_metadata,
    redoc_url=None,
)
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
