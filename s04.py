from fastapi import FastAPI, Cookie, Request, Header, Response
from pydantic import BaseModel, EmailStr
from typing import Annotated, Any
from fastapi.responses import JSONResponse

app = FastAPI()


class UserIn(BaseModel):
    login: str
    password: str
    email: EmailStr
    about: str | None = None


class UserOut(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None


class UserInInherited(UserOut):
    password: str


@app.get("/cookies")
async def cookie_param_get(
    request: Request, cookieparam: Annotated[str | None, Cookie()] = None
):
    to_return = request.headers
    to_return_c = request.cookies
    return {"cookie": cookieparam, "headers_get": to_return, "cookie_get": to_return_c}


@app.get("/headers/")
async def header_param_get(
    header: Annotated[str | None, Header()] = None,
    header_2: Annotated[list[str] | None, Header()] = None,
):
    return {"header": header, "header_2": header_2}


@app.post("/adduser_rm", response_model=UserOut)
async def add_user(user: UserIn) -> Any:
    return user


@app.post("/adduser")
async def add_user_inherited(user: UserInInherited) -> UserOut:
    return user


@app.get("/disable_model", response_model=None)
async def disabled(json: bool) -> Response | str:
    if json:
        return JSONResponse({"something": 3})
    return "lol"


@app.get("/only_set", response_model_exclude_unset=True)
async def o_set() -> UserOut:
    user = UserOut(login="test", email="as@fdf.com")
    return user


@app.get("/only_non_def", response_model_exclude_defaults=True)
async def o_nd() -> UserOut:
    user = UserOut(login="test", email="as@fdf.com", abbout="ooo")
    return user


@app.get("/only_non_none", response_model_exclude_none=True)
async def o_nn() -> UserOut:
    user = UserOut(login="test", email="as@fdf.com", abbout=None)
    return user


@app.get("/only_included", response_model_include={"login"})
async def o_inc() -> UserOut:
    user = UserOut(login="test", email="as@fdf.com", abbout=None)
    return user


@app.get("/only_exluded", response_model_exclude={"login"})
async def o_exc() -> UserOut:
    user = UserOut(login="test", email="as@fdf.com", abbout=None)
    return user
