from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel, EmailStr

app = FastAPI()

oauth2_authentication = OAuth2PasswordBearer(tokenUrl="get_token")


fake_db_users = {
    "alias10": {
        "login": "alias10",
        "email": "alias10@random.org",
        "about": "im cool",
        "hashed_pwd": "fakehash123",
    },
    "beta5": {
        "login": "beta5",
        "email": "beta5@random.org",
        "about": "im very cool",
        "hashed_pwd": "fakehash321",
    },
    "delta4": {
        "login": "delta4",
        "email": "delta4@random.org",
        "about": "im not really cool",
        "active": False,
        "hashed_pwd": "fakehash000",
    },
}


class CustomUser(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None
    active: bool = True


class CustomUserInDB(CustomUser):
    hashed_pwd: str


async def fake_hashing(pwd: str):
    return "fakehash" + pwd


async def get_user_from_db(db: dict, username: str):
    user = db.get(username)
    if user:
        user_model = CustomUserInDB(**user)
        return user_model


async def fake_token_decode(token: str) -> CustomUser:
    user = await get_user_from_db(fake_db_users, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_authentication)]):
    user = await fake_token_decode(token)
    if not user:
        raise HTTPException(401, "Invalid credentials", {"WWW-Authenticate": "Bearer"})
    return user


async def get_current_user_active(
    user: Annotated[CustomUserInDB, Depends(get_current_user)]
):
    if user.active:
        return user
    raise HTTPException(400, "Inactive user")


@app.post("/get_token")
async def get_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = fake_db_users.get(credentials.username)
    if not user:
        raise HTTPException(400, "Invalid username or password")
    user_model = CustomUserInDB(**user)
    if user_model.hashed_pwd == await fake_hashing(credentials.password):
        return {"access_token": user_model.login, "token_type": "bearer"}
    raise HTTPException(400, "Invalid username or password")


@app.get("/test_auth_form")
async def test_get_auth_form(token: Annotated[str, Depends(oauth2_authentication)]):
    return token


@app.get("/users/current")
async def get_curr_user(
    user: Annotated[CustomUserInDB, Depends(get_current_user_active)]
) -> CustomUser:
    return user
