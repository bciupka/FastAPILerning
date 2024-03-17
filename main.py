from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class ModelName(str, Enum):
    first = "1st"
    second = "2nd"
    third = "3rd"


@app.get("/")
async def root():
    return {"message": "hello FastAPI"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/enum/{enum_model}")
async def read_enum(enum_model: ModelName):
    if enum_model is ModelName.first:
        return {"model": enum_model, "message": "This one"}
    if enum_model is ModelName.second:
        return {"model": enum_model, "message": "This other one"}
    return {"model": enum_model, "message": "This final one"}
