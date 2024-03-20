from fastapi import FastAPI, Cookie, Request, Header
from typing import Annotated

app = FastAPI()


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
