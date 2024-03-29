from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()


oauth2_authentication = OAuth2PasswordBearer(tokenUrl="get_token")


@app.get("/test_auth_form")
async def test_get_auth_form(token: Annotated[str, Depends(oauth2_authentication)]):
    return token
