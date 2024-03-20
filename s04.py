from fastapi import FastAPI, Cookie, Request
from typing import Annotated

app = FastAPI()


@app.get("/cookies")
async def cookie_param_get(
    request: Request, cookieparam: Annotated[str | None, Cookie()] = None
):
    to_return = request.headers
    to_return_c = request.cookies
    return {"cookie": cookieparam, "headers_get": to_return, "cookie_get": to_return_c}
