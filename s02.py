from fastapi import FastAPI, Query, Path, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()


class Sample(BaseModel):
    name: str
    score: int
    about: str | None = None


class User(BaseModel):
    first_name: str
    last_name: str
    email: str


class RestrictiveUser(BaseModel):
    first_name: Annotated[str, Field(max_length=10)]
    last_name: Annotated[str, Field(max_length=12)]
    age: Annotated[int | None, Field(gt=15)] = None


@app.post("/new_sample")
async def add_sample(sample: Sample):
    return sample


@app.put("/update_sample/{id}")
async def update_sample(id: int, sample: Sample, email: str):
    put_sample = {"id": id, **dict(sample)}
    put_sample["email"] = email
    return put_sample


@app.put("/update_about/{id}")
async def update_about(id: int, sample: Sample, new_about: str):
    if id:
        put_sample = Sample(**{"name": "test", "score": 5})
        put_sample.about = new_about
        return put_sample


@app.get("/tiny_query")
async def query_valid(q: Annotated[str | None, Query(min_length=3, max_length=6)]):
    return {"query_param": q}


@app.get("/list_query")
async def list_query(q: Annotated[list[str], Query()]):
    return {"query_param": q}


@app.get("/10_to_15_only/{number}")
async def read_number(
    *,
    add_msg: Annotated[str | None, Query(deprecated=True, max_length=5)] = "Hello",
    number: Annotated[
        int | float,
        Path(
            title="10<x<15", description="Pass number between 10 and 15", ge=10, le=15
        ),
    ]
):
    return {"message": add_msg, "number_ok": True}


@app.post("/two_bodies")
async def two_bodies(sample: Sample, user: User):
    return {"sample": sample, "user": user}


@app.post("/embed_in")
async def embed_test(user: Annotated[User, Body(embed=True)]):
    return {"user": user}


@app.post("/not_embed_in")
async def embed_test(user: User):
    return {"user": user}


@app.post("/model_and_single")
async def embed_test(user: User, motto: Annotated[str, Body()]):
    return {"user": user, "motto": motto}


@app.post("/bounded_age_user")
async def validate_age(user: RestrictiveUser):
    return {"user": user}
