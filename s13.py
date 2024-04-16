from fastapi import FastAPI, Header, HTTPException, status, Path
from typing import Annotated
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


class DataIn(BaseModel):
    name: Annotated[str, Field(max_length=10)]
    qty: int
    address: str


@app.post("/add-item", status_code=status.HTTP_201_CREATED)
async def add_item(active: Annotated[bool, Header()], item_in: DataIn):
    if not active:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE)
    return {"msg": "item added", "item": item_in}


@app.get("/get-item/{id}")
async def get_item(id: Annotated[int, Path(lt=10)]) -> DataIn:
    if id > 5:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    fictional_item = DataIn(name="test", qty=8, address="test_place")
    return fictional_item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
