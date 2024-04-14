from fastapi import APIRouter, Depends
import dependencies

router = APIRouter(
    prefix="/items", tags=["items"], dependencies=[(Depends(dependencies.random_dep))]
)


@router.get("/smth")
async def some_endp(what: str):
    return {"msg": what}
