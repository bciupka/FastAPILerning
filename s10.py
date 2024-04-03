from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
)


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
