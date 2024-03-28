from fastapi import FastAPI, Depends, status, HTTPException, Header
from typing import Annotated


async def dependency_3(token: str):
    if token != "123":
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


async def dependency_w_yield_1(a: int):
    yield a
    a = a + 2
    print(f"New a: {a}")
    # raise HTTPException(400, {"a": a})


async def dep_w_yield_try(a: int, b: int):
    try:
        c = a / b
        yield c
    except ZeroDivisionError as e:
        print(e)
        raise HTTPException(400, str(e) + " DEP")
    finally:
        print(a, b)


@app.get(
    "/dependencies_test", dependencies=[Depends(dependency_1), Depends(dependency_2)]
)
async def test():
    return "OK"


@app.get("/dep_yield_test")
async def yield_test(dep: Annotated[int, Depends(dependency_w_yield_1)]):
    if dep > 5:
        raise HTTPException(400, f"wrong a = {dep}")
    return {"a": dep}


@app.get("/dep_yield_try")
async def try_test(dep: Annotated[int, Depends(dep_w_yield_try)]):
    final = 10 / (dep - 2)
    return final
