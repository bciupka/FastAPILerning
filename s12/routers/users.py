from fastapi import APIRouter, Depends
import dependencies

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(dependencies.random_dep)]
)


@router.get("/another")
async def another_endp(active: bool):
    return {"user_active": active}
