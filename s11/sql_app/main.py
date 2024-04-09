from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
import database, models, schemas, crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from pydantic import EmailStr


models.Base.metadata.create_all(database.engine)

app = FastAPI()


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=dict(
            detail=[
                dict(
                    type="integrity_error",
                    args=exc.args,
                    detail=exc.detail,
                    statement=exc.statement,
                    params=exc.params,
                )
            ]
        ),
    )


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_user")
def post_user(
    user_in: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]
) -> schemas.User:
    return crud.user_create(db, user_in)


@app.get("/get_all_users")
def get_users(
    db: Annotated[Session, Depends(get_db)], limit: int = 100, skip: int = 0
) -> list[schemas.User]:
    return crud.user_get(db, limit, skip)


@app.get("/user_by_email")
def get_items(db: Annotated[Session, Depends(get_db)], email: EmailStr) -> schemas.User:
    return crud.user_get_by_mail(db, email)


@app.post("/add_item")
def post_item(
    db: Annotated[Session, Depends(get_db)], item_in: schemas.ItemCreate, owner: int
) -> schemas.Item:
    return crud.item_create(db, item_in, owner)


@app.get("/get_items")
def get_items(
    db: Annotated[Session, Depends(get_db)], limit: int = 100, skip: int = 0
) -> list[schemas.Item]:
    return crud.item_get(db, limit, skip)
