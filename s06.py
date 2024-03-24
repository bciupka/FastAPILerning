from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import BaseModel

app = FastAPI()


class MyException(Exception):
    def __init__(self, name: str, *args: object) -> None:
        self.name = name
        super().__init__(*args)


@app.exception_handler(MyException)
async def my_exception_handler(request: Request, exc: MyException):
    return PlainTextResponse(
        status_code=406,
        content=str({"msg": "Thats bad", "additional": f"string is: {exc.name}"}),
    )


@app.exception_handler(StarletteHTTPException)
async def my_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(content={"original": exc.detail, "new": "my handler addons"})


# @app.exception_handler(RequestValidationError)
# async def my_req_val_error(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"old": exc.errors(), "new": "new data", "body": exc.body},
# )


@app.exception_handler(RequestValidationError)
async def my_req_val_error_email(request: Request, exc: RequestValidationError):
    print("Executing funcion send_email_about_error")
    return await request_validation_exception_handler(request, exc)


class Item(BaseModel):
    name: str
    qty: int
    about: str | None = None


@app.get("/get_info/{int}")
async def get_info(p: int):
    if p == 5:
        raise HTTPException(
            detail={"msg": "Not 5, please"}, status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    return {"msg": "OK"}


@app.get("/get_headers")
async def head_get(q: int):
    if q > 5:
        raise HTTPException(
            detail={"msg": "Please lower"}, status_code=406, headers={"hint": "than 5"}
        )
    return q


@app.get("/my_error")
async def error_test(q: int):
    if q > 5:
        raise MyException("Bad q param")
    return q


@app.post("/valid_mod")
async def v_mod(item: Item):
    return item
