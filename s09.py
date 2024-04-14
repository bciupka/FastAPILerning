from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime

app = FastAPI()

oauth2_authentication = OAuth2PasswordBearer(tokenUrl="get_token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "77155793faf14c916a987b8b937d77300856204975a553b102ebd905a9aaf732"
ALGOTITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


fake_db_users = {
    "alias10": {
        "login": "alias10",
        "email": "alias10@random.org",
        "about": "im cool",
        "hashed_pwd": "$2y$10$32Wj.hgGPquOMvP5WddAe.Z5gl2iFWMrXIy.UrvZOdggoUH0gZBVW",
        # 123
    },
    "beta5": {
        "login": "beta5",
        "email": "beta5@random.org",
        "about": "im very cool",
        "hashed_pwd": "$2y$10$CS9kv2Tj0yrBk1CK2KbbPOEMLJ3Hs43Nj54Zo1vv8H4hjjkKq8Ina",
        # 321
    },
    "delta4": {
        "login": "delta4",
        "email": "delta4@random.org",
        "about": "im not really cool",
        "active": False,
        "hashed_pwd": "$2y$10$edQljSFBke6/kKDXXcnok.nh/srW87/Jg0cFyxa0MJctsuhEnX0mu",
        # 000
    },
}


class CustomUser(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None
    active: bool = True


class CustomUserInDB(CustomUser):
    hashed_pwd: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


async def verify_pwd(pwd: str, hashed_pwd: str):
    return pwd_context.verify(pwd, hashed_pwd)


async def create_hash(pwd: str):
    return pwd_context.hash(pwd)


async def get_user_from_db(db: dict, username: str):
    user = db.get(username)
    if user:
        user_model = CustomUserInDB(**user)
        return user_model


async def authenticate_user(db: dict, username: str, password: str):
    user = await get_user_from_db(fake_db_users, username)
    if not user:
        return False
    if not await verify_pwd(password, user.hashed_pwd):
        return False
    return user


async def encode_token(data: dict, exp: timedelta | None = None):
    if timedelta:
        expire = datetime.now() + exp
    else:
        expire = datetime + timedelta(minutes=15)
    to_encode = data.copy()
    to_encode["exp"] = expire
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOTITHM)
    return encoded


async def get_current_user(token: Annotated[str, Depends(oauth2_authentication)]):
    try:
        decoded = jwt.decode(token, SECRET_KEY, ALGOTITHM)
        username = decoded.get("sub")
        if not username:
            raise HTTPException(
                401, "Invalid credentials", {"WWW-Authenticate": "Bearer"}
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(401, "Invalid credentials", {"WWW-Authenticate": "Bearer"})
    user = await get_user_from_db(fake_db_users, token_data.username)
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
async def get_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user_model = await authenticate_user(
        fake_db_users, credentials.username, credentials.password
    )
    if not user_model:
        raise HTTPException(401, "Invalid credentials", {"WWW-Authenticate": "Bearer"})
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await encode_token({"sub": user_model.login}, access_token_expire)
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/test_auth_form")
async def test_get_auth_form(token: Annotated[str, Depends(oauth2_authentication)]):
    return token


@app.get("/users/current")
async def get_curr_user(
    user: Annotated[CustomUserInDB, Depends(get_current_user_active)]
) -> CustomUser:
    return user
