from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr
from typing import Union
from http import HTTPStatus

app = FastAPI()


class BaseUser(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None


class UserIn(BaseUser):
    password: str
    password_2: str


class UserOut(BaseUser): ...


class UserDB(BaseUser):
    hashed_password: str


def hash_pass(password: str):
    return str(reversed(password))


def save_to_db(user: UserIn):
    hashed = hash_pass(user.password)
    db_user = UserDB(**user.model_dump(), hashed_password=hashed)
    return db_user


@app.post("/new_user")
async def post_user(user: UserIn) -> UserOut | str:
    if user.password == user.password_2:
        db_user = save_to_db(user)
        return UserOut(**db_user.model_dump())
    return "Passwords don't match"


@app.post("/new_user_union", response_model=Union[UserOut, str])
async def post_user(user: UserIn):
    if user.password == user.password_2:
        db_user = save_to_db(user)
        return UserOut(**db_user.model_dump())
    return "Passwords don't match"


@app.get("/all_users", response_model_exclude_unset=True)
async def read_users() -> list[UserOut]:
    user1 = UserOut(login="asd", email="ds@fg.pl")
    user2 = UserOut(login="asdsd", email="dssss@fsda.pl", about="tralala")
    return user1, user2


@app.get("/http_status", status_code=200)
async def get_stat():
    return "OK"


@app.get("/http_status_http", status_code=HTTPStatus.OK)
async def get_stat_http():
    return "OK"


@app.get("/http_status_fastapi", status_code=status.HTTP_200_OK)
async def get_stat_fast():
    return "OK"
