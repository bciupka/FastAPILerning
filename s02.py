from fastapi import FastAPI

# from enum import Enum
from pydantic import BaseModel

app = FastAPI()


class Sample(BaseModel):
    name: str
    score: int
    about: str | None = None


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