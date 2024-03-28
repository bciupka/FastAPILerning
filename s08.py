from fastapi import FastAPI, Depends, status, HTTPException, Header
from typing import Annotated


async def dependency_3(token: str):
    if token != "09871234":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


app = FastAPI(dependencies=[Depends(dependency_3)])


async def dependency_1(id: int, desc: str):
    if id > 5:
        raise HTTPException(
            status.HTTP_418_IM_A_TEAPOT, {"message": "please less than 5"}
        )
    if len(desc) > 10:
        raise HTTPException(status.HTTP_417_EXPECTATION_FAILED, {"message": "im bored"})


async def dependency_2(active: Annotated[bool, Header()]):
    if active:
        return
    raise HTTPException(status.HTTP_423_LOCKED, {"message": "not active!"})


@app.get(
    "/dependencies_test", dependencies=[Depends(dependency_1), Depends(dependency_2)]
)
async def test():
    return "OK"
