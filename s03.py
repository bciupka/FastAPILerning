from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()


class Country(BaseModel):
    name: str
    symbol: str | None = None

    model_config = {
        "json_schema_extra": {"examples": [{"name": "England", "symbol": "ENG"}]}
    }


class Author(BaseModel):
    first_name: str
    last_name: str
    country: Country

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "country": Country.model_config["json_schema_extra"]["examples"][0],
                }
            ]
        }
    }


class Book(BaseModel):
    title: str
    author: Author


class Shelf(BaseModel):
    books: list[Book] | None = None


@app.post("/add_book")
async def post_book(book: Book):
    return book


@app.post("/define-shelf")
async def post_shelf(shelf: Shelf):
    return shelf


@app.get("/shelf")
async def get_shelf():
    country = Country(name="Poland", symbol="PL")
    author = Author(first_name="Bartek", last_name="XYZ", country=country)
    book_1 = Book(title="test", author=author)
    book_2 = Book(title="test2", author=author)
    shelf = Shelf(books=[book_1, book_2])
    return shelf


@app.post("/add_keys")
async def add_operation(
    body: Annotated[dict[int, int], Body(max_length=2, min_length=2)]
):
    key_sum = list(body.keys())[0] + list(body.keys())[1]
    val_sum = list(body.values())[0] + list(body.values())[1]
    return {"key_sum": key_sum, "val_sum": val_sum}


@app.post("/author_example")
async def author_get(author: Author):
    return author


@app.post("/body_example")
async def country_example(
    country: Annotated[Country, Body(examples=[{"name": "Poland", "symbol": "PL"}])]
):
    return country


@app.post("/openapi_example")
async def country_openapi_example(
    country: Annotated[
        Country,
        Body(
            openapi_examples={
                "polish": {
                    "summary": "polish example",
                    "description": "example for country: Poland",
                    "value": {"name": "Poland", "symbol": "PL"},
                },
                "english": {
                    "summary": "english example",
                    "description": "example for country: England",
                    "value": {"name": "England", "symbol": "ENG"},
                },
            }
        ),
    ]
):
    return country
