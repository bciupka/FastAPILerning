import dependencies
from fastapi import FastAPI, Depends
from routers import users, items
from internal import admin

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/", dependencies=[Depends(dependencies.random_dep)])
async def main():
    return {"msg": "main"}
