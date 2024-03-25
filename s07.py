from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


class Book(BaseModel):
    title: str
    length: int | None = None
    author: str
    available: bool = False


class UpdateBook(Book):
    title: str | None = None
    author: str | None = None


class UpdatePandanticModel:
    def __init__(
        self, model_id: str | int, update_model: BaseModel, log: bool = False
    ) -> None:
        self.model_id = model_id
        self.update_model = update_model
        self.log = log


books = {
    "first": {"title": "first book", "author": "Xander Lang", "available": True},
    "second": {"title": "second book", "author": "Jack Smith"},
    "third": {
        "title": "third book",
        "author": "Neo Vim",
        "length": 450,
        "available": True,
    },
}


@app.get("/show_book/{book_id}")
async def show_book(book_id: str) -> dict:
    return books[book_id]


@app.get("/show_book_model/{book_id}")
async def show_book_model(book_id: str) -> Book:
    return books[book_id]


@app.put("/put_book/{book_id}")
async def put_book(book_id: str, book: Book) -> Book:
    updated_book = jsonable_encoder(book)
    books[book_id] = updated_book
    return updated_book


@app.patch("/patch_book/{book_id}")
async def patch_book(book_id: str, book: UpdateBook) -> Book:
    updated_data = book.model_dump(exclude_unset=True)
    updated_book = Book(**books[book_id]).model_copy(update=updated_data)
    books[book_id] = jsonable_encoder(updated_book)
    return updated_book


async def update_pydantic_model(
    model_id: str | int, update_model: BaseModel, log: bool = False
):
    return {"model_id": model_id, "update_model": update_model, "log": log}


UpdateModel = Annotated[dict, Depends(update_pydantic_model)]


@app.put("/sample_put")
async def sample_put(commons: UpdateModel):
    return {"updated": True, "method": "PUT"}


@app.patch("/sample_patch")
async def sample_patch(commons: UpdateModel):
    return {"updated": True, "method": "PATCH"}


async def update_pydantic_admin(commons: UpdateModel, password: str):
    return {**commons, "password": password}


UpdateAdmin = Annotated[dict, Depends(update_pydantic_admin)]


@app.put("/sample_sub_put")
async def sample_sub_put(commons: UpdateAdmin):
    return {"updated": True, "method": "PUT w/ Admin"}


UpdateModelClass = Annotated[UpdatePandanticModel, Depends()]


@app.put("/sample_class_put")
async def sample_class_put(commons: UpdateModelClass):
    return {"updated": True, "method": "PUT w/ Class"}


async def test_sub_dependency(q: str | int | None = None):
    return q


async def test_dependency(
    q: Annotated[str | int | None, Depends(test_sub_dependency)],
    alt_q: str | int | None = None,
):
    if q:
        return q
    return alt_q


@app.get("/test_sub_dependency", summary="Test that sub_dep")
async def test_sub_dep(q_or_alt: Annotated[str | int | None, Depends(test_dependency)]):
    return q_or_alt
