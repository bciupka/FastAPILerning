from fastapi import FastAPI, status, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from typing import Union, Annotated
from http import HTTPStatus

app = FastAPI()


class BaseUser(BaseModel):
    login: str
    email: EmailStr
    about: str | None = None


class UserIn(BaseUser):
    password: str
    password_2: str


class UserOut(BaseUser):
    pass


class UserDB(BaseUser):
    hashed_password: str


def hash_pass(password: str):
    return str(reversed(password))


def save_to_db(user: UserIn):
    hashed = hash_pass(user.password)
    db_user = UserDB(**user.model_dump(), hashed_password=hashed)
    return db_user


@app.post("/new_user")
async def post_user(user: UserIn) -> UserOut | str:
    if user.password == user.password_2:
        db_user = save_to_db(user)
        return UserOut(**db_user.model_dump())
    return "Passwords don't match"


@app.post("/new_user_union", response_model=Union[UserOut, str])
async def post_user_u(user: UserIn):
    if user.password == user.password_2:
        db_user = save_to_db(user)
        return UserOut(**db_user.model_dump())
    return "Passwords don't match"


@app.get("/all_users", response_model_exclude_unset=True)
async def read_users() -> list[UserOut]:
    user1 = UserOut(login="asd", email="ds@fg.pl")
    user2 = UserOut(login="asdsd", email="dssss@fsda.pl", about="tralala")
    return user1, user2


@app.get("/http_status", status_code=200)
async def get_stat():
    return "OK"


@app.get("/http_status_http", status_code=HTTPStatus.OK)
async def get_stat_http():
    return "OK"


@app.get("/http_status_fastapi", status_code=status.HTTP_200_OK)
async def get_stat_fast():
    return "OK"


@app.post("/form_test")
async def form_test(
    f: Annotated[str, Form()], f2: Annotated[int | None, Form()] = None
):
    return {"f": f, "f2": f2}


@app.post("/add_file")
async def file_add(file: Annotated[bytes, File(description="Cool file")]):
    return {"filesize": len(file)}


@app.post("/add_multi_uploadfiles")
async def add_m_uf(files: list[UploadFile]):
    return {
        "names": [i.filename for i in files],
        "content_type": [i.content_type for i in files],
    }


@app.post("/read_file")
async def read_file(
    file: Annotated[UploadFile, File(description="Upload file async read")],
    signs: int = 5,
):
    first_signs = await file.read(signs)
    return {"first_signs": first_signs}


@app.get("/")
async def main():
    content = """
<body>
<form action="/add_file/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
<form action="/add_multi_uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/forms_and_files")
async def f_a_f(
    file1: Annotated[bytes, File(description="First file")],
    file2: Annotated[UploadFile, File(description="Second file")],
    form: Annotated[str, Form()],
):
    file1_ret = file1.decode()[:5]
    return {"concat": file1_ret + form + file2.filename}
