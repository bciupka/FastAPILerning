from fastapi import FastAPI, Request, Response
import time

app = FastAPI()


@app.middleware("http")
async def time_tracker(request: Request, call_next):
    now = time.perf_counter()
    response: Response = await call_next(request)
    response.headers["X-perf-counter"] = str(time.perf_counter() - now)
    response.set_cookie("Warning", "Watch out: big values == null")
    return response


@app.get("/test")
async def test_fot_middleware(x: int, y: int):
    return {"result": x**y}
