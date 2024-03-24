from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    length: int | None = None
    author: str
    available: bool = False


class UpdateBook(Book):
    title: str | None = None
    author: str | None = None


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
