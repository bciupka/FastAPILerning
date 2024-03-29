from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import BaseModel, EmailStr

app = FastAPI()

oauth2_authentication = OAuth2PasswordBearer(tokenUrl="get_token")


class CustomUser(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None


async def fake_token_decode(token: str) -> CustomUser:
    return CustomUser(
        login=token + " user",
        email="random@email.com",
        about="nice token user - " + token,
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_authentication)]):
    return await fake_token_decode(token)


@app.get("/test_auth_form")
async def test_get_auth_form(token: Annotated[str, Depends(oauth2_authentication)]):
    return token


@app.get("/users/current")
async def get_curr_user(user: Annotated[CustomUser, Depends(get_current_user)]):
    return user
