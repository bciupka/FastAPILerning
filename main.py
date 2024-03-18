from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class ModelName(str, Enum):
    first = "1st"
    second = "2nd"
    third = "3rd"


class CarType(str, Enum):
    van = "van"
    coupe = "coupe"
    sedan = "sedan"


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


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


@app.get("/items/range/")
async def get_range(stop: int | None = None, start: int = 0):
    items_to_response = (
        fake_items_db[start:stop]
        if stop is not None
        else fake_items_db[start:]
    )
    return {"items": items_to_response}


@app.get("/cars/{cartype}")
async def is_cool(cartype: CarType, iscool: bool = False):
    return {"car_type": cartype, "cool": iscool}
